from flask import render_template
from SST_api import app

@app.route('/')
@app.route('/about')
def index():
    return render_template("index.html",
                           title = 'What is it?',
                           )