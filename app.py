from flask import Flask, render_template,jsonify, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)
@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
@cross_origin()
def reviews():
    fname = request.form['content']
    f1name = request.form['content1']
    searchstring = fname.replace(" ", "-")
    flipkart_url = "https://www.flipkart.com/search?q=" + searchstring
    uClient = uReq(flipkart_url)
    flipkartPage = uClient.read()
    uClient.close()

    flipkart_html = bs(flipkartPage, "html.parser")

    bigboxes = flipkart_html.findAll("div", {"class": "_2pi5LC col-12-12"})

    del bigboxes[0:3]  # this is just to delete unnecessary boxes
    box = bigboxes[0]

    xlink = box.div.div.div.a['href']
    for i in range(1, len(xlink)):
        if xlink[i] == '/':
            break

    ylink = xlink[0:i + 1] + "product-reviews" + xlink[i + 2:len(xlink)]
    revlink = "http://www.flipkart.com" + ylink + "&sortOrder=" + f1name

    revRes = requests.get(revlink)
    revRes.encoding = 'utf-8'
    rev_html = bs(revRes.text, "html.parser")

    revBoxes = rev_html.findAll("div", {"class": "_27M-vq"})

    reviews = []

    for revBox in revBoxes:
        try:
            name = revBox.findAll("p", {"class": "_2sc7ZR _2V5EHH"})[0].text
        except:
            name = "No name"

        try:
            rating = revBox.findAll("div", {"class": "_3LWZlK _1BLPMq"})[0].text
        except:
            rating = "No rating"

        try:
            commentHead = revBox.findAll("p", {"class": "_2-N8zT"})[0].text
        except:
            commentHead = "No comment heading"

        try:
            comment = revBox.findAll("div", {"class": ""})[0].text
            #del comment[len(comment)-9:len(comment)]
            comment = comment[0:len(comment)-9]
        except:
            comment = "No comments"

        mydict = {"Product": fname, "Name": name, "Rating": rating, "CommentHead": commentHead,"Comment": comment}

        reviews.append(mydict)

    return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])

if __name__ == "__main__":
    app.run()















