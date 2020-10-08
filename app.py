# 3rd party packages
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # Dummy home page
    return render_template('index.html')


@app.route('/about')
def about():
    # Dummy about page
    return render_template('about.html')

@app.route('/home')
def home():
    # Dummy about page
    return render_template('home.html')

@app.route('/driver')
def driver():
    # Dummy about page
    return render_template('driver.html')        


if __name__ == '__main__':
    app.run(debug=True)