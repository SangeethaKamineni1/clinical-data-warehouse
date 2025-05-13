import csv

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def can_add_patient(self):
        return self.role in ['clinician', 'nurse']

    def can_remove_patient(self):
        return self.role in ['clinician', 'nurse']

    def can_retrieve_patient(self):
        return self.role in ['clinician', 'nurse']

    def can_view_note(self):
        return self.role in ['clinician', 'nurse']

    def can_count_visits(self):
        return self.role in ['clinician', 'nurse', 'admin']

    def can_generate_statistics(self):
        return self.role == 'management'

    def is_admin(self):
        return self.role == 'admin'


def authenticate_user(credentials_file, input_username, input_password):
    input_username = input_username.strip()
    input_password = input_password.strip()

    try:
        with open(credentials_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                file_username = row['username'].strip()
                file_password = row['password'].strip()
                file_role = row['role'].strip()

                print(f"[DEBUG] Comparing: {file_username} == {input_username} and {file_password} == {input_password}")

                if file_username == input_username and file_password == input_password:
                    print(f" Login successful. Role: {file_role}")
                    return User(file_username, file_role)

    except FileNotFoundError:
        print("Credentials file not found.")
    except Exception as e:
        print(f"Error reading credentials file: {e}")

    print("Invalid credentials. Access denied.")
    return None



