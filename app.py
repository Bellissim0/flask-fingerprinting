import os
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, request, make_response
from flask_cors import CORS

CREATE_FINGERPRINTS_TABLE = (
    "CREATE TABLE IF NOT EXISTS fingerprints (id SERIAL PRIMARY KEY, date TIMESTAMP, platform TEXT, cookiesEnabled BOOLEAN, timezone TEXT, preferredLanguages TEXT, adblockEnabled BOOLEAN, doNotTrack TEXT, navigatorPropertiesCount INT, buildID TEXT, product TEXT, productSub TEXT, vendor TEXT, vendorSub TEXT, hardwareConcurrency INT, javaEnabled BOOLEAN, deviceMemory TEXT, screenWidth INT, screenHeight INT, screenDepth INT, screenAvailTop INT, screenAvailLeft INT, screenAvailHeight INT, screenAvailWidth INT, screenLeft INT, screenTop INT, geolocationPermission TEXT, notificationsPermission TEXT, persistentStoragePermission TEXT, pushPermission TEXT, webGLVendor TEXT, webGLRenderer TEXT, localStorageAvailable BOOLEAN, sessionStorageAvailable BOOLEAN, indexedDB BOOLEAN, mp3Supported TEXT, mp4Supported TEXT, aifSupported TEXT, oggSupported TEXT, ogg2Supported TEXT, h264Supported TEXT, webmSupported TEXT, vp9Supported TEXT, hlsSupported TEXT, enumerateDevicesActive BOOLEAN, mediaDevicesID INT, gyroscope BOOLEAN, vmScore FLOAT);"
)

CREATE_MEDIA_DEVICES_TABLE = (
    "CREATE TABLE IF NOT EXISTS mediadevices (id SERIAL PRIMARY KEY, deviceId TEXT, kind TEXT, label TEXT, groupId TEXT);"
)

CREATE_HELLO_TABLE = (
    "CREATE TABLE IF NOT EXISTS hello (id SERIAL PRIMARY KEY, message TEXT);"
)

INSERT_FINGERPRINT = "INSERT INTO fingerprints (date, platform, cookiesEnabled, timezone, preferredLanguages, adblockEnabled, doNotTrack, navigatorPropertiesCount, buildID, product, productSub, vendor, vendorSub, hardwareConcurrency, javaEnabled, deviceMemory, screenWidth, screenDepth, screenAvailTop, screenAvailLeft, screenAvailHeight, screenAvailWidth, screenLeft, screenTop, geolocationPermission, notificationsPermission, persistentStoragePermission, pushPermission, webGLVendor, webGLRenderer, localStorageAvailable, sessionStorageAvailable, indexedDB, mp3Supported, mp4Supported, aifSupported, oggSupported, ogg2Supported, h264Supported, webmSupported, vp9Supported, hlsSupported, enumerateDevicesActive, mediaDevicesID, gyroscope, vmScore) VALUES (%s) RETURNING id;"

SELECT_FINGERPRINT_BY_ID = "SELECT * FROM fingerprints WHERE id = (%s);"

load_dotenv()

app = Flask(__name__)
CORS(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/data")
def create_fingerprint():
    data= request.get_json()
    date = datetime.now(timezone.utc)
    print(data)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_FINGERPRINTS_TABLE)
            cursor.execute(INSERT_FINGERPRINT, (date,))
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
