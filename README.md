# Mission-to-Mars

## Web Scraping
### Overview of Assignment
- Gain familiarity with and use HTML elements, as well as class and id attributes, to identify content for web scraping.
- Use BeautifulSoup and Splinter to automate a web browser and perform a web scrape.
- Create a MongoDB database to store data from the web scrape.
- Create a web application with Flask to display the data from the web scrape.

### Tools Utilized
- Splinter
    - Splinter is the tool that will automate our web browser as we begin scraping. This means that it will open the browser, visit a webpage, and then interact with it (such as logging in or searching for an item)
- Web-Driver Manager
    - The web driver manager package will allow us to easily use a driver that to scrape websites without having to go through the complicated process of installing the stand alone ChromeDriver
- BeautifulSoup
    - Beautiful Soup is a Python package for parsing HTML and XML documents. It creates a parse tree for parsed pages that can be used to extract data from HTML.
- MongoDB
    - MongoDB (also known as Mongo) is a document database that is flexible when it comes to storing data than a structured database such as SQL. It's able to handle smaller, more personal projects, as well as larger-scale projects that a company might require. For this module, Mongo is a better choice than SQL because the data we'll scrape from the web isn't going to be uniform. For example, how would we break down an image into rows and columns? We can't. But Mongo will store and access it as a document instead.
- Flask-PyMongo
    - To bridge Flask and Mongo
- Additional Libraries
    - There are two final Python libraries required to run scraping code successfully: html5lib and lxml. Both packages are used to parse HTML in Python, which will be important to traverse through different web pages to find and collect information.

### Challenge Portion
- Use BeautifulSoup and Splinter to scrape full-resolution images of Mars’s hemispheres and the titles of those images, store the scraped data on a Mongo database, use a web application to display the data, and alter the design of the web app to accommodate these images.
    - Deliverable 1: Scrape Full-Resolution Mars Hemisphere Images and Titles
    - Deliverable 2: Update the Web App with Mars Hemisphere Images and Titles
    - Deliverable 3: Add Bootstrap 3 Components