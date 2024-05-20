from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from kivymd.uix.screenmanager import MDScreenManager

class ClassicStyleDashBoard(MDScreen):
    pass

class SportStyleDashBoard(MDScreen):
    pass

class Engine(MDScreen):
    pass

class Main(BoxLayout):
    pass

kv = '''
<ClassicStyleDashBoard>:
    name: 'classic'
    BoxLayout:
        canvas:
            Color:                           
                rgba: 1, 0, 0, 1  # red      
            Rectangle:                       
                pos: self.pos                
                size: self.size              
        orientation: 'vertical'
        Label:
            text: 'Classic Style Dashboard'

<SportStyleDashBoard>:
    name: 'sport'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Sport Style Dashboard'

<Engine>:
    name: 'engine'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Engine Information'

<Main>:
    orientation: 'vertical'
    MDTopAppBar:
        title: "Dashboard"
        left_action_items: [['menu', lambda x: app.switch_screen('classic')]]
        right_action_items: [['settings', lambda x: app.switch_screen('sport')], ['account', lambda x: app.switch_screen('engine')]]
    MDScreenManager:
        id: screen_manager
        ClassicStyleDashBoard:
            name: 'classic'
        SportStyleDashBoard:
            name: 'sport'
        Engine:
            name: 'engine'
'''

class DashboardApp(MDApp):
    def build(self):
        print("Loading KV string")
        Builder.load_string(kv)
        print("KV string loaded successfully")
        return Main()

    def switch_screen(self, screen_name):
        print(f"Switching to screen: {screen_name}")
        self.root.ids.screen_manager.current = screen_name

if __name__ == '__main__':
    DashboardApp().run()