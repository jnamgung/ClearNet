# Handle all end user transactions through link
from flask import Flask, redirect, render_template, make_response, request
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/check', methods = ['POST', 'GET'])
def check():
    if request.method == 'POST':
        user = request.form['user']
        return render_template('register.html', value=user)


@app.route('/link/<out>')
def link(out):
    return '<h1>Hello, World! Welcome to ' + out + '!</h1>'

@app.route('/redirect/<link>/<out>') 
def redirection(link, out):
    return redirect("https://www." + link + ".com/" + out)



if __name__ == '__main__':
    app.run(debug=True)