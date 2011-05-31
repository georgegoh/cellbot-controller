import json
import android

WEBVIEW="/sdcard/sl4a/scripts/html/robot.html"

droid = android.Android()
droid.eventClearBuffer()
droid.log("Showing robot.html")
droid.webViewShow(WEBVIEW)

action = ""
while action != "EXIT":
    droid.log("Waiting for event")
    properties = str(droid.eventWaitFor("robotpython").result["data"])
    action = json.loads(properties)['action']
    droid.eventClearBuffer()
    droid.log("Event Properties: " + action)
