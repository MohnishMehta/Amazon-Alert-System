#import libraries
from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime
import re
import csv


#function to send mail to user if price is below their desired price point
def send_mail(user_name, amazon_link, desired_price, user_email, app_password):
    # Connect to the server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()

    # Login to the email account
    server.login(user_email,app_password)  # Replace 'password' with your actual password or use an app-specific password

    # Email content
    subject = (f"The item you want is below {desired_price} ! Now is your chance to buy!")
    body = (f"{user_name}, this is the moment we have been waiting for. Now is your chance to pick up the item of your dreams. Don't mess it up! Link here: {amazon_link}")

    msg = (f"Subject: {subject}\n\n{body}")

    # Send the email
    server.sendmail(
        'WebScraper@gmail.com',  # From
        user_email,  # To (Replace with the actual recipient email)
        msg  # Message
    )

#automatic script that will run everyday to check price point and call the send_mail function if price is below user's desired price
def gather_data(user_name, amazon_link, desired_price, user_email, app_password, headers):

    #Connects to Amazon link and gathers data
    page = requests.get(amazon_link, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id='productTitle').get_text()
    whole_price_element = soup2.find('span', {'class': 'a-price-whole'})
    fraction_price_element = soup2.find('span', {'class': 'a-price-fraction'})

    # Cleans data and makes it easier to read
    if whole_price_element and fraction_price_element:
        whole_price = re.sub(r'\D', '', whole_price_element.text.strip())
        fraction_price = re.sub(r'\D', '', fraction_price_element.text.strip())
        price = float(f'{whole_price}.{fraction_price}')

    title = title.strip()

    # Creates a timestamp to track when data was collected
    today = datetime.date.today()

    # Create a csv file and writes headers and data into CSV file
    header = ['Title', 'Price', 'Date']
    data = [title, price, today]

    # to append data to the file
    with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    #to send mail to user once product price is lower than desired price
    if (price < desired_price):
        send_mail(user_name,amazon_link,desired_price,user_email,app_password)
        return True
    return False

#function to keep the script running everyday and till email is sent
def start_scraper(user_name , amazon_link , desired_price , user_email , app_password, user_headers):
    keep_running = True
    while(keep_running):
        keep_running = not gather_data(user_name, amazon_link, desired_price, user_email, app_password, user_headers)
        if keep_running:
            time.sleep(86400)













