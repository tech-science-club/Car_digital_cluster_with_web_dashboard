import re
import sys
import serial
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy_garden.mapview import MapSource, MapView, MapMarkerPopup
import re
import time
from io import BytesIO
import requests
import serial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Rectangle, Color, Line
from math import sin, cos, pi
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.carousel import MDCarousel
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.theming import ThemeManager
from kivymd.uix.screen import Screen, MDScreen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDRectangleFlatIconButton, \
    MDFloatingActionButton
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
from kivymd.font_definitions import theme_font_styles
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import Image
from datetime import datetime
from kivy_garden.graph import Graph, MeshLinePlot, LinePlot
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import pyrebase



class Ruler(MDFloatLayout):
    pass

class GPS(MDFloatLayout):
    latitude   = NumericProperty()
    longitude  = NumericProperty()
    lat = NumericProperty()
    lon = NumericProperty()
    
    def __init__(self, **kwargs):
        super(GPS, self).__init__(**kwargs)
        #self.mapview = self.ids.mapview  # Adjust this based on your actual structure
        # Set the size of the MapView to match the parent size
        #self.ids.mapview.size = self.size

        #self.mapview = MapView(zoom=15,  lat='55.736061', lon='11.509603')
        #self.marker = MapMarkerPopup(lat=self.lat, lon=self.lon)
        #self.mapview.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        #self.mapview.size_hint = 0.5, 0.5
        #
        #self.mapview.add_widget(self.marker)
        #self.add_widget(self.mapview)
        #self.bind(on_mouse_wheel=self.update_text)
        #self.add_widget(Ruler())
        #self.scale_text = "200 m"
        #self.data = serial.Serial("com5", 9600)
        self.Longt = []
        self.Lat = []
        self.new_longitude = None
        self.new_latitude = None

        #Clock.schedule_interval(self.start, 1)
        #self.update_marker(self.lat, self.lon)
    def start(self, *args):

        self.read_data = self.data.readline()
        self.read_data = self.read_data.decode()
        digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
        self.longitude = digits[0]
        self.latitude = digits[1]

        if self.new_longitude != self.longitude and self.new_latitude != self.latitude:
            self.Longt.append(self.longitude)
            new_longitude = self.longitude

            self.Lat.append(self.latitude)
            new_latitude = self.latitude
        #print(digits)
        self.lat = self.Longt[-1]
        self.lon = self.Lat[-1]
        #print(self.Longt)
        #print(self.Lat)

        self.long = float(self.Lat[0])
        self.lati = float(self.Longt[0])

    def on_touch_down(self, touch):
        #if self.ids.slider_box.collide_point(*touch.pos):
        zoom = Animation(size_hint=(0.95, 0.9), duration=1.0, t='in_out_elastic')
        #self.ids.map.size_hint = (0.95, 0.9)
        zoom.start(self.ids.map)
   #        return True
   #    else:
   #        #self.mapview.disabled = False
   #        return super(GPS, self).on_touch_up(touch)
class Scale(MDFloatLayout):
    pass

class Ruler(MDFloatLayout):
    pass




class Map(MDApp):
    #def build(self):
    #    return MapView()
    pass
Map().run()