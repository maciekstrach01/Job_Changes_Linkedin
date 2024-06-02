

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QLabel, QMessageBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys
import asyncio
import aiohttp
import json
from datetime import datetime
import openpyxl
from qasync import QEventLoop, asyncSlot

class AsyncLinkedInGUI(QMainWindow):
    API_KEY = ''  # API key defined in class individual for each profile in ProxyCurl

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LinkedIn Profile Analyzer")
        self.setGeometry(100, 100, 800, 500)
        self.initUI()    

    def initUI(self):

        self.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 5px;
            }
            QTextEdit QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 10px 0 10px 0;
                border-radius: 5px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background: #b0b0b0;
                min-height: 20px;
                border-radius: 5px;
            }
            QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
                background: none;
            }
            QTextEdit QScrollBar::up-arrow:vertical, QTextEdit QScrollBar::down-arrow:vertical {
                background: none;
            }
            QTextEdit QScrollBar::add-page:vertical, QTextEdit QScrollBar::sub-page:vertical {
                background: none;
            }
            QWidget {
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
                color: #333;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #555;
            }
            QTextEdit, QLineEdit {
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton {
                color: #fff;
                background-color: #007bff;
                border-radius: 5px;
                padding: 10px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        # Initialization of widgets
        self.urlsLabel = QLabel("Adresy URL profilu LinkedIn:")
        self.urlsText = QTextEdit()
        self.dateLabel = QLabel("Data od (dd-mm-yyyy):")
        self.date_entry = QLineEdit()
        self.fetchButton = QPushButton("Pobierz profile")
        self.analyzeButton = QPushButton("Analizuj i eksportuj")

        # Adding widgets to the layout
        layout.addWidget(self.urlsLabel)
        layout.addWidget(self.urlsText)
        layout.addWidget(self.dateLabel)
        layout.addWidget(self.date_entry)
        layout.addWidget(self.fetchButton)
        layout.addWidget(self.analyzeButton)

        # Combination of buttons with functions
        self.fetchButton.clicked.connect(self.on_fetch_profiles)
        self.analyzeButton.clicked.connect(self.analyze_and_export)


        centralWidget.setLayout(layout)


    @asyncSlot()
    async def on_fetch_profiles(self):
        urls = self.urlsText.toPlainText().split('\n')

        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_profile(session, url, self.API_KEY) for url in urls if url.strip()]
            profiles_data = await asyncio.gather(*tasks)

        profiles_data = [profile for profile in profiles_data if profile]
        with open('profiles_data.json', 'w', encoding='utf-8') as file:
            json.dump(profiles_data, file, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Zakończono", "Pobieranie profili zakończone. Dane zapisane w pliku profiles_data.json.")
            
    async def fetch_profile(self, session, url, api_key):
        try:
            async with session.get('https://nubela.co/proxycurl/api/v2/linkedin', params={'url': url, 'skills': 'include'}, headers={'Authorization': 'Bearer ' + api_key}) as response:
                if response.status == 200:
                    data = await response.json()
                    profile_data = {
                        "full_name": data.get("full_name"),
                        "experiences": self.extract_experiences(data.get("experiences", [])),
                        "linkedin_url": url  # Add profile URL to profile data
                    }
                    return profile_data
        except Exception as e:
            print(f"Error fetching profile {url}: {e}")
            return None

    def extract_experiences(self, experiences):
        # Auxiliary function for experience processing and date formatting
        formatted_experiences = []
        for exp in experiences:
            # We assume that 'starts_at' and 'ends_at' are dictionaries with keys 'day', 'month', 'year'
            start_date = exp.get("starts_at")
            end_date = exp.get("ends_at")
            
            # Format the dates
            start_date_str = f"{start_date['day']}-{start_date['month']}-{start_date['year']}" if start_date else "Brak danych"
            end_date_str = f"{end_date['day']}-{end_date['month']}-{end_date['year']}" if end_date else "Do teraz"
            
            formatted_experiences.append({
                "job_title": exp.get("title"),
                "company_name": exp.get("company"),
                "start_date": start_date_str,
                "end_date": end_date_str
            })
        return formatted_experiences


    def analyze_and_export(self):
        date_from_str = self.date_entry.text()
        try:
            date_from = datetime.strptime(date_from_str, "%d-%m-%Y")  
        except ValueError:
            QMessageBox.critical(self, "Błąd", "Nieprawidłowy format daty. Proszę użyć formatu DD-MM-YYYY.")
            return  # Stops further execution of the function in case of error

        try:
            with open('profiles_data.json', 'r', encoding='utf-8') as file:
                profiles_data = json.load(file)
            self.check_new_positions_since(profiles_data, date_from)  
        except FileNotFoundError:
            QMessageBox.critical(self, "Błąd", "profiles_data.json not found. Fetch profiles first.")
            return
        

    def check_new_positions_since(self, profiles, date_from):
        eligible_profiles_json = []

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Eligible Profiles"
        ws.append(["Full Name", "Job Title", "Company Name", "Start Date", "End Date", "LinkedIn URL"])  # Dodaj nagłówek dla URL

        for profile in profiles:
            new_positions = []
            for experience in profile["experiences"]:
                start_date_str = experience.get("start_date", "Brak danych")
                if start_date_str != "Brak danych":
                    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
                    if start_date >= date_from:
                        new_positions.append(experience)

            if new_positions:
                profile_info = {
                    "full_name": profile['full_name'],
                    "new_positions": new_positions,
                    "linkedin_url": profile['linkedin_url']  #  We store the profile URL
                }

                for position in new_positions:
                    ws.append([
                        profile['full_name'],
                        position['job_title'],
                        position['company_name'],
                        position['start_date'],
                        position['end_date'],
                        profile['linkedin_url']  # Add profile URL to each line
                    ])

                eligible_profiles_json.append(profile_info)

        wb.save('eligible_profiles.xlsx')
        QMessageBox.information(self, "Info", "Wyszukiwanie zakończone. Wyniki zapisane w pliku eligible_profiles.xlsx")


def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = AsyncLinkedInGUI()
    window.show()

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    main()
