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

# ### Mars Facts
# scraping tables
# you can read html tables directly with Pandas and read_html - most of the time you are going to want to set the column headers and the index but if you don't they will just be numeric
df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

# take the pandas table and convert back to html with to_html which can then be embedded in a web application
df.to_html()

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
# url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
# pass html to beautiful soup
mars_soup = soup(html, 'html.parser')

# locate unique class to find image links
image_link_class = mars_soup.findAll('div', class_='description')

# get the hrefs from each of the description classes
hrefs = [href.find('a').get('href') for href in image_link_class]

# create urls to navigate to the webpage where full size images can be found
image_page_links = [f'{url}{page}' for page in hrefs] # --> list of pages to visit

# for loop starts here 
# nvaigate to each of the image page links
for page in image_page_links:
    
    # initialize dictionary to hold results
    hemispheres = {}

    # go to image page
    browser.visit(page)
    image_html = browser.html
    image_soup = soup(image_html, 'html.parser')

    # scrape the title 
    title = image_soup.find('div', class_='cover').h2.text
    # put the title in dictionary with 'title': scraped text
    hemispheres['title'] = title
    
    # scrape the image src link
    img_source = image_soup.find('img', class_='wide-image').get('src')
    # put the src link the dictionary with 'img_url': scraped src
    hemispheres['img_url'] = f"https://marshemispheres.com/{img_source}"
    
    # put dictionary entry into list hemisphere_image_urls[]
    hemisphere_image_urls.append(hemispheres)

# print list of image titles and urls
print(hemisphere_image_urls)

# quit browser instance
browser.quit()