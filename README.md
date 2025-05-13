# Clinical Data Warehouse System

A Tkinter-based Clinical Data Warehouse System for managing patient data, clinical visits, and notes using role-based access control. Developed as part of a health informatics programming assignment.

---

## 🚀 Features
-  Login system with authentication using Credentials.csv
-  Clinician/Nurse dashboard:
- Add patient visits with dynamic prompts
- Retrieve latest patient data
-  Count daily visits
- View clinical notes
-  Admin dashboard:
- Review total visits on a given date
-  Management dashboard:
 - Generate monthly visit trends and demographic breakdowns
 - Export summary statistics to CSV
-  Data Persistence using CSV files

## Project Structure

ClinicalDataWarehouse/
│
├── main.py # Entry point to launch the application
├── ui.py # All UI components and role-based dashboards
├── users.py # Handles login authentication and permissions
├── patients.py # Manages patient, visit, and notes data models
├── stats.py # Utilities for statistical data aggregation
├── log_usage.py # Logs system usage to usage_log.txt
│
├── Credentials.csv # Stores usernames, passwords, and roles
├── Patient_data.csv # Stores patient demographics and visit records
├── Notes.csv # Stores visit-specific note text
├── summary_report.csv # Auto-generated file when stats are exported
│
└── README.md # Project documentation and instructions

## 📁 Folder & File Structure

Place *all the following files in a single folder*, e.g., ClinicalDataWarehouse/
## 💻 Setup Instructions

1. *Install Python 3.7 or above*
   - Download from [https://www.python.org/downloads](https://www.python.org/downloads)

2. *Install Required Libraries*
Run the following in Terminal or Command Prompt:
- pip install matplotlib

3. Run the main python file -
   - Python main.py : launches the interface

## Role-Based Access

Role	Capabilities
Clinician	Add visits, retrieve patient data, count visits, view notes
Nurse	Same as clinician
Admin	Count and review patient visits by date
Management	Generate and visualize key statistics; export report

Login credentials must be added to the Credentials.csv file before use.

📌** Notes**
All actions (login, visit add/remove, statistics access) are logged to usage_log.txt

New patient visits are saved directly to Patient_data.csv after data entry

Note content for a given patient and date is matched against entries in Notes.csv

Summary report is generated as summary_report.csv upon management export


