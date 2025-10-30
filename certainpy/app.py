from flask import Flask, render_template, request, jsonify
from .llm_interface.request_manager import RequestsManager
from .server_to_latex_glue import send_llm_parsing
from .llm_to_server_glue import parse_json
from flask import Response
import json

app = Flask(__name__)
manager = RequestsManager()

@app.route("/")
def home(): #Sets the website to index - main html
    return render_template("index.html")

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
    dictionery, equationPY = parse_json(response)
    value, solution, equation = send_llm_parsing(equationPY,dictionery)
    payload = {"val": value, "sol": solution, "equ": equation, "console": "Done!", "failed": False}
    return Response(
        json.dumps(payload, ensure_ascii=False),
        mimetype="application/json"
    )

def start_server():
    print("=== Starting server ===")
    app.run()
    print("=== Server closed ===")
#python -m flask run