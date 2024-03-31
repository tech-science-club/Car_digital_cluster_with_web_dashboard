import re
from datetime import datetime
import time
import requests
import serial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Rectangle, Color, Ellipse, Line
from math import sin, cos, pi

from kivy_garden.mapview import MapView
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
from kivy.animation import Animation
import math

Window.size = (1200, 700)


class Dash_Board(MDFloatLayout):
#w = NumericProperty(0)
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		#self.Arduino_Data = serial.Serial("com9", 9600)
		#self.speed = Speedometr()
		#self.tacho = Tachometr()
		#self.start()

		self.box = MDFloatLayout(
			pos_hint = {"center_x": 0.5, "center_y": 0.50},
			size_hint = (0.25, 0.25))
		self.car_img = Image(
			pos_hint = {"center_x": 0.5, "center_y": 0.5},
			source = 'stock.png')
		self.box.add_widget(self.car_img)
		self.add_widget(self.box)
		self.map_box = MDAnchorLayout(
			size_hint = (1, 1),
			pos_hint = {"center_x": 0.5, "center_y": 0.5})
		self.map = MapView(
			pos_hint = {"center_x": 0.5, "center_y": 0.5},
			size_hint = (0.7, 0.7),
			#size = self.parent.size,
			zoom = 15,
			lat= '55.736061',
			lon= '11.509603',
			#MapMarkerPopup = ('55.736061', '11.509603')
		)
		self.map_box.add_widget(self.map)
		self.scheduled = False
		self.scheduled_2 = False

	def start(self):
		Clock.schedule_interval(self.data, 0.01)

	def data(self, dt):
		self.read_data = self.Arduino_Data.readline()
		self.read_data = self.read_data.decode()
		self.digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
		#print(self.digits)
		self.angle = self.digits[0]

		self.w = str(self.angle*250/1023)
		print(self.angle)

		if int(self.angle) > 50 and not self.scheduled and not self.scheduled_2:
			self.remove_widget(self.box)
			self.add_widget(self.map_box)
			self.scheduled = True
			self.scheduled_2 = True
			Speedometr().move_speedometr()
			Tachometr().move_tachometr()
			
		elif int(self.angle) <= 50 and not self.scheduled and self.scheduled_2:
			self.remove_widget(self.map_box)
			self.add_widget(self.box)
			
			self.scheduled = True
			self.scheduled_2 = False
		elif int(self.angle) <= 50 and self.scheduled:
			self.scheduled = False
		
class Speedometr(MDFloatLayout):
	w = NumericProperty(0)

	def __init__(self, **kwargs):
		super(Speedometr, self).__init__(**kwargs)
		print(self.ids)

		self.speed_scale = Image(

		source = "speedometr.png",
		size_hint = (None, None),
		size = (400, 400),
		# pos_hint: None, None
		pos = (55, 157)
		)
		self.speed_scale.id = "speed_img"
		self.arrow = Image(

			#,
			source = "arrow3.png",
			size_hint = (None, None),
			size = (513 / 2.5, 139 / 2.5),
			pos = (87, 328))
		self.arrow.id =  "arrow1"
		self.add_widget(self.speed_scale)

	def move_speedometr(self):
		print("Move Speedometr method called!")
		changes = Animation(size=(200, 200), duration=1.0, t='in_out_elastic')
		changes.start(self.speed_scale)
		#print("object here" + str(type(self.ids.speed_img)))
		arrow = Animation(size=(513/5, 139/5), duration=1.0, t='in_out_elastic')
		arrow.start(self.arrow)
		self.arrow.size = 513/5, 139/5
		self.arrow.pos = 70, 245
	# self.start()
	#def start(self):
	#	Clock.schedule_interval(self.data, 0.01)

	def data(self, *args):
		self.read_data = self.Arduino_Data.readline()
		self.read_data = self.read_data.decode()
		self.digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
		print(self.digits)
		self.angle = self.digits[0]
		print(self.w)
		self.w = str(self.angle * 250 / 1023)

class Tachometr(MDFloatLayout):
	w = NumericProperty(0)
	def __init__(self, **kwargs):
		super(Tachometr, self).__init__(**kwargs)
		self.pos_hint = {"x": 0.65, "y": 0.2}


	def move_tachometr(self):
		print("Move Tachometr method called!")
		changes1 = Animation(size=(200, 200), pos=(950, 158), duration=1.0, t='in_out_elastic')
		arrow1 = Animation(size=(513 / 5, 139 / 5), duration=1.0, t='in_out_elastic')
		changes1.start(self.ids.tacho_img)
		arrow1.start(self.ids.arrow2)
		self.ids.arrow2.pos = 962, 245

	#def start(self):
	#	Clock.schedule_interval(self.data, 0.01)

	def data(self, *args):
		self.read_data = self.Arduino_Data.readline()
		self.read_data = self.read_data.decode()
		self.digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
		print(self.digits)
		self.angle = self.digits[0]
		print(self.w)
		self.w = str(self.angle * 250 / 1023)

class Car_pattern(MDFloatLayout):
	pass

class dash_brd_modern(MDApp):

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Red"


dash_brd_modern().run()