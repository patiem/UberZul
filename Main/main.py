from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from Main.database import DataBase
from Main.database import Notice
from kivy.core.window import Window



class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created


class CreateNoticeWindow(Screen):
    namee = ObjectProperty(None)
    whom = ObjectProperty(None)
    job_type = ObjectProperty(None)
    price_value = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.job_type.text != "" and self.price_value.text != "" and self.whom.text != "":
            nt.add_notice(self.namee.text, self.whom.text, self.job_type.text, self.price_value.text)
            self.reset()
        else:
            invalidForm()

    def reset(self):
        self.namee.text = ""
        self.whom.text = ""
        self.job_type.text = ""
        self.price_value.text = ""


class NoticeListWindow(Screen):
    n = ObjectProperty(None)
    opis = ObjectProperty(None)
    lista = ObjectProperty(None)
    current = ""

    def on_enter(self, *args):
        self.n.text = "List of notices: "
        self.opis.text = "Tu bedzie lista ogloszen"
        nt.load()
        notices = nt.get_notices()
        str_notices = [key + "- kategoria: " + value[2] + ", co: " + value[0] + ", kto: " + value[1] + ", za ile: " + value[3] for key, value in notices.items()]
        self.lista.text = "\n".join(str_notices)



class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")
nt = Notice()

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"),
           NoticeListWindow(name="noticeList"), CreateNoticeWindow(name="createNotice")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
