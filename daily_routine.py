import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QLineEdit, QCalendarWidget)
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont

class DigitalDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Dashboard for Daily Routine")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #333; color: #fff;")

        layout = QVBoxLayout()

        self.clock = QLabel("00:00:00")
        self.clock.setFont(QFont("Arial", 30))
        self.clock.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.clock)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        calendar = QCalendarWidget()
        calendar.setStyleSheet("color: #fff; background-color: #555;")
        layout.addWidget(calendar)

        self.todo_list = QListWidget()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Add a new task...")
        add_task_btn = QPushButton("Add Task")
        add_task_btn.clicked.connect(self.add_task)
        layout.addWidget(self.task_input)
        layout.addWidget(add_task_btn)
        layout.addWidget(self.todo_list)

        self.weather = QLabel("Weather: Fetching...")
        self.quote = QLabel("Quote: Loading...")
        layout.addWidget(self.weather)
        layout.addWidget(self.quote)

        self.update_weather()
        self.update_quote()
        self.setLayout(layout)

        def update_time(self):
            current_time = QTime.currentTime().toString("hh:mm:ss A")
            self.clock.setText(current_time)

        def add_task(self):
            task = self.task_input.text()
            if task:
                self.todo_list.addItem(task)
                self.task_input.clear()

        def update_weather(self):
            try:
                response = requests.get("http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=London")
                data = response.json()
                temp = data["current"]["temp_c"]
                condition = data["current"]["condition"]["text"]
                self.weather.setText(f"Weather: {temp}°C, {condition}")
            except:
                self.weather.setText("Weather: Unable to fetch data.")

        def update_quote(self):
            try:
                response = requests.get("https://api.quotable.io/random")
                data = response.json()
                quote = data["content"]
                self.quote.setText(f"Quote: {quote}")
            except:
                self.quote.setText("Quote: Unable to fetch data.")

            if __name__ == "__main__":
                app = QApplication(sys.argv)
                dashboard = DigitalDashboard()
                dashboard.show()
                sys.exit(app.exec_())