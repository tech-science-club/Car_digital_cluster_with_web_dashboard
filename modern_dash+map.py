import re
from datetime import datetime
import time

import numpy as np
import requests
import serial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Rectangle, Color, Ellipse, Line
from math import sin, cos, pi

from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.uix.anchorlayout import MDAnchorLayout
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

Window.size = (1200, 700)


class Dash_Board(MDFloatLayout):
	w = NumericProperty(0)

	#def on_touch_down(self, touch):
	#	print(touch.pos)


	def __init__(self, **kwargs):
		super(Dash_Board, self).__init__(**kwargs)
		#self.Arduino_Data = serial.Serial("com7", 9600)
		#self.start()
		#self.box = MDFloatLayout()
		##self.box.size_hint = 0.3, 0.3
		#self.box.pos_hint = {"center_x": 0.5, "center_y": 0.5}
		#self.box.add_widget(GPS())
		#self.add_widget(self.box)
		
	def start(self):
		Clock.schedule_interval(self.data, 0.01)

	def data(self, *args):
		self.read_data = self.Arduino_Data.readline()
		self.read_data = self.read_data.decode()
		self.digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
		print(self.digits)
		self.angle = self.digits[0]
		print(self.w)
		self.w = str(self.angle*250/1023)
		#self.ids.speed.text = str(self.w / 10)

class GPS(MDFloatLayout):
	latitude = NumericProperty()
	longitude = NumericProperty()
	lat = NumericProperty()
	lon = NumericProperty()

	def __init__(self, **kwargs):
		super(GPS, self).__init__(**kwargs)
		#self.size_hint =  0.65, 0.45
		#self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
		#self.mapview = MapView(zoom=10, lat='55.736061', lon='11.509603')
		##self.mapview.center_on(self.lat, self.lon)
		#self.marker = MapMarkerPopup(lat='55.736061', lon='11.509603')
		#self.mapview.pos_hint = {"center_x": 0.5, "center_y": 0.5}
		#self.mapview.size = self.parent.size
		#self.map_box = MDAnchorLayout(
		#	pos_hint = {"center_x": 0.5, "center_y": 0.5},
		#	size_hint =( 0.65, 0.45),
		#	#size = (750, 400),
		#	id ="mapbox"
		#)
		#self.map_box.id = "mapbox"
		#self.mapview.add_widget(self.marker)
		#self.add_widget(self.mapview)
		#self.add_widget(self.map_box)

		#self.add_widget(Ruler())
		
		#self.data = serial.Serial("com5", 9600)
		self.Longt = []
		self.Lat = []
		self.new_longitude = None
		self.new_latitude = None
		#self.start()
		#Clock.schedule_interval(self.start, 1)

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
		# print(digits)
		self.lat = self.Longt[-1]
		self.lon = self.Lat[-1]
		# print(self.Longt)
		# print(self.Lat)

		self.long = float(self.Lat[0])
		self.lati = float(self.Longt[0])
		#self.update_marker(self.lat, self.lon)
		#self.data.close()

	def update_marker(self, lat, lon):
		# Update the marker position with new GPS data
		self.marker.lat = lat
		self.marker.lon = lon

	#def update_position(self, lat, lon):
	#	self.mapview.center_on(self.lat, self.lon)

	def update_text(self):
		ruler = Ruler()
		# if touch.is_mouse_scrolling:
		max_zoom = 19  # Maximum zoom level
		min_scale = 50  # Minimum scale in meters per cm

		# Calculate the scale based on the exponential relationship
		self.scale = min_scale * (2 ** (max_zoom - self.mapview.zoom))
		# self.scale = 200 / 2**self.mapview.zoom  # Adjust the scale factor as needed
		self.ids.scale_text.text = f"{int(self.scale)} m"
		if self.scale > 999:
			self.ids.scale_text.text = f"{int(self.scale / 1000)} km"
		# print(self.ids.scale_text.text)
		print(self.mapview.zoom)

	#def on_touch_down(self, touch):
	#	zoom = Animation(size_hint=(0.95, 0.9), duration=1.0, t='in_out_elastic')
	#	zoom.start(self.ids.map)

class Scale(MDFloatLayout):
    pass

class Ruler(MDFloatLayout):
    pass

class Map(MDFloatLayout):
	def __init__(self, **kwargs):
		super(Map, self).__init__(**kwargs)

		
	def on_touch_down(self, touch):
		#self.ids.map.size_hint = (0.95, 0.9)
		zoom = Animation(size_hint=(0.95, 0.9), duration=1.0, t='in_out_elastic')
		zoom.start(self.ids.map)


		
class LBl(MDFloatLayout):
	def __init__(self, **kwargs):
		super(LBl, self).__init__(**kwargs)
		#self.lbl_speed = MDLabel(text = " --- ", font_size = 46, pos = (500, 40), text_color = (1,0,0,1))
		
	def on_touch_down(self, touch):
		self.canvas.remove(self.canvas.children[10])
		self.canvas.remove(self.canvas.children[12])

		#self.add_widget(self.lbl_speed)
		#shift = Animation( size = (75, 75), pos=(120, 40),duration=1.0, t='in_out_elastic')
		#shift.start(self.ids.lbl1)
		#shift1 = Animation( pos=(46, 44),duration=1.0, t='in_out_elastic')
		#shift1.start(self.ids.lbl2)
		#print(self.canvas.children)
	#pass
class Digital_box(MDLabel):
	def __init__(self, **kwargs):
		super(Digital_box, self).__init__(**kwargs)
		self.lbl_speed = MDLabel(text="100", pos=(300, 10),
							)
		self.lbl_kmh = MDLabel(text="KM/H", pos=(380, 0),
							)
		self.lbl_tacho = MDLabel(text="2500", #pos=(600, 10),
		)
		self.lbl_rpm = MDLabel(text="RPM", pos=(920, 0),
		)
		self.lbl_tacho.font_size = 60
		self.lbl_tacho.font_name = 'TickingTimebombBB'
		self.lbl_tacho.size = 200, 50
		self.lbl_tacho.pos = 800, 35

		self.lbl_speed.font_size = 60
		self.lbl_speed.font_name = 'TickingTimebombBB'

	def on_touch_down(self, touch):
		self.add_widget(self.lbl_speed)
		self.add_widget(self.lbl_kmh)
		self.add_widget(self.lbl_tacho)
		self.add_widget(self.lbl_rpm)

class Speedometr(MDFloatLayout):
	w = NumericProperty(0)
	def __init__(self, **kwargs):
		super(Speedometr, self).__init__(**kwargs)

	def on_touch_down(self, touch):
		changes = Animation(size=(200, 200), pos=(46, 44),duration=1.0, t='in_out_elastic')
		changes.start(self.ids.speed_img)
		arrow = Animation( size = (513 / 5, 139 / 5), pos = (62, 130), duration=1.0, t='in_out_elastic')
		arrow.start(self.ids.arrow1)

		with self.canvas.before:
			Color(0, 0, 0, 1)
			Ellipse(pos=(41, 38), size=(210, 210))
			Color(0, 0, 0, 1)
			Ellipse(pos=(951, 38), size=(210, 210))
			Color(0, 0, 0, 0.5)
			Rectangle(pos=(130, 39), size=(940, 50), radius = [20,20,20,20] )
		with self.canvas.after:
			Color(0.1, 0.1, 0.1, 1)
			Ellipse(pos=(102, 102), size=(85, 85))


	# self.Arduino_Data = serial.Serial("com7", 9600)
	# self.start()

	#def start(self):
	#	Clock.schedule_interval(self.data, 0.01)

	def data(self, *args):
		self.read_data = self.Arduino_Data.readline()
		self.read_data = self.read_data.decode()
		self.digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
		print(self.digits)
		self.angle = self.digits[0]
		#print(self.w)
		self.w = str(self.angle * 250 / 1023)

class Tachometr(MDFloatLayout):
	w = NumericProperty(0)

	def on_touch_down(self, touch):
		changes1 = Animation(size=(200, 200), pos=(956, 44), duration=1.0, t='in_out_elastic')
		arrow1 = Animation(size = (513 / 5, 139 / 5), pos = (970, 130), duration=1.0, t='in_out_elastic')
		changes1.start(self.ids.tacho_img)
		arrow1.start(self.ids.arrow2)
		#self.ids.arrow2.size = (513 / 5, 139 / 5)
		#self.ids.arrow2.pos = 970, 130
		print(touch.pos)
		with self.canvas.after:
			Color(0.1, 0.1, 0.1, 1)
			Ellipse(pos=(1012, 102), size=(85, 85))

	def __init__(self, **kwargs):
		super(Tachometr, self).__init__(**kwargs)

##self.y = 400
# self.ids.tacho_img.pos = 740, 155
# self.pos_x = 740
# self.pos_y = 155


# self.Arduino_Data = serial.Serial("com7", 9600)
# self.start()

class dash_map(MDApp):

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Red"


dash_map().run()