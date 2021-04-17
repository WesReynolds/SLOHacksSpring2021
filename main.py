from kivy.app import App
from kivy.uix.widget import Widget

from switchingScreen import SwitchingScreen

screenManager = SwitchingScreen.getScreenManager()

class MainScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)

class SecondScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(SecondScreen, self).__init__(**kw)

class StatsApp(App):
    def __init__(self):
        super(StatsApp, self).__init__()
        self.mainScreen = None
        self.secondScreen = None

    def build(self):
        self.mainScreen = MainScreen(name="main")
        self.secondScreen = SecondScreen(name="second")
        
        screenManager.add_widget(self.mainScreen)
        screenManager.add_widget(self.secondScreen)
        return screenManager

if __name__ == '__main__':
    StatsApp().run()
