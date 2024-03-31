from datetime import datetime
import time
import re

import numpy as np
import requests
import serial
from kivy.core.text import LabelBase
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Rectangle, Color, Ellipse, Line
from math import sin, cos, pi
from kivymd.uix.carousel import MDCarousel
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage
from kivy.uix.widget import Widget
from kivy_garden.graph import LinePlot, Graph
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.theming import ThemeManager
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.slider import MDSlider
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import OneLineIconListItem, MDList, ThreeLineIconListItem, ImageRightWidget, ImageLeftWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.toolbar import MDTopAppBar, MDBottomAppBar
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, SwapTransition
import math
LabelBase.register("LCD14", fn_regular="C:/Users/admin/PycharmProjects/dashpanel/lcd/lcd-font/otf/LCD14.otf")

Window.size = (1200,700)


#class Arduino():
#   def __init__(self, **kwargs):
#       super(Arduino, self).__init__(**kwargs)
#
#       self.Arduino_Data = serial.Serial("com9", 9600)
        #Clock.schedule_interval(self.result, 1)
    # self.read_data = self.Arduino_Data.readline()
    # self.read_data = self.read_data.decode('utf-8', errors='ignore')
    # print(self.read_data)              # ------------------------d
#   def result(self):
#       #while True:
#       #    time.sleep(1)
#           # Read all available data from the serial port
#       self.read_data = self.Arduino_Data.readline()
#       self.read_data = self.read_data.decode('utf-8', errors='ignore')
#       digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
#       #digits = digits[0]
#       #if digits:
#       return int (digits[0])
#       #else:
#       #    return 0
#       print(digits)


class Dash_brd(MDFloatLayout):
    x_rpm_scale = NumericProperty()
    rotate = NumericProperty()
    def __init__(self, **kwargs):
        super(Dash_brd, self).__init__(**kwargs)
        #self.Arduino_Data = serial.Serial("com9", 9600)


        #Clock.schedule_interval(self.rpm, 0.05)
        #Clock.schedule_interval(self.velocity, 1)
        #self.rpm()



    def rpm(self, dt):

        self.read_data = self.Arduino_Data.readline()
        self.read_data = self.read_data.decode('utf-8', errors='ignore')
        digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
        digits = digits[0]
        #digits = 120
        #n = np.random.randint(100, 1120)
        #self.data = Arduino()
        #self.rotate = self.data.result()
        self.x_rpm_scale = digits#self.rotate
        print(digits)
        #for self.x_rpm_scale in range(1000):
        #
        #    self.x_rpm_scale += 1
        #    if self.x_rpm_scale == 1000:
        #        self.x_rpm_scale -= 1
        #        self.x_rpm_scale = 0
        #    print(self.x_rpm_scale)

        self.ids.rpm.text = str(digits)
    def velocity(self, dt):

        n = np.random.randint(0, 300)
        self.ids.speed.text = str(n)

class Gauge_temp(MDFloatLayout):

    x_coolant_temp = NumericProperty()
    def __init__(self, **kwargs):
        super(Gauge_temp, self).__init__(**kwargs)
        #Clock.schedule_interval(self.coolant_temp, 1)
        
    def coolant_temp(self, dt):
        n = np.random.randint(0, 100)
        self.x_coolant_temp = n

class Gauge_tank(MDFloatLayout):
    x_tank = NumericProperty()

    def __init__(self, **kwargs):
        super(Gauge_tank, self).__init__(**kwargs)
        #Clock.schedule_interval(self.tank, 1)

    def tank(self, dt):
        n = np.random.randint(0, 100)
        self.x_tank = n

class Oil_gauge(MDFloatLayout):
    angle_oil_pressure = NumericProperty()
    def __init__(self, **kwargs):
        super(Oil_gauge, self).__init__(**kwargs)
        #Clock.schedule_interval(self.arrow, 0.1)
    #def on_touch_down(self, touch):
    #    print(touch.pos)
    #def arrow(self, dt):
    #    data =
        #n = np.random.randint(0, 180)
        #self.angle_oil_pressure = n

class Turbo_presure_gauge(MDFloatLayout):
    angle_turbo_pressure = NumericProperty()

    def __init__(self, **kwargs):
        super(Turbo_presure_gauge, self).__init__(**kwargs)
        #Clock.schedule_interval(self.arrow, 0.01)

    # def on_touch_down(self, touch):
    #    print(touch.pos)
    def arrow(self, dt):
        n = np.random.randint(0, 270)
        self.angle_turbo_pressure = n

class sport_view(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

sport_view().run()