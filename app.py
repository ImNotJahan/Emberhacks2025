from flask import Flask, render_template, request, jsonify
from latex_extension.data import MeasuredData

app = Flask(__name__)

@app.route("/")
def home(): #Sets the website
    return render_template("index.html")
@app.route("/getInput", methods=["POST"])  #Gets the input
def getInput():
    data = request.get_json()
    text = data.get("text", "")
    isFull = data.get("isFull", "")
    print(text)
    print(isFull)
    return jsonify({"message": f"Answer: {text}"}) #Gives out teh answer

#python -m flask run