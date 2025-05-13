import csv
import datetime
import os
import random
import pandas as pd

class Visit:
    def __init__(self, visit_id, visit_time, visit_department, chief_complaint, note_id, note_type):
        self.visit_id = visit_id
        if isinstance(visit_time, datetime.datetime):
            self.visit_time = visit_time
        else:
            try:
                self.visit_time = datetime.datetime.strptime(visit_time, '%Y-%m-%d')
            except ValueError:
                try:
                    self.visit_time = datetime.datetime.strptime(visit_time, '%m/%d/%Y')
                except ValueError:
                    raise ValueError(f"Invalid visit_time format: {visit_time}")

        self.visit_department = visit_department
        self.chief_complaint = chief_complaint
        self.note_id = note_id
        self.note_type = note_type

class Patient:
    def __init__(self, patient_id, gender, race, age, ethnicity, insurance, zip_code):
        self.patient_id = patient_id
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

class Department:
    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path
        self.patients = {}
        self.columns = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            print("File not found. Starting with empty department.")
            return

        with open(self.file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.columns = reader.fieldnames
            for row in reader:
                pid = str(row['Patient_ID'])
                try:
                    age = int(row['Age'])
                except ValueError:
                    age = 0

                if pid not in self.patients:
                    self.patients[pid] = Patient(
                        pid, row['Gender'], row['Race'], age,
                        row['Ethnicity'], row['Insurance'], row['Zip_code']
                    )

                visit = Visit(
                    row['Visit_ID'],
                    row['Visit_time'],
                    row['Visit_department'],
                    row.get('Chief_complaint', ''),
                    row.get('Note_ID', ''),
                    row.get('Note_type', '')
                )
                self.patients[pid].add_visit(visit)

    def save_data(self):
        fieldnames = ['Patient_ID', 'Visit_ID', 'Visit_time', 'Visit_department', 'Race',
                      'Gender', 'Ethnicity', 'Age', 'Zip_code', 'Insurance',
                      'Chief_complaint', 'Note_ID', 'Note_type']
        with open(self.file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for pid, patient in self.patients.items():
                for visit in patient.visits:
                    writer.writerow({
                        'Patient_ID': pid,
                        'Visit_ID': visit.visit_id,
                        'Visit_time': visit.visit_time.strftime('%Y-%m-%d'),
                        'Visit_department': visit.visit_department,
                        'Race': patient.race,
                        'Gender': patient.gender,
                        'Ethnicity': patient.ethnicity,
                        'Age': patient.age,
                        'Zip_code': patient.zip_code,
                        'Insurance': patient.insurance,
                        'Chief_complaint': visit.chief_complaint,
                        'Note_ID': visit.note_id,
                        'Note_type': visit.note_type
                    })

    def export_statistics_report(self, output_file):
        if not self.patients:
            return False

        import csv
        import datetime

        summary = []

        # Monthly Visits
        visits = []
        for patient in self.patients.values():
            for visit in patient.visits:
                visits.append(visit.visit_time.strftime("%Y-%m"))

        from collections import Counter
        monthly_counts = Counter(visits)
        summary.append(["Monthly Visit Summary"])
        summary.append(["Month", "Number of Visits"])
        for month, count in sorted(monthly_counts.items()):
            summary.append([month, count])
        summary.append([])

        # Insurance Distribution
        ins_counts = Counter([p.insurance for p in self.patients.values()])
        summary.append(["Insurance Distribution"])
        summary.append(["Insurance", "Count"])
        for insurance, count in ins_counts.items():
            summary.append([insurance, count])
        summary.append([])

        # Save summary to CSV
        try:
            with open(output_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(summary)
            return True
        except Exception:
            return False

    def add_visit_from_ui(self, patient_id, visit_time_str, visit_dept, chief_complaint):
        import tkinter as tk
        from tkinter import simpledialog, messagebox

        try:
            visit_time = datetime.datetime.strptime(visit_time_str, "%Y-%m-%d")
        except ValueError:
            return False

        if patient_id not in self.patients:
            # Use popup dialogs to ask for required fields
            root = tk.Tk()
            root.withdraw()  # Hide the root window

            gender = simpledialog.askstring("Input", f"Enter gender for new patient {patient_id}:", parent=root)
            race = simpledialog.askstring("Input", f"Enter race for new patient {patient_id}:", parent=root)
            try:
                age = int(simpledialog.askstring("Input", f"Enter age for new patient {patient_id}:", parent=root))
            except (TypeError, ValueError):
                age = 0
            ethnicity = simpledialog.askstring("Input", f"Enter ethnicity for new patient {patient_id}:", parent=root)
            insurance = simpledialog.askstring("Input", f"Enter insurance for new patient {patient_id}:", parent=root)
            zip_code = simpledialog.askstring("Input", f"Enter zip code for new patient {patient_id}:", parent=root)

            self.patients[patient_id] = Patient(
                patient_id,
                gender or "Unknown",
                race or "Unknown",
                age,
                ethnicity or "Unknown",
                insurance or "Unknown",
                zip_code or "00000"
            )

        visit_id = f"V{len(self.patients[patient_id].visits) + 1:03d}"
        note_id = str(random.randint(100000, 999999))
        note_type = simpledialog.askstring("Input", f"Enter note type for this visit (e.g., Discharge, Progress, Admission):", parent=root) or "Unspecified"
        root.destroy()

        visit = Visit(visit_id, visit_time, visit_dept, chief_complaint, note_id, note_type)
        self.patients[patient_id].add_visit(visit)
        self.save_data()
        messagebox.showinfo("Success", f"Patient {patient_id} and visit saved to CSV successfully.")
        return True

    def retrieve_patient(self, patient_id, output_file):
        if patient_id not in self.patients:
            print("Patient not found.")
            return
        fieldnames = ['Patient_ID', 'Visit_ID', 'Visit_time', 'Visit_department', 'Race',
                      'Gender', 'Ethnicity', 'Age', 'Zip_code', 'Insurance',
                      'Chief_complaint', 'Note_ID', 'Note_type']
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            patient = self.patients[patient_id]
            for visit in patient.visits:
                writer.writerow({
                    'Patient_ID': patient.patient_id,
                    'Visit_ID': visit.visit_id,
                    'Visit_time': visit.visit_time.strftime('%Y-%m-%d'),
                    'Visit_department': visit.visit_department,
                    'Race': patient.race,
                    'Gender': patient.gender,
                    'Ethnicity': patient.ethnicity,
                    'Age': patient.age,
                    'Zip_code': patient.zip_code,
                    'Insurance': patient.insurance,
                    'Chief_complaint': visit.chief_complaint,
                    'Note_ID': visit.note_id,
                    'Note_type': visit.note_type
                })
        print(f"Patient data saved to {output_file}")

    def add_visit(self, patient_id):
        print("\nPlease enter the following visit details:")
        department = input("Department: ")
        complaint = input("Chief Complaint: ")
        gender = input("Gender: ")
        race = input("Race: ")
        ethnicity = input("Ethnicity: ")
        try:
            age = int(input("Age: "))
        except ValueError:
            age = 0
        zip_code = input("Zip Code: ")
        insurance = input("Insurance: ")
        note_type = input("Note Type (e.g., Discharge, Progress, Admission): ")
        note_id = str(random.randint(100000, 999999))
        visit_id = str(random.randint(100000, 999999))
        visit_time = datetime.datetime.now()

        if patient_id not in self.patients:
            self.patients[patient_id] = Patient(
                patient_id, gender, race, age, ethnicity, insurance, zip_code
            )
        else:
            patient = self.patients[patient_id]
            patient.gender = gender
            patient.race = race
            patient.age = age
            patient.ethnicity = ethnicity
            patient.zip_code = zip_code
            patient.insurance = insurance

        visit = Visit(visit_id, visit_time, department, complaint, note_id, note_type)
        self.patients[patient_id].add_visit(visit)
        self.save_data()
        print("New patient visit added successfully.")

    def remove_patient(self, patient_id):
        if patient_id not in self.patients:
            print("Patient not found.")
            return
        del self.patients[patient_id]
        self.save_data()
        print(f"Patient ID {patient_id} removed successfully.")

    def review_visits(self, date_str):
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            count = 0
            for patient in self.patients.values():
                for visit in patient.visits:
                    if visit.visit_time.date() == date_obj:
                        count += 1
            print(f"Total visits on {date_str}: {count}")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

class Note:
    def __init__(self, patient_id, visit_id, note_id, note_text):
        self.patient_id = str(patient_id)
        self.visit_id = str(visit_id)
        self.note_id = str(note_id)
        self.note_text = note_text

class NotesDatabase:
    def __init__(self, notes_file_path):
        self.notes_file_path = notes_file_path
        self.notes = []
        self.load_notes()

    def load_notes(self):
        with open(self.notes_file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                note = Note(
                    row['Patient_ID'],
                    row['Visit_ID'],
                    row['Note_ID'],
                    row['Note_text']
                )
                self.notes.append(note)

    def get_notes_by_patient_and_date(self, patient_id, visit_date, patient_data):
        try:
            visit_date_obj = datetime.datetime.strptime(visit_date, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return []

        notes_found = []
        if patient_id not in patient_data.patients:
            print("Patient not found.")
            return []

        for visit in patient_data.patients[patient_id].visits:
            if visit.visit_time.date() == visit_date_obj:
                for note in self.notes:
                    if note.visit_id == visit.visit_id and note.patient_id == patient_id:
                        notes_found.append(note)

        return notes_found
