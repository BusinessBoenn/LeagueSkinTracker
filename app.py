from flask import Flask, render_template, jsonify, redirect, url_for
import json
import os
import subprocess
import threading

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)


app = Flask(__name__)

def run_GetSkins():
    subprocess.run(["python", "GetSkins.py"], check=True)


def load_skins():
    with open("final.json", "r", encoding="utf-8-sig") as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("loading.html")

@app.route("/data")
def data():
    try:
        run_GetSkins()
        skins = load_skins()
        return render_template("index.html", skins=skins)
    except Exception as e:
        return f"<h1>Fehler beim Laden:</h1><pre>{e}</pre>"



if __name__ == "__main__":
    app.run(debug=True)