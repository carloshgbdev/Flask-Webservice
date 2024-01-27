from flask import Flask, request, render_template, make_response 

app = Flask(__name__, template_folder='view') 

@app.route('/')
def home():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)
