import json
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATA_FILE = "entries.json"

def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return[]

def save_entries():
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f)

entries = load_entries()
next_id = max([e["id"] for e in entries], default=0) + 1

@app.route("/", methods=["GET", "POST"])
def home():
    global next_id
    if request.method == "POST":
        entry = {
            "id": next_id,
            "title" : request.form["title"],
            "type": request.form["type"],
            "site": request.form["site"],
            "progress": int(request.form["progress"]),
        }
        next_id += 1
        entries.append(entry)
        return redirect("/")
    return render_template("index.html", entries=entries)

@app.route("/increment/<int:entry_id>", methods=["POST"])
def increment(entry_id):
    for entry in entries:
        if entry["id"] == entry_id:
            entry["progress"] +=1
    save_entries()    
    return redirect("/")

@app.route("/update/<int:entry_ids>", methods=["POST"])
def update(entry_id):
    for entry in entries:
        if entry["id"] == entry_id:
            entry["progress"] = int(request.form["progress"])
    save_entries()
    return redirect("/")

@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete(entry_id):
    global entries
    entries = [e for e in entries if e["id"] != entry_id]
    save_entries()
    return redirect("/")