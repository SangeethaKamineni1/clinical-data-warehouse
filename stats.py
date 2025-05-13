# stats.py
import pandas as pd

def load_patient_data(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates=['Visit_time'], dayfirst=False)
        df['Visit_time'] = pd.to_datetime(df['Visit_time'], errors='coerce')
        return df.dropna(subset=['Visit_time'])
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def print_visit_trend(df):
    print("\n Monthly Visit Trends:")
    visit_counts = df['Visit_time'].dt.to_period('M').value_counts().sort_index()
    for period, count in visit_counts.items():
        print(f" - {period.strftime('%Y-%m')}: {count} visits")

def print_insurance_trend(df):
    print("\n Visits by Insurance Type:")
    insurance_counts = df['Insurance'].value_counts()
    for insurance, count in insurance_counts.items():
        print(f" - {insurance}: {count} visits")

def print_demographics(df):
    print("\n Demographics Breakdown:")

    print("\n  ▪ Gender Distribution:")
    for gender, count in df['Gender'].value_counts().items():
        print(f"    - {gender}: {count}")

    print("\n  ▪ Race Distribution:")
    for race, count in df['Race'].value_counts().items():
        print(f"    - {race}: {count}")

    print("\n  ▪ Age Groups:")
    bins = [0, 18, 35, 50, 65, 80, 100]
    labels = ['0-18', '19-35', '36-50', '51-65', '66-80', '81-100']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    for group, count in df['Age_Group'].value_counts().sort_index().items():
        print(f"    - {group}: {count}")

def generate_all_statistics(data_file_path):
    df = load_patient_data(data_file_path)
    if df.empty:
        print(" No valid data available for statistics.")
        return

    print_visit_trend(df)
    print_insurance_trend(df)
    print_demographics(df)
    print("\n Summary statistics displayed successfully.")
