from flask import Flask, render_template, request, redirect

app = Flask(__name__)
tasks = []  # Lista zadań trzymana w pamięci (znika po restarcie)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            tasks.append({"text": task, "done": False})
    return render_template("index.html", tasks=tasks)

@app.route("/done/<int:task_id>")
def done(task_id):
    tasks[task_id]["done"] = True
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks.pop(task_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
