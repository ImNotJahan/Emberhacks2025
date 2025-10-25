from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    text = data.get("text", "")
    isFull = data.get("isFull", "")
    print(text)
    print(isFull)
    return jsonify({"message": f"Answer: {text}"})

"""
@app.route("/submit", methods=["POST"])
def submit():
    isFull = request.form.get("fullWork") 
    if isFull:
        print("Full")
    else:
        print("NotFull")
    return None
"""

#python -m flask run