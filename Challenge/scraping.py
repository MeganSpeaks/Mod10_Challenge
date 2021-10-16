from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scraping():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": facts(),
    "hemispheres": hemisphere(browser),
    "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def news(browser):
    url = 'https://redplanetscience.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    try:
        slide_elem = news.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None,None

def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url + 'index.html')

    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for index in range(4):
        h3s = browser.find_by_tag('h3')


        h3s[0].click()

        # get url
        lis = browser.find_by_tag('li').find_by_tag('a')
        link = lis
        url = link[0]._element.get_attribute('href')

        # get title
        h2s = browser.find_by_tag('h2')
        title = h2s[0].text

        hemisphere_image_urls.append({
            'img_url': url,
            'title': title
        })

        browser.back()

    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    #parse html text
    hemi_soup = soup(html_text, "html.parser")

    # adding try/except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres
