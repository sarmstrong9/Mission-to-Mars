#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
    # searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as <ul class="item_list">.
    # we're telling our browser to wait one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.


# In[4]:


# set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[6]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Image

# In[7]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[8]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[9]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[10]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[11]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Table Data

# In[12]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[13]:


#  convert our DataFrame back into HTML-ready code using the .to_html() function
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[14]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[15]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# set up the HTML parser:
html = browser.html
hem_img_soup = soup(html, 'html.parser')

product_pages = hem_img_soup.find_all('div', class_='item')

for product_page in product_pages:
    hem_img_url_rel = product_page.find('a').get('href')

    # Use the base URL to create an absolute URL for product urls
    product_url = f'https://marshemispheres.com/{hem_img_url_rel}'
    
    # once on the individual product page, find urls for .jpg image
    browser.visit(product_url)
    html2 = browser.html
    hem_prod_img_soup = soup(html2, 'html.parser')
    
    hem_prod_img_desc = hem_prod_img_soup.find('div', class_='downloads')
    hem_prod_img_url_rel = hem_prod_img_desc.find('a').get('href')
    
    # Use the base URL to create an absolute URL for product urls
    hem_prod_img_url = f'https://marshemispheres.com/{hem_prod_img_url_rel}'

    # Get the title of the image
    hem_prod_title_desc = hem_prod_img_soup.find('h2', class_='title').get_text()

    hemispheres = {
        "img_url": hem_prod_img_url,
        "title": hem_prod_title_desc,
    }
    
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()


# In[16]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[17]:


# 5. Quit the browser
browser.quit()

