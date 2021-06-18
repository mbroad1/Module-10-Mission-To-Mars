#!/usr/bin/env python
# coding: utf-8

# ### Article Scraping

# In[1]:


pip install regex


# In[2]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[6]:


# "slide_elem holds a ton of info, so look inside of it for this specific data"
slide_elem.find('div', class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Image Scraping - Featured Images

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[12]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scrape Table of Mars Facts

# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


# Convert DataFrame back into HTML-ready code
df.to_html()


# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
base_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'
browser.visit(url)

html = browser.html
img_soup = soup(html, 'html.parser')


# In[21]:


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


# In[22]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[23]:


# # Quits Splinter created browser-IMPORTANT because browser won't shut down otherwise
browser.quit()


# In[ ]:




