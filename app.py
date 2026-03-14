from flask import Flask, render_template, request
from govflow import run_agent

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = None

    if request.method == "POST":
        user_request = request.form["request"]
        response = run_agent(user_request)

    return render_template("templates_index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)