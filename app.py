# import dependencies for creating flask app connected to mongo
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__, template_folder='templates')

# use flask_pymongo to set connection to mongo db
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create flask route to HTML home landing page
@app.route("/")
def index():
    # uses PyMongo - from line 11 - to connect the code to the mars database and search with find_one which will return a single doc from the database
    mars = mongo.db.mars.find_one()
    # tells Flask to return HTML template and use the information from the mars database in the HTML template
    return render_template("index.html", mars=mars)

# create route for new page "scrape"
@app.route("/scrape")
def scrape():
    # set mars variaable to the mongo db
    mars = mongo.db.mars
    # collect data for the db
    mars_data = scraping.scrape_all()
    # update the db
    mars.update({}, mars_data, upsert=True)
    # go back to the home page and show what was scraped
    return redirect("/", code=302)
    # mars.update_many({}, mars_data, upsert=True) - this might be the better way to do it because update is deprecated. 

# code to make Flask run - the app will not work without this!
if __name__ == "__main__":
    app.run(debug=True)

