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
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy_garden.mapview import MapView, MapMarkerPopup
# import pyrebase
from kivy.core.text import LabelBase
from matplotlib import pyplot as plt

LabelBase.register("01_DigiGraphics",
                   fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\01-digitgraphics\\01_DigiGraphics.mtt")
LabelBase.register("Hemi-Head",
                   fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\Hemi-Head\\Hemi Head\\hemi head bd it.ttf")
LabelBase.register("lcd14",
                   fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\lcd\\lcd-font\\otf\\LCD14.otf")  # "C:\Users\admin\PycharmProjects\smart home\01-digitgraphics\01_DigiGraphics.mtt"
Window.size = (1200, 700)


class Main(MDFloatLayout):
    pass


class Dash_Board(MDFloatLayout):
    rpm = 0
    speed = 0
    t = 0
    fuel = 0
    widget_name = None


class Classic_style_dash_board(MDScreen):
    latitude = NumericProperty()
    longitude = NumericProperty()
    lat = NumericProperty()
    lon = NumericProperty()
    my_list = ListProperty()

    def __init__(self, **kwargs):
        super(Classic_style_dash_board, self).__init__(**kwargs)
        # self.update_widget()

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

        # self.read_data = self.data.readline()
        # self.read_data = self.read_data.decode()

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

    def __init__(self, **kwargs):
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
        self.w = float(Dash_Board.speed) * 260 / 200  # ----------------> speedometer's arrow


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
            Color(43 / 255, 46 / 255, 47 / 255, 1)
            Ellipse(size=(220, 220), pos=(825, 245))

    def update_value(self, *args):
        self.rpm = float(Dash_Board.rpm) * 243 / 7000


class Speed_rpm_labels(MDFloatLayout):
    kmh = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Speed_rpm_labels, self).__init__(**kwargs)
        self.val_data = Dash_Board()
        # self.kmh = self.val_data.val
        Clock.schedule_interval(self.update_label, 0.01)

    def update_label(self, dt):
        self.ids.speed_lbl.text = str(self.val_data.speed)
        self.ids.rpm_lbl.text = str(round(float(Dash_Board.rpm)))
        # print(self.kmh)


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
        self.x_rpm_scale = float(Dash_Board.rpm) * 246 / 7000
        self.ids.speed.text = str(round(float(Dash_Board.speed)))
        self.ids.rpm.text = str(round(float(Dash_Board.rpm)))

    def on_touch_down(self, touch):
        # print(touch.pos)
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
            return True #  # S


class Gauge_temp(MDFloatLayout):
    x_coolant_temp = NumericProperty()

    def __init__(self, **kwargs):
        super(Gauge_temp, self).__init__(**kwargs)
        Clock.schedule_interval(self.coolant_temp, 0.1)

    def coolant_temp(self, dt):
        n = np.random.randint(0, 100)
        self.x_coolant_temp = int(Dash_Board.t) * 180 / 110
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Temp())
        self.add_widget(Gear_box_oil())
        self.add_widget(Voltmetr())
        self.add_widget(oil_pressure())
        self.add_widget(turbo_pressure())

    def on_touch_move(self, touch):

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



# -----------------> Widgets of 3d Screen are bellow (Coolant temp, gearbox temp, Voltage, Oil pressure, Turbo)
class Temp(MDFloatLayout, TouchBehavior):
    dialog = None
    name = "Temperature"

    def __init__(self, **kwargs):
        super(Temp, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y) == True:
            Dash_Board.widget_name = "Temperature t °C"
            print("temp event")
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(0.6, 0.5),
                # radius=[2, 2, 2, 2],
                md_bg_color=(0, 0, 0, 0),
                # text = "dialog",

                elevation=3,
                shadow_softness=5,

                buttons=[
                    Button(
                        text="Close"
                    )]
            )
            self.dialog.bind(on_dismiss=self.on_dialog_dismiss)
            self.dialog.open()

    def on_dialog_dismiss(self, *args):

        # if self.dialog:
        plot_box = self.dialog.content_cls
        plot_box.stop_process()


class Gear_box_oil(MDFloatLayout, TouchBehavior):
    dialog = None

    def on_touch_down(self, touch):

        if self.collide_point(touch.x, touch.y) == True:
            print("gear box event")
            Dash_Board.widget_name = "Gearbox oil t °C"
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(0.6, 0.5),
                # radius=[2, 2, 2, 2],
                md_bg_color=(0, 0, 0, 0),
                # text = "dialog",

                elevation=3,
                shadow_softness=5,

                buttons=[
                    Button(
                        text="Close"
                    )]
            )
            self.dialog.bind(on_dismiss=self.on_dialog_dismiss)
            self.dialog.open()

    def on_dialog_dismiss(self, *args):

        # if self.dialog:
        plot_box = self.dialog.content_cls
        plot_box.stop_process()


class Voltmetr(MDFloatLayout, TouchBehavior):
    dialog = None

    def on_touch_down(self, touch):

        if self.collide_point(touch.x, touch.y) == True:
            print("gear box event")
            Dash_Board.widget_name = "Alternator output, V"
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(0.6, 0.5),
                # radius=[2, 2, 2, 2],
                md_bg_color=(0, 0, 0, 0),
                # text = "dialog",

                elevation=3,
                shadow_softness=5,

                buttons=[
                    Button(
                        text="Close"
                    )]
            )
            self.dialog.bind(on_dismiss=self.on_dialog_dismiss)
            self.dialog.open()

    def on_dialog_dismiss(self, *args):

        # if self.dialog:
        plot_box = self.dialog.content_cls
        plot_box.stop_process()


class oil_pressure(MDFloatLayout, TouchBehavior):
    dialog = None

    def on_touch_down(self, touch):

        if self.collide_point(touch.x, touch.y) == True:
            print("gear box event")
            Dash_Board.widget_name = "Oil pressure, PSI"
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(0.6, 0.5),
                # radius=[2, 2, 2, 2],
                md_bg_color=(0, 0, 0, 0),
                # text = "dialog",

                elevation=3,
                shadow_softness=5,

                buttons=[
                    Button(
                        text="Close"
                    )]
            )
            self.dialog.bind(on_dismiss=self.on_dialog_dismiss)
            self.dialog.open()

    def on_dialog_dismiss(self, *args):

        # if self.dialog:
        plot_box = self.dialog.content_cls
        plot_box.stop_process()


class turbo_pressure(MDFloatLayout, TouchBehavior):
    dialog = None

    def on_touch_down(self, touch):

        if self.collide_point(touch.x, touch.y) == True:
            print("gear box event")
            Dash_Board.widget_name = "Turbo boost, PSI"
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(0.6, 0.5),
                # radius=[2, 2, 2, 2],
                md_bg_color=(0, 0, 0, 0),
                # text = "dialog",

                elevation=3,
                shadow_softness=5,

                buttons=[
                    Button(
                        text="Close"
                    )]
            )
            self.dialog.bind(on_dismiss=self.on_dialog_dismiss)
            self.dialog.open()

    def on_dialog_dismiss(self, *args):

        # if self.dialog:
        plot_box = self.dialog.content_cls
        plot_box.stop_process()

# -------------------------> plotting of incoming data. Class is evoked from MDDialog as custom class
class Plot_box(MDFloatLayout):
    y = NumericProperty(0)
    x = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Plot_box, self).__init__(**kwargs)
        self.engine_cls = Engine()
        self.pos = 225, 100
        self.size_hint = None, None
        self.size = 750, 500
        self.x = 0
        self.y = 0
        self.x_axes = []
        self.y_axes = []

        self.Clock_id = Clock.schedule_interval(self.get_data, 0.001)
        self.Clock_id()

        self.graf = plt.gcf()
        self.graph = None

    def get_data(self, dt):

        self.x += 1
        if self.x == 180:
            self.x = 180
            self.x -= 1
            if self.x == 0:
                self.x = 0
                self.x += 1

        self.y = round(sin(self.x), 1)

        self.x_axes.append(self.x)
        self.y_axes.append(self.y)

        if len(self.x_axes) > 50:
            self.x_axes.pop(0)
            self.y_axes.pop(0)

        print(self.x_axes)
        print(self.y_axes)

        plt.clf()

        plt.title(Dash_Board.widget_name)
        plt.legend(["ϰ/t"], loc="upper right")
        plt.plot(self.x_axes, self.y_axes,
                 color='red',
                 linestyle='-',
                 linewidth=3,
                 animated=False,
                 markerfacecolor='blue',
                 markersize=12)

        plt.xlabel('t, sec')
        plt.ylabel('ϰ, 1/R')
        plt.grid(False)
        plt.ylim(-1, 1)
        plt.style.context('dark_background')
        self.graf.canvas.draw()
        obj = FigureCanvasKivyAgg(self.graf)
        obj.pos = 225, 100
        self.add_widget(obj)

    def stop_process(self):
        Clock.unschedule(self.Clock_id)

        self.x_axes.clear()
        self.y_axes.clear()
        print("stop, lists are: ")
        print(self.x_axes)
        print(self.y_axes)


class Dashboard_project(MDApp):
    # Dash_Board.val = 0
    cnt = True

    def build(self):
        # obd.logger.setLevel(obd.logging.DEBUG)
        # self.connection = obd.OBD(portstr="COM3", fast=False, timeout=30)
        # self.connection = obd.OBD(portstr="COM9")
        # self.Arduino_Data = serial.Serial("com2", 115200)
        self.connection = obd.OBD(portstr="COM9")
        self.FLOATING_POINT_PATTERN = r"-?\d+\.\d+|-?\d+"
        # self.Arduino_Data = serial.Serial("com2", 115200)
        Clock.schedule_interval(self.data, 0.001)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        sm = ScreenManager()

        sm.add_widget(Classic_style_dash_board(name="dash1"))
        sm.add_widget(Sport_style_dash_board(name="dash2"))
        sm.add_widget(Engine(name="dash3"))

        return sm

    def data(self, dt):
        rpm_raw = self.connection.query(obd.commands.RPM)
        speed_raw = self.connection.query(obd.commands.SPEED)
        coolant_temp_raw = self.connection.query(obd.commands.COOLANT_TEMP)
        rpm_raw = str(rpm_raw)
        speed_raw = str(speed_raw)
        coolant_temp_raw = str(coolant_temp_raw)
        # Extract values using regex
        rpm_values = (re.findall(self.FLOATING_POINT_PATTERN, rpm_raw))
        speed_values = (re.findall(self.FLOATING_POINT_PATTERN, speed_raw))
        coolant_temp_values = (re.findall(self.FLOATING_POINT_PATTERN, coolant_temp_raw))
        #
        ## Join values with units
        try:
            Dash_Board.rpm = int(float(', '.join(rpm_values)))
            Dash_Board.rpm = round(Dash_Board.rpm / 50) * 50
            Dash_Board.speed = int(float(', '.join(speed_values)))
            Dash_Board.t = ', '.join(coolant_temp_values)

            # Print values
            # print(rpm_raw.value)
            # print(speed_raw.value)
            # print(coolant_temp_raw.value)
            print(Dash_Board.rpm)
            print(Dash_Board.speed)
            print(Dash_Board.t)
        except Exception as e:
            print("Error:", e)

    #    if self.cnt:
    #        Dash_Board.val += 1
    #        if Dash_Board.val >= 250:
    #            self.cnt = False
    #    else:
    #        Dash_Board.val = Dash_Board.val - 1
    #        if Dash_Board.val <= 0:
    #            self.cnt =True
    #    print(Dash_Board.val)

    # threading.Thread(target=self._arduino_thread, daemon=True).start()

    # def _arduino_thread(self):

    # self.read_data = self.Arduino_Data.readline()
    # self.read_data = self.read_data.decode("cp1252")
    # self.digits = re.findall(r"-?\d+\.\d+|-?\d+", self.read_data)
    # if self.digits:
    #    Dash_Board.val = self.digits[0]
    #    print(Dash_Board.val)
    # def test_data(self):


if __name__ == '__main__':
    Dashboard_project().run()