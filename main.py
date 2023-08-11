"""
Derived data refers to information that is obtained or generated through the processing, analysis, 
or transformation of existing data. It is derived from raw or primary data sources and often involves 
aggregating, manipulating, or combining data to produce new insights, patterns, or metrics.
"""

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen 
import logging
import sys

# Set the encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

flipkart_url = "https://www.flipkart.com/search?q=" + "iphone12pro"
print(flipkart_url)
url_client = urlopen(flipkart_url)

# print(url_client.read())
flipkart_page = url_client.read()

"""
-> Abhi ye human readable form me nhi hai so hum abhi beautifulSoup use karege
-> Parsing refers to the process of analyzing and breaking down structured data, 
such as code or markup, into its constituent parts based on specific rules or 
grammar. It involves examining the input and extracting meaningful information 
for further processing. Parsing is commonly used in programming to interpret and 
manipulate data in various formats, such as HTML, XML, or JSON. Programming languages 
often provide libraries or modules that simplify the parsing process by offering 
pre-built parsers following the grammar rules of specific formats.
"""

flipkart_html = bs(flipkart_page, "html.parser")

"""Creating click on a product"""
"""Bigbox refers to product available on a page and we are trying to access each product"""
bigbox = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) # It returns a list

# print(len(bigbox)) here there as 29 products
del bigbox[0:3]
# del bigbox[-1:-4:-1]

# bigbox[0].div.div.div.a['href'] or bigbox[0].find("a")['href']
product_link = "https://www.flipkart.com" + bigbox[3].find("a")['href']
print(product_link)

# for box in bigbox:
#     """This code extracts the URL of the product by finding the anchor 
#     element within the box element and accessing its href attribute."""
#     product_url = "https://www.flipkart.com" + box.find("a")['href']
#     print(product_url)

"""Getting data from product link"""
product_request_page = requests.get(product_link)

product_html = bs(product_request_page.text, "html.parser")
"""In the context of web scraping and parsing HTML documents, the .text attribute 
is commonly used to extract the textual content of an HTML element."""

comment_bigbox = product_html.findAll("div", {"class": "_16PBlm"})
print(len(comment_bigbox))

for box in comment_bigbox:
    """Finding buyer's name"""
    # print(box.div.div.findAll("p", {"class": "_2sc7ZR _2V5EHH"})[0].text)
    print(box.div.div.p.text)
    """For ratting"""
    print(box.div.div.div.div.text)
    """Comment header"""
    # print(box.div.div.div.findAll("p", {"class": "_2-N8zT"})[0].text)
    print(box.div.div.div.p.text)  
    """Actual comment"""
    print(box.div.div.findAll("div", {"class": "t-ZTKy"})[0].text)
