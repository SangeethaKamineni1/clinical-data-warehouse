import tkinter as tk
from ui import LoginWindow, ClinicianDashboard, AdminDashboard, ManagementDashboard

def on_login_success(user):
    print(f" Logged in as: {user.username} ({user.role})")

    if user.role in ['clinician', 'nurse']:
        ClinicianDashboard(user)
    elif user.role == 'admin':
        AdminDashboard(user)
    elif user.role == 'management':
        ManagementDashboard(user)
    else:
        print("Unknown role. No dashboard available.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root, on_login_success)
    root.mainloop()
