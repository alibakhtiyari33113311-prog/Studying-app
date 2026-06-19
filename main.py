import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window

Window.clearcolor = (0.06, 0.07, 0.1, 1)

DATA_FILE = "study_data.json"

# ---------------- DATA ----------------
def load():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "tasks": [],
            "progress": 0,
            "streak": 1,
            "timer": 1500
        }

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load()

# ---------------- HOME ----------------
class Home(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=20)
        layout.add_widget(Label(text="📚 Study PRO", font_size=30, color=(1,1,1,1)))
        layout.add_widget(Label(text="Focus mode activated 🔥", color=(0.7,0.7,0.7,1)))

        self.add_widget(layout)

# ---------------- TASKS ----------------
class Tasks(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=20)

        self.input = TextInput(hint_text="Add study topic")
        layout.add_widget(self.input)

        btn = Button(text="Add Task ➕")
        btn.bind(on_press=self.add)
        layout.add_widget(btn)

        self.label = Label(text="", color=(1,1,1,1))
        layout.add_widget(self.label)

        self.refresh()
        self.add_widget(layout)

    def add(self, instance):
        if self.input.text:
            data["tasks"].append(self.input.text)
            save()
            self.input.text = ""
            self.refresh()

    def refresh(self):
        self.label.text = "\n".join(["📌 " + t for t in data["tasks"]])

# ---------------- PROGRESS ----------------
class Progress(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=20)

        self.label = Label(text=f"📊 Progress: {data['progress']}%", font_size=24, color=(1,1,1,1))
        layout.add_widget(self.label)

        btn = Button(text="Complete +10% 🚀")
        btn.bind(on_press=self.up)
        layout.add_widget(btn)

        self.add_widget(layout)

    def up(self, instance):
        data["progress"] = min(100, data["progress"] + 10)
        save()
        self.label.text = f"📊 Progress: {data['progress']}%"

# ---------------- STREAK ----------------
class Streak(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout = BoxLayout(orientation="vertical", padding=20)

        self.label = Label(text=f"🔥 Streak: {data['streak']} days", font_size=24, color=(1,1,1,1))
        layout.add_widget(self.label)

        btn = Button(text="Study done today ✔")
        btn.bind(on_press=self.add_day)
        layout.add_widget(btn)

        self.add_widget(layout)

    def add_day(self, instance):
        data["streak"] += 1
        save()
        self.label.text = f"🔥 Streak: {data['streak']} days"

# ---------------- TIMER (POMODORO) ----------------
class Timer(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.time_left = data["timer"]

        layout = BoxLayout(orientation="vertical", padding=20)

        self.label = Label(text=self.format_time(), font_size=40, color=(1,1,1,1))
        layout.add_widget(self.label)

        start = Button(text="Start ⏱")
        start.bind(on_press=self.start)
        layout.add_widget(start)

        reset = Button(text="Reset 🔄")
        reset.bind(on_press=self.reset)
        layout.add_widget(reset)

        self.add_widget(layout)

    def format_time(self):
        m = self.time_left // 60
        s = self.time_left % 60
        return f"{m:02d}:{s:02d}"

    def tick(self, dt):
        if self.time_left > 0:
            self.time_left -= 1
            self.label.text = self.format_time()
        else:
            self.label.text = "🔥 Session Done!"

    def start(self, instance):
        Clock.schedule_interval(self.tick, 1)

    def reset(self, instance):
        self.time_left = 1500
        self.label.text = self.format_time()

# ---------------- APP ----------------
class StudyPRO(App):
    def build(self):

        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(Home(name="home"))
        sm.add_widget(Tasks(name="tasks"))
        sm.add_widget(Progress(name="progress"))
        sm.add_widget(Streak(name="streak"))
        sm.add_widget(Timer(name="timer"))

        root = BoxLayout(orientation="vertical")

        root.add_widget(sm)

        nav = BoxLayout(size_hint_y=0.12)

        def go(screen):
            sm.current = screen

        buttons = [
            ("🏠", "home"),
            ("📚", "tasks"),
            ("📊", "progress"),
            ("🔥", "streak"),
            ("⏱", "timer")
        ]

        for text, screen in buttons:
            b = Button(text=text)
            b.bind(on_press=lambda x, s=screen: go(s))
            nav.add_widget(b)

        root.add_widget(nav)

        return root


StudyPRO().run()
