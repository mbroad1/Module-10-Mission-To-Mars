# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Function initalizes the browser, creats a data dictionary, and ends the WebDriver and returns the scraped data
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Turn into function
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # "slide_elem holds a ton of info, so look inside of it for this specific data"
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image

# Turn into function
def featured_image(browser):

    # Visit URL
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
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
      return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
### Hemispheres
# 1. Use browser to visit the URL
def hemisphere_data(browser):

    # Use browser to visit the URL
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    base_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'
    browser.visit(url)

    html = browser.html
    img_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    div_description = img_soup.find_all('div', class_='description')

    for div_desc in div_description:
        a_tag = div_desc.find('a', class_='itemLink product-item')
        planet_img_url = base_url+a_tag['href']
        browser.visit(planet_img_url)
        html = browser.html
        planet_soup = soup(html, 'html.parser')
        full_image_url = base_url + planet_soup.find('img', class_='wide-image').get('src')
        
        full_image_title = planet_soup.find('h2', class_='title').text
        hemispheres = {}
        hemispheres['image_url'] = full_image_url
        hemispheres['title'] = full_image_title
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls

# Tells Flask that our script is complete and ready for action
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

