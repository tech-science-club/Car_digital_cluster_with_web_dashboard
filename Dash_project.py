import re
import threading
import time
from io import BytesIO
import obd
import numpy as np
import requests
import serial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Canvas, Rectangle, Color, Line, Ellipse
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
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDRectangleFlatIconButton
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
from kivy_garden.mapview import MapView, MapMarkerPopup
#import pyrebase
from kivy.core.text import LabelBase

LabelBase.register("01_DigiGraphics", fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\01-digitgraphics\\01_DigiGraphics.mtt")
LabelBase.register("Hemi-Head", fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\Hemi-Head\\Hemi Head\\hemi head bd it.ttf")
LabelBase.register("lcd14", fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\lcd\\lcd-font\\otf\\LCD14.otf")                                        #"C:\Users\admin\PycharmProjects\smart home\01-digitgraphics\01_DigiGraphics.mtt"
Window.size = (1200,700)

class Main(MDFloatLayout):
    pass
class Dash_Board(MDFloatLayout):
    rpm = 0
    speed = 0
    t = 0
    fuel = 0
class Classic_style_dash_board(MDScreen):
    latitude = NumericProperty()
    longitude = NumericProperty()
    lat = NumericProperty()
    lon = NumericProperty()
    my_list = ListProperty()

    def __init__(self, **kwargs):
        super(Classic_style_dash_board, self).__init__(**kwargs)
        #self.update_widget()

        self.Longt = []
        self.Lat = []
        self.new_longitude = None
        self.new_latitude = None
        self.val_pattern = Dash_Board()
        self.add_widget(LBl())

        self.add_widget(Speedometr())
        self.add_widget(Tachometr())
        self.add_widget(Speed_rpm_labels())
        self.map = Map()
        self.val_pattern = Dash_Board()
        self.speed_lable = Speed_rpm_labels()
        self.stock_box = MDFloatLayout(pos_hint={"center_x": 0.5, "center_y": 0.50},
            size_hint=(0.25, 0.25))
        img = Image(pos_hint={"center_x": 0.5, "center_y": 0.5},
            source='stock.png')
        self.stock_box.add_widget(img)
        self.add_widget(self.stock_box)
        self.scheduled = False
        self.scheduled_2 = False

        Clock.schedule_interval(self.update_widget, 0.01)

    def update_widget(self, dt):
        if float(self.val_pattern.speed) > 10 and not self.scheduled and not self.scheduled_2:
            self.remove_widget(self.stock_box)
            self.add_widget(self.map, 4)
            self.scheduled = True
            self.scheduled_2 = True

        elif float(self.val_pattern.speed) <= 10 and not self.scheduled and self.scheduled_2:
            self.remove_widget(self.map)
            self.add_widget(self.stock_box)

            self.scheduled = True
            self.scheduled_2 = False

        elif float(self.val_pattern.speed) <= 10 and self.scheduled:
            self.scheduled = False

    def start(self, *args):

        #self.read_data = self.data.readline()
        #self.read_data = self.read_data.decode()

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
    # self.update_marker(self.lat, self.lon)
    # self.data.close()
    def update_marker(self, lat, lon):
        # Update the marker position with new GPS data
        self.marker.lat = lat
        self.marker.lon = lon
    # def update_position(self, lat, lon):
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

    def on_touch_down(self, touch):

        self.box1 = MDBoxLayout()

        self.Img1 = Image(source="screen3.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.Img2 = Image(source="screen1.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.Img3 = Image(source="screen2.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},

        )
        self.Img1.bind(on_touch_down=self.shift_to_1screen)
        self.Img2.bind(on_touch_down=self.shift_to_2screen)
        self.Img3.bind(on_touch_down=self.shift_to_3screen)

        self.box1.add_widget(self.Img1)
        self.box1.add_widget(self.Img2)
        self.box1.add_widget(self.Img3)

        self.dialog = MDDialog(


            pos_hint={"center_x": 0.5, "center_y": 0.75},
            size_hint=(0.95, 0.3),
            radius=[20, 20, 20, 20],
            md_bg_color=(0, 0, 0, 0)
        )
        self.dialog.add_widget(self.box1)
        self.dialog.open()

    def shift_to_1screen(self, instance, touch):
        #
        if self.Img1.collide_point(*touch.pos):
            if touch.is_touch:
                self.Img1.size_hint = (0.9, 0.9)
                self.manager.current = "dash1"
                self.manager.transition.direction = "left"
                self.dialog.dismiss()
            return True

    def shift_to_2screen(self, instance, touch):
        # self.dialog.dismiss()
        if self.Img2.collide_point(*touch.pos):
            if touch.is_touch:
                self.Img2.size_hint = (0.9, 0.9)
                self.manager.current = "dash2"
                self.manager.transition.direction = "left"
                self.dialog.dismiss()
            return True

    def shift_to_3screen(self, instance, touch):
        # self.dialog.dismiss()
        if self.Img3.collide_point(*touch.pos):
            if touch.is_touch:
                self.Img3.size_hint = (0.9, 0.9)
                self.manager.current = "dash3"
                self.manager.transition.direction = "left"
                self.dialog.dismiss()
            return True
        # else:

        # return super(Dash_Board, self).on_touch_down(touch)

class Scale(MDFloatLayout):
    pass
class Ruler(MDFloatLayout):
    pass
class Map(MDFloatLayout):
    pass
class LBl(MDFloatLayout):
    def __init__(self, **kwargs):
        super(LBl, self).__init__(**kwargs)

    # self.lbl_speed = MDLabel(text = " --- ", font_size = 46, pos = (500, 40), text_color

    def on_touch_down(self, touch):
        self.canvas.remove(self.canvas.children[10])
        self.canvas.remove(self.canvas.children[12])

    # self.add_widget(self.lbl_speed)
    # shift = Animation( size = (75, 75), pos=(120, 40),duration=1.0, t='in_out_elastic')
    # shift.start(self.ids.lbl1)
    # shift1 = Animation( pos=(46, 44),duration=1.0, t='in_out_elastic')
    # shift1.start(self.ids.lbl2)
    # print(self.canvas.children)
class Digital_box(MDLabel):
    def __init__(self, **kwargs):
        super(Digital_box, self).__init__(**kwargs)
        self.lbl_speed = MDLabel(text="100", pos=(300, 10),
        )
        self.lbl_kmh = MDLabel(text="KM/H", pos=(380, 0),
        )
        self.lbl_tacho = MDLabel(text="2500",  # pos=(600, 10),
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
    w = NumericProperty()
    kmh = "0"
    speed_lbl = StringProperty()

    def __init__(self,  **kwargs):
        super(Speedometr, self).__init__(**kwargs)
        self.val_data = Dash_Board()
        self.speed = Speed_rpm_labels()
        Clock.schedule_interval(self.update_value, 0.01)

    def on_touch_down(self, touch):
        changes = Animation(size=(200, 200), pos=(46, 44), duration=1.0, t='in_out_elastic')
        changes.start(self.ids.speed_img)
        arrow = Animation(size=(513 / 5, 139 / 5), pos=(62, 130), duration=1.0, t='in_out_elastic')
        arrow.start(self.ids.arrow1)
        print(touch.pos)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Ellipse(pos=(41, 38), size=(210, 210))
            Color(0, 0, 0, 1)
            Ellipse(pos=(951, 38), size=(210, 210))
            Color(0, 0, 0, 0.5)
            Rectangle(pos=(130, 39), size=(940, 50), radius=[20, 20, 20, 20])
        with self.canvas.after:
            Color(0.1, 0.1, 0.1, 1)
            Ellipse(pos=(102, 102), size=(85, 85))

    def update_value(self, *args):
        self.w = float(Dash_Board.speed) * 260 / 200    #----------------> speedometer's arrow
class Tachometr(MDFloatLayout):
    rpm = NumericProperty(0)
    rpm_lbl = StringProperty()
    def on_touch_down(self, touch):
        changes1 = Animation(size=(200, 200), pos=(956, 44), duration=1.0, t='in_out_elastic')
        arrow1 = Animation(size=(513 / 5, 139 / 5), pos=(970, 130), duration=1.0, t='in_out_elastic')
        changes1.start(self.ids.tacho_img)
        arrow1.start(self.ids.arrow2)
        # self.ids.arrow2.size = (513 / 5, 139 / 5)
        # self.ids.arrow2.pos = 970, 130
        print(touch.pos)
        with self.canvas.after:
            Color(0.1, 0.1, 0.1, 1)
            Ellipse(pos=(1012, 102), size=(85, 85))

    def __init__(self, **kwargs):
        super(Tachometr, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_value, 0.01)

        with self.canvas:
            Color(43/255, 46/255, 47/255,1)
            Ellipse(size=(220, 220), pos = (825,245))

    def update_value(self, *args):
        self.rpm = float(Dash_Board.rpm) * 243 / 7000
class Speed_rpm_labels(MDFloatLayout):
    kmh = NumericProperty(0)
    def __init__(self,  **kwargs):
        super(Speed_rpm_labels, self).__init__(**kwargs)
        self.val_data = Dash_Board()
        #self.kmh = self.val_data.val
        Clock.schedule_interval(self.update_label, 0.01)
        

    def update_label(self, dt):
        self.ids.speed_lbl.text = str(self.val_data.speed)
        self.ids.rpm_lbl.text = str(round(float(Dash_Board.rpm)))
        #print(self.kmh)
class Sport_style_dash_board(MDScreen):
    x_rpm_scale = NumericProperty()
    rotate = NumericProperty()
    w = NumericProperty()

    def __init__(self, **kwargs):
        super(Sport_style_dash_board, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_data, 0.01)

        self.add_widget(Gauge_temp())
        self.add_widget(Turbo_presure_gauge())
        self.add_widget(Oil_gauge())
        self.add_widget(Gauge_tank())

    def update_data(self, *args):
        self.x_rpm_scale = float(Dash_Board.rpm)*246/7000
        self.ids.speed.text = str(round(float(Dash_Board.speed)))
        self.ids.rpm.text = str(round(float(Dash_Board.rpm)))

    def on_touch_down(self, touch):
        #print(touch.pos)
        self.box1 = MDBoxLayout()

        self.Img1 = Image(source="screen3.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            )

        self.Img2 = Image(source="screen1.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.Img3 = Image(source="screen2.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.Img1.bind(on_touch_down=self.shift_to_1screen)
        self.Img2.bind(on_touch_down=self.shift_to_2screen)
        self.Img3.bind(on_touch_down=self.shift_to_3screen)

        self.box1.add_widget(self.Img1)
        self.box1.add_widget(self.Img2)
        self.box1.add_widget(self.Img3)


        self.dialog = MDDialog(

            pos_hint={"center_x": 0.5, "center_y": 0.75},
            size_hint=(0.95, 0.3),
            radius=[20, 20, 20, 20],
            md_bg_color=(0, 0, 0, 0)
        )
        self.dialog.add_widget(self.box1)
        self.dialog.open()

    def shift_to_1screen(self, instance, touch):
        #
        if self.Img1.collide_point(*touch.pos):

            if touch.is_touch:
                self.Img1.size_hint = (0.9, 0.9)
                self.manager.current = "dash1"
                self.manager.transition.direction = "right"
                self.dialog.dismiss()
            return True

    def shift_to_2screen(self, instance, touch):
        # self.dialog.dismiss()
        if self.Img2.collide_point(*touch.pos):

            if touch.is_touch:
                self.Img2.size_hint = (0.9, 0.9)
                self.manager.current = "dash2"
                self.manager.transition.direction = "left"
                self.dialog.dismiss()
            return True

    def shift_to_3screen(self, instance, touch):

        if self.Img3.collide_point(*touch.pos):
            if touch.is_touch:
                self.Img3.size_hint = (0.9, 0.9)
                self.manager.current = "dash3"
                self.manager.transition.direction = "left"
                self.dialog.dismiss()
            return True
class Gauge_temp(MDFloatLayout):
    x_coolant_temp = NumericProperty()

    def __init__(self, **kwargs):
        super(Gauge_temp, self).__init__(**kwargs)
        Clock.schedule_interval(self.coolant_temp, 0.1)

    def coolant_temp(self, dt):
        n = np.random.randint(0, 100)
        self.x_coolant_temp = int(Dash_Board.t)*180/110
        self.ids.temp_label.text = str(Dash_Board.t)
class Gauge_tank(MDFloatLayout):
    x_tank = NumericProperty()

    def __init__(self, **kwargs):
        super(Gauge_tank, self).__init__(**kwargs)
        Clock.schedule_interval(self.tank, 0.1)

    def tank(self, dt):
        n = np.random.randint(0, 100)
        self.x_tank = n

class Oil_gauge(MDFloatLayout):
    angle_oil_pressure = NumericProperty()

    def __init__(self, **kwargs):
        super(Oil_gauge, self).__init__(**kwargs)
        Clock.schedule_interval(self.arrow, 0.1)
    # def on_touch_down(self, touch):
    #    print(touch.pos)
    def arrow(self, dt):
    #    data =
        n = np.random.randint(0, 180)
        self.angle_oil_pressure = n

class Turbo_presure_gauge(MDFloatLayout):

    angle_turbo_pressure = NumericProperty()

    def __init__(self, **kwargs):
        super(Turbo_presure_gauge, self).__init__(**kwargs)
        Clock.schedule_interval(self.arrow, 0.1)

    # def on_touch_down(self, touch):
    #    print(touch.pos)
    def arrow(self, dt):
        n = np.random.randint(0, 270)
        self.angle_turbo_pressure = n

class Engine(MDScreen):
    graph = ObjectProperty()
    get_data = ListProperty()
    get_time = ListProperty()
    theta = NumericProperty()
    dt = NumericProperty()
    time_count = NumericProperty(0)

    def on_touch_down(self, touch):

        self.box1 = MDBoxLayout()

        self.Img1 = Image(source="screen3.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            )

        self.Img2 = Image(source="screen1.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.Img3 = Image(source="screen2.png",
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.Img1.bind(on_touch_down=self.shift_to_1screen)
        self.Img2.bind(on_touch_down=self.shift_to_2screen)
        self.Img3.bind(on_touch_down=self.shift_to_3screen)

        self.box1.add_widget(self.Img1)
        self.box1.add_widget(self.Img2)
        self.box1.add_widget(self.Img3)


        self.dialog = MDDialog(

            pos_hint={"center_x": 0.5, "center_y": 0.75},
            size_hint=(0.95, 0.3),
            radius=[20, 20, 20, 20],
            md_bg_color=(0, 0, 0, 0)
        )
        self.dialog.add_widget(self.box1)
        self.dialog.open()

    def shift_to_1screen(self, instance, touch):
        #
        if self.Img1.collide_point(*touch.pos):

            if touch.is_touch:
                self.Img1.size_hint = (0.9, 0.9)
                self.manager.current = "dash1"
                self.manager.transition.direction = "left"
                self.dialog.dismiss()
            return True


    def shift_to_2screen(self, instance, touch):
        # self.dialog.dismiss()
        if self.Img2.collide_point(*touch.pos):

            if touch.is_touch:
                self.Img2.size_hint = (0.9, 0.9)
                self.manager.current = "dash2"
                self.manager.transition.direction = "right"
                self.dialog.dismiss()
            return True


    def shift_to_3screen(self, instance, touch):

        if self.Img3.collide_point(*touch.pos):
            if touch.is_touch:
                self.Img3.size_hint = (0.9, 0.9)
                self.manager.current = "dash3"
                self.manager.transition.direction = "left"
                self.dialog.dismiss()
            return True


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.on_touch_down(self)
        self.get_data = []
        self.get_time = []
        # self.arduino_Data = serial.Serial("com3", 9600, timeout=1)
        # Clock.schedule_interval(self.read_data, 0.5)
        #self.update()

    #    self.box1 = MDFloatLayout(  # pos_hint={"x": 0.03, "y": 0.03},
    #        size_hint=(0.46, 0.5))
    #    self.box2 = MDFloatLayout(  # pos_hint= ({"x": 0.5, "y": 0.03})
    #        size_hint=(0.46, 0.5))
    #    # self.plotting()
    #    # self.on_start()
    #    self.graph1 = Graph(xlabel='t', ylabel='load', x_ticks_minor=1,
    #        x_ticks_major=1, y_ticks_major=5,
    #        y_grid_label=True, x_grid_label=True, padding=5,
    #        x_grid=True, y_grid=True, xmin=-0, xmax=20, ymin=-2, ymax=2,
    #        pos_hint={"x": 0.05, "y": 0.03}
    #    )
    #    self.plot = MeshLinePlot(color=[0, 1, 0, 1])
    #
    #    self.plot_x = self.get_time
    #    self.plot_y = self.get_data
    #
    #    self.graph1.add_plot(self.plot)
    #    self.box1.add_widget(self.graph1)
    #
    #    self.add_widget(self.box1)
    #    self.graph2 = Graph(xlabel='t', ylabel='Air pressure', x_ticks_minor=1,
    #        x_ticks_major=1, y_ticks_major=5, y_ticks_minor=1,
    #        y_grid_label=True, x_grid_label=True, padding=5,
    #        x_grid=True, y_grid=True, xmin=-0, xmax=5, ymin=-2, ymax=2,
    #        pos_hint={"x": 1.05, "y": 0.03}
    #    )
    #    self.plot2 = LinePlot(color=[1, 0, 0, 1], line_width=2)
    #
    #    self.plot_x = self.get_time
    #    self.plot_y = self.get_data
    #
    #    self.graph2.add_plot(self.plot2)
    #    self.box2.add_widget(self.graph2)
    #    self.add_widget(self.box2)

    def read_data(self, dt=0.1):
        self.time_count += dt
        # self.time_count = round(self.time_count)
        # self.data = self.arduino_Data.readline()
        # self.data = str(self.data, 'utf-8')
        # self.data = self.data.strip('\r\n')
        # self.data = float(self.data)
        # self.fuel_data = self.data *180/1023
        # self.fuel_data = round(self.fuel_data)

        # self.time_count = round(self.time_count)
        # self.get_data.append(self.fuel_data)
        self.get_time.append(self.time_count)
        # print(self.get_data)
        #print(self.get_time)

    #def update(self):
    #    Clock.schedule_interval(self.read_data, 0.05)
    #    Clock.schedule_interval(self.update_points, 0.05)
    #    Clock.schedule_interval(self.update_xaxis, 0.05)
    #
    #def update_xaxis(self, *args):
    #    self.graph1.xmin = self.get_time[0]
    #    self.graph1.xmax = self.get_time[-1]
    #    self.graph2.xmin = self.get_time[0]
    #    self.graph2.xmax = self.get_time[-1]
    #
    #def update_points(self, *args):
    #    # time.sleep(1)
    #    # if len(self.get_data) == len(self.get_time):
    #    self.plot.points = [(x / 100, sin(x / 10)) for x in range(1, 1000)]  # self.get_time]
    #    self.plot2.points = [(x / 100, cos(x / 10)) for x in range(1, 1000)]
    #    if len(self.get_time) > 10:
    #        self.get_time.pop(0)
            # self.get_data.pop(0)

    # def plotting(self):
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
class Dashboard_project(MDApp):
    #Dash_Board.val = 0
    cnt = True
    def build(self):
        #obd.logger.setLevel(obd.logging.DEBUG)
        #self.connection = obd.OBD(portstr="COM3", fast=False, timeout=30)
        self.connection = obd.OBD(portstr="COM9")
        #self.Arduino_Data = serial.Serial("com2", 115200)
        Clock.schedule_interval(self.data, 0.01)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        sm = ScreenManager()

        sm.add_widget(Classic_style_dash_board(name = "dash1"))
        sm.add_widget(Sport_style_dash_board(name = "dash2"))
        sm.add_widget(Engine(name = "dash3"))

        return sm

    def data(self, dt):
        rpm = str(self.connection.query(obd.commands.RPM))
        Dash_Board.rpm = re.findall(r"-?\d+\.\d+|-?\d+", rpm)
        Dash_Board.rpm = 4000 #Dash_Board.rpm[0]
        print(Dash_Board.rpm)
        speed = str(self.connection.query(obd.commands.SPEED))
        Dash_Board.speed = re.findall(r"-?\d+\.\d+|-?\d+", speed)
        Dash_Board.speed = 5#Dash_Board.speed[0]
        print(Dash_Board.speed)
        t = str(self.connection.query(obd.commands.COOLANT_TEMP))
        Dash_Board.t = re.findall(r"-?\d+\.\d+|-?\d+", t)
        Dash_Board.t = 90 #Dash_Board.t[0]
        print(Dash_Board.t)

    #    if self.cnt:
    #        Dash_Board.val += 1
    #        if Dash_Board.val >= 250:
    #            self.cnt = False
    #    else:
    #        Dash_Board.val = Dash_Board.val - 1
    #        if Dash_Board.val <= 0:
    #            self.cnt =True
    #    print(Dash_Board.val)

        #threading.Thread(target=self._arduino_thread, daemon=True).start()

    #def _arduino_thread(self):



        #self.read_data = self.Arduino_Data.readline()
        #self.read_data = self.read_data.decode("cp1252")
        #self.digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
        #if self.digits:
        #    Dash_Board.val = self.digits[0]
        #    print(Dash_Board.val)
    #def test_data(self):



if __name__ == '__main__':


    Dashboard_project().run()