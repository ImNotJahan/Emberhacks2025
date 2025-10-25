from flask import Flask, render_template, request, jsonify
from latex_extension.data import MeasuredData
from llm_interface.request_manager import RequestsManager
from main import parce_json
from server_to_latex_glue import send_llm_parsing

app = Flask(__name__)
manager = RequestsManager()

@app.route("/")
def home(): #Sets the website
    return render_template("index.html")
@app.route("/getInput", methods=["POST"])  #Gets the input
def getInput():
    value = "1"
    solution = "solution 1111+1111=2222"
    equation = "equation***"
    
    data = request.get_json()
    text = data.get("text", "")
    answerDic, equationPy = parce_json(manager.get_response(text))
    send_llm_parsing(equationPy,answerDic)
    return jsonify({"message": f"Answer: {answerDic}"},{"val": f"Answer: {value}"},{"sol": f"Answer: {solution}"},{"equ": f"Answer: {equation}"}) #Gives out the answer

#python -m flask run