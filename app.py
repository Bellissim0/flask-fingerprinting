import os
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, request, make_response
from flask_cors import CORS
import json

CREATE_FINGERPRINTS_TABLE = (
    "CREATE TABLE IF NOT EXISTS fingerprints (id SERIAL PRIMARY KEY, date TIMESTAMP, platform TEXT, cookiesEnabled BOOLEAN, timezone TEXT, preferredLanguages TEXT, adblockEnabled BOOLEAN, doNotTrack TEXT, navigatorPropertiesCount INT, buildID TEXT, product TEXT, productSub TEXT, vendor TEXT, vendorSub TEXT, hardwareConcurrency INT, javaEnabled BOOLEAN, deviceMemory TEXT, screenWidth INT, screenHeight INT, screenDepth INT, screenAvailTop INT, screenAvailLeft INT, screenAvailHeight INT, screenAvailWidth INT, screenLeft INT, screenTop INT, geolocationPermission TEXT, notificationsPermission TEXT, persistentStoragePermission TEXT, webGLVendor TEXT, webGLRenderer TEXT, localStorageAvailable BOOLEAN, sessionStorageAvailable BOOLEAN, indexedDB BOOLEAN, mp3Supported TEXT, mp4Supported TEXT, aifSupported TEXT, oggSupported TEXT, ogg2Supported TEXT, h264Supported TEXT, webmSupported TEXT, vp9Supported TEXT, hlsSupported TEXT, enumerateDevicesActive BOOLEAN, gyroscope BOOLEAN, vmScore FLOAT);"
)

CREATE_MEDIA_DEVICES_TABLE = (
    "CREATE TABLE IF NOT EXISTS mediadevices (deviceId TEXT, kind TEXT, label TEXT, groupId TEXT, fingerprintId INT, FOREIGN KEY(fingerprintId) REFERENCES fingerprints(id));"
)

CREATE_HELLO_TABLE = (
    "CREATE TABLE IF NOT EXISTS hello (id SERIAL PRIMARY KEY, message TEXT);"
)

INSERT_MEDIA_DEVICE = (
    "INSERT INTO mediadevices (deviceId, kind, label, groupId, fingerprintId) values (%s,%s,%s,%s,%s)"
)

UPDATE_HELLO = (
    "UPDATE hello SET message = (%s) WHERE id = 1"
)

SELECT_MEDIA = (
    "SELECT * FROM mediaDevices WHERE fingerprintId = (%s)"
)

SELECT_HELLO = (
    "SELECT * FROM hello"
)

INSERT_FINGERPRINT = "INSERT INTO fingerprints (date, platform, cookiesEnabled, timezone, preferredLanguages, adblockEnabled, doNotTrack, navigatorPropertiesCount, buildID, product, productSub, vendor, vendorSub, hardwareConcurrency, javaEnabled, deviceMemory, screenWidth, screenHeight, screenDepth, screenAvailTop, screenAvailLeft, screenAvailHeight, screenAvailWidth, screenLeft, screenTop, geolocationPermission, notificationsPermission, persistentStoragePermission, webGLVendor, webGLRenderer, localStorageAvailable, sessionStorageAvailable, indexedDB, mp3Supported, mp4Supported, aifSupported, oggSupported, ogg2Supported, h264Supported, webmSupported, vp9Supported, hlsSupported, enumerateDevicesActive, gyroscope, vmScore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"

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
    print(data["mediaDevices"])
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_FINGERPRINTS_TABLE)
                cursor.execute(CREATE_MEDIA_DEVICES_TABLE)
                cursor.execute(INSERT_FINGERPRINT, (date, data["platform"],data["cookiesEnabled"],data["timezone"],data["preferredLanguages"],data["adblockEnabled"],data["doNotTrack"],data["navigatorPropertiesCount"],
                    data["buildID"],data["product"],data["productSub"],data["vendor"],data["vendorSub"],data["hardwareConcurrency"],data["javaEnabled"],data["deviceMemory"],data["screenWidth"],data["screenHeight"],
                    data["screenDepth"],data["screenAvailTop"],data["screenAvailLeft"],data["screenAvailHeight"],data["screenAvailWidth"],data["screenLeft"],data["screenTop"],data["permissions"]["geolocation"],
                    data["permissions"]["notifications"],data["permissions"]["persistentStorage"],data["webGLvendor"],data["webGLrenderer"],data["localStorageAvailable"],data["sessionStorageAvailable"],data["indexedDB"],
                    data["supportedAudioFormats"]["mp3"],data["supportedAudioFormats"]["mp4"],data["supportedAudioFormats"]["aif"],data["supportedVideoFormats"]["ogg"],data["supportedVideoFormats"]["ogg2"],data["supportedVideoFormats"]["h264"],
                    data["supportedVideoFormats"]["webm"],data["supportedVideoFormats"]["vp9"],data["supportedVideoFormats"]["hls"],data["enumerateDevicesActive"],data["gyroscope"],data["vmScore"]))
                id = cursor.fetchone()[0]
                for device in data["mediaDevices"]:
                    cursor.execute(INSERT_MEDIA_DEVICE, (device["deviceId"], device["kind"], device["label"], device["groupId"], id))
        return {"message": "fingerprint successfully saved."},  201
    except:
        return {}, 500

@app.get("/api/data/<id>")
def retrieve_fingerprint(id):
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_FINGERPRINTS_TABLE)
            cursor.execute(SELECT_FINGERPRINT_BY_ID, (id,))
            results = cursor.fetchone()
            id = results[0]
            date = results[1]
            platform = results[2]
            cookiesEnabled = results[3]
            timezone = results[4]
            preferredLanguages = results[5]
            adblockEnabled = results[6]
            doNotTrack = results[7]
            navigatorPropertiesCount = results[8]
            buildID = results[9]
            product = results[10]
            productSub = results[11]
            vendor = results[12]
            vendorSub = results[13]
            hardwareConcurrency = results[14]
            javaEnabled = results[15]
            deviceMemory = results[16]
            screenWidth = results[17]
            screenHeight = results[18]
            screenDepth = results[19]
            screenAvailTop = results[20]
            screenAvailLeft = results[21]
            screenAvailHeight = results[22]
            screenAvailWidth= results[23]
            screenLeft = results[24]
            screenTop = results[25]
            geolocationPermission = results[26]
            notificationsPermission = results[27]
            persistentStoragePermission = results[28]
            webGLVendor = results[29]
            webGLRenderer = results[30]
            localStorageAvailable = results[31]
            sessionStorageAvailable = results[32]
            indexedDB = results[33]
            mp3Supported = results[34]
            mp4Supported = results[35]
            aifSupported = results[36]
            oggSupported = results[37]
            ogg2Supported = results[38]
            h264Supported = results[39]
            webmSupported = results[40]
            vp9Supported = results[41]
            hlsSupported = results[42]
            enumerateDevicesActive = results[43]
            gyroscope = results[44]
            vmScore= results[45]
            cursor.execute(SELECT_MEDIA, (id, ))
            mediaDevices = cursor.fetchall()
            print(mediaDevices)
    return {"id": id, "date": date, "platform": platform, "cookiesEnabled": cookiesEnabled, "timezone": timezone, "preferredLanguages": preferredLanguages, "adblockEnabled": adblockEnabled, "doNotTrack": doNotTrack,
    "navigatorPropertiesCount": navigatorPropertiesCount, "buildID": buildID, "product": product,"productSub": productSub, "vendor": vendor, "vendorSub": vendorSub, "hardwareConcurrency": hardwareConcurrency, 
    "javaEnabled": javaEnabled, "deviceMemory": deviceMemory, "screenWidth": screenWidth, "screenHeight": screenHeight, "screenDepth": screenDepth, "screenAvailTop": screenAvailTop, "screenAvailLeft": screenAvailLeft, "screenAvailHeight": screenAvailHeight,
    "screenAvailWidth": screenAvailWidth, "screenLeft": screenLeft, "screenTop": screenTop, "geolocationPermission": geolocationPermission, "notificationsPermission": notificationsPermission, "persistentStoragePermission": persistentStoragePermission, "webGLVendor": webGLVendor,
    "webGLRenderer": webGLRenderer, "localStorageAvailable": localStorageAvailable, "sessionStorageAvailable": sessionStorageAvailable, "indexedDB": indexedDB, "mp3Supported": mp3Supported, "mp4Supported": mp4Supported, "aifSupported": aifSupported,
    "oggSupported": oggSupported, "ogg2Supported": ogg2Supported, "h264Supported": h264Supported, "webmSupported": webmSupported, "vp9Supported": vp9Supported, "hlsSupported": hlsSupported, "enumerateDevicesActive": enumerateDevicesActive, "gyroscope": gyroscope,
    "vmScore": vmScore, "mediaDevices": mediaDevices} , 200
    #except:
        #return {}, 404

@app.post("/api/hello")
def hellopost():
    data = request.get_json()
    print(data)
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_HELLO_TABLE)
                cursor.execute(UPDATE_HELLO, (data["message"], ))
        return {}, 201
    except:
        return {}, 500

@app.get("/api/hello")
def hello():
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_HELLO_TABLE)
                cursor.execute(SELECT_HELLO)
                results = cursor.fetchone()
                message = results[1]
                print(message)
                return {"message": message}, 200
    except:
        return {}, 500
