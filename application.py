
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as ureq
import pandas as pd
from flask import Flask,render_template,request,jsonify,render_template_string
from flask_cors import CORS,cross_origin

application= Flask(__name__) # intializing the flask

@application.route('/',methods=['GET','POST'])
@cross_origin()

def Home_page():
    if request.method == 'POST':
        try:
            searchString = request.form['content']
            searchString = searchString.replace(" ", "+")
            my_url = "https://www.flipkart.com/search?q=" + searchString
            uclient = ureq(my_url)
            # opended hte URL and stored in the page_html
            page_html = uclient.read()
            uclient.close()
            page_soup = soup(page_html, 'html.parser')

            def scrapping(myurl):
                uclient = ureq(myurl)
                # opended hte URL and stored in the page_html
                page_html = uclient.read()

                uclient.close()
                page_soup = soup(page_html, 'html.parser')
                # grab each Product
                containers = page_soup.find_all('div', {'class': '_1xHGtK _373qXS'})
                Style = []
                Discount_Price = []
                Actual_price = []
                Product = []
                Offer = []
                for container in containers:

                    try:
                        discount_Price = container.findAll('div', {'class': '_30jeq3'})[0].text
                    except:
                        discount_Price = 'No Discount'
                    Discount_Price.append(discount_Price)
                    try:
                        actual_price = container.findAll('div', {'class': '_3I9_wc'})[0].text
                    except:
                        actual_price = 'No actual Price'

                    Actual_price.append(actual_price)
                    product = container.findAll('a', {'class': 'IRpwTa'})[0].text
                    Product.append(product)
                    try:
                        offer = container.findAll('div', {'class': "_3Ay6Sb"})[0].text
                    except:
                        offer = 'No Offer'
                    Offer.append(offer)
                Jack_jones = pd.DataFrame()
                Jack_jones['Model'] = Product
                Jack_jones['Product'] = searchString.replace("+",'')
                Jack_jones['Actual_price'] = Actual_price
                Jack_jones['Discount_Price'] = Discount_Price
                Jack_jones['Offer'] = Offer
                return (Jack_jones)

            pages = page_soup.findAll('a', {'class': 'ge-49M'})
            lst = []
            for page in pages:
                x = "https://www.flipkart.com" + page['href']
                lst.append(x)
            Frames = []
            for i in range(len(lst)):
                page = scrapping(lst[i])
                Frames.append(page)
            reviews = pd.concat(Frames,ignore_index=True)
            result_html=reviews.to_html(justify='inherit',border=5)


            return render_template_string(result_html)
        except Exception as e:
            return print(e)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    application.run(debug=True) # running

