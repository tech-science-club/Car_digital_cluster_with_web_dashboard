#from item import Item
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import MDList, OneLineListItem
import serial as serial
from kivy.core.window import Window
from kivy.graphics import Canvas, Rectangle, PushMatrix, Translate, PopMatrix
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.theming import ThemeManager
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton
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


Window.size = (800, 500)
class Main_window(Screen):
    pass

#class Arduino():
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        #self.pre_enter()
#        self.arduino_Data = serial.Serial("com3", 9600, timeout=1)
#    #def pre_enter(self, *args):
#        Clock.schedule_interval(self.get_data, 0.01)
#        #self.data_list = []
#
#    def get_data(self, dt):
#
#
#
#        self.data = self.arduino_Data.readline()
#        self.data = str(self.data, 'utf-8')
#        self.data = self.data.strip('\r\n')
#        #self.round_data = str(self.data)                                      #self.data[:2]
#        #self.round_data = str(self.round_data)
#        #print(self.data)
#        #self.round_data = str(self.round_data)
#        #self.data_list.append(self.round_data)
#
#        #if len(self.data_list) > 10:
#        #    self.data_list.pop(0)
#            #print(self.data_list)
#    #def pre_leave(self, *args):
#    #    self.arduino_Data.close()
#
#        #return self.get_data

class Content_bathroom(MDBoxLayout):
    def __init__(self, **kwargs):
        super(Content_bathroom, self).__init__(**kwargs)
        self.pre_enter()
    #Clock.schedule_interval(self.pre_enter, 0.01)

    def pre_enter(self, *args):
        self.arduino_Data = serial.Serial("com3", 9600)
        self.data = self.arduino_Data.readline()
        self.data = str(self.data, 'utf-8')
        self.data.encode()
        self.data = self.data.strip('\r\n')                                

        self.round_data = self.data[:2]
        self.temp = str(self.data)
        self.ids.temp_sensor_data_bathroom.text = self.temp + " °C"
        print(self.temp)
    #def pre_leave(self, *args):
        self.arduino_Data.close()

class Content_badroom(MDBoxLayout):
    def __init__(self, **kwargs):
       super(Content_badroom, self).__init__(**kwargs)
       self.pre_enter()
       #Clock.schedule_interval(self.pre_enter, 0.01)

    def pre_enter(self, *args):
        self.arduino_Data = serial.Serial("com3", 9600)
        self.data = self.arduino_Data.readline()
        self.data = str(self.data, 'utf-8')
        self.data = self.data.strip('\r\n')


        self.temp = str(self.data)
        self.ids.temp_sensor_data_badroom.text = self.temp + " °C"
        print(self.temp)
    #def pre_leave(self, *args):
        self.arduino_Data.close()

class Content_kitchen(MDBoxLayout):
   def __init__(self, **kwargs):
       super(Content_kitchen, self).__init__(**kwargs)
       self.pre_enter()
       #Clock.schedule_interval(self.pre_enter, 0.01)

   def pre_enter(self, *args):
       self.arduino_Data = serial.Serial("com3", 9600)
       self.data = self.arduino_Data.readline()
       self.data = str(self.data, 'utf-8')
       self.data = self.data.strip('\r\n')


       self.temp = str(self.data)
       self.ids.temp_sensor_data.text = self.temp + " °C"
       print(self.temp)
   #def pre_leave(self, *args):
       self.arduino_Data.close()

class Content_all_apartment(MDBoxLayout):
    pass


class Second_Window(Screen):

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.bg = Rectangle(source='apartment.png', size=(0.8,0.8), pos_hint = {"x": 0, "y": 0})
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
            self.bg.pos = instance.pos
            self.bg.size = instance.size

    def on_touch_down(self, touch ):

        if self.ids.general_set.collide_point(*touch.pos):
            self.change_apartment()
            if touch.is_double_tap:
                self.popup_all_apartment(self)
            return True

        elif self.ids.add_in_hall.collide_point(*touch.pos):
            self.change_color_hall()
            if touch.is_double_tap:
                self.popup_kitchen(self)

            return True

        elif self.ids.add_in_bathroom.collide_point(*touch.pos):
            self.change_bathroom()

            if touch.is_double_tap:
                self.popup_bathroom(self)

            return True

        elif self.ids.add_in_bedroom.collide_point(*touch.pos):
            self.change_bedroom()
            if touch.is_double_tap:
                self.popup_badroom(self)
            return True
        else:
            self.bg.source = 'apartment.png'

            return super(Second_Window, self).on_touch_down(touch)

    def popup_bathroom(self, instance):

        self.message = MDDialog(title="Bathroom review",
                                type="custom",
                                opacity=0.85,

                                content_cls=Content_bathroom(),
                                buttons=[MDFlatButton(text="Settings", on_press=self.set_bathroom, pos_hint={"center_x": 0.5, "center_y": 0.2})])
        self.message.open()

    def popup_kitchen(self, instance):

        self.message = MDDialog(title="Kitchen review",
                            type="custom",
                            opacity=0.85,

                            content_cls=Content_kitchen(),
                            buttons=[MDFlatButton(text="Settings", on_press=self.set_bathroom, pos_hint={"center_x": 0.5, "center_y": 0.2})])
        self.message.open()

    def popup_badroom(self, instance):
        self.message = MDDialog(title="Badroom review",
                            type="custom",
                            opacity=0.85,

                            content_cls=Content_badroom(),
                            buttons=[MDFlatButton(text="Settings", on_press=self.set_bathroom, pos_hint={"center_x": 0.5, "center_y": 0.2})])
        self.message.open()

    def popup_all_apartment(self, instance):
        self.message = MDDialog(title="All apartment review",
                            type="custom",
                            opacity=0.85,

                            content_cls=Content_all_apartment(),
                            buttons=[MDFlatButton(text="Settings", on_press=self.set_bathroom, pos_hint={"center_x": 0.5, "center_y": 0.2})])
        self.message.open()

    def change_bathroom(self):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.bg.source = "pic3.png"

    def context_menu(self, arg):
       # #self.arduino_data = serial.Serial("com3", 9600)
       # data = self.arduino_Data.readline()
       # data = data.decode()
       # #time.sleep(0.5)
       # data = data.strip('\r\n')
       # data.split()
       # self.round_data = data[:2]

        self.message = MDDialog(title = "Bathroom review",
                                buttons = [MDFlatButton(text = "Settings", on_press = self.set_bathroom)])
   
        self.message.open()
    def set_bathroom(self, arg):
        pass
    def change_color_hall(self):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.bg.source = "pic1.png"
    def context_menu_kitchen(self, args):
        self.message = MDDialog(title = "Kitchen review",
                                text = "Temperature:  " + "\n" +
                                        "Huminity: " + "\n" +
                                        "Floor heating status:" + "\n" +
                                        "A/C status:" + "\n" +
                                        "Radiator status: " + "\n" +
                                        "Light status: ",
                                buttons = [MDFlatButton(text = "Settings", on_press = self.set_kitchen)])
        self.message.open()
    def set_kitchen(self, args):
        pass
    def change_bedroom(self):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.bg.source = "pic2.png"
    def context_menu_bedroom(self, args):
        self.message = MDDialog(title = "Bedroom review",
                                text = "Temperature:  " + "\n" +
                                        "Huminity: " + "\n" +
                                        "Floor heating status:" + "\n" +
                                        "A/C status:" + "\n" +
                                        "Radiator status: ",
                                buttons = [MDFlatButton(text = "Settings", on_press = self.set_bedroom)])
        self.message.open()
    def set_bedroom(self, args):
        pass

    def change_apartment(self):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.bg.source = "pattern.png"

    def back(self):
        print("here you are")
class Info_line(MDBoxLayout):
    pass

class Join_canvas_button(Second_Window, Info_line):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = MDFloatLayout()
        self.but = Button(size_hint=(120, 120), pos_hint= {"x": 0.5, "y": 0.5})
        self.box.add_widget(self.but)

class Sechd_windowApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"


Sechd_windowApp().run()
