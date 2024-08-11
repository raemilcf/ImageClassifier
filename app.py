
    # Load model and tokenizer
import tensorflow as tf
from transformers import TFBartForConditionalGeneration
import pickle
import re
from utils import util


from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def getSumarization():
    userText = request.args.get('fullText')
    minWords = request.args.get('minWords')
    maxWords = request.args.get('maxWords')
    # if minWords == '':
    #     minWords=40

    # if maxWords =='':
    #     maxWords=100
    



    # #get summary 
    # result =  getSummary(userText, int(minWords), int(maxWords))

   
    return userText


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4700)
    app.run()
