from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq


app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        reviews = []
        searchString = request.form['content'].replace(" ","+")
        flipkart_url = "https://www.flipkart.com/search?q=" + searchString
        uClient = uReq(flipkart_url)
        flipkartPage = uClient.read()
        uClient.close()
        flipkart_html = bs(flipkartPage, "html.parser")

        product_url = "https://www.flipkart.com" + flipkart_html.find('div', class_="_1YokD2 _3Mn1Gg").findAll('div', class_="_1AtVbE col-12-12")[0].a['href']
        uClient = uReq(product_url)
        productPage = uClient.read()
        uClient.close()
        product_html = bs(productPage, "html.parser")

        product_name = product_html.find('div', class_="aMaAEs").div.text

        rvuA = product_html.find('div',class_="col JOpGWq").findAll('a')
        review_url = 'https://www.flipkart.com' + rvuA[len(rvuA)-1]['href']
        uClient = uReq(review_url)
        reviewPage = uClient.read()
        uClient.close()
        review_html = bs(reviewPage, "html.parser")

        reviewBox = review_html.findAll('div', class_="col _2wzgFH K0kLPL")


            
        for review in reviewBox:
            try:
                name = review.find('div', class_="row _3n8db9").find('div', class_="row").p.text
            except:
                name = 'no name'
            try:
                star = review.findAll('div', class_="row")[0].div.text
            except:
                star = 'not rated'
            try:
                title = review.findAll('div', class_="row")[0].p.text
            except:
                title = 'not reviewed'
            try:
                comment = review.findAll('div', class_="row")[1].div.div.div.text  
            except:
                comment = 'not reviewed'
            try:
                duration = review.find('div', class_="row _3n8db9").find('div', class_="row").findAll('p')[2].text
            except:
                duration = 'not reviewed'
            mydict = {"Product": product_name, "Name":name, "Star":star,"Title":title, "Review":comment, "Duration":duration}
            reviews.append(mydict)
        return render_template('result.html', reviews = reviews[0:(len(reviews)-1)])
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0")
