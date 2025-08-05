"""Tracker Application."""

import sys
from PyQt5.QtWidgets import(
    QApplication, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, 
    QDateEdit, QPushButton, QListWidget,
    QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import QDate, Qt



# module for implimenting history features.
import json

import os

class AssignmentTracker(QWidget):
    def __init__(self):
        super().__init__()

       
        self.apply_styles()
        self.setWindowTitle("Assignment Deadline Tracker")
        self.setGeometry(400,200,500,500)
        self.init_ui()
        self.assignments = []  # this holds all the assingmetn reason: so it can be sorted
        self.load_assignments()  # this automatically loads data from the file whan lunched
        self.show_due_reminders()

    def init_ui(self):
        layout = QVBoxLayout()

        special_layout = QHBoxLayout()

        # The Title input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter assignment title")
        self.title_input.returnPressed.connect(self.add_assignment)

        # The Due Date Picker
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())  # this gives us the current date
        self.date_input.setCalendarPopup(True)

        # add button
        self.add_button = QPushButton("Add Assignemt")
        self.add_button.clicked.connect(self.add_assignment)

        # edit Button
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_assignment)
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 17px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: darkGreen;
            }
        """)

        # exit Button
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_)
        self.exit_button.setStyleSheet("""                          
            QPushButton {
                background-color: red;
                color: white;
               
            }

            QPushButton:hover {
                background-color: darkRed;
            }""")


        # Assignment list
        self.assignment_list = QListWidget()


        # Layouts
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.title_input)
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.add_button)

        new_layout = QHBoxLayout()
        # Delete Button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_assignment)
        new_layout.addWidget(self.edit_button)
        new_layout.addWidget(self.delete_button)
        new_layout.addWidget(self.exit_button)

        layout.addLayout(input_layout)
        layout.addWidget(QLabel("Upcoming assignments:"))
        layout.addWidget(self.assignment_list)
        layout.addLayout(new_layout)
        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI, sans-serif;
                font-size: 17px; font-weight: bold
            }

            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 4px;
                padding: 4px 6px;
            }

            QDateEdit {
                padding: 4px;
                border: 2px solid #ccc;
                border-radius: 4px;
            }

            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #005F9E;
            }

            QLabel {
                font-weight: bold;
                margin-bottom: 9px;
            }

            QListWidget {
                border: 1px solid #ccc;
                padding: 4px;
                background-color: #f9f9f9;
            }

            QListWidget::item {
                padding: 4px;
            }

            QListWidget::item:selected {
                
                font-color: black
            }
        """)


    # adds
    def add_assignment(self):
        title = self.title_input.text().title()
        due_date = self.date_input.date()

        if title.strip():
            # Add the assignment to our internal list
            self.assignments.append({
                "title": title,
                "due": due_date
            })

            # Sort the list by due date
            self.assignments.sort(key=lambda x: x["due"])

            # Clear the QListWidget before updating
            self.assignment_list.clear()

            # Add sorted .items to the  list
            today = QDate.currentDate()
            for item in self.assignments:
                due_str = item["due"].toString("yyyy-MM-dd")
                days_left = today.daysTo(item["due"])
                text = f"{item['title']} - Due: {due_str}........({days_left} days left)"
                if days_left < 0:
                    text += " [OVERDUE]"
                    item = QListWidgetItem(text)
                    item.setForeground(Qt.red) 

                elif days_left == 0:
                    text += " [DUE]"
                    item = QListWidgetItem(text)
                    item.setForeground(Qt.darkBlue)
                    
                else:
                    item =QListWidgetItem(text)
                    item.setForeground(Qt.darkGreen)

                self.assignment_list.addItem(item)
            
            # Clear input field
            self.title_input.clear()
            self.save_assignments()
        else:
            QMessageBox.warning(self,"No Selection","Enter Assignment")            

    # saves
    def save_assignments(self):
        data = []
        for item in self.assignments:
            data.append({
                "title": item["title"],
                "due": item["due"].toString("yyyy-MM-dd")
            })

        with open("assignments.json", "w") as file:
            json.dump(data, file, indent=2)


    # loads
    def load_assignments(self):
        if os.path.exists("assignments.json"):
            with open("assignments.json", "r") as file:
                data = json.load(file)

            self.assignments.clear()

            for item in data:
                due_date = QDate.fromString(item["due"], "yyyy-MM-dd")
                self.assignments.append({
                    "title": item["title"],
                    "due": due_date
                })

            self.refresh_assignment_list()
        else:
            ...  # used insted of 'Pass'


    # refresh
    def refresh_assignment_list(self):
        self.assignment_list.clear()
        today = QDate.currentDate()

        for task in self.assignments:
            title = task["title"]

            due_date = task["due"]
            due_str = due_date.toString("yyyy-MM-dd")  # changes the Qdate to string
            days_left = today.daysTo(due_date)  # checks the numbers of days left

            text = f"{title} - Due: {due_str}........({days_left} days left)"

            if days_left < 0:
                text += " [OVERDUE]"
                item = QListWidgetItem(text)
                item.setForeground(Qt.red)
            elif days_left == 0:
                text += " [DUE]"
                item = QListWidgetItem(text)
                
                item.setForeground(Qt.darkYellow)
            else:
                item = QListWidgetItem(text)

                item.setForeground(Qt.darkGreen)


            self.assignment_list.addItem(item)


    def delete_assignment(self):
        selected_row = self.assignment_list.currentRow()

        if selected_row >= 0:  # this happens when a row is picked from the QlistWidget
            reply = QMessageBox.information(self,
            "Confirm Delete",
            "Are you sure you want to delete this?",
            QMessageBox.Yes|QMessageBox.No)

            if reply == QMessageBox.Yes:
                del self.assignments[selected_row]  # delets the item in the self.ass..list
                self.refresh_assignment_list()  # this will be added from the data available
                self.save_assignments()  # this helps to save it to the file
        else:
            QMessageBox.warning(self,"No Selection",
            "Please select an assignment to delete")


    def exit_(self):
        if self.exit_button:
            reply = QMessageBox.information(self,
            "exit","Are you sure you want to",
            QMessageBox.Yes|QMessageBox.No)

            if reply == QMessageBox.Yes:
                sys.exit()        

    # this reminder is manual as user opens the application
    def show_due_reminders(self):
        today = QDate.currentDate()
        due_today = []
        overdue = []

        for task in self.assignments:
            days_left = today.daysTo(task["due"])

            if days_left < 0:
                overdue.append(task["title"])
            elif days_left == 0:
                due_today.append(task["title"])

        message = ""
        if overdue:
            message += "Due Today:\n" + "\n".join(f"• {t}" for t in overdue)

        if due_today:
            message += "Due Today:\n" + "\n".join(f"• {t}" for t in due_today)


        if message:
            QMessageBox.information(self,"Assignment Reminder", message)


    
    def edit_assignment(self):
        selected_row = self.assignment_list.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self,"Warnning","Please selet an assignment to edit ")
            return

        # Loads selected assignmet details
        # just like reversing them, gettin salt out of a water
        task = self.assignments[selected_row]
        self.title_input.setText(task["title"])
        self.date_input.setDate(task["due"])

        # Remove the old task temporarly so it can be re-added
        del self.assignments[selected_row]
        self.assignment_list.takeItem(selected_row)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssignmentTracker()
    window.show()
    sys.exit(app.exec())