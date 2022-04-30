# Import Splinter, BeautifulSoup, and Pandas
from dataclasses import dataclass
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    #Set up Splinter
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
        "hemisphere_image_urls": hemisphere_data(browser),
    }

    # Stop webdriver and return data
    browser.quit()
    return data

#creating a function to run scrape steps
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
        # searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as <ul class="item_list">.
        # we're telling our browser to wait one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the HTML parser:
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #print(news_title)

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #print(news_p)
    
    except AttributeError:
        return None, None
    
    return news_title, news_p 

# ### Featured Image
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


# ### Mars Table Data
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #  convert our DataFrame back into HTML-ready code using the .to_html() function
    return df.to_html()

# Hemisphere images and titles
def hemisphere_data(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # set up the HTML parser:
    html = browser.html
    hem_img_soup = soup(html, 'html.parser')

    try:
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

    except AttributeError:
        return None

    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())