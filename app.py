from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def create_table():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


@app.route('/add', methods=['POST'])
def add_task():

    task = request.form['task']
    due_date = request.form['due_date']

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, due_date) VALUES (?, ?)",
        (task, due_date)
    )

    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/delete/<int:id>')
def delete_task(id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/complete/<int:id>')
def complete_task(id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/edit/<int:id>', methods=['POST'])
def edit_task(id):

    print("UPDATE BUTTON CLICKED")

    task = request.form['task']
    due_date = request.form['due_date']

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET task = ?, due_date = ? WHERE id = ?",
        (task, due_date, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/')
def home():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    total_tasks = len(tasks)

    completed_tasks = 0
    for task in tasks:
        if task[3] == 1:
            completed_tasks += 1

    pending_tasks = total_tasks - completed_tasks

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
    )    

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
    app.run(host="0.0.0.0", port=10000)