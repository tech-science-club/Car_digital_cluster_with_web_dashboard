from datetime import datetime
import time
import requests
import serial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Rectangle, Color, Ellipse, Line
from math import sin, cos, pi

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

Window.size = (1200,700)

class Suspension(Screen):
    data = NumericProperty()
    x = NumericProperty()
    y = NumericProperty()

    def __init__(self, **kwargs):
        super(Suspension, self).__init__(**kwargs)
        #self.data = 0

    def common_clearance(self, *args):
        self.ids.frame.pos_hint = {"center_x": 0.5, "center_y": 0.5 + float(self.ids.common_clearance.value)/10000}

    def val(self, *args):
        self.data = (float((-1)*self.ids.front_clearance.value)/100)

    def back_axes_val(self, *args):
        self.prop = self.ids.body_frame.canvas.before.get_group('rotate')[1]
        self.prop = 300, 300 #self.ids.body_frame.pos
        
        self.data = (float((-1)*self.ids.back_axes.value)/100)

class db_2nd_wndApp(MDApp):
    def build(self):
       self.theme_cls.theme_style = "Dark"
       self.theme_cls.primary_palette = "Red"



db_2nd_wndApp().run()
