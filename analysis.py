import pandas as pd
import pyodbc
import sqlalchemy as sal
from sqlalchemy import text
from sqlalchemy import create_engine
import logging
import os
import time
from datetime import datetime

engine = sal.create_engine(r'mssql://ABHISHEK\SQLEXPRESS/Hospital_db?driver=ODBC+DRIVER+17+FOR+SQL+SERVER')
conn=engine.connect()

query = "SELECT * FROM patients"
patients_df = pd.read_sql(query, engine)

query = "SELECT * FROM appointment"
appointment_df = pd.read_sql(query, engine)

query = "SELECT * FROM doctors"
doctors_df = pd.read_sql(query, engine)

query = "SELECT * FROM billing"
billing_df = pd.read_sql(query, engine)

query = "SELECT * FROM treatments"
treatments_df = pd.read_sql(query, engine)

def get_filtered_data(department=None):

    # If no department is selected, return original data
    if department is None:
        return {
            "patients": patients_df,
            "appointments": appointment_df,
            "doctors": doctors_df,
            "treatments": treatments_df,
            "billing": billing_df
        }

    # Filter doctors
    doctors = doctors_df[
        doctors_df["specialization"] == department
    ]

    # Filter appointments
    appointments = appointment_df[
        appointment_df["doctor_id"].isin(doctors["doctor_id"])
    ]

    # Filter patients
    patients = patients_df[
        patients_df["patient_id"].isin(appointments["patient_id"])
    ]

    # Filter treatments
    treatments = treatments_df[
        treatments_df["appointment_id"].isin(
            appointments["appointment_id"]
        )
    ]

    # Filter billing
    billing = billing_df[
        billing_df["patient_id"].isin(patients["patient_id"])
    ]

    return {
        "patients": patients,
        "appointments": appointments,
        "doctors": doctors,
        "treatments": treatments,
        "billing": billing
    }


def get_total_patients(department=None):
    data = get_filtered_data(department)
    return len(data["patients"])
def get_total_doctors(department=None):
    if department is None:
        return len(doctors_df)
    return len(
        doctors_df[
            doctors_df["specialization"] == department
        ]
    )
def get_total_appointments(department=None):
    if department is None:
        return len(appointment_df)
    doctor_ids = doctors_df[
        doctors_df["specialization"] == department
    ]["doctor_id"]
    filtered_appointments = appointment_df[
        appointment_df["doctor_id"].isin(doctor_ids)
    ]
    return len(filtered_appointments)
def get_total_treatments(department=None):
    completed = appointment_df[
        appointment_df["status"] == "Completed"
    ]
    if department is not None:
        doctor_ids = doctors_df[
            doctors_df["specialization"] == department
        ]["doctor_id"]
        completed = completed[
            completed["doctor_id"].isin(doctor_ids)
        ]
    return treatments_df[
        treatments_df["appointment_id"].isin(
            completed["appointment_id"]
        )
    ].shape[0]
def get_total_revenue(department=None):
    paid_bills = billing_df[
        billing_df["payment_status"] == "Paid"
    ]
    if department is None:
        return paid_bills["amount"].sum()
    # Doctors of selected department
    doctor_ids = doctors_df[
        doctors_df["specialization"] == department
    ]["doctor_id"]
    # Appointments of those doctors
    appointment_ids = appointment_df[
        appointment_df["doctor_id"].isin(doctor_ids)
    ]["appointment_id"]
    # Treatments from those appointments
    treatment_ids = treatments_df[
        treatments_df["appointment_id"].isin(appointment_ids)
    ]["treatment_id"]
    # Revenue from those treatments
    filtered_bills = paid_bills[
        paid_bills["treatment_id"].isin(treatment_ids)
    ]
    return filtered_bills["amount"].sum()
def get_average_bill(department=None):
    paid_bills = billing_df[
        billing_df["payment_status"] == "Paid"
    ]
    if department is None:
        return paid_bills["amount"].mean()
    # Doctors of selected department
    doctor_ids = doctors_df[
        doctors_df["specialization"] == department
    ]["doctor_id"]
    # Appointments of those doctors
    appointment_ids = appointment_df[
        appointment_df["doctor_id"].isin(doctor_ids)
    ]["appointment_id"]
    # Treatments from those appointments
    treatment_ids = treatments_df[
        treatments_df["appointment_id"].isin(appointment_ids)
    ]["treatment_id"]
    # Bills for those treatments
    filtered_bills = paid_bills[
        paid_bills["treatment_id"].isin(treatment_ids)
    ]
    return filtered_bills["amount"].mean()
def get_data():
    return (
        patients_df,
        appointment_df,
        doctors_df,
        billing_df,
        treatments_df
    )
def get_revenue_trend(department=None):
    revenue = billing_df[
        billing_df["payment_status"] == "Paid"
    ].copy()
    if department is not None:
        # Doctors of selected department
        doctor_ids = doctors_df[
            doctors_df["specialization"] == department
        ]["doctor_id"]
        # Appointments of those doctors
        appointment_ids = appointment_df[
            appointment_df["doctor_id"].isin(doctor_ids)
        ]["appointment_id"]
        # Treatments of those appointments
        treatment_ids = treatments_df[
            treatments_df["appointment_id"].isin(appointment_ids)
        ]["treatment_id"]
        # Filter billing
        revenue = revenue[
            revenue["treatment_id"].isin(treatment_ids)
        ]
    revenue["Month"] = (
        revenue["bill_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )
    revenue = (
        revenue.groupby("Month")["amount"]
        .sum()
        .reset_index()
    )
    return revenue
def get_top_doctors(department=None):
    completed = appointment_df[
        appointment_df["status"] == "Completed"
    ]
    if department is not None:
        doctor_ids = doctors_df[
            doctors_df["specialization"] == department
        ]["doctor_id"]
        completed = completed[
            completed["doctor_id"].isin(doctor_ids)
        ]
    merged = completed.merge(
        treatments_df,
        on="appointment_id"
    )
    merged = merged.merge(
        doctors_df,
        on="doctor_id"
    )
    merged["Doctor"] = (
        merged["first_name"] + " " + merged["last_name"]
    )
    top_doctors = (
        merged.groupby(
            [
                "Doctor",
                "years_experience",
                "specialization",
                "hospital_branch"
            ]
        )
        .size()
        .reset_index(name="Successful Treatments")
        .sort_values(
            "Successful Treatments",
            ascending=False
        )
        .head(5)
    )
    return top_doctors
def get_treatment_distribution(department=None):
    treatments = treatments_df.copy()
    if department is not None:
        doctor_ids = doctors_df[
            doctors_df["specialization"] == department
        ]["doctor_id"]
        appointment_ids = appointment_df[
            appointment_df["doctor_id"].isin(doctor_ids)
        ]["appointment_id"]
        treatments = treatments[
            treatments["appointment_id"].isin(appointment_ids)
        ]
    return (
        treatments.groupby("treatment_type")
        .size()
        .reset_index(name="Treatment Count")
        .sort_values("Treatment Count", ascending=False)
    )
def get_appointment_trend(department=None):
    appointments = appointment_df.copy()
    if department is not None:
        doctor_ids = doctors_df[
            doctors_df["specialization"] == department
        ]["doctor_id"]
        appointments = appointments[
            appointments["doctor_id"].isin(doctor_ids)
        ]
    appointments["Month"] = (
        appointments["appointment_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )
    appointments = (
        appointments.groupby("Month")
        .size()
        .reset_index(name="Appointments")
    )
    return appointments
def get_departments():

    query = """
    SELECT DISTINCT specialization
    FROM doctors
    ORDER BY specialization
    """

    df = pd.read_sql(query, conn)

    return df["specialization"].tolist()
def get_total_valid_appointments():

    return appointment_df[
        appointment_df["status"].isin(
            ["Scheduled", "Completed"]
        )
    ].shape[0]
def get_doctors_by_specialization():

    return (
        doctors_df
        .groupby("specialization")
        .size()
        .reset_index(name="Doctors")
        .sort_values("Doctors", ascending=False)
    )
def get_doctors_by_branch():

    return (
        doctors_df
        .groupby("hospital_branch")
        .size()
        .reset_index(name="Doctors")
        .sort_values("Doctors", ascending=False)
    )
def get_experience_distribution():
    df = doctors_df.copy()
    df["Experience Group"] = pd.cut(
        df["years_experience"],
        bins=[0, 10, 20, 25, 30],
        labels=[
            "0-10 Years",
            "11-20 Years",
            "21-25 Years",
            "26-30 Years"
        ],
        include_lowest=True
    )
    experience_df = (
        df.groupby("Experience Group")
        .size()
        .reset_index(name="Doctors")
    )
    return experience_df
def get_patient_visits_by_reason(department=None):

    data = get_filtered_data(department)

    appointments = data["appointments"]

    df = appointments[
        appointments["status"].isin(
            ["Scheduled", "Completed"]
        )
    ]

    return (
        df.groupby("reason_for_visit")
        .size()
        .reset_index(name="Visits")
        .sort_values("Visits", ascending=False)
    )
def get_appointments_by_doctor():
    df = appointment_df[
        appointment_df["status"].isin(
            ["Scheduled", "Completed"]
        )
    ]
    df = df.merge(
        doctors_df[
            ["doctor_id", "first_name", "last_name"]
        ],
        on="doctor_id"
    )
    df["Doctor"] = (
        df["first_name"] + " " + df["last_name"]
    )
    return (
        df.groupby("Doctor")
        .size()
        .reset_index(name="Appointments")
        .sort_values(
            "Appointments",
            ascending=False
        )
        .head(5)
    )
def get_doctor_performance():
    appointments = (
        appointment_df[
            appointment_df["status"].isin(
                ["Scheduled", "Completed"]
            )
        ]
        .groupby("doctor_id")
        .size()
        .reset_index(name="Appointments")
    )
    treatments = (
        appointment_df[
            appointment_df["status"] == "Completed"
        ][["appointment_id", "doctor_id"]]
        .merge(
            treatments_df,
            on="appointment_id"
        )
        .groupby("doctor_id")
        .size()
        .reset_index(name="Successful Treatments")
    )
    df = doctors_df.merge(
        appointments,
        on="doctor_id",
        how="left"
    )
    df = df.merge(
        treatments,
        on="doctor_id",
        how="left"
    )
    df = df.fillna(0)
    df["Doctor"] = (
        df["first_name"] + " " + df["last_name"]
    )
    return df[
    [
        "Doctor",
        "specialization",
        "years_experience",
        "hospital_branch",
        "Appointments",
        "Successful Treatments",
        "phone_number"
    ]
].rename(
    columns={
        "specialization": "Specialization",
        "years_experience": "Experience",
        "hospital_branch": "Branch",
        "phone_number": "Phone Number"
    }
)
def get_patients_by_gender_age(department=None):

    data = get_filtered_data(department)

    patients = data["patients"].copy()

    patients["date_of_birth"] = pd.to_datetime(
        patients["date_of_birth"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    today = pd.Timestamp.today()

    patients["Age"] = (
        today.year
        - patients["date_of_birth"].dt.year
        - (
            (today.month < patients["date_of_birth"].dt.month)
            |
            (
                (today.month == patients["date_of_birth"].dt.month)
                &
                (today.day < patients["date_of_birth"].dt.day)
            )
        )
    )

    result = (
        patients.groupby(["Age", "gender"])
        .size()
        .reset_index(name="Patients")
        .sort_values("Age")
    )

    return result
def get_patient_registration_trend(department=None):

    data = get_filtered_data(department)

    patients = data["patients"].copy()

    patients["registration_date"] = pd.to_datetime(
        patients["registration_date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    result = (
        patients
        .dropna(subset=["registration_date"])
        .assign(
            Month=lambda x: (
                x["registration_date"]
                .dt.to_period("M")
                .dt.to_timestamp()
            )
        )
        .groupby("Month")
        .size()
        .reset_index(name="Patients")
        .sort_values("Month")
    )

    return result
def get_patient_treatment_type(department=None):

    # Get department-filtered data
    data = get_filtered_data(department)

    appointments = data["appointments"]
    treatments = data["treatments"]

    # Connect Treatments → Appointments
    treatment_data = treatments.merge(
        appointments[
            ["appointment_id", "patient_id"]
        ],
        on="appointment_id",
        how="inner"
    )

    # Count unique patients for each treatment type
    result = (
        treatment_data
        .dropna(subset=["treatment_type"])
        .groupby("treatment_type")["patient_id"]
        .nunique()
        .reset_index(name="Patients")
        .sort_values("Patients", ascending=False)
    )

    return result
def get_patient_details(department=None):

    # Get department-filtered data
    data = get_filtered_data(department)

    appointments = data["appointments"]
    patients = data["patients"]
    treatments = data["treatments"]

    # Connect appointments with patients
    patient_appointments = appointments.merge(
        patients,
        on="patient_id",
        how="inner"
    )

    # Keep only completed appointments
    completed = patient_appointments[
        patient_appointments["status"]
        .astype(str)
        .str.lower() == "completed"
    ]

    # Find patients with more than one completed appointment
    repeat_patients = (
        completed
        .groupby("patient_id")
        .size()
        .reset_index(name="Completed Appointments")
    )

    repeat_patients = repeat_patients[
        repeat_patients["Completed Appointments"] > 1
    ]

    # Keep only repeat patients
    result = completed.merge(
        repeat_patients[
            ["patient_id", "Completed Appointments"]
        ],
        on="patient_id",
        how="inner"
    )

    # Add treatment information
    result = result.merge(
        treatments[
            ["appointment_id", "treatment_type"]
        ],
        on="appointment_id",
        how="left"
    )
    return result
def get_paid_amount(department=None):

    paid_bills = billing_df[
        billing_df["payment_status"] == "Paid"
    ]

    if department is None:
        return paid_bills["amount"].sum()

    doctor_ids = doctors_df[
        doctors_df["specialization"] == department
    ]["doctor_id"]

    appointment_ids = appointment_df[
        appointment_df["doctor_id"].isin(doctor_ids)
    ]["appointment_id"]

    treatment_ids = treatments_df[
        treatments_df["appointment_id"].isin(appointment_ids)
    ]["treatment_id"]

    filtered_bills = paid_bills[
        paid_bills["treatment_id"].isin(treatment_ids)
    ]

    return filtered_bills["amount"].sum()

def get_pending_bills_count(department=None):

    pending_bills = billing_df[
        billing_df["payment_status"] == "Pending"
    ]

    if department is None:
        return len(pending_bills)

    doctor_ids = doctors_df[
        doctors_df["specialization"] == department
    ]["doctor_id"]

    appointment_ids = appointment_df[
        appointment_df["doctor_id"].isin(doctor_ids)
    ]["appointment_id"]

    treatment_ids = treatments_df[
        treatments_df["appointment_id"].isin(appointment_ids)
    ]["treatment_id"]

    filtered_bills = pending_bills[
        pending_bills["treatment_id"].isin(treatment_ids)
    ]

    return len(filtered_bills)

def get_pending_bills_amount(department=None):
    pending_bills = billing_df[
        billing_df["payment_status"] == "Pending"
    ]
    if department is None:
        return pending_bills["amount"].sum()
    doctor_ids = doctors_df[
        doctors_df["specialization"] == department
    ]["doctor_id"]
    appointment_ids = appointment_df[
        appointment_df["doctor_id"].isin(doctor_ids)
    ]["appointment_id"]
    treatment_ids = treatments_df[
        treatments_df["appointment_id"].isin(appointment_ids)
    ]["treatment_id"]
    filtered_bills = pending_bills[
        pending_bills["treatment_id"].isin(treatment_ids)
    ]
    return filtered_bills["amount"].sum()
def get_billing_total_revenue(department=None):

    data = get_filtered_data(department)

    billing = data["billing"]

    # Revenue includes Paid + Pending bills
    valid_bills = billing[
        billing["payment_status"].isin(
            ["Paid", "Pending"]
        )
    ]
    return valid_bills["amount"].sum()
def get_billing_revenue_by_month(department=None):

    data = get_filtered_data(department)

    billing = data["billing"].copy()

    # Include Paid + Pending, exclude Failed
    billing = billing[
        billing["payment_status"].isin(
            ["Paid", "Pending"]
        )
    ]

    billing["bill_date"] = pd.to_datetime(
        billing["bill_date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    result = (
        billing
        .dropna(subset=["bill_date"])
        .assign(
            Month=lambda x: (
                x["bill_date"]
                .dt.to_period("M")
                .dt.to_timestamp()
            )
        )
        .groupby("Month")["amount"]
        .sum()
        .reset_index(name="Revenue")
        .sort_values("Month")
    )

    return result
def get_billing_revenue_by_payment_method(department=None):

    data = get_filtered_data(department)

    billing = data["billing"].copy()

    # Include Paid + Pending, exclude Failed
    billing = billing[
        billing["payment_status"].isin(
            ["Paid", "Pending"]
        )
    ]

    result = (
        billing
        .dropna(subset=["payment_method"])
        .groupby("payment_method")["amount"]
        .sum()
        .reset_index(name="Revenue")
        .sort_values("Revenue", ascending=False)
    )

    return result
def get_billing_revenue_by_hospital(department=None):

    data = get_filtered_data(department)

    billing = data["billing"]
    treatments = data["treatments"]
    appointments = data["appointments"]
    doctors = data["doctors"]

    # Billing → Treatments
    revenue_data = billing.merge(
        treatments[
            ["treatment_id", "appointment_id"]
        ],
        on="treatment_id",
        how="inner"
    )

    # Treatments → Appointments
    revenue_data = revenue_data.merge(
        appointments[
            ["appointment_id", "doctor_id"]
        ],
        on="appointment_id",
        how="inner"
    )

    # Appointments → Doctors
    revenue_data = revenue_data.merge(
        doctors[
            ["doctor_id", "hospital_branch"]
        ],
        on="doctor_id",
        how="inner"
    )

    # Include Paid + Pending, exclude Failed
    revenue_data = revenue_data[
        revenue_data["payment_status"].isin(
            ["Paid", "Pending"]
        )
    ]

    result = (
        revenue_data
        .dropna(subset=["hospital_branch"])
        .groupby("hospital_branch")["amount"]
        .sum()
        .reset_index(name="Revenue")
        .sort_values("Revenue", ascending=False)
    )

    return result
def get_billing_revenue_by_treatment_type(department=None):

    data = get_filtered_data(department)

    billing = data["billing"]
    treatments = data["treatments"]

    # Billing → Treatments
    revenue_data = billing.merge(
        treatments[
            ["treatment_id", "treatment_type"]
        ],
        on="treatment_id",
        how="inner"
    )

    # Include Paid + Pending, exclude Failed
    revenue_data = revenue_data[
        revenue_data["payment_status"].isin(
            ["Paid", "Pending"]
        )
    ]

    result = (
        revenue_data
        .dropna(subset=["treatment_type"])
        .groupby("treatment_type")["amount"]
        .sum()
        .reset_index(name="Revenue")
        .sort_values("Revenue", ascending=False)
    )

    return result
def get_pending_bill_details(department=None):

    data = get_filtered_data(department)

    billing = data["billing"].copy()
    treatments = data["treatments"].copy()
    appointments = data["appointments"].copy()
    patients = data["patients"].copy()

    # --------------------------------
    # 1. Pending bills only
    # --------------------------------
    pending = billing[
        billing["payment_status"] == "Pending"
    ][
        ["treatment_id", "amount"]
    ].copy()

    # --------------------------------
    # 2. Billing → Treatments
    # --------------------------------
    treatment_info = treatments[
        [
            "treatment_id",
            "appointment_id",
            "treatment_type"
        ]
    ].copy()

    result = pending.merge(
        treatment_info,
        on="treatment_id",
        how="inner"
    )

    # --------------------------------
    # 3. Treatments → Appointments
    # --------------------------------
    appointment_info = appointments[
        [
            "appointment_id",
            "patient_id",
            "appointment_date"
        ]
    ].copy()

    result = result.merge(
        appointment_info,
        on="appointment_id",
        how="inner"
    )

    # --------------------------------
    # 4. Appointments → Patients
    # --------------------------------
    patient_info = patients[
        [
            "patient_id",
            "first_name",
            "last_name",
            "address",
            "contact_number"
        ]
    ].copy()

    result = result.merge(
        patient_info,
        on="patient_id",
        how="inner"
    )

    # --------------------------------
    # 5. Rename treatment date
    # --------------------------------
    result = result.rename(
        columns={
            "appointment_date": "Treatment Date"
        }
    )

    # --------------------------------
    # 6. Final columns
    # --------------------------------
    return result[
        [
            "patient_id",
            "first_name",
            "last_name",
            "amount",
            "treatment_type",
            "Treatment Date",
            "address",
            "contact_number"
        ]
    ]