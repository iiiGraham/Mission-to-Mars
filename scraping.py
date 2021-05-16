# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # set path for driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # provide driver path to splinter and intiate headless driver
    browser = Browser('chrome', **executable_path, headless=True)

    # set variables to pull
    news_title, news_paragraph = mars_news(browser)
    
    # put the scraped results into a dictionary 
    data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified": dt.datetime.now(),
            "hemisphere_images": hemisphere_images(browser)}
    # quit the automated broswer session.  
    browser.quit()
    return data
    
def mars_news(browser):
    ''' takes one arguement: webdriver path
        navigates to url defined in function and returns 
        the latest article headline and teaser text'''

    # asign url 
    url = 'https://redplanetscience.com'
    # visit mars nasa news site
    browser.visit(url)

    # optional delay - this can help when scraping elements that are behind JS
    # look for div elements tha have "list_text" attributes
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # parse html
    html = browser.html
    # parse the html found and save to a variable as soup object
    news_soup = soup(html, 'html.parser')
    
    # define try and except clauses
    try:     
        # declare parent element that we can reference later for filtering results. Note '.' is used for selecting classes so div '.' list_text selects div elements with list_text class
        slide_elem = news_soup.select_one('div.list_text') # I don't totally understand this one - look up select_one method

        # Note: could asign this to a variable and as .text at the end to return the same result as get_text() method. 
        # get the text from the html parent element from slide_elem.find = return the first 'a' tag
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Soup Note: find() returns the first item found. find_all() returns all of the items that match the parameters
        # get the article teaser text from parent element
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()       
    except AttributeError:
        # if we get an error during the scraping process don't return anything
        return None, None

    return news_title, news_p

# Featured Images scrape below

def featured_image(browser):
    ''' takes one arguement: webdriver path
        navigates to url defined in fucntion and returns 
        featured image on website homepage'''   
    # visit target URL - figure out why this doesn't work if you already have the window open?
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find the full image button for the featured image and click it
    full_image_elem = browser.find_by_tag('button')[1] # there are more buttons on the page so we need to specif which one with the list index fo the button tag we want
    full_image_elem.click()

    # parse the html from the spaceimages website
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # pull information from the featured image
        # use the image tag to get the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # add base url to the code to create full url to the featured image
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Mars Facts scrape below

def mars_facts():
    ''' collects data from table on url
        defined in function and returns table
        data in html format'''   
    try:
        # read html tables directly with Pandas and read_html 
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # take the pandas table and convert back to html with to_html which can then be embedded in a web application
    return df.to_html(classes="table table-striped")

def hemisphere_images(browser):
    '''collect image links for each
        mars hemisphere to display
        on web app. Returns list of dicionaries
        with image titles and src links'''
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # naviagte to hemisphere image webpage
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    # pass html to beautiful soup
    mars_soup = soup(html, 'html.parser')

    try:
        # locate unique class to find image links
        image_link_class = mars_soup.findAll('div', class_='description')

    except AttributeError:
        return None

    # get the hrefs from each of the description classes
    hrefs = [href.find('a').get('href') for href in image_link_class]

    # create urls to navigate to the webpage where full size images can be found
    image_page_links = [f'{url}{page}' for page in hrefs] # --> list of pages to visit

    try:
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
            
    except BaseException:
        return None     
    
    return hemisphere_image_urls

# tell Flask that the script has run and print out the results
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())