# 🏥 Hospital Analytics Dashboard

An interactive **Hospital Analytics Dashboard** built with **Python, Streamlit, SQL Server, Pandas, and Plotly** to analyze patients, appointments, treatments, and billing information.

The dashboard provides department-wise analysis through interactive filters and presents key healthcare and financial metrics in a simple, business-friendly interface.

---

## Project Overview

This project transforms hospital operational data into an interactive analytical dashboard that helps users understand:

* Patient demographics and registration trends
* Appointment and visit patterns
* Treatment distribution
* Doctor and hospital performance
* Revenue and payment patterns
* Pending bills and outstanding amounts
* Department-wise performance

The project combines **data analysis, SQL, Python programming, and interactive dashboard development**.

---

## Project Objectives

The main objectives of this project are to:

* Analyze hospital patient data
* Monitor appointment and treatment activity
* Understand patient demographics
* Track revenue and payment performance
* Identify pending bills
* Compare performance across departments
* Present important metrics through interactive visualizations
* Build a practical dashboard suitable for hospital management reporting

---

#  Dashboard Pages

## 1.  Hospital Overview

The main dashboard provides a high-level summary of hospital operations through KPIs and visualizations.

Key metrics include:

* Total Patients
* Total Appointments
* Total Treatments
* Total Revenue
* Other operational KPIs

---

## 2. Patient Analytics

This page focuses on patient-related analysis.

### Visualizations include:

* Patients by Gender and Age
* Patient Visits by Reason
* Patient Registration Trend
* Patients by Treatment Type
* Repeat Patient Details

### Repeat Patient Table

The dashboard identifies patients who have completed more than one appointment and displays:

* Patient ID
* Patient Name
* Gender
* Treatment Type
* Completed Appointments

---

## 3. Treatment & Appointment Analytics

This page analyzes hospital treatments and appointment activity.

It provides insights into:

* Appointment trends
* Treatment distribution
* Patient visit reasons
* Treatment types
* Department-wise treatment activity

The page helps understand how different departments contribute to hospital treatment activity.

---

## 4. Billing Analytics

The Billing page provides financial analysis of hospital operations.

### KPIs

* Total Revenue
* Paid Amount
* Pending Bills Count
* Pending Bills Amount

### Visualizations

* Revenue by Month
* Revenue by Payment Method
* Revenue by Hospital
* Revenue by Treatment Type

### Pending Bills Table

The dashboard identifies patients with pending bills and displays:

* Patient ID
* Patient Name
* Pending Amount
* Treatment Type
* Treatment Date
* Address
* Contact Number

---

# Interactive Department Filter

The dashboard includes a **Department filter** available across the analytical pages.

When a department is selected, the relevant:

* KPIs
* Charts
* Tables
* Revenue metrics
* Patient metrics
* Treatment metrics

are dynamically updated.

---

# 🛠️ Technology Stack

| Technology       | Purpose                                     |
| ---------------- | ------------------------------------------- |
| Python           | Data processing and application development |
| Pandas           | Data cleaning and analysis                  |
| SQL Server       | Data storage and querying                   |
| Streamlit        | Interactive dashboard development           |
| Plotly           | Interactive data visualization              |
| Jupyter Notebook | Data cleaning, exploration and analysis     |

---

# 📁 Project Structure

```text
hospital-analytics-dashboard/
│
├── app.py
├── analysis.py
├── requirements.txt
├── README.md
│
├── data/
│   └── hospital_dataset.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   └── 03_analysis.ipynb
│
└── screenshots/
    ├── dashboard.png
    ├── patient_analytics.png
    ├── treatment_analytics.png
    └── billing_analytics.png
```

> The exact notebook and dataset filenames may vary depending on the final project files uploaded to the repository.

---


# 📓 Jupyter Notebook Analysis

The project also includes Jupyter notebooks documenting the analytical process.

The notebooks cover areas such as:

* Data understanding
* Data cleaning
* Exploratory data analysis
* Patient analysis
* Appointment analysis
* Treatment analysis
* Billing analysis
* Business insights

These notebooks demonstrate the analysis performed before developing the final interactive dashboard.

---

# Data Source

The dataset used in this project was obtained from **Kaggle** and was used for educational and portfolio purposes.
Dataset source and licensing information should be retained according to the original Kaggle dataset's terms.

---


---

# Key Features

* Interactive hospital analytics dashboard
* Department-wise filtering
* Patient demographic analysis
* Appointment analysis
* Treatment analysis
* Revenue analysis
* Pending bill monitoring
* Interactive Plotly charts
* Scrollable analytical tables
* SQL Server integration
* Python-based data analysis
* Streamlit-based interactive interface

---

# Future Improvements

Possible future enhancements include:

* Hospital management authentication
* Additional financial KPIs
* Automated data refresh
* Deployment to Streamlit Cloud
* More advanced predictive analytics
* Patient appointment forecasting
* Revenue forecasting

---

# 👨‍💻 Author

**Abhishek Verma**

Aspiring Data Analyst

**Skills:** Python | SQL | Excel | Power BI | Data Analysis | Dashboard Development

---

⭐ If you find this project useful, feel free to explore the repository and connect with me on LinkedIn.

