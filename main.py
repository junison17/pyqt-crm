import sys
import sqlite3
import hashlib
import re
from PyQt5.QtWidgets import (QApplication, QWidget,QMessageBox, QVBoxLayout,QTableWidget,QTableWidgetItem, QPushButton, QTextEdit, QLineEdit, QTableWidget, QCalendarWidget, QMessageBox)
from PyQt5.QtCore import Qt

class PatientApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the database
        self.init_db()

        # Initialize the UI
        self.init_ui()

    def init_db(self):
        # Create a connection to sqlite3 database
        self.conn = sqlite3.connect('patients.db')
        cursor = self.conn.cursor()
        # Create the patients table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                date TEXT,
                chart_number INTEGER,
                name TEXT,
                ssn TEXT,
                address TEXT,
                phone TEXT
            )
        ''') 

    def save_data(self):
        # Get the values from the input fields
        chart_number = self.chart_number_edit.text()
        name = self.name_edit.text()
        ssn = self.ssn_edit.text()
        address = self.address_edit.text()
        phone = self.phone_edit.text()
        date = self.calendar.selectedDate().toString(Qt.ISODate)

        # Validate the input fields

        # Validate SSN and Phone format
        if not self.validate_ssn(ssn):
            QMessageBox.warning(self, "Invalid SSN", "Please enter a valid 13-digit SSN without '-'")
            return
        if not self.validate_phone(phone):
            QMessageBox.warning(self, "Invalid Phone", "Please enter a valid 11-digit phone number without '-'")
            return
        if not chart_number or not name or not ssn or not address or not phone:
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return

        if not re.match(r'^\d{13}$', ssn):
            QMessageBox.warning(self, "Warning", "Invalid Resident Registration Number.")
            return

        if not re.match(r'^\d{11}$', phone):
            QMessageBox.warning(self, "Warning", "Invalid phone number.")
            return

        # Hash the ssn
        hashed_ssn = hashlib.sha256(ssn.encode()).hexdigest()

        # Insert the data into the database
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?)', (date, chart_number, name, hashed_ssn, address, phone))

        # Commit the changes
        self.conn.commit()


# Show a success message
        self.QMessageBox.information( "Success", "Data saved successfully.")
  

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Patient Data Management')
        self.resize(3000, 2500)  # Making window 100% larger

        layout = QVBoxLayout()

        # Add input fields for patient details
        self.chart_number_edit = QLineEdit(self)
        self.chart_number_edit.setPlaceholderText("Patient Chart Number")
        layout.addWidget(self.chart_number_edit)

        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("Name")
        layout.addWidget(self.name_edit)

        self.ssn_edit = QLineEdit(self)
        self.ssn_edit.setPlaceholderText("Resident Registration Number")
        layout.addWidget(self.ssn_edit)

        self.address_edit = QLineEdit(self)
        self.address_edit.setPlaceholderText("Address")
        layout.addWidget(self.address_edit)

        self.phone_edit = QLineEdit(self)
        self.phone_edit.setPlaceholderText("Phone Number")
        layout.addWidget(self.phone_edit)

        # Add buttons
        self.save_btn = QPushButton("Save", self)
        self.save_btn.clicked.connect(self.save_data)
        layout.addWidget(self.save_btn)

        self.view_btn = QPushButton("Inquiry", self)
        self.view_btn.clicked.connect(self.view_data)
        layout.addWidget(self.view_btn)

        self.delete_btn = QPushButton("Delete", self)
        self.delete_btn.clicked.connect(self.delete_data)
        layout.addWidget(self.delete_btn)

        # Add calendar
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        # Add Text Area for displaying data
        self.details_area = QTextEdit(self)
        layout.addWidget(self.details_area)

        # Add table to display all patient data
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Date", "Chart Number", "Name", "SSN", "Address", "Phone"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def view_data(self):
        chart_number = self.chart_number_edit.text()
        ssn = self.ssn_edit.text()
        name = self.name_edit.text()

        cursor = self.conn.cursor()

        if not any([chart_number, ssn, name]):
            # Fetch all records in ascending order by date
            query = "SELECT * FROM patients ORDER BY date ASC"
            cursor.execute(query)
        else:
            query = "SELECT * FROM patients WHERE chart_number=? OR ssn=? OR name=?"
            cursor.execute(query, (chart_number, ssn, name))

        data = cursor.fetchall()

        if not data:
            QMessageBox.warning(self, 'Error', 'No matching data found.')
            return

        # Displaying data in the text area
        result_text = ""
        for entry in data:
            result_text += f"Date: {entry[0]}, Chart Number: {entry[1]}, Name: {entry[2]}, SSN: {entry[3]}, Address: {entry[4]}, Phone: {entry[5]}"

        self.details_area.setText(result_text)

    def delete_data(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, 'Error', 'Please select a row from the table to delete.')
            return

        chart_number = self.table.item(current_row, 1).text()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM patients WHERE chart_number=?", (chart_number,))
        self.conn.commit()

        QMessageBox.information(self, 'Info', 'Data Deleted Successfully!')
        self.populate_table()

    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCalendarWidget, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PatientApp()
    window.show()
    sys.exit(app.exec_())


