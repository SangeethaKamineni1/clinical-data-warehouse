CLINICAL DATA WAREHOUSE SYSTEM
==============================

Description:
------------
This is a Tkinter-based Clinical Data Warehouse System developed as part of a health informatics programming assignment. It is designed to allow clinicians, nurses, admins, and management users to interact with patient data using a clean graphical user interface (GUI). The system uses role-based access control and stores all data in CSV files.

Main File to Run:
-----------------
- The entry point for the application is: *main.py*
- To start the program, open your terminal or Python IDE inside the project folder and run:
  
    python main.py

Folder and File Structure:
--------------------------
Ensure all the following files are placed in the *same folder*:

1. *main.py*
   - Entry point of the application that launches the login screen.

2. *ui.py*
   - Contains the LoginWindow and dashboard classes for different user roles (Clinician/Nurse, Admin, Management).
   - UI interactions and logic.

3. *users.py*
   - Handles user authentication and role permissions using Credentials.csv.

4. *patients.py*
   - Contains Patient, Visit, Department, and NotesDatabase classes.
   - Manages patient and visit data and handles data persistence to CSV.

5. *stats.py*
   - Utility to load and preprocess patient data for visualization.

6. *log_usage.py*
   - Logs login attempts and system actions with timestamps to a file called usage_log.txt.


Data Files (Required):
----------------------
1. *Credentials.csv* - Stores username, password, and role for login.
2. *Patient_data.csv* - Stores all patient demographic and visit data.
3. *Notes.csv* - Stores patient clinical note data.
4. *summary_report.csv* (Generated when management exports statistics)

Requirements:
-------------
- Python 3.7 or above
- Libraries: pandas, matplotlib, tkinter (built-in)

Instructions:
-------------
1. Install required packages:
   pip install pandas matplotlib

2. Run the application:
   python main.py

3. Use the credentials in Credentials.csv to log in as:
   - Clinician or Nurse: Full access to patient data and notes
   - Admin: Count visits on specific dates
   - Management: View and export key statistics

Important Notes:
----------------
- Do not change file names or move files into subfolders.
- All changes to data (visits, new patients) are saved directly into CSV files.
- The system is designed to work on any machine without hardcoded paths (uses relative paths).