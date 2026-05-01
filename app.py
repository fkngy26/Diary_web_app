from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    html=render_template('home_page.html')
    return html

if __name__ == "__main__":
    app.run()