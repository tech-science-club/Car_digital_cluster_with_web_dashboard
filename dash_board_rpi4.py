import re
from threading import Thread
import queue
import can
from can import Message
import time
from io import BytesIO
import obd
import numpy as np
import requests
import serial
import pynmea2
import serial
import time
import multiprocessing
#from PCANBasic import *
import sys
import threading
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
from kivymd.uix.screenmanager import MDScreenManager
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
from kivymd.font_definitions import theme_font_styles
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import Image
from datetime import datetime
from kivy_garden.graph import Graph, MeshLinePlot, LinePlot
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.config import Config
from kivy.core.text import LabelBase
from matplotlib import pyplot as plt

LabelBase.register("01_DigiGraphics",
                   fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\01-digitgraphics\\01_DigiGraphics.mtt")
LabelBase.register("Hemi-Head",
                   fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\Hemi-Head\\Hemi Head\\hemi head bd it.ttf")
LabelBase.register("lcd14",
                   fn_regular="C:\\Users\\admin\\PycharmProjects\\dashpanel\\lcd\\lcd-font\\otf\\LCD14.otf")
# for Windows path--------------
#abelBase.register("01_DigiGraphics",
#                  fn_regular="/home/admin/Downloads/Car_Dashboard_with_web_access/01-digitgraphics/01 DigiGraphics.ttf")
#abelBase.register("Hemi-Head",
#                  fn_regular="/home/admin/Downloads/Car_Dashboard_with_web_access/Hemi-Head/Hemi Head/hemi head bd it.ttf")
#abelBase.register("lcd14",
#                  fn_regular="/home/admin/Downloads/Car_Dashboard_with_web_access/lcd/LCD14.otf")  # "C:\Users\admin\PycharmProjects\smart home\01-digitgraphics\01_DigiGraphics.mtt"
Window.size = (1050, 700)

Builder.load_string('''

#---------------------------first screen-----------------------------------------------

<Classic_style_dash_board>:
    name: "dash1"
    canvas:
        Color:
            rgba: 0, 0, 0, 1  # red
        Rectangle:
            pos: self.pos
            size: self.size


#----------------------------second screen--------------------------------------------            

<Sport_style_dash_board>:

    name: "dash2"

    canvas.before:
        Color:
            rgba: 0, 0, 0, 1  
        Ellipse:
            pos: self.x+220, self.y+50
            size: 600, 600
        Color:
            rgba: 0+root.x_rpm_scale/240, 1-root.x_rpm_scale/240, 0, 1  # red
        Ellipse:
            pos: self.x+220, self.y+50
            size: 600, 600
            angle_start: 237
            angle_end: 237+root.x_rpm_scale

        Color:
            rgba: 0, 0, 0, 1
        Ellipse:
            pos: self.x+270, self.y+100
            size: 500, 500

        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.x+300, self.y+125
            size: 450, 450
            source: "central_ring2.png"
        Color:
            rgba: 0,0,1,1
        Rectangle:
            pos: 445, 440
            size: 155, 67
            source: "rpm_label.png"
    canvas:
        Color:
            rgba: 1, 1, 1, 1  # red
        Rectangle:
            pos: self.x+220, self.y+50
            size: 600, 600
            source: "rpm.png" 

    MDLabel:
        id: speed
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        #pos: 500, 250
        halign:'center'
        text: "000"
        font_name: "Hemi-Head"
        font_size: 160
        markup: True

    MDLabel:

        text: "km/h"

        font_size: 40
        pos_hint: {"center_x": 0.5, "center_y": 0.35}
        #pos: 600, 220
        font_name: "Hemi-Head"
        halign:'center'

    MDLabel:
        id: rpm
        pos_hint: {"center_x": 0.5, "center_y": 0.692}
        halign:'center'
        text: "0000"
        font_name: "Hemi-Head"
        font_size: 50
        markup: True

    MDLabel:
        pos_hint: {"center_x": 0.54, "center_y": 0.645}
        halign:'center'
        text: "RPM"
        font_name: "Hemi-Head"
        font_size: 24
        markup: True
    FitImage:
        pos: 0, 0
        size_hint_y: 0.20
        source: "road_to_horizont.png"
<LBl>:
    id: lbl
    canvas.before:
        InstructionGroup:
            id: circles
        Color:
            rgba: 0.1,0.1,0.1,1
        Ellipse:
            size: 380,380
            pos: 45, 163
            #group: "circle"
        Color:
            rgba: 0.1,0.1,0.1,1
        Ellipse:
            size:  380,380
            pos: 630, 162

<Center_rings>:
    canvas:
        Color:
            rgba: (43 / 255, 46 / 255, 47 / 255, 1)
        Ellipse:
            size: 220,220
            pos: 120, 245

        Color:
            rgba: (43 / 255, 46 / 255, 47 / 255, 1)
        Ellipse:
            size: 220,220
            pos: 710, 245

<Speedometr>:

    Image:
        id: speed_img
        source: "speedometr.png"
        size_hint: None, None
        size: 400, 400
        pos: 30, 157

    Image:
        id: arrow1
        source: "arrow3.png"
        size_hint: None, None
        size: 513/2.5, 139/2.5

        pos: 60, 330
        canvas.before:
        #    #InstructionGroup:
            PushMatrix:

            Rotate:
               #group: 'rotate'

                angle: 31 - root.w
                origin: 231, 355
                axis: 0,0,1
        canvas.after:
            PopMatrix:

<Tachometr>:
    Image:
        id: tacho_img
        source: 'tacho3.png' #"tachometr.png"
        size_hint: None, None
        size: 400, 400
        #pos_hint: None, None
        pos: 625, 155

    Image:
        id: arrow2
        source: "arrow3.png"
        size_hint: None, None
        size: 513/2.5, 139/2.5
        #pos_hint: None, None
        pos: 655, 330
        canvas.before:
            #InstructionGroup:
            PushMatrix:

            Rotate:
                #group: 'rotate'

                angle: 28 - root.rpm
                origin: 825, 356
                axis: 0,0,1
        canvas.after:
            PopMatrix:

<Speed_rpm_labels>:

    MDLabel:
        id: speed_lbl
        pos_hint: {"center_x": 0.215, "center_y": 0.52}
        halign:'center'
        text: str(root.kmh) #"75"
        font_name: '01_DigiGraphics'
        font_size: 75
        markup: True

    MDLabel:
        id: km_h
        pos_hint: {"center_x": 0.21, "center_y": 0.42}
        halign:'center'
        text: "KM/H"
        font_name: '01_DigiGraphics'
        font_size: 28
        markup: True

    MDLabel:
        id: rpm_lbl
        pos_hint: {"center_x": 0.78, "center_y": 0.53}
        halign:'center'
        text: "0"
        font_name: '01_DigiGraphics'
        font_size: 60
        markup: True

    MDLabel:
        id: rpm
        pos_hint: {"center_x": 0.78, "center_y": 0.42}
        halign:'center'
        text: "RPM"
        font_name: '01_DigiGraphics'
        font_size: 24
        markup: True

#.................................... widget of 2nd screen................................
<Gauge_temp>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # red
        Rectangle:
            pos: 10, 280
            size: 190, 190
            source: "temp_gauge2.png"
    Image:
        size_hint: None, None
        pos: 35, 340
        #size: 5, 30
        size: 80, 75
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:

            Rotate:
                group: 'rotate'

                angle: 0 - root.x_coolant_temp
                origin: 101, 378
                axis: 0,0,1
        canvas.after:
            PopMatrix:
    Image: 
        size_hint: 0.05, 0.05
        source: "temp.png"
        pos: 72, 300

    MDLabel:
        pos_hint: {"center_x": 0.12, "center_y": 0.5}
        halign:'center'
        text: "°C"
        font_name: 'lcd14'
        font_size: 20
        markup: True
    MDLabel:
        id: temp_label
        pos_hint: {"center_x": 0.07, "center_y": 0.50}
        halign:'center'
        text: "0"
        font_name: 'lcd14'
        font_size: 20
        markup: True


<Gauge_tank>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # red
        Rectangle:
            pos: 10, 80
            size: 190, 190
            source: "fuel_gauge2.png"
    Image:
        size_hint: None, None
        pos: 35, 140
        #size: 5, 30
        size: 80, 75
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:

            Rotate:
                group: 'rotate'

                angle: 0 - root.x_tank
                origin: 101, 177
                axis: 0,0,1
        canvas.after:
            PopMatrix:
    Image:
        size_hint: 0.03, 0.03
        source: "petrol.png"
        pos: 85, 98
<Oil_gauge>:
    canvas.before:

        Color:
            rgba: 1, 1, 1, 1  # red
        Rectangle:
            pos: 840, 65
            size: 210, 210
            source: "oil_pressure.png"


    Image:
        size_hint: None, None
        pos: 880, 138
        #size: 5, 30
        size: 80, 75
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:

            Rotate:
                group: 'rotate'

                angle: 45 - root.angle_oil_pressure
                origin: 943, 176
                axis: 0,0,1
        canvas.after:
            PopMatrix:
    MDLabel:

        pos_hint: {"center_x": 0.9, "center_y": 0.16}
        halign:'center'
        text: "L/100 km"
        font_name: 'lcd14'
        font_size: 14
        markup: True

    MDLabel:
        id: consm_label
        text: "0" 
        pos_hint: {"center_x": 0.9, "center_y": 0.20}
        halign:'center'
        font_name: 'lcd14'
        font_size: 24
        markup: True


<Turbo_presure_gauge>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # red
        Rectangle:
            pos: 840, 270
            size: 210, 210
            source: "turbo_pressure.png"     #  ----------------------> turbo gauge

    Image:
        size_hint: None, None
        pos: 880, 340
        #size: 5, 30
        size: 80, 75
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:

            Rotate:
                group: 'rotate'

                angle: 0 - root.angle_turbo_pressure
                origin: 946, 378
                axis: 0,0,1
        canvas.after:
            PopMatrix:
    Image:
        size_hint: 0.05, 0.05
        source: "turbo2.png"
        pos: 915, 300

<Dash_Board>:

#--------------------------------------------3d screen----------------------------------------------------------------
<Engine>:

    name: "dash3"

    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.width-30, self.height-100
            pos: 20, 70
            source: "frame_engine_control.png"


    MDLabel:
        pos_hint: {"center_x": 0.5, "center_y": 0.9}
        text: " Engine control "
        halign: "center"
        font_name: 'TickingTimebombBB'
        theme_text_color: "Custom"
        text_color: "white"
        font_size: 32

    MDFloatLayout:
        # canvas.before:
            # Color:
                # rgba: 1, 1, 1, 1
            # Rectangle:
                # size: self.width-30, self.height-100
                # pos: 20, 70
                # source: "frame_engine_control.png"

        id: graph_box
        pos_hint: {"x": 0.25, "y": 0}
        size_hint: 0.5, 0.50
        MDRectangleFlatButton:
            text: "Test GSM module"
            theme_text_color: "Custom"
            text_color: "white"
            line_color: "red"
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
            on_press: root.test_gsm()
        MDRectangleFlatButton:
            text: "Test GPS module"
            theme_text_color: "Custom"
            text_color: "white"
            line_color: "red"
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
            on_press: root.test_gps()
        MDRectangleFlatButton:
            text: "Test CAN bus"
            theme_text_color: "Custom"
            text_color: "white"
            line_color: "red"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            on_press: root.test_can_bus()

#...............................3d screen's widgets...................................................
<Temp>:

    pos_hint: {"center_x": 0.15, "center_y": 0.3}
    size_hint: None, None
    size: 200, 200

    Image:
        id: gif_img
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        #size_hint: 0.3, 0.3

        #size: 200, 200
        source: "temp_gauge2.png"
    MDLabel:
        id: temp_label
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
        text: " coolant temp "
        halign: "center"
        font_name: 'TickingTimebombBB'
        theme_text_color: "Custom"
        text_color: "white"
        font_size: 18
    Image:
        pos_hint: {"center_x": 0.35, "center_y": 0.52}
        size_hint: None, None
        size: 90, 30
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:
            Rotate:
                #group: 'rotate'

                angle: 0 - root.x_coolant_temp
                origin: 156, 212
                axis: 0,0,1
        canvas.after:
            PopMatrix:
#---------------------------------------------------------------------------------------------------------
<Gear_box_oil>:
    # canvas.before:
        # Color:
            # rgba: 0, 1, 0, 0.5
        # Rectangle:
            # size: self.size
            # pos: self.pos
    pos_hint: {"center_x": 0.15, "center_y": 0.7}
    size_hint: None, None
    size: 200, 200

    Image:
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        #size_hint: 0.3, 0.3
        source: "gear_box_oil_temp_gauge2.png"
    MDLabel:
        id: gearbox_oil_label
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
        text: " gearbox oil temp "
        halign: "center"
        font_name: 'TickingTimebombBB'
        theme_text_color: "Custom"
        text_color: "white"
        font_size: 18

    Image:
        pos_hint: {"center_x": 0.35, "center_y": 0.52}
        size_hint: None, None
        size: 90, 30
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:
            Rotate:
                #group: 'rotate'

                angle: 0 - root.x_gear_temp
                origin: 157, 493
                axis: 0,0,1
        canvas.after:
            PopMatrix:
#---------------------------------------------------------------------------------------

<Voltmetr>:
    # canvas.before:
        # Color:
            # rgba: 0, 0, 1, 0.5
        # Rectangle:
            # size: self.size
            # pos: self.pos
    pos_hint: {"center_x": 0.5, "center_y": 0.7}
    size_hint: None, None
    size: 200, 200

    Image:
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 1.1, 1.1
        source: "voltmetr.png"
    MDLabel:
        id: volt_label
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
        text: " Volt "
        halign: "center"
        font_name: 'TickingTimebombBB'
        theme_text_color: "Custom"
        text_color: "white"
        font_size: 18
    Image:
        pos_hint: {"center_x": 0.35, "center_y": 0.52}
        size_hint: None, None
        size: 90, 30
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:

            Rotate:
                #group: 'rotate'

                angle: 0
                origin: 118, 527
                axis: 0,0,1
        canvas.after:
            PopMatrix:
#-----------------------------------------------------------------------------------------------
<oil_pressure>:
    # canvas.before:
        # Color:
            # rgba: 0.5, 0.5, 0.5, 0.5
        # Rectangle:
            # size: self.size
            # pos: self.pos
    pos_hint: {"center_x": 0.85, "center_y": 0.7}
    size_hint: None, None
    size: 200, 200

    Image:
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 1.1, 1.1
        source: "oil_pressure.png"
    MDLabel:
        id: oil_label
        pos_hint: {"center_x": 0.5, "center_y": 0.20}
        text: " oil pressure "
        halign: "center"
        font_name: 'TickingTimebombBB'
        theme_text_color: "Custom"
        text_color: "white"
        font_size: 18
    Image:
        pos_hint: {"center_x": 0.35, "center_y": 0.53}
        size_hint: None, None
        size: 90, 30
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:

            Rotate:
                #group: 'rotate'

                angle: 0 - root.angle_oil_pressure
                origin: 892, 494
                axis: 0,0,1
        canvas.after:
            PopMatrix:
#--------------------------------------------------------------------------------------------------
<turbo_pressure>:
    # canvas.before:
        # Color:
            # rgba: 0.25, 0.25, 0, 0.5
        # Rectangle:
            # size: self.size
            # pos: self.pos
    pos_hint: {"center_x": 0.85, "center_y": 0.3}
    size_hint: None, None
    size: 200, 200

    Image:
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 1.1, 1.1
        source: "turbo_pressure.png"
    MDLabel:
        id: turbo_label
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
        text: " turbo pressure "
        halign: "center"
        font_name: 'TickingTimebombBB'
        theme_text_color: "Custom"
        text_color: "white"
        font_size: 18
    Image:
        pos_hint: {"center_x": 0.35, "center_y": 0.51}
        size_hint: None, None
        size: 90, 30
        source: "arrow2.png"
        canvas.before:
            #InstructionGroup:
            PushMatrix:

            Rotate:
                #group: 'rotate'

                angle: 0 - root.angle_turbo_pressure
                origin: 893, 210
                axis: 0,0,1
        canvas.after:
            PopMatrix:
#---------------------------------------------------------------------------------

<Plot_box>:

<Slides>:
    #name: "slide"
    #Carousel:
    #	scroll_distance: 50
    MDBoxLayout:
        orientation: "horizontal"
        MDFloatLayout:

            Image:
                id: img1
                #size_hint: 0.6, 0.6
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                source: "screen1.png"
                on_touch_down: root.ids.img1.size_hint = 0.75, 0.75
                #on_touch_up: #root.slider_bar() #root.ids.img1.size_hint = 0.6, 0.6
        MDBoxLayout:

            Image:
                id: img2
                size_hint: 0.6, 0.6
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                source: "screen2.png"
                on_touch_down: root.ids.img2.size_hint = 0.75, 0.75
                #on_touch_up: root.enginescreen()#root.ids.img2.size_hint = 0.6, 0.6

        MDBoxLayout:

            Image:
                id: img3
                size_hint: 0.6, 0.6
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                source: "screen3.png"
                #on_touch_down: root.ids.img3.size_hint = 0.75, 0.75
                #on_touch_up: root.modernscreen()#root.ids.img3.size_hint = 0.6, 0.6

<test_gps_module>: 

    size_hint: None, None                               
    size: 800, 500                                      
    pos_hint: {"center_x": 0.5, "center_y": 0.5}        

    MDLabel:                                            
        text: "GPS TX pynmea2 messages"                 
        #halign: "center"
        valign: "top"                                
        size_hint: (1, None)                            
        pos_hint: {"center_x": 0.6, "center_y": 0.85}   
        font_size: "24"                                 
        height: 50                                      


    MDLabel:                                            
        id: lbl                                         
        pos_hint: {"center_x": 0.5, "center_y": 0.25}   
        valign: 'top'                                   
        size: self.texture_size                         
        text_size: self.size

<test_gsm_module>: 

    size_hint: None, None                               
    size: 800, 500                                      
    pos_hint: {"center_x": 0.5, "center_y": 0.5}        

    MDLabel:                                            
        text: "GSM module AT request-response"                 
        valign: "top"                                
        size_hint: (1, None)                            
        pos_hint: {"center_x": 0.6, "center_y": 0.85}   
        font_size: "24"                                 
        height: 50                                      


    MDLabel:                                            
        id: lbl                                         
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
        #size: self.texture_size   
        valign: 'top'                                   
        size: self.texture_size                         
        text_size: self.size

<test_can_bus>: 

    size_hint: None, None                               
    size: 800, 500                                      
    pos_hint: {"center_x": 0.5, "center_y": 0.5}        

    MDLabel:                                            
        text: "CAN bus TX messages"                 
        valign: "top"                                 
        size_hint: (1, None)                            
        pos_hint: {"center_x": 0.65, "center_y": 0.85}   
        font_size: "24"                                 
        height: 50                                      


    MDLabel:                                            
        id: lbl1                                         
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
        #size: self.texture_size   
        valign: 'top'                                   
        size: self.texture_size                         
        text_size: self.size
    MDLabel:                                            
        id: lbl2                                         
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        #size: self.texture_size   
        valign: 'middle'                                   
        size: self.texture_size                         
        text_size: self.size

#

''')


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

    def __init__(self, **kwargs):
        Thread.__init__(self)
        # to check values accessibility in global scope uncoment bellow  
        # Clock.schedule_interval(self.print_data, 0.001)

    # def print_data(self, dt):
    # self.num = self.num + 1
    # print(self.num, "---> ", self.rpm, " ", self.speed, " ", self.t, " ", self.fuel, " ", self.consm, " ", self.lat, " / ", self.lon)


# ============ First screen ==================================
class Classic_style_dash_board(MDScreen):
    latitude = NumericProperty()
    longitude = NumericProperty()
    my_list = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.back_ground_circle = LBl()
        self.add_widget(self.back_ground_circle)  # ---------------------- add background to speed, tacho

        self.add_widget(Speedometr())
        self.add_widget(Tachometr())

        self.center_rings = Center_rings()
        self.add_widget(self.center_rings)
        self.speed_lable = Speed_rpm_labels()
        self.add_widget(Speed_rpm_labels())
        self.tachometr = Tachometr()
        self.speedometr = Speedometr()

        self.stock_box = MDFloatLayout(pos_hint={"center_x": 0.5, "center_y": 0.50},
                                       size_hint=(0.25, 0.25))
        img = Image(pos_hint={"center_x": 0.5, "center_y": 0.5},
                    source='stock.png')
        self.stock_box.add_widget(img)
        self.add_widget(self.stock_box)

        self.scheduled = False
        self.scheduled_2 = False

        self.flag = False
        self.flag2 = False

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        pass
        # Clock.schedule_interval(self.update_widget, 1)

    def update_widget(self, dt):
        self.speedometr = Speedometr()
        if float(Dash_Board.speed) > 10 and not self.scheduled and not self.scheduled_2:
            self.remove_widget(self.stock_box)
            self.add_widget(self.map, 6)
            self.scheduled = True
            self.scheduled_2 = True

        elif float(Dash_Board.speed) <= 10 and not self.scheduled and self.scheduled_2:
            self.remove_widget(self.map)
            self.add_widget(self.stock_box)

            self.scheduled = True
            self.scheduled_2 = False

        elif float(Dash_Board.speed) <= 10 and self.scheduled:
            self.scheduled = False

    def on_touch_down(self, touch):
        print(touch.pos)
        self.box1 = MDBoxLayout()
        self.layout1 = MDFloatLayout()
        self.layout2 = MDFloatLayout()
        self.layout3 = MDFloatLayout()

        self.Img1 = Image(source="screen3.png",
                          size_hint=(0.9, 0.9),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},
                          )

        self.Img2 = Image(source="screen1.png",
                          size_hint=(0.9, 0.9),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},
                          )
        self.Img3 = Image(source="screen2.png",
                          size_hint=(0.8, 0.8),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},

                          )

        self.layout1.add_widget(self.Img1)
        self.layout2.add_widget(self.Img2)
        self.layout3.add_widget(self.Img3)

        self.Img1.bind(on_touch_down=self.shift_to_1screen)
        self.Img2.bind(on_touch_down=self.shift_to_2screen)
        self.Img3.bind(on_touch_down=self.shift_to_3screen)

        self.box1.add_widget(self.layout1)
        self.box1.add_widget(self.layout2)
        self.box1.add_widget(self.layout3)

        self.dialog = MDDialog(

            pos_hint={"center_x": 0.5, "center_y": 0.75},
            size_hint=(1, 0.3),
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
        # print("waitng for gps connection")


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

    def initialize_gsm(self):  # --------------------------------> initializtion of communication of gsm module

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
        command = f"AT+HTTPPOST=\"http://vehicledata.atwebpages.com/get_data.php\",\"application/x-www-form-urlencoded\",\"{data}\""
        command += self.delim
        self.send_gsm_command(command)
        # print("send command: ",command)


class Center_rings(MDFloatLayout):
    pass


class LBl(MDFloatLayout):
    def __init__(self, **kwargs):
        super(LBl, self).__init__(**kwargs)


class Speedometr(MDFloatLayout):
    w = NumericProperty()
    kmh = "0"
    speed_lbl = StringProperty()

    def __init__(self, **kwargs):
        super(Speedometr, self).__init__(**kwargs)

        self.speed = Speed_rpm_labels()

        self.flag1 = True
        self.flag2 = True

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        Clock.schedule_interval(self.update_value, 0.05)

    def update_value(self, dt):
        self.w = (Dash_Board.speed) * 260 / 200  # ----------------> speedometer's arrow


class Tachometr(MDFloatLayout):
    rpm = NumericProperty(0)
    rpm_lbl = StringProperty()

    def __init__(self, **kwargs):
        super(Tachometr, self).__init__(**kwargs)
        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        Clock.schedule_interval(self.update_value, 0.05)

    def update_value(self, *args):
        # print("updating tacho")
        self.rpm = (Dash_Board.arrow_rpm) * 243 / 7000


class Speed_rpm_labels(MDFloatLayout):
    kmh = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Speed_rpm_labels, self).__init__(**kwargs)

        self.lbl = LBl()

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        Clock.schedule_interval(self.update_label, 0.05)

    def update_label(self, dt):
        self.ids.speed_lbl.text = str(round(float(Dash_Board.speed)))
        self.ids.rpm_lbl.text = str(round(float(Dash_Board.rpm)))


# =============================================================================== Second screen =====================================================
class Sport_style_dash_board(MDScreen):
    x_rpm_scale = NumericProperty()
    rotate = NumericProperty()
    w = NumericProperty()

    def __init__(self, **kwargs):
        super(Sport_style_dash_board, self).__init__(**kwargs)
        self.add_widget(Gauge_temp())
        self.add_widget(Turbo_presure_gauge())
        self.add_widget(Oil_gauge())
        self.add_widget(Gauge_tank())
        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):

        Clock.schedule_interval(self.update_data, 0.05)

    def update_data(self, *args):
        self.x_rpm_scale = float(Dash_Board.rpm) * 246 / 7000
        self.ids.speed.text = str(round(float(Dash_Board.speed)))
        self.ids.rpm.text = str(round(float(Dash_Board.rpm)))

    def on_touch_down(self, touch):
        print(touch.pos)
        self.box1 = MDBoxLayout()
        self.layout1 = MDFloatLayout()
        self.layout2 = MDFloatLayout()
        self.layout3 = MDFloatLayout()

        self.Img1 = Image(source="screen3.png",
                          size_hint=(0.9, 0.9),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},
                          )

        self.Img2 = Image(source="screen1.png",
                          size_hint=(0.9, 0.9),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},
                          )
        self.Img3 = Image(source="screen2.png",
                          size_hint=(0.8, 0.8),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},

                          )

        self.layout1.add_widget(self.Img1)
        self.layout2.add_widget(self.Img2)
        self.layout3.add_widget(self.Img3)

        self.Img1.bind(on_touch_down=self.shift_to_1screen)
        self.Img2.bind(on_touch_down=self.shift_to_2screen)
        self.Img3.bind(on_touch_down=self.shift_to_3screen)

        self.box1.add_widget(self.layout1)
        self.box1.add_widget(self.layout2)
        self.box1.add_widget(self.layout3)

        self.dialog = MDDialog(

            pos_hint={"center_x": 0.5, "center_y": 0.75},
            size_hint=(1, 0.3),
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
            return True  # # S


class Gauge_temp(MDFloatLayout):
    x_coolant_temp = NumericProperty()

    def __init__(self, **kwargs):
        super(Gauge_temp, self).__init__(**kwargs)

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        # Clock.schedule_interval(self.coolant_temp, 0.001)
        Clock.schedule_interval(self.coolant_temp, 0.1)

    def coolant_temp(self, dt):
        self.x_coolant_temp = int(
            Dash_Board.t)  # * 130 / 150                             # --------------------------------------------- set temp  scale
        self.ids.temp_label.text = str(Dash_Board.t)


class Gauge_tank(MDFloatLayout):
    x_tank = NumericProperty()

    def __init__(self, **kwargs):
        super(Gauge_tank, self).__init__(**kwargs)
        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        Clock.schedule_interval(self.tank, 0.1)

    def tank(self, dt):
        self.x_tank = Dash_Board.fuel * 180 / 100


class Oil_gauge(MDFloatLayout):
    angle_oil_pressure = NumericProperty()

    def __init__(self, **kwargs):
        super(Oil_gauge, self).__init__(**kwargs)

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        Clock.schedule_interval(self.arrow, 0.1)

    def arrow(self, dt):
        self.angle_oil_pressure = Dash_Board.consm * 270 / 20
        self.ids.consm_label.text = str(round(Dash_Board.consm, 1))


class Turbo_presure_gauge(MDFloatLayout):
    angle_turbo_pressure = NumericProperty()

    def __init__(self, **kwargs):
        super(Turbo_presure_gauge, self).__init__(**kwargs)

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        Clock.schedule_interval(self.arrow, 0.1)

    def arrow(self, dt):
        self.angle_turbo_pressure = Dash_Board.consm * 180 / 20


class Engine(MDScreen):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Temp())
        self.add_widget(Gear_box_oil())
        self.add_widget(Voltmetr())
        self.add_widget(oil_pressure())
        self.add_widget(turbo_pressure())

    def on_touch_move(self, touch):

        print(touch.pos)
        self.box1 = MDBoxLayout()
        self.layout1 = MDFloatLayout()
        self.layout2 = MDFloatLayout()
        self.layout3 = MDFloatLayout()

        self.Img1 = Image(source="screen3.png",
                          size_hint=(0.9, 0.9),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},
                          )

        self.Img2 = Image(source="screen1.png",
                          size_hint=(0.9, 0.9),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},
                          )
        self.Img3 = Image(source="screen2.png",
                          size_hint=(0.8, 0.8),
                          pos_hint={"center_x": 0.5, "center_y": 0.5},

                          )

        self.layout1.add_widget(self.Img1)
        self.layout2.add_widget(self.Img2)
        self.layout3.add_widget(self.Img3)

        self.Img1.bind(on_touch_down=self.shift_to_1screen)
        self.Img2.bind(on_touch_down=self.shift_to_2screen)
        self.Img3.bind(on_touch_down=self.shift_to_3screen)

        self.box1.add_widget(self.layout1)
        self.box1.add_widget(self.layout2)
        self.box1.add_widget(self.layout3)

        self.dialog = MDDialog(

            pos_hint={"center_x": 0.5, "center_y": 0.75},
            size_hint=(1, 0.3),
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

    def test_gsm(self):

        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            type='custom',
            content_cls=test_gsm_module(),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.5, 0.6),
            md_bg_color=(0, 0, 0, 0),
            elevation=3,
            shadow_softness=5,

            buttons=[
                Button(
                    text="Close"
                )]
        )
        self.dialog.open()

    def test_gps(self):

        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(

            type='custom',
            content_cls=test_gps_module(),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.5, 0.6),
            md_bg_color=(0, 0, 0, 0),
            elevation=3,
            shadow_softness=5,

            buttons=[
                Button(
                    text="Close"
                )]
        )
        self.dialog.open()

    def test_can_bus(self):

        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            type='custom',
            content_cls=test_can_bus(),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.5, 0.6),
            md_bg_color=(0, 0, 0, 0),
            elevation=3,
            shadow_softness=5,

            buttons=[
                Button(
                    text="Close"
                )]
        )
        self.dialog.open()


# -----------------> Widgets of 3d Screen are bellow (Coolant temp, gearbox temp, Voltage, Oil pressure, Turbo)
class Temp(MDFloatLayout, TouchBehavior):
    dialog = None
    name = "Temperature"
    x_coolant_temp = NumericProperty()

    def __init__(self, **kwargs):
        super(Temp, self).__init__(**kwargs)

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):

        # Clock.schedule_interval(self.coolant_temp, 0.001)
        Clock.schedule_interval(self.coolant_temp, 0.1)

    def coolant_temp(self, dt):

        self.x_coolant_temp = int(
            Dash_Board.t)  # * 130 / 150                             # --------------------------------------------- set temp  scale

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y) == True:
            Dash_Board.widget_name = "Temperature t °C"
            Dash_Board.widget_yaxes_name = "t °C"
            # print("temp event")

            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(value=Dash_Board.t),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(0.8, 0.8),
                md_bg_color=(0, 0, 0, 0),
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
    x_gear_temp = NumericProperty()

    def __init__(self, **kwargs):
        super(Gear_box_oil, self).__init__(**kwargs)

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):

        Clock.schedule_interval(self.coolant_temp, 0.1)

    def coolant_temp(self, dt):

        self.x_gear_temp = int(Dash_Board.t * 0.8)

    def on_touch_down(self, touch):

        if self.collide_point(touch.x, touch.y) == True:

            Dash_Board.widget_name = "Gearbox oil t °C"
            Dash_Board.widget_yaxes_name = "t °C"

            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(value=Dash_Board.t * 0.8),
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

            Dash_Board.widget_name = "Alternator output, Volts"
            Dash_Board.widget_yaxes_name = "V"
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(value=14),
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
    angle_oil_pressure = NumericProperty()

    def __init__(self, **kwargs):
        super(oil_pressure, self).__init__(**kwargs)

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        Clock.schedule_interval(self.arrow, 0.1)

    def arrow(self, dt):
        self.angle_oil_pressure = Dash_Board.consm * 250 / 20

    def on_touch_down(self, touch):

        if self.collide_point(touch.x, touch.y) == True:

            Dash_Board.widget_name = "Oil pressure, PSI"
            Dash_Board.widget_yaxes_name = "PSI"
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(value=Dash_Board.consm / 2.3),
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
    angle_turbo_pressure = NumericProperty()

    def __init__(self, **kwargs):
        super(turbo_pressure, self).__init__(**kwargs)

        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()

    def start_updt_widget(self):
        Clock.schedule_interval(self.arrow, 0.1)

    def arrow(self, dt):

        self.angle_turbo_pressure = Dash_Board.consm * 180 / 20

    def on_touch_down(self, touch):

        if self.collide_point(touch.x, touch.y) == True:

            Dash_Board.widget_name = "Turbo boost, PSI"
            Dash_Board.widget_yaxes_name = "PSI"
            if self.dialog:
                self.dialog.dismiss()

            self.dialog = MDDialog(
                type='custom',
                content_cls=Plot_box(value=Dash_Board.consm * 0.75),
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


class test_gps_module(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()
        self.count = 0

    def start_updt_widget(self):
        Clock.schedule_interval(self.show_data, 0.5)

    def show_data(self, dt):
        self.count += 1
        self.ids.lbl.text += f"Latitude: {Dash_Board.lat} Longitude: {Dash_Board.lon}\n"
        if self.count > 12:
            self.ids.lbl.text = ""
            self.count = 0


class test_gsm_module(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()
        self.count = 0

    def start_updt_widget(self):
        Clock.schedule_interval(self.show_data, 1)

    def show_data(self, dt):
        self.count += 1
        data = str(Dash_Board.at_response).replace('&', '\n')
        new_data = data.replace(',', '\n')
        self.ids.lbl.text += new_data + '\n'
        if self.count > 2:
            self.ids.lbl.text = ""
            self.count = 0


class test_can_bus(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()
        self.count = 0
        self.bus = Read_bus_data()
        self.ids.lbl1.text = f"port: {str(self.bus.PcanHandle.value)}\n"
        self.ids.lbl1.text += f"bitrate: {str(self.bus.Bitrate.value)}\n"
        self.ids.lbl1.text += f"amount of recieved msg: {str(Dash_Board.line)}\n"
        self.ids.lbl1.text += f"---------------------------------------\n"

    def start_updt_widget(self):
        Clock.schedule_interval(self.show_data, 0.5)

    def show_data(self, dt):
        self.count += 1
        self.ids.lbl2.text += str(Dash_Board.msg) + '\n'
        if self.count > 12:
            self.ids.lbl2.text = ""
            count = 0


# -------------------------> plotting of incoming data. Class is evoked from MDDialog as custom class
class Plot_box(MDFloatLayout):
    y = NumericProperty()
    x = NumericProperty(0)
    x_axes = ListProperty([])
    y_axes = ListProperty([])

    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        # self.pos = 225, 100
        self.pos_hint = {"center_x": 0.2, "center_y": 0.5}
        # self.size = 800, 500
        self.size_hint = (0.95, 0.95)
        self.x = 0
        self.y = 0
        self.x_axes = []
        self.y_axes = []

        self.graf = plt.gcf()
        self.graph = None
        self.thread_ = threading.Thread(target=self.start_updt_widget, daemon=True)
        self.thread_.start()
        self.thread_ = threading.Thread(target=self.start_draw_graf, daemon=True)
        self.thread_.start()

        plt.clf()

        plt.title(Dash_Board.widget_name)
        plt.legend(["ϰ/t"], loc="upper right")
        plt.xlabel('t, sec')
        plt.ylabel(f"{Dash_Board.widget_yaxes_name}")
        plt.grid(False)
        plt.ylim(self.value - 5, self.value + 5)
        plt.style.context('dark_background')
        plt.plot(self.x_axes, self.y_axes,
                 color='red',
                 linestyle='-',
                 linewidth=3,
                 animated=False,
                 markerfacecolor='blue',
                 markersize=12)

    def start_updt_widget(self):
        self.Clock_id1 = Clock.schedule_interval(self.get_data, 0.1)
        self.Clock_id1()

    def start_draw_graf(self):
        self.Clock_id2 = Clock.schedule_interval(self.draw_plot, 0.1)
        self.Clock_id2()

    def get_data(self, dt):
        self.x += 1
        self.x_axes.append(self.x)
        self.y_axes.append(self.value)

        if len(self.x_axes) > 100:
            self.x_axes.pop(0)
            self.y_axes.pop(0)
            plt.xlim(self.x_axes[0], self.x_axes[-1])

        # print(self.value)

    def draw_plot(self, dt):
        plt.plot(self.x_axes, self.y_axes,
                 color='red',
                 linestyle='-',
                 linewidth=3,
                 animated=False,
                 markerfacecolor='blue',
                 markersize=12)

        self.graf.canvas.draw()
        obj = FigureCanvasKivyAgg(self.graf)
        obj.pos = 225, 100
        self.add_widget(obj)

    def stop_process(self):
        # print("stop, lists are: ")
        Clock.unschedule(self.Clock_id1)
        Clock.unschedule(self.Clock_id2)
        self.x_axes.clear()
        self.y_axes.clear()
        self.value = None
        plt.clf()


# -------------------------------------------------------> retrieving data from canbus network

class TimerRepeater(object):
    """
    A simple timer implementation that repeats itself
    """

    ## Constructor
    def __init__(self, name, interval, target):
        """
        Creates a timer.

        Parameters:
            name = name of the thread
            interval = interval in second between execution of target
            target = function that is called every 'interval' seconds
        """
        # define thread and stopping thread event
        self._name = name
        self._thread = None
        self._event = None
        # initialize target
        self._target = target
        # initialize timer
        self._interval = interval

    # Runs the thread that emulates the timer
    #
    def _run(self):
        """
        Runs the thread that emulates the timer.

        Returns:
            None
        """
        while not self._event.wait(self._interval):
            self._target()

    # Starts the timer
    #
    def start(self):
        """
        Starts the timer

        Returns:
            None
        """
        # avoid multiple start calls
        if (self._thread == None):
            self._event = threading.Event()
            self._thread = threading.Thread(None, self._run, self._name)
            self._thread.start()

    # Stops the timer
    #
    def stop(self):
        """
        Stops the timer

        Returns:
            None
        """
        if (self._thread != None):
            self._event.set()
            self._thread.join()
            self._thread = None


class Read_bus_data(Thread):

    def __init__(self, **kwargs):
        Thread.__init__(self)
        self.line = 0

        # Timerinterval (ms) for reading
        self.TimerInterval = 100
        # self.data_queue = data_queue
        self.PcanHandle = PCAN_USBBUS1
        self.Bitrate = PCAN_BAUD_500K

        self.m_objTimer = TimerRepeater("ReadMessages", 0.0001, self.Read_data)
        self.m_objTimer.start()

        self.m_objPCANBasic = PCANBasic()
        self.stsResult = self.m_objPCANBasic.Initialize(self.PcanHandle, self.Bitrate)

    def Read_data(self):
        self.ReadMessages()

    def ReadMessages(self):
        Dash_Board.line += 1
        # print(self.line)
        try:
            self.Result = self.m_objPCANBasic.Read(self.PcanHandle)

            msg = self.Result[1]
            timestamp = self.Result[2]
            Dash_Board.msg = list(msg.DATA)

            if msg.ID == 0x316 and msg is not None:
                Dash_Board.rpm = msg.DATA[3] * 7000 / 110
                # self.rpm = msg.DATA[3]*7000/110
                # print(f"rpm: {msg.DATA[3]*7000/110}")
                Dash_Board.arrow_rpm = Dash_Board.rpm
                # RPM = { 'RPM': msg.DATA[3]*7000/110}
                # self.data_queue.put(RPM)
                # self.data_queue.put(Dash_Board.arrow_rpm)
                # print("rpm: ", Dash_Board.rpm)
                Dash_Board.rpm = round(Dash_Board.rpm / 50) * 50

            elif msg.ID == 0x1F1 and msg is not None:
                Dash_Board.speed = msg.DATA[4] * 220 / 100
                # self.speed = msg.DATA[4]*220/100
                # SPEED = {'SPEED': msg.DATA[4]*220/100}
                # print(f"speed: {msg.DATA[4]*220/110}")
                Dash_Board.arrow_speed = Dash_Board.speed * 260 / 220
                # self.data_queue.put(SPEED)

                # print("t: ", Dash_Board.speed)
                # uncoment to filter data
            elif msg.ID == 0x0A0 and msg is not None:
                Dash_Board.t = msg.DATA[1] - 40
                ##T = {'T': (msg.DATA[1] -40)}
                # self.data_queue.put(T)

                # print(f"t: {msg.DATA[1] - 40}")
                # print("t: ", Dash_Board.t)
            elif msg.ID == 0x0A1 and msg is not None:
                Dash_Board.consm = msg.DATA[4] * 20 / 100
                # BOOST = {'BOOST': msg.DATA[4]}
                # self.data_queue.put(BOOST)

                # print(f"boost: {msg.DATA[4]}")
                # print("boost: ", Dash_Board.boost)
            elif msg.ID == 0x0350 and msg is not None:
                Dash_Board.fuel = msg.DATA[3] * 0.75
                # FUEL = {'FUEL': msg.DATA[3]*0.75}
                # self.data_queue.put(FUEL)

                # print(f"fuel: {msg.DATA[3]*0.75}")
            # print(f"{Dash_Board.line}: --> {Dash_Board.rpm} {Dash_Board.speed} {Dash_Board.t} {Dash_Board.boost} {Dash_Board.fuel}")
        except Exception as e:
            print("eror: ", e)
            self.Read_data()

    # def store_data(self):


class Dashboard(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        sm = MDScreenManager()
        sm.add_widget(Classic_style_dash_board())
        sm.add_widget(Sport_style_dash_board())
        sm.add_widget(Engine())
        return sm


if __name__ == '__main__':
    # -------------------- launching treads of reading data classes

   # bus = Read_bus_data()
   # gps = GPS()
   # gsm = GSM()
   #
   # db = Dash_Board()
   #
   # bus.start()
   # db.start()
   # gps.start()
   # gsm.start()

    Dashboard().run()


