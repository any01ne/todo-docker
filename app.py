from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, db

# Inicjalizacja Firebase z kluczem serwisowym
cred = credentials.Certificate("firebase_key.json")  # Plik JSON z Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://todo-app-cloud-521e9-default-rtdb.firebaseio.com/'
})

# Flask app
app = Flask(__name__)
ref = db.reference('/tasks')  # Referencja do zadań w Firebase

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_text = request.form.get("task")
        if task_text:
            # Dodaj nowe zadanie do Firebase
            ref.push({
                'text': task_text,
                'done': False
            })

    # Pobierz wszystkie zadania z Firebase
    tasks_data = ref.get() or {}
    tasks = [{"key": k, "text": v["text"], "done": v["done"]} for k, v in tasks_data.items()]
    return render_template("index.html", tasks=tasks)

@app.route("/done/<key>")
def done(key):
    # Oznacz zadanie jako wykonane
    ref.child(key).update({"done": True})
    return redirect("/")

@app.route("/delete/<key>")
def delete(key):
    # Usuń zadanie
    ref.child(key).delete()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
