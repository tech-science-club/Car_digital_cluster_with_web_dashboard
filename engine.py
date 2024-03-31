import io
from datetime import datetime
import time
import requests
import serial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Rectangle, Color, Ellipse, Line
from math import sin, cos, pi
#from gif import GifImage
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage
from kivy.uix.widget import Widget
from kivy_garden.graph import LinePlot, Graph, BarPlot
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
from PIL import Image, GifImagePlugin
from kivy_garden.graph import Graph, MeshLinePlot, LinePlot
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


Window.size = (1200, 700)

class Engine(Screen):
    graph = ObjectProperty()
    get_data = ListProperty()
    get_time = ListProperty()
    theta = NumericProperty()
    dt = NumericProperty()
    time_count = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.on_touch_down(self)
        self.get_data = []
        self.get_time = []
        #self.arduino_Data = serial.Serial("com3", 9600, timeout=1)
        #Clock.schedule_interval(self.read_data, 0.5)
        self.update()

        self.box1 = MDFloatLayout(#pos_hint={"x": 0.03, "y": 0.03},
                                        size_hint = (0.46, 0.5))
        self.box2 = MDFloatLayout(#pos_hint= ({"x": 0.5, "y": 0.03})
                                        size_hint = (0.46, 0.5))
        #self.plotting()
        #self.on_start()
        self.graph1 = Graph(xlabel='t', ylabel='load', x_ticks_minor=1,
                       x_ticks_major=1, y_ticks_major=5,
                       y_grid_label=True, x_grid_label=True, padding=5,
                       x_grid=True, y_grid=True, xmin=-0, xmax=20, ymin=-2, ymax=2,
                       pos_hint={"x": 0.05, "y": 0.03}
                           )
        self.plot = MeshLinePlot(color=[0, 1, 0, 1])
        
        self.plot_x = self.get_time
        self.plot_y = self.get_data
        
        self.graph1.add_plot(self.plot)
        self.box1.add_widget(self.graph1)

        self.add_widget(self.box1)
        self.graph2 = Graph(xlabel='t', ylabel='Air pressure', x_ticks_minor=1,
                       x_ticks_major=1, y_ticks_major=5, y_ticks_minor = 1,
                       y_grid_label=True, x_grid_label=True, padding=5,
                       x_grid=True, y_grid=True, xmin=-0, xmax=5, ymin= -2, ymax=2,
                            pos_hint= {"x": 1.05, "y": 0.03}
                            )
        self.plot2 = LinePlot(color=[1, 0, 0, 1], line_width=2)

        self.plot_x = self.get_time
        self.plot_y = self.get_data

        self.graph2.add_plot(self.plot2)
        self.box2.add_widget(self.graph2)
        self.add_widget(self.box2)

    #def on_touch_down(self, touch):
    #    print(touch)

    def read_data(self, dt=0.1):

        self.time_count += dt
        #self.time_count = round(self.time_count)
        #self.data = self.arduino_Data.readline()
        #self.data = str(self.data, 'utf-8')
        #self.data = self.data.strip('\r\n')
        #self.data = float(self.data)
        #self.fuel_data = self.data *180/1023
        #self.fuel_data = round(self.fuel_data)

        #self.time_count = round(self.time_count)
        #self.get_data.append(self.fuel_data)
        self.get_time.append(self.time_count)
        #print(self.get_data)
        print(self.get_time)

    def update(self):
        Clock.schedule_interval(self.read_data, 0.05)
        Clock.schedule_interval(self.update_points, 0.05)
        Clock.schedule_interval(self.update_xaxis, 0.05)

    def update_xaxis(self,*args):

        self.graph1.xmin = self.get_time[0]
        self.graph1.xmax = self.get_time[-1]
        self.graph2.xmin = self.get_time[0]
        self.graph2.xmax = self.get_time[-1]

    def update_points(self, *args):
        #time.sleep(1)
        #if len(self.get_data) == len(self.get_time):
        self.plot.points = [(x/100, sin(x/10)) for x in range (1, 1000)] #self.get_time]
        self.plot2.points = [(x/100, cos(x/10)) for x in range (1, 1000)]
        if len(self.get_time) > 10:
            self.get_time.pop(0)
            #self.get_data.pop(0)

    #def plotting(self):
    #    self.graph = Graph(xlabel='t', ylabel='load', x_ticks_minor=1,
    #                           x_ticks_major=1, y_ticks_major=5,
    #                           y_grid_label=True, x_grid_label=True, padding=5,
    #                           x_grid=False, y_grid=False, xmin=-0, xmax=5, ymin=-1, ymax=20)
    #    self.plot = LinePlot(color=[1, 0, 0, 1], line_width=2)
    #
    #    self.plot_x = self.get_time
    #    self.plot_y = self.get_data
    #
    #    self.graph.add_plot(self.plot)
    #    self.ids.engine_fuel_cons.add_widget(self.graph)


class engineApp(MDApp):
    def build(self):
       self.theme_cls.theme_style = "Dark"
       self.theme_cls.primary_palette = "Red"
engineApp().run()
