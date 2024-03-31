from datetime import datetime
import time
import re

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

Window.size = (1200,800)

class Dash_brd(MDFloatLayout):
    w = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Dash_brd, self).__init__(**kwargs)
        #self.Arduino_Data = serial.Serial("com7", 9600)
        #self.start()
    def start(self):
        Clock.schedule_interval(self.data, 0.01)

    def data(self, *args):
        self.read_data = self.Arduino_Data.readline()
        self.read_data = self.read_data.decode()       
        self.digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
        #print(self.digits)
        self.w = self.digits[0]
        print(self.w)
        speed = round(self.w/10)
        self.ids.speed.text = str(speed)

class dash_retro_styleApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

dash_retro_styleApp().run()