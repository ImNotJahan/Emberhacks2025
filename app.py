from flask import Flask, render_template, request, jsonify
from llm_interface.request_manager import RequestsManager
from server_to_latex_glue import send_llm_parsing
from llm_to_server_glue import parse_json
from flask import Response
import json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

#auth = HTTPBasicAuth()
USERS = {
    "alice": "1111",
    "bob":   "1111",
}


app = Flask(__name__)
manager = RequestsManager()
console_txt = "Console"

@app.route("/verifylogin")
def verifylogin(username, password):
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    if username in USERS and password == USERS[username]:
        return username  # return any user object/identifier
    else:
        return render_template("index.html")


@app.route("/")
def home(): #Sets the website to index - main html
    return render_template("index.html")
@app.route("/sighnin")
def sighnin():
    return render_template("sighnin.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/getInput", methods=["POST"])  #Gets the req
def getInput():
    data = request.get_json()
    text = data.get("text", "")
    response = manager.get_response(text)
    # check if an error occurred
    if response[:5] == "[ERR]":
        return Response(
            json.dumps({"failed": True, "console": response[5:]}),
            mimetype="application.json"
        )
    answerDic, equationPy = parse_json(response)
    value, solution, equation = send_llm_parsing(equationPy,answerDic)
    console_txt = "Done!"
    payload = {"val": value, "sol": solution, "equ": equation, "console": console_txt, "failed": False}
    return Response(
        json.dumps(payload, ensure_ascii=False),
        mimetype="application/json"
    )
def start_server():
    print("=== Starting server ===")
    app.run()
    print("=== Server closed ===")
#python -m flask run