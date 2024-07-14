from flask import Flask, request, render_template,redirect,url_for
import threading
from main import start_scraper


app = Flask(__name__)

submitted_data = []

#renders templates of various pages
@app.route('/')
def alert_system():
    return render_template('alert_system.html')

@app.route('/app_password')
def app_password():
    return render_template('app_password.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/submisson_page')
def submission_page():
    return render_template('submission_page.html')


@app.route('/goto_alert_system')
def goto_alert_system():
    return redirect(url_for('alert_system'))


#once form is sumbitted, the varibles are assigned and set to the data dictionary
@app.route('/submit', methods = ['POST'])
def submit():
    name = request.form['name']
    amazon_link = request.form["amazon_link"]
    desired_price = request.form["desired_price"]
    email = request.form["email"]
    apps_password = request.form["app_password"]


    user_headers = {
        'User-Agent': request.headers.get('User-Agent'),
        'Accept-Language': request.headers.get('Accept-Language'),
        'Accept-Encoding': request.headers.get('Accept-Encoding'),
        'Referer': request.headers.get('Connection'),
        'Upgrade-Insecure-Requests': request.headers.get('Upgrade-Insecure-Requests')
    }


    data = {
        'name': name,
        'amazon_link': amazon_link,
        'desired_price': desired_price,
        'email': email,
        'apps_password': apps_password,
        'headers': user_headers
    }

    #appends to array to use as parameters
    submitted_data.append(data)

    #calls the script with parameters
    threading.Thread(target=start_scraper, args=(name, amazon_link, float(desired_price), email, apps_password, user_headers)).start()

    #renders the submission page
    return render_template('submission_page.html')

if __name__ == '__main__':
    app.run(debug=True)

