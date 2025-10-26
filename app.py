from flask import Flask, render_template, request, jsonify
from llm_interface.request_manager import RequestsManager
from server_to_latex_glue import send_llm_parsing
from llm_to_server_glue import parse_json
from flask import Response
import json

app = Flask(__name__)
manager = RequestsManager()
console_txt = "Console"

@app.route("/")
def home(): #Sets the website
    return render_template("index.html")

@app.route("/getInput", methods=["POST"])  #Gets the input
def getInput():
    data = request.get_json()
    text = data.get("text", "")
    answerDic, equationPy = parse_json(manager.get_response(text))
    value, solution, equation = send_llm_parsing(equationPy,answerDic)
    print(value)
    print(solution)
    print(equation)
    console_txt = "Done!"
    payload = {"val": value, "sol": solution, "equ": equation, "console": console_txt}

    return Response(
        json.dumps(payload, ensure_ascii=False),
        mimetype="application/json"
    )

def start_server():
    print("=== Starting server ===")

    app.run()

    print("=== Server closed ===")
#python -m flask run