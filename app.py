from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
CORS(app)

DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tasksdb")

def get_db():
    conn = psycopg2.connect(DB_URL)
    return conn

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "title is required"}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING *", (data["title"],))
    task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(task)), 201

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    if not task:
        return jsonify({"error": "not found"}), 404
    done = bool(data.get("done", task["done"]))
    title = data.get("title", task["title"])
    cur.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *", (title, done, task_id))
    task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(task))

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
