from flask import Flask, render_template, request, redirect

app = Flask(__name__)

entries = []
next_id = 1
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
        return redirect("/")

@app.route("/update/<int:entry_ids>", methods=["POST"])
def update(entry_id):
    for entry in entries:
        if entry["id"] == entry_id:
            entry["progress"] = int(request.form["progress"])
    return redirect("/")

@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete(entry_id):
    global entries
    entries = [e for e in entries if e["id"] != entry_id]
    return redirect("/")