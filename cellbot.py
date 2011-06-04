#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: George Goh (georgegoh@spodon.com)

import json
import android
import bluetooth

SCAN_VIEW="/sdcard/sl4a/scripts/html/scan.html"
CONTROL_VIEW="/sdcard/sl4a/scripts/html/control.html"
CELLBOT_UUID = "00001101-0000-1000-8000-00805F9B34FB"


class CellbotController(object):

    def __init__(self):
        self.droid = android.Android()
        self.droid.toggleBluetoothState(True)
        self.discovered_devices = []
        self.socket = None
        self.handlers = {"scanBluetooth": self.scan_bluetooth,
            "connectBluetoothDevice": self.connect_bluetooth_device,
            "move": self.move}


    def start(self):
        self.droid.eventClearBuffer()
        self.droid.log("Showing bluetooth scan screen.")
        self.droid.webViewShow(SCAN_VIEW)

        action = ""
        while action != "EXIT":
            self.droid.log("Python: Waiting for event.")
            event_data = self.droid.eventWaitFor("PYTHON").result["data"]
            self.droid.log("Python: Event received. Processing...")
           
            # unpack the event data and perform action(if available).
            properties = json.loads(event_data)
            self.droid.log("Result: " + str(properties))
            action = properties["action"]
            if action in self.handlers:
                self.handlers[action](properties["data"])


    def scan_bluetooth(self, arg):
        """ Discover nearby Bluetooth devices and trigger an SL4A event
            "bluetoothDevicesFound" with the list of devices found.
        """
        self.droid.log("Scanning bluetooth devices")
        self.discovered_devices = bluetooth.discover_devices(lookup_names=True)
        self.droid.log("Devices found: " + str(self.discovered_devices))
        self.droid.eventPost("bluetoothDevicesFound", json.dumps(self.discovered_devices))


    def connect_bluetooth_device(self, bd_addr):
        """ Connect to a Bluetooth device specified by the bd_addr address
            and display the control view for the device.
        """
        service = bluetooth.find_service(uuid=CELLBOT_UUID, address=bd_addr)[0]
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.connect((service["host"], service["port"]))
        self.droid.webViewShow(CONTROL_VIEW)


    def move(self, direction):
        """ Move a connected Cellbot in one of the following directions:
                f - Forward
                b - Back
                l - Left
                r - Right
                s - Stop
        """
        if self.socket:
            self.socket.send(direction + "\n")


if __name__ == "__main__":
    connection = CellbotController()
    connection.start()
