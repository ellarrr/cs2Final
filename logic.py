import re
from gui import *
import csv
from PyQt6.QtWidgets import QMainWindow


class Logic(QMainWindow, Ui_MainWindow):
    """
    Logic for program
    """
    def __init__(self):
        """
        Initializer
        """
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.messageLabel.hide()
        self.message2Label.hide()
        self.message2Label.hide()
        self.message3Label.hide()

    def enter_page1(self):
        """
        Saves valid profile into users.csv
        Checks for errors
        """
        passw = self.passEdit.text()
        username = self.nameEdit.text()
        user_exists = False
        password_criteria = r"^(?=.*[A-Z])(?=.*[!@#$&])(?=.*\d).{8,}$"

        try:
            with open("users.csv",'r',newline='') as file0:
                reader = csv.reader(file0)
                for row in reader:
                    if len(row) > 0 and row[0] == username:
                        user_exists = True
                        break
        except Exception as e:
            pass

        try:
            if user_exists:
                self.messageLabel.setText("Username already exists")
                self.messageLabel.show()
            elif not username.strip():
                self.messageLabel.setText("Username cannot be empty")
                self.messageLabel.show()
            elif not passw.strip():
                self.messageLabel.setText("Password cannot be empty")
            elif not re.fullmatch(password_criteria, passw):
                self.messageLabel.setText("Invalid password")
                self.messageLabel.show()
            elif not re.fullmatch(r"[a-zA-Z0-9]+", username):
                self.messageLabel.setText("Invalid username")
                self.messageLabel.show()
            else:
                with open("users.csv",'a',newline='') as file:
                    writer=csv.writer(file)
                    writer.writerow([username,passw])
                    self.messageLabel.setText("Profile created successfully")
                    self.messageLabel.show()
                    self.nameEdit.clear()
                    self.passEdit.clear()
        except Exception as e:
            pass

    def logout(self):
        """
        Logs out user after logging in
        """
        self.stackedWidget.setCurrentIndex(0)
        self.name2Edit.clear()
        self.pass2Edit.clear()
        self.message3Label.clear()
        self.message2Label.hide()
        self.textEdit.clear()

    def login_page1(self):
        """
        Moves user to login page
        """
        self.messageLabel.hide()
        self.nameEdit.clear()
        self.passEdit.clear()
        self.stackedWidget.setCurrentIndex(1)

    def back(self):
        """
        Brings user back to create profile page
        """
        self.stackedWidget.setCurrentIndex(0)
        self.message2Label.hide()
        self.name2Edit.clear()
        self.pass2Edit.clear()

    def login_page2(self):
        """
        Checks for valid username and password
        Displays user's journal entry if existing
        """
        username = self.name2Edit.text()
        passw = self.pass2Edit.text()
        user_found = False
        try:
            with open('users.csv','r',newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username and row[1] == passw:
                        user_found = True
                        self.journalLabel.setText(f"{username}'s journal entry:")
                        break

            if user_found:
                self.stackedWidget.setCurrentIndex(2)
                with open('data.csv','r',newline='') as file0:
                    reader = csv.reader(file0)
                    for row in reader:
                        if row[0] == username:
                            text = row[1]
                            break
                self.textEdit.setPlainText(text)
            else:
                self.message2Label.setText("Invalid username or password.")
                self.message2Label.show()
        except Exception as e:
            pass

    def save(self):
        """
        Save journal entry and username into data.csv
        """
        username = self.name2Edit.text()
        text = self.textEdit.toPlainText()

        rows = []
        user_found_in_data = False

        with open('data.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    if row[0] == username:
                        row[1] = text
                        user_found_in_data = True
                    rows.append(row)

        if not user_found_in_data:
            rows.append([username, text])

        with open('data.csv', 'w', newline='') as file0:
            writer = csv.writer(file0)
            writer.writerows(rows)

        self.message3Label.setText('Journal saved successfully')
        self.message3Label.show()







