from flask import Flask, render_template, request

from auth.models import RequestDto, UserDto
from llm_interface.request_manager import RequestsManager
from server_to_latex_glue import send_llm_parsing
from llm_to_server_glue import parse_json
from flask import Response
from auth.main import Database
import json


class Application:
    app = Flask(__name__)

    def __init__(self):
        # self.app = Flask(__name__)
        self.manager = RequestsManager()
        self.console_txt = "Console"
        self.db = Database()
        self.current_user = None
        self.add_routes()

    def add_routes(self):
        # Register the methods on the instance's app object
        self.app.add_url_rule("/", view_func=self.home)
        self.app.add_url_rule("/verifylogin", view_func=self.verify_login)
        self.app.add_url_rule("/signin", view_func=self.sign_in)
        self.app.add_url_rule("/login", view_func=self.login)
        self.app.add_url_rule("/getInput", view_func=self.get_input,
                              methods=["POST"])
        self.app.add_url_rule("/verify-signup", view_func=self.verify_signup, methods=["POST"])

    # @app.route("/verifylogin")
    def verify_login(self):
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        user = self.db.get_user_by_username(username)
        if user is None or user.password != password:
            return "username or password are incorrect"
        self.current_user = user
        return render_template("index.html")


    def verify_signup(self):
        data = request.get_json()
        username = data.get("username", None)
        email = data.get("")
        password = data.get("password", None)
        if all(i is not None for i in (username, email, password)):
            return "All fields must be filled"
        if self.db.username_is_taken(username):
            return "Username is taken"
        if self.db.email_is_taken(email):
            return "Email is taken"
        self.current_user = self.db.post_user(UserDto(username, email, password))
        return render_template("index.html")


    # @app.route("/")
    def home(self): #Sets the website to index - main html
        return render_template("index.html")

    # @app.route("/signin")
    def sign_in(self):
        return render_template("signin.html")

    # @app.route("/login")
    def login(self):
        return render_template("login.html")

    # @app.route("/getInput", methods=["POST"])  #Gets the req
    def get_input(self):
        data = request.get_json()
        text = data.get("text", "")
        response = self.manager.get_response(text)
        # check if an error occurred
        if response[:5] == "[ERR]":
            return Response(
                json.dumps({"failed": True, "console": response[5:]}),
                mimetype="application.json"
            )
        answer_dict, equation_py = parse_json(response)
        value, solution, equation = send_llm_parsing(equation_py, answer_dict)
        console_txt = "Done!"
        payload = {"val": value, "sol": solution, "equ": equation, "console": console_txt, "failed": False}
        if not payload["failed"] and self.current_user is not None:
            self.db.post_request(RequestDto(self.current_user.id, text, value, solution, equation))
        return Response(
            json.dumps(payload, ensure_ascii=False),
            mimetype="application/json"
        )

    def start_server(self):
        print("=== Starting server ===")
        self.app.run()
        print("=== Server closed ===")
#python -m flask run