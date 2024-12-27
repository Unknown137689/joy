# server.py
from flask import Flask, redirect, url_for, make_response
import time

app = Flask(__name__)
temp_links = {}

@app.route('/generate-temp-link')
def generate_temp_link():
    temp_link = f"/temp-link-{int(time.time())}"
    temp_links[temp_link] = time.time() + 600  # Expires in 10 minutes
    return temp_link

@app.route('/temp-link-<int:timestamp>')
def temp_link(timestamp):
    link = f"/temp-link-{timestamp}"
    current_time = time.time()
    if link in temp_links and temp_links[link] > current_time:
        response = make_response(redirect(url_for('main')))
        response.headers['X-Temp-Link'] = link
        return response
    else:
        return "This link has expired."

@app.route('/main')
def main():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Main Page</title>
    </head>
    <body>
        <h1>Welcome to the Main Page!</h1>
        <p>This is the content of the main.html file.</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
