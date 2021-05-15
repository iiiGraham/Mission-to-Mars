# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# set path for driver
executable_path = {'executable_path': ChromeDriverManager().install()}
# provide driver path to splinter 
browser = Browser('chrome', **executable_path, headless=False)


# asign url 
url = 'https://redplanetscience.com'

# visit url with splinter browser
browser.visit(url)

# optional delay - this can help when scraping elements that are behind JS
# look for div elements tha have "list_text" attributes
browser.is_element_present_by_css('div.list_text', wait_time=1)


# parse html
html = browser.html
# parse the html found and save to a variable
news_soup = soup(html, 'html.parser')
# declare parent element that we can reference later for filtering results. Note '.' is used for selecting classes so div '.' list_text selects div elements with list_text class
slide_elem = news_soup.select_one('div.list_text') # I don't totally understand this one - look up select_one method

# find the content that we want
slide_elem.find('div', class_='content_title') # Note: could asign this to a variable and ass .text at the end to return the same result as get_text() method. 


# get the text from the html object returned from slide_elem.find
news_title = slide_elem.find('div', class_='content_title').get_text() # Note: you can also use .text but get_text may provide more customization?
news_title


# Soup Note: find() returns the first item found. find_all() returns all of the items that match the parameters

# get the article teaser text 
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Featured Images scrape below

# visit target URL - figure out why this doesn't work if you already have the window open?
url = 'https://spaceimages-mars.com'
browser.visit(url)

# find the full image button for the featured image and click it
full_image_elem = browser.find_by_tag('button')[1] # there are more buttons on the page so we need to specif which one with the list index fo the button tag we want
full_image_elem.click()

# parse the html from the spaceimages website
html = browser.html
img_soup = soup(html, 'html.parser')

# pull information from the featured image
# use the image tag to get the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# add base url to the code to create full url to the featured image
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# Mars Facts scrape below
# read html tables directly with Pandas and read_html 
df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

# take the pandas table and convert back to html with to_html which can then be embedded in a web application
df.to_html()

# quit the automated broswer session.  
browser.quit()