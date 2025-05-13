import tkinter as tk
from tkinter import messagebox, font
from users import authenticate_user
from log_usage import log_event
from patients import Department, NotesDatabase
from stats import load_patient_data
import datetime
import pandas as pd
import matplotlib.pyplot as plt

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Clinical Data Warehouse Login")
        self.root.geometry("500x350")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(False, False)

        self.custom_font = font.Font(family="Helvetica", size=12)

        self.frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=250)

        tk.Label(self.frame, text="Secure Login", font=("Helvetica", 16, "bold"), bg="white").pack(pady=(20, 10))

        tk.Label(self.frame, text="Username", font=self.custom_font, bg="white").pack(anchor="w", padx=20)
        self.username_entry = tk.Entry(self.frame, font=self.custom_font)
        self.username_entry.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(self.frame, text="Password", font=self.custom_font, bg="white").pack(anchor="w", padx=20)
        self.password_entry = tk.Entry(self.frame, show="*", font=self.custom_font)
        self.password_entry.pack(fill="x", padx=20, pady=(0, 20))

        self.login_btn = tk.Button(self.frame, text="Login", font=self.custom_font, bg="#4CAF50", fg="white",
                                   command=self.login)
        self.login_btn.pack(pady=(0, 10))

        self.root.bind('<Return>', lambda event: self.login())
        self.on_login_success = on_login_success

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        user = authenticate_user("Credentials.csv", username, password)
        if user:
            log_event(username, user.role, "Login Success")
            self.root.destroy()
            self.on_login_success(user)
        else:
            log_event(username, "Unknown", "Login Failed")
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")


class ClinicianDashboard:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title(f"{user.role.capitalize()} Dashboard - Welcome {user.username}")
        self.root.geometry("600x400")
        self.root.configure(bg="#f9f9f9")

        self.department = Department("General", "Patient_data.csv")
        self.notes_db = NotesDatabase("Notes.csv")

        tk.Label(self.root, text="Clinician Dashboard", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=20)
        btn_frame = tk.Frame(self.root, bg="#f9f9f9")
        btn_frame.pack(pady=10)

        actions = [
            ("Retrieve Patient", self.retrieve_patient),
            ("Add Patient Visit", self.add_patient_visit),
            ("Remove Patient", self.remove_patient),
            ("Count Visits", self.count_visits),
            ("View Note", self.view_note),
            ("Exit", self.root.destroy)
        ]

        for text, command in actions:
            tk.Button(btn_frame, text=text, width=25, font=("Helvetica", 12), command=command).pack(pady=5)

        self.root.mainloop()

    def add_patient_visit(self):
        def submit():
            patient_id = entry_id.get().strip()
            visit_time = entry_time.get().strip()
            visit_dept = entry_dept.get().strip()
            complaint = entry_complaint.get().strip()

            if not all([patient_id, visit_time, visit_dept, complaint]):
                messagebox.showerror("Error", "All fields are required.")
                return

            success = self.department.add_visit_from_ui(patient_id, visit_time, visit_dept, complaint)
            if success:
                log_event(self.user.username, self.user.role, f"Added visit for {patient_id}")
                messagebox.showinfo("Success", f"Visit for patient {patient_id} added.")
                top.destroy()
            else:
                messagebox.showerror("Error", "Failed to add visit. Patient may not exist.")

        top = tk.Toplevel(self.root)
        top.title("Add Patient Visit")
        top.geometry("400x300")

        tk.Label(top, text="Patient ID:").pack(pady=5)
        entry_id = tk.Entry(top)
        entry_id.pack(pady=5)

        tk.Label(top, text="Visit Time (YYYY-MM-DD):").pack(pady=5)
        entry_time = tk.Entry(top)
        entry_time.pack(pady=5)

        tk.Label(top, text="Visit Department:").pack(pady=5)
        entry_dept = tk.Entry(top)
        entry_dept.pack(pady=5)

        tk.Label(top, text="Chief Complaint:").pack(pady=5)
        entry_complaint = tk.Entry(top)
        entry_complaint.pack(pady=5)

        tk.Button(top, text="Submit", command=submit).pack(pady=15)

    def retrieve_patient(self):
        patient_id = self.simple_prompt("Retrieve Patient", "Enter Patient ID:")
        if not patient_id:
            return
        output = []
        if patient_id in self.department.patients:
            patient = self.department.patients[patient_id]
            if patient.visits:
                latest_visit = sorted(patient.visits, key=lambda v: v.visit_time)[-1]
                output = [
                    f"Patient ID: {patient.patient_id}",
                    f"Gender: {patient.gender}",
                    f"Race: {patient.race}",
                    f"Age: {patient.age}",
                    f"Ethnicity: {patient.ethnicity}",
                    f"Insurance: {patient.insurance}",
                    f"Zip Code: {patient.zip_code}",
                    f"Visit ID: {latest_visit.visit_id}",
                    f"Visit Time: {latest_visit.visit_time}",
                    f"Department: {latest_visit.visit_department}",
                    f"Chief Complaint: {latest_visit.chief_complaint}"
                ]
                messagebox.showinfo("Latest Visit Info", "\n".join(output))
            else:
                messagebox.showinfo("Info", "No visits found for this patient.")
        else:
            messagebox.showerror("Error", "Patient not found.")

    def remove_patient(self):
        patient_id = self.simple_prompt("Remove Patient", "Enter Patient ID:")
        if patient_id:
            self.department.remove_patient(patient_id)
            log_event(self.user.username, self.user.role, f"Removed patient {patient_id}")

    def count_visits(self):
        date = self.simple_prompt("Count Visits", "Enter date (YYYY-MM-DD):")
        if date:
            self.department.review_visits(date)
            log_event(self.user.username, self.user.role, f"Counted visits on {date}")

    def view_note(self):
        pid = self.simple_prompt("View Note", "Enter Patient ID:")
        date = self.simple_prompt("View Note", "Enter Visit Date (YYYY-MM-DD):")
        if pid and date:
            notes = self.notes_db.get_notes_by_patient_and_date(pid, date, self.department)
            if notes:
                content = "\n\n".join([f"Note ID: {n.note_id}\nText: {n.note_text}" for n in notes])
                messagebox.showinfo("Notes", content)
            else:
                messagebox.showinfo("No Notes", "No notes found for given date.")

    def simple_prompt(self, title, prompt):
        prompt_win = tk.Toplevel(self.root)
        prompt_win.title(title)
        prompt_win.geometry("350x150")
        tk.Label(prompt_win, text=prompt, font=("Helvetica", 12)).pack(pady=10)
        entry = tk.Entry(prompt_win, font=("Helvetica", 12))
        entry.pack(pady=5)

        result = []

        def submit():
            result.append(entry.get().strip())
            prompt_win.destroy()

        tk.Button(prompt_win, text="Submit", command=submit).pack(pady=10)
        self.root.wait_window(prompt_win)
        return result[0] if result else None

class AdminDashboard:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title(f"Admin Dashboard - {user.username}")
        self.root.geometry("400x250")
        self.root.configure(bg="#f2f2f2")

        self.department = Department("General", "Patient_data.csv")

        tk.Label(self.root, text="Admin Dashboard", font=("Helvetica", 16, "bold"), bg="#f2f2f2").pack(pady=20)
        tk.Button(self.root, text="Count Visits on Date", font=("Helvetica", 12),
                  command=self.count_visits).pack(pady=10)

        tk.Button(self.root, text="Exit", font=("Helvetica", 12), command=self.root.destroy).pack(pady=10)

        self.root.mainloop()

    def count_visits(self):
        date_input = self.simple_prompt("Count Visits", "Enter Date (YYYY-MM-DD):")
        if not date_input:
            return
        try:
            parsed_date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return

        count = 0
        for patient in self.department.patients.values():
            for visit in patient.visits:
                visit_date = visit.visit_time.date() if hasattr(visit.visit_time, 'date') else visit.visit_time
                if isinstance(visit_date, str):
                    try:
                        visit_date = datetime.datetime.strptime(visit_date, "%m/%d/%Y").date()
                    except ValueError:
                        try:
                            visit_date = datetime.datetime.strptime(visit_date, "%Y-%m-%d").date()
                        except ValueError:
                            continue
                if visit_date == parsed_date:
                    count += 1

        log_event(self.user.username, self.user.role, f"Counted visits on {date_input}")
        messagebox.showinfo("Visit Count", f"Total visits on {date_input}: {count}")

    def simple_prompt(self, title, prompt):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("350x150")
        tk.Label(win, text=prompt, font=("Helvetica", 12)).pack(pady=10)
        entry = tk.Entry(win, font=("Helvetica", 12))
        entry.pack(pady=5)

        result = []

        def submit():
            result.append(entry.get().strip())
            win.destroy()

        tk.Button(win, text="Submit", command=submit).pack(pady=10)
        self.root.wait_window(win)
        return result[0] if result else None


class ManagementDashboard:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title(f"Management Dashboard - {user.username}")
        self.root.geometry("400x250")
        self.root.configure(bg="#e9f0f4")

        tk.Label(self.root, text="Management Dashboard", font=("Helvetica", 16, "bold"), bg="#e9f0f4").pack(pady=20)

        tk.Button(self.root, text="Generate Key Statistics", font=("Helvetica", 12),
                  command=self.show_statistics).pack(pady=10)
        tk.Button(self.root, text="Export Statistics Summary", font=("Helvetica", 12),
                  command=self.export_summary).pack(pady=10)

        tk.Button(self.root, text="Exit", font=("Helvetica", 12), command=self.root.destroy).pack(pady=10)

        self.root.mainloop()

    def show_statistics(self):
        df = load_patient_data("Patient_data.csv")
        if df.empty:
            messagebox.showerror("Error", "No data available to generate statistics.")
            return

        df['Month_Year'] = df['Visit_time'].dt.to_period('M')
        monthly_visits = df.groupby('Month_Year').size().sort_index()

        monthly_visits = monthly_visits[-12:]

        plt.figure(figsize=(10, 5))
        monthly_visits.plot(kind='bar', color='steelblue', width=0.6)
        plt.title('Monthly Visit Trends (Last 12 Months)')
        plt.xlabel('Month')
        plt.ylabel('Number of Visits')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        plt.show()

        # Insurance Distribution
        plt.figure(figsize=(6, 4))
        df['Insurance'].value_counts().plot(kind='bar', color='skyblue')
        plt.title('Visits by Insurance Type')
        plt.xlabel('Insurance')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()

        # Gender Distribution
        plt.figure(figsize=(6, 4))
        df['Gender'].value_counts().plot(kind='bar', color='salmon')
        plt.title('Gender Distribution')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()

        # Race Distribution
        plt.figure(figsize=(6, 4))
        df['Race'].value_counts().plot(kind='bar', color='orange')
        plt.title('Race Distribution')
        plt.xlabel('Race')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()

        # Age Group Distribution
        bins = [0, 18, 35, 50, 65, 80, 100]
        labels = ['0-18', '19-35', '36-50', '51-65', '66-80', '81-100']
        df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
        plt.figure(figsize=(6, 4))
        df['Age_Group'].value_counts().sort_index().plot(kind='bar', color='green')
        plt.title('Age Group Distribution')
        plt.xlabel('Age Group')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()

        log_event(self.user.username, self.user.role, "Generated key statistics")

    def export_summary(self):
        dept = Department("General", "Patient_data.csv")
        success = dept.export_statistics_report("summary_report.csv")
        if success:
            messagebox.showinfo("Exported", "Summary statistics exported to 'summary_report.csv'")
        else:
            messagebox.showwarning("No Data", "No records found to export.")


