from flask import Flask, render_template, request
from govflow import run_agent


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():

    response=None
    pdf=None

    if request.method=="POST":

        user_request=request.form["request"]

        response=run_agent(user_request)

        if "passport" in user_request.lower():
            pdf="/forms/passport_renewal.pdf"

    return render_template("templates_index.html",response=response,pdf=pdf)


if __name__=="__main__":
    app.run(debug=True)

from flask import send_from_directory
import os

@app.route('/forms/<path:filename>')
def download_file(filename):
    return send_from_directory('forms', filename)