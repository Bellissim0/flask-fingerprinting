import os
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, request

CREATE_FINGERPRINTS_TABLE = (
    "CREATE TABLE IF NOT EXISTS fingerprints (id SERIAL PRIMARY KEY, date TIMESTAMP, description TEXT);"
)

INSERT_FINGERPRINT = "INSERT INTO fingerprints (date, description) VALUES (%s, %s) RETURNING id;"

SELECT_FINGERPRINT_BY_ID = "SELECT * FROM fingerprints WHERE id = (%s);"

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/data")
def create_fingerprint():
    data= request.get_json()
    description = data["description"]
    date = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_FINGERPRINTS_TABLE)
            cursor.execute(INSERT_FINGERPRINT, (date, description))
            fingerprint_id = cursor.fetchone()[0]
    return {"id": fingerprint_id, "message": f"fingerprint successfully saved."},  201     

@app.get("/api/data/<id>")
def retrieve_fingerprint(id):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_FINGERPRINTS_TABLE)
                cursor.execute(SELECT_FINGERPRINT_BY_ID, (id,))
                results = cursor.fetchone()
                id = results[0]
                date = results[1]
                description = results[2]
        return {"id": id, "date": date, "description": description}, 200
    except:
        return {}, 404
