from datetime import time
from threading import Thread

import pynmea2
import serial
from kivy.clock import Clock

class Dash_Board(Thread):
    rpm = 0
    speed = 0
    t = 21
    fuel = 0
    consm = 0
    arrow_angle = 0
    widget_name = None
    widget_yaxes_name = None
    arrow_speed = 0
    arrow_rpm = 0
    lat = 0
    lon = 0
    num = 0
    line = 0
    gps_message = None
    at_response = None
    msg = None

class GPS(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

        Clock.schedule_interval(self.read_gps_data, 0.5)
        self.ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.2)
        # print("gps class launched")

    def read_gps_data(self, dt):
        newdata = self.ser.readline()

        data = newdata.decode("ISO-8859-1")
        data = data.strip("b\r\n")
        Dash_Board.gps_message = data
        # print(data)
        if data[0:6] == "$GPRMC":
            newmsg = pynmea2.parse(data)
            Dash_Board.lat = newmsg.latitude
            Dash_Board.lon = newmsg.longitude

class GSM(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

        self.gsm_serial = serial.Serial('/dev/ttyAMA2', 115200, timeout=1)
        # print("gsm port is opened")

        self.root_class = Dash_Board()

        self.lon = self.root_class.lon
        self.lat = self.root_class.lat
        self.speed = self.root_class.speed
        self.rpm = self.root_class.rpm
        self.consm = self.root_class.consm
        self.delim = '\r\n'
        self.gps_data = "&longitude=" + str(self.lon) + "&latitude=" + str(self.lat)
        self.engine_data = "&speed=" + str(self.speed) + "&rpm=" + str(self.rpm) + "&consm=" + str(
            self.consm) + "&CO2=" + str(self.consm * 2.3)
        self.data = self.engine_data + " " + self.gps_data

        self.initialize_gsm()
        Clock.schedule_interval(self.transmit_gsm_data, 1)

    def initialize_gsm(
            self):  # --------------------------------> initializtion of communication of gsm module

        self.gsm_serial.reset_input_buffer()
        commands = [
            "AT",
            "AT+CSQ",
            "AT+CREG?",
            "AT+CGATT=1",
            "AT+CGDCONT=1,\"IP\",\"internet\"",
            "AT+CGACT=1,1"
        ]
        for cmd in commands:
            self.send_gsm_command(cmd)
            time.sleep(0.5)

    def send_gsm_command(self, cmd):
        cmd += '\r\n'
        self.gsm_serial.write(cmd.encode())
        line = self.gsm_serial.read(100).decode("ISO-8859-1").rstrip()
        Dash_Board.at_response = line
        # print(line)                                                    #gsm's callback about connection

    def transmit_gsm_data(self, dt):
        # print("data is transmitting")
        gps_data = f"&longitude={Dash_Board.lon}&latitude={Dash_Board.lat}"
        engine_data = f"&speed={Dash_Board.speed}&rpm={Dash_Board.rpm}&consm={Dash_Board.consm}&CO2={Dash_Board.consm * 2.3}"
        data = f"{engine_data} {gps_data}"
        command = f"AT+HTTPPOST=\"http://*your_php_page_is_here*\",\"application/x-www-form-urlencoded\",\"{data}\""
        command += self.delim
        self.send_gsm_command(command)
        # print("send command: ",command)