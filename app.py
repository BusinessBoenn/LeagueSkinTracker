from flask import Flask, render_template
import json
import os
import subprocess
import webbrowser
from threading import Timer


path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)


app = Flask(__name__)
def run_GetSkins():
    subprocess.run(["python", "GetSkins.py"], check=True)

def load_skins():
        with open("final.json", "r") as f:
            return json.load(f)


@app.route("/")
def home():
    try:
        skins = load_skins()
        return render_template("index.html", skins=skins)
    except:
        run_GetSkins()
        return f"<h1>First time use?</h1><pre>Make sure League of Legends is running and to <a href='/'>create the needed file.</a></pre>"


@app.route("/update")
def update():
    try:
        run_GetSkins()
        skins = load_skins()
        return render_template("index.html", skins=skins)
    except Exception as e:
        return f"<h1>Error updating skins</h1><pre>{e}</pre>"

if __name__ == "__main__":
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
    app.run()
