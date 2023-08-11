from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen 
import logging
import pymongo
import sys

# Database connection
uri = "mongodb+srv://shreyashsingh1:Lookinto1234@cluster0.cihs6do.mongodb.net/"
client = pymongo.MongoClient(uri)
db = client["Scrapper"]
collection_scrapper = db["Reviews"]

# Set the encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/review", methods=['GET', 'POST'])
def web_scrap():
    
    if request.method == "POST":
        try: 
    
            search_input = request.form["content"].replace(" ", "")
    
            flipkart_page = urlopen('https://www.flipkart.com/search?q=' + search_input)
            flipkart_page_read = flipkart_page.read()
            flipkart_html = bs(flipkart_page_read, "html.parser")
            
            Bigbox = flipkart_html.find_all("div", {"class": "_1AtVbE col-12-12"})
            del Bigbox[0:3]
            box = Bigbox[0]
    
            # creating link to reach a product so that we can remove reviews
            product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
    
            product_page = requests.get(product_link)
            product_page_html = bs(product_page.text, "html.parser")
    
            comment_bigbox = product_page_html.findAll("div", {"class": "_16PBlm"})
            
            
            reviews = []
            
            for box in comment_bigbox:
                
                Name = ''
                try:
                    Name = box.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
   
                except:
                    logging.info("name")
                  
                    
                Rating = ''
                try:
                    Rating = box.div.div.div.div.text
                    
                except:
                    Rating = 'No Rating'
                    logging.info("rating")
                  
                   
                CommentHead = '' 
                try:
                    CommentHead = box.div.div.div.p.text
                    
                except:
                    CommentHead = 'No Comment Heading'
                    logging.info(CommentHead)
                  
                    
                Comment = ''
                try:
                    # Ye use karne se read more nhi a raha
                    CustComment = box.div.div.findAll("div", {"class"  : ""})
                    Comment = CustComment[0].div.text
                    
                except Exception as e:
                    logging.info(e)
                 
                    
                mydict = {
                    "Product": search_input, 
                    "Name": Name, 
                    "Rating": Rating, 
                    "CommentHead": CommentHead, 
                    "Comment": Comment
                }
                reviews.append(mydict)
                
            logging.info(f"log my final result {reviews}")
            collection_scrapper.insert_many(reviews)  
            
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        
        except Exception as e:
            logging.info(e)
            return 'something is wrong'

    else:
        return render_template('index.html')

        
if __name__=="__main__":
    app.run(host="0.0.0.0")
