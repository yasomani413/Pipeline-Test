FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY index.html .
COPY init.sql .

# Init the DB from SQL file
RUN python -c "import sqlite3; conn = sqlite3.connect('tasks.db'); conn.executescript(open('init.sql').read()); conn.commit(); conn.close()"

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
