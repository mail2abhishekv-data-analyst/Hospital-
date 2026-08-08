import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from analysis import (
    get_data,
    get_total_patients,
    get_total_doctors,
    get_total_appointments,
    get_total_treatments,
    get_total_revenue,
    get_average_bill,
    get_revenue_trend,
    get_top_doctors,
    get_treatment_distribution,
    get_appointment_trend,
    get_departments,
    get_total_valid_appointments,
    get_doctors_by_specialization,
    get_doctors_by_branch,
    get_experience_distribution,
    get_patient_visits_by_reason,
    get_appointments_by_doctor,
    get_doctor_performance,
    get_patients_by_gender_age,
    get_patient_registration_trend,
    get_patient_treatment_type,
    get_patient_details,
    get_paid_amount,
    get_pending_bills_count,
    get_pending_bills_amount,
    get_billing_total_revenue,
    get_billing_revenue_by_month,
    get_billing_revenue_by_payment_method,
    get_billing_revenue_by_hospital,
    get_billing_revenue_by_treatment_type,
    get_pending_bill_details
)
patients_df, appointment_df, doctors_df, billing_df, treatments_df = get_data()

st.set_page_config(
    page_title="Hospital Dashboard",
    page_icon="🏥",
    layout="wide"
)
st.markdown("""
<style>
[data-testid="stAppViewContainer"] > .main {
    padding-top: 0rem;
}

[data-testid="stAppViewContainer"] .block-container {
    padding-top: 0rem;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #EAF7EA;
    border: 1px solid #D9D9D9;
    border-left: 4px solid #198754;
    padding: 5px;
    border-radius: 5px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.10);
    transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 4px 6px 14px rgba(0,0,0,0.18);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* KPI Label */
label[data-testid="stMetricLabel"] p {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #145A32 !important;
    line-height: 1.3 !important;
    margin-bottom: 5px !important;
}

/* KPI Value */
div[data-testid="stMetricValue"] {
    font-size: 35px !important;
    font-weight: bold !important;
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("assets/hospital_logo.png", width=120)
    page = option_menu(
        menu_title="🏥 VERMA\nHOSPITALS",
        options=[
            "Dashboard",
            "Doctors",
            "Patients",
            "Billing"
        ],
        icons=[
            "speedometer2",
            "person-badge-fill",
            "people-fill",
            "cash-stack"
        ],
        menu_icon="hospital",
        default_index=0,
        styles={
            "container": {
                "padding": "5!important",
            },
            "icon": {
                "font-size": "20px",
                "color": "#198754"
            },
            "nav-link": {
                "font-size": "18px",
                "font-weight": "bold",
                "text-align": "left",
                "margin": "8px 0",
                "padding": "12px 15px",
                "--hover-color": "#FFE5B4",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "background-color": "#198754",
                "color": "white",
                "font-weight": "bold",
                "border-radius": "12px",
                "padding": "12px 15px",
                "border": "2px solid #145A32",
            },
        }
    )
if "selected_department" not in st.session_state:
    st.session_state.selected_department = None
st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Developed By")
st.sidebar.markdown(
    """
**Abhishek Verma**

🐙 **GitHub:** https://github.com/mail2abhishekv-data-analyst \n
📧 **Email:** mail2abhishek.v@gmail.com  \n
🔗 **LinkedIn:\nhttps://www.linkedin.com/in/analyst-abhishek-verma/
"""
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Tools Used")
st.sidebar.markdown(
    """
- Python
- SQL Server
- Streamlit
- Pandas
- Plotly
"""
)

if page == "Dashboard":
    title_col, filter_col = st.columns([3, 3])

    with title_col:
        st.markdown("""
        <h1 style="
            color:#145A32;
            margin-bottom:0px;
            font-weight:800;
        ">
        🏥 VERMA HOSPITALS
        </h1>

        <p style="
            color:#6C757D;
            font-size:20px;
            margin-top:0;
        ">
        WELCOME TO VERMA HOSPITAL ANALYTICS DASHBOARD.
        </p>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] button {
            border: 2px solid #145A32;
            color: #145A32;
            font-weight: 600;
            border-radius: 8px;
        }

        div[data-testid="stHorizontalBlock"] button:hover {
            background-color: #145A32;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    with filter_col:
        st.write("")
        st.write("")
        departments = get_departments()
        col1, col2, col3 = st.columns(3)
        button_cols = [col1, col2, col3]
        for i, dept in enumerate(departments):
            with button_cols[i]:
                if st.button(
                        dept,
                        key=f"dept_{dept}",
                        use_container_width=True
                ):
                    if st.session_state.selected_department == dept:
                        st.session_state.selected_department = None
                    else:
                        st.session_state.selected_department = dept
                    st.rerun()
        if st.session_state.selected_department:
            st.markdown(
                f"""
                <p style="
                    color:#145A32;
                    font-size:16px;
                    font-weight:bold;
                    margin-top:8px;
                    margin-bottom:0px;
                ">
                Fetching: <b>{st.session_state.selected_department}</b> Dept.-- PRESS AGAIN TO DE-SELECT.
                </p>
                """,
                unsafe_allow_html=True
            )
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric(
            "👥 Total Patients",
            get_total_patients(st.session_state.selected_department)
        )
    with col2:
        st.metric(
            "👨‍⚕️ Total Doctors",
            get_total_doctors(st.session_state.selected_department)
        )
    with col3:
        st.metric(
            "📅 Total Appointments",
            get_total_appointments(st.session_state.selected_department)
        )
    with col4:
        st.metric(
            "💊 Total Treatments",
            get_total_treatments(st.session_state.selected_department)
        )
    with col5:
        st.metric(
            "💰 Total Revenue",
            f"₹ {get_total_revenue(st.session_state.selected_department):,.0f}"
        )
    with col6:
        st.metric(
            "💳 Average Bill",
            f"₹ {get_average_bill(st.session_state.selected_department):,.0f}"
        )
    st.markdown("<div style='margin-top:-15px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    col3, col4 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <h4 style="
            color:#145A32;
            font-size:22px;
            font-weight:700;
            margin-top:0px;
            margin-bottom:2px;
        ">
        📈 Revenue Trend
        </h4>
        """, unsafe_allow_html=True)
        revenue_df = get_revenue_trend(st.session_state.selected_department)
        fig = px.line(
            revenue_df,
            x="Month",
            y="amount",
            markers=True,
        )
        fig.update_traces(
            line=dict(color="#2E7D32", width=3),
            marker=dict(
                size=8,
                color="#66BB6A",
                line=dict(color="#2E7D32", width=2)
            )
        )
        fig.update_traces(
            line=dict(color="#2E7D32", width=3),
            marker=dict(size=8, color="#66BB6A", line=dict(color="#2E7D32", width=2)),
            hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>"
        )
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Amount",
            height=240,
            margin=dict(l=20, r=20, t=5, b=20)
        )
        with st.container(border=True):
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )
    with col2:
        st.markdown("""
        <h4 style="
            color:#145A32;
            font-size:22px;
            font-weight:700;
            margin-top:0px;
            margin-bottom:2px;
        ">
        👨‍⚕️ Top 5 Doctors
        </h4>
        """, unsafe_allow_html=True)
        doctor_df = get_top_doctors(st.session_state.selected_department)
        fig = px.bar(
            doctor_df,
            x="Successful Treatments",
            y="Doctor",
            orientation="h",
            height=240,
        )
        fig.update_traces(
            width=0.75
        )
        fig.update_layout(
            height=240,
            margin=dict(l=20, r=20, t=5, b=20),
            yaxis=dict(
                tickfont=dict(size=16)
            ),
            xaxis=dict(
                tickfont=dict(size=14)
            )
        )
        fig.update_traces(
            marker_color="#66BB6A",
            marker_line_color="#2E7D32",
            marker_line_width=2,
            textposition="outside"
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Total : %{x}<extra></extra>"
        )
        with st.container(border=True):
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    with col4:
        st.markdown("""
        <h4 style="
            color:#145A32;
            font-size:22px;
            font-weight:700;
            margin-top:0px;
            margin-bottom:2px;
        ">
        💊 Treatment Distribution
        </h4>
        """, unsafe_allow_html=True)
        treatment_df = get_treatment_distribution(st.session_state.selected_department)
        fig = px.bar(
            treatment_df,
            x="Treatment Count",
            y="treatment_type",
            orientation="h",
            color="Treatment Count",
        )
        fig.update_layout(
            template="plotly_white",
            yaxis=dict(
                autorange="reversed",
                tickfont=dict(size=15)
            ),
            xaxis=dict(
                tickfont=dict(size=14)
            ),
            margin=dict(l=20, r=20, t=5, b=20),
            height=240,
            paper_bgcolor="#F8FFF8",
            plot_bgcolor="white",
            coloraxis_showscale=False,
        )
        fig.update_layout(
            coloraxis_colorscale=[
                [0.0, "#C8E6C9"],
                [0.5, "#81C784"],
                [1.0, "#2E7D32"]
            ]
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Total : %{x}<extra></extra>"
        )
        with st.container(border=True):
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )
    with col3:
        st.markdown("""
        <h4 style="
            color:#145A32;
            font-size:22px;
            font-weight:700;
            margin-top:0px;
            margin-bottom:2px;
        ">
        📅 Appointment Trend
        </h4>
        """, unsafe_allow_html=True)
        appointment_df_chart = get_appointment_trend(st.session_state.selected_department)
        fig = px.line(
            appointment_df_chart,
            x="Month",
            y="Appointments",
            markers=True
        )
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Month",
            height=240,
            paper_bgcolor="#F8FFF8",
            plot_bgcolor="white",
        )
        fig.update_traces(
            line=dict(color="#198754", width=3),
            marker=dict(size=8),
            hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>"
        )
        fig.update_traces(
            line=dict(color="#2E7D32", width=3),
            marker=dict(size=8, color="#66BB6A", line=dict(color="#2E7D32", width=2)),
            hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>"
        )
        with st.container(border=True):
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

elif page == "Doctors":
    st.markdown("""
    <h1 style="
        color:#145A32;
        margin-top:0px;
        margin-bottom:5px;
        font-weight:700;
        line-height:1.1;
    ">
    👨‍⚕️ DOCTOR ANALYTICS
    </h1>
    """, unsafe_allow_html=True)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("👨‍⚕️ Total Doctors",get_total_doctors()
        )
    with kpi2:
        st.metric("📅 Total Appointments",get_total_valid_appointments()
        )
    with kpi3:
        st.metric("💊 Successful Treatments",get_total_treatments()
        )
    with kpi4:
        st.markdown("""
        <div style="
            background-color:#FF8C00;
            color:white;
            border-radius:10px;
            padding:10px;
            text-align:center;
            height:90px;
            font-family:Arial;
            font-weight:bold;
            line-height:1.3;
        ">
            🚑 EMERGENCY SERVICE<br>
            <span style="font-size:18px;">
                24 × 7 AVAILABLE
            </span>
        </div>
        """, unsafe_allow_html=True)
    chart1, chart2 = st.columns(2)
    with chart1:
        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:0px;
            margin-bottom:2px;
            font-weight:700;
        ">
        👨‍⚕️ Doctors by Specialization
        </h4>
        """, unsafe_allow_html=True)
        specialization_df = get_doctors_by_specialization()
        fig = px.pie(
            specialization_df,
            names="specialization",
            values="Doctors",
            hole=0.55
        )
        fig.update_layout(
            height=180,
            showlegend=False,
            margin=dict(l=0, r=10, t=5, b=5)
        )

        fig.update_traces(
            textinfo="label+value",
            textposition="outside",
            pull=[0.03, 0.03, 0.03],
            domain=dict(x=[0.00, 0.82], y=[0, 1]),
            marker=dict(
                colors=["#145A32", "#F39C12", "#FFFFFF"],
                line=dict(
                    color="#000000",
                    width=2
                )
            )
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    with chart2:

        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:0px;
            margin-bottom:2px;
            font-weight:700;
        ">
        🏥 Doctors by Hospital Branch
        </h4>
        """, unsafe_allow_html=True)

        branch_df = get_doctors_by_branch()

        fig = px.pie(
            branch_df,
            names="hospital_branch",
            values="Doctors"
        )

        fig.update_layout(
            height=180,
            showlegend=False,
            margin=dict(l=10, r=10, t=5, b=5)
        )

        fig.update_traces(
            textinfo="label+value",
            textposition="outside",
            pull=[0.03] * len(branch_df),
            marker=dict(
                colors=["#145A32", "#F39C12", "#FFFFFF"],
                line=dict(
                    color="#000000",
                    width=2
                )
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    chart3, chart4 = st.columns(2)
    with chart3:
        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:0px;
            margin-bottom:2px;
            font-weight:700;
        ">
        📈 Experience Distribution
        </h4>
        """, unsafe_allow_html=True)
        experience_df = get_experience_distribution()
        fig = px.scatter(
            experience_df,
            x="Experience Group",
            y="Doctors",
            size="Doctors",
            text="Doctors",
            size_max=70
        )
        fig.update_layout(
            height=180,
            showlegend=False,
            margin=dict(l=10, r=10, t=5, b=5),
            xaxis_title="",
            yaxis_title="Doctors"
        )

        fig.update_traces(
            textposition="middle center",
            marker=dict(
                color=["#145A32", "#F39C12", "#145A32", "#F39C12"],
                line=dict(
                    color="#000000",
                    width=2
                )
            )
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    with chart4:

        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:0px;
            margin-bottom:2px;
            font-weight:700;
        ">
        🏆 Top 5 Doctors by Appointments
        </h4>
        """, unsafe_allow_html=True)

        doctor_df = get_appointments_by_doctor()

        fig = px.funnel(
            doctor_df,
            y="Doctor",
            x="Appointments"
        )

        fig.update_traces(
            textinfo="value+label",
            marker=dict(
                color=["#145A32", "#F39C12", "#145A32", "#F39C12", "#145A32"],
                line=dict(
                    color="#000000",
                    width=2
                )
            )
        )

        fig.update_layout(
            height=180,
            showlegend=False,
            margin=dict(l=5, r=5, t=5, b=5),
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    st.markdown("""
        <h4 style="
        color:#145A32;
        margin-top:0px;
        margin-bottom:2px;
        font-weight:700;
    ">
    📋 Doctor Performance Summary
    </h4>
    """, unsafe_allow_html=True)
    doctor_table = get_doctor_performance()
    rows = ""
    for _, row in doctor_table.iterrows():
        rows += f"""
        <tr>
            <td>{row['Doctor']}</td>
            <td>{row['Specialization']}</td>
            <td>{int(row['Experience'])} years</td>
            <td>{row['Branch']}</td>
            <td>{int(row['Appointments'])}</td>
            <td>{int(row['Successful Treatments'])}</td>
            <td>{row['Phone Number']}</td>
        </tr>
        """
    html_table = f"""
    <table style="
        width:100%;
        border-collapse:collapse;
        font-family:Arial,sans-serif;
        font-size:18px;
        text-align:center;
    ">
    <tr style="
        background-color:#145A32;
        color:white;
        font-weight:bold;
    ">
        <th style="padding:7px;border:1px solid black;">Doctor</th>
        <th style="padding:7px;border:1px solid black;">Specialization</th>
        <th style="padding:7px;border:1px solid black;">Experience</th>
        <th style="padding:7px;border:1px solid black;">Branch</th>
        <th style="padding:7px;border:1px solid black;">Appointments</th>
        <th style="padding:7px;border:1px solid black;">Successful Treatments</th>
        <th style="padding:7px;border:1px solid black;">Phone Number</th>
    </tr>
    {rows}
    </table>
    """
    components.html(
        html_table,
        height=330,
        scrolling=False
    )
elif page == "Patients":
    title_col, filter_col = st.columns([3, 3])
    with title_col:
        st.markdown("""
        <h1 style="
            color:#145A32;
            margin-top:0px;
            margin-bottom:5px;
            font-weight:700;
            line-height:1.1;
        ">
        👨‍⚕️ PATIENT ANALYTICS
        </h1>
        """, unsafe_allow_html=True)
    with filter_col:
        st.write("")
        departments = get_departments()
        col1, col2, col3 = st.columns(3)
        button_cols = [col1, col2, col3]
        for i, dept in enumerate(departments):
            with button_cols[i]:
                if st.button(
                        dept,
                        key=f"dept_{dept}",
                        use_container_width=True
                ):
                    if st.session_state.selected_department == dept:
                        st.session_state.selected_department = None
                    else:
                        st.session_state.selected_department = dept
                    st.rerun()
        if st.session_state.selected_department:
            st.markdown(
                f"""
                <p style="
                    color:#145A32;
                    font-size:16px;
                    font-weight:bold;
                    margin-top:8px;
                    margin-bottom:0px;
                ">
                Fetching: <b>{st.session_state.selected_department}</b> Dept.-- PRESS AGAIN TO DE-SELECT.
                </p>
                """,
                unsafe_allow_html=True
            )
    st.markdown("""
    <div style="height:0px; margin:0px; padding:0px;"></div>
    """, unsafe_allow_html=True)
    kpi1, kpi2, kpi3 = st.columns([1, 1, 1])
    selected_department = st.session_state.selected_department
    with kpi1:
        st.metric(
            "👥 Total Patients",
            get_total_patients(selected_department)
        )

    with kpi2:
        st.metric(
            "📅 Patient Appointments",
            get_total_appointments(selected_department)
        )

    with kpi3:
        st.metric(
            "💊 Successful Treatments",
            get_total_treatments(selected_department)
        )
    st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        padding-top: 4px;
        padding-bottom: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
        👥 Patients by Gender & Age
        </h4>
        """, unsafe_allow_html=True)

        gender_age_df = get_patients_by_gender_age(
            st.session_state.selected_department
        )

        gender_age_pivot = (
            gender_age_df
            .pivot(
                index="Age",
                columns="gender",
                values="Patients"
            )
            .fillna(0)
            .reset_index()
        )

        fig = px.line(
            gender_age_pivot,
            x="Age",
            y=gender_age_pivot.columns[1:],
            markers=True
        )

        fig.update_layout(
            height=180,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Age",
            yaxis_title="Patients",
            legend_title=""
        )

        theme_colors = ["#145A32", "#FF8C00"]

        for i, trace in enumerate(fig.data):
            color = theme_colors[i % 2]

            trace.update(
                line=dict(
                    color=color,
                    width=3
                ),
                marker=dict(
                    color=color,
                    size=5,
                    line=dict(
                        color="#000000",
                        width=2
                    )
                )
            )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with chart2:
        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
        📋 Patient Visits by Reason
        </h4>
        """, unsafe_allow_html=True)

        reason_df = get_patient_visits_by_reason(
            st.session_state.selected_department
        )

        fig = px.bar(
            reason_df,
            x="Visits",
            y="reason_for_visit",
            orientation="h",
            text="Visits",
            color="Visits",
            color_continuous_scale="Greens"
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(
                size=12,
                color="#000000"
            )
        )

        fig.update_layout(
            height=180,
            margin=dict(
                l=5,
                r=25,
                t=5,
                b=5
            ),
            xaxis_title="Number of Visits",
            yaxis_title="",
            showlegend=False,
            coloraxis_showscale=False,
            yaxis=dict(
                automargin=True
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    chart3, chart4 = st.columns(2)

    with chart3:
        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
        📈 Patient Registration Trend
        </h4>
        """, unsafe_allow_html=True)

        registration_df = get_patient_registration_trend(
            st.session_state.selected_department
        )

        fig = px.line(
            registration_df,
            x="Month",
            y="Patients",
            markers=True
        )

        fig.update_traces(
            line=dict(
                color="#145A32",
                width=3
            ),
            marker=dict(
                color="#FF8C00",
                size=8,
                line=dict(
                    color="#000000",
                    width=2
                )
            )
        )

        fig.update_layout(
            height=180,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Month",
            yaxis_title="Patients",
            showlegend=False

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    with chart4:
        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
        💊 Patients by Treatment Type
        </h4>
        """, unsafe_allow_html=True)

        treatment_type_df = get_patient_treatment_type(
            st.session_state.selected_department
        )

        fig = px.bar(
            treatment_type_df,
            x="Patients",
            y="treatment_type",
            orientation="h",
            text="Patients"
        )

        theme_colors = ["#145A32", "#FF8C00"]

        for i, trace in enumerate(fig.data):
            trace.update(
                marker=dict(
                    color=[
                        theme_colors[j % 2]
                        for j in range(len(treatment_type_df))
                    ],
                    line=dict(
                        color="#000000",
                        width=1
                    )
                ),
                textposition="outside"
            )

        fig.update_layout(
            height=180,
            margin=dict(l=10, r=25, t=10, b=10),
            xaxis_title="Number of Patients",
            yaxis_title="",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    st.markdown("""
    <h4 style="
        color:#145A32;
        margin-top:8px;
        margin-bottom:5px;
        font-weight:700;
    ">
    👤 Patient Details — Repeat Patients
    </h4>
    """, unsafe_allow_html=True)

    patient_table = get_patient_details(
        st.session_state.selected_department
    )

    html_table = """
    <div style="
        height:180px;
        overflow-y:auto;
        width:100%;
        border:1px solid #145A32;
        border-radius:6px;
    ">
    <table style="
        width:100%;
        border-collapse:collapse;
        text-align:center;
        font-family:Arial;
        font-size:13px;
    ">
    <thead>
    <tr style="
        background-color:#145A32;
        color:white;
    ">
        <th style="padding:7px; border:1px solid #000;">Patient ID</th>
        <th style="padding:7px; border:1px solid #000;">Patient Name</th>
        <th style="padding:7px; border:1px solid #000;">Gender</th>
        <th style="padding:7px; border:1px solid #000;">Treatment Type</th>
        <th style="padding:7px; border:1px solid #000;">Completed Appointments</th>
    </tr>
    </thead>
    <tbody>
    """

    for _, row in patient_table.iterrows():
        html_table += f"""
    <tr>
        <td style="padding:6px; border:1px solid #ddd;">
            {row['patient_id']}
        </td>
        <td style="padding:6px; border:1px solid #ddd;">
            {row['first_name']} {row['last_name']}
        </td>
        <td style="padding:6px; border:1px solid #ddd;">
            {row['gender']}
        </td>
        <td style="
            padding:6px;
            border:1px solid #ddd;
            color:#145A32;
            font-weight:600;
        ">
            {row['treatment_type']}
        </td>
        <td style="
            padding:6px;
            border:1px solid #ddd;
            font-weight:700;
        ">
            {int(row['Completed Appointments'])}
        </td>
    </tr>
    """

    html_table += """
    </tbody>
    </table>
    </div>
    """

    st.markdown(
        html_table,
        unsafe_allow_html=True
    )
elif page == "Billing":
    title_col, filter_col = st.columns([3, 3])
    with title_col:
        st.markdown("""
        <h2 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
            💰 Billing Analytics
        </h2>
        """, unsafe_allow_html=True)
    with filter_col:
        st.markdown(
            """
            <div style="margin-top:5px;"></div>
            """,
            unsafe_allow_html=True
        )
        departments = get_departments()
        col1, col2, col3 = st.columns(3)
        button_cols = [col1, col2, col3]
        for i, dept in enumerate(departments):
            with button_cols[i]:
                if st.button(
                        dept,
                        key=f"billing_dept_{dept}",
                        use_container_width=True
                ):
                    if st.session_state.selected_department == dept:
                        st.session_state.selected_department = None
                    else:
                        st.session_state.selected_department = dept
                    st.rerun()
        if st.session_state.selected_department:
            st.markdown(
                f"""
                <p style="
                    color:#145A32;
                    font-size:16px;
                    font-weight:bold;
                    margin-top:8px;
                    margin-bottom:0px;
                ">
                Fetching:
                <b>{st.session_state.selected_department}</b>
                Dept. — PRESS AGAIN TO DE-SELECT.
                </p>
                """,
                unsafe_allow_html=True
            )
    selected_department = st.session_state.selected_department
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            "💰 Total Revenue",
            f"₹{get_billing_total_revenue(selected_department):,.0f}"
        )

    with kpi2:
        st.metric(
            "💵 Paid Amount",
            f"₹{get_paid_amount(selected_department):,.0f}"
        )

    with kpi3:
        st.metric(
            "📋 Pending Bills",
            f"{get_pending_bills_count(selected_department):,}"
        )

    with kpi4:
        st.metric(
            "⚠️ Pending Amount",
            f"₹{get_pending_bills_amount(selected_department):,.0f}"
        )
    revenue_month_df = get_billing_revenue_by_month(
        st.session_state.selected_department
    )
    chart1, chart2 = st.columns(2)
    with chart1:
        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
        📈 Revenue by Month
        </h4>
        """, unsafe_allow_html=True)

        revenue_month_df = get_billing_revenue_by_month(
            st.session_state.selected_department
        )

        fig = px.line(
            revenue_month_df,
            x="Month",
            y="Revenue",
            markers=True
        )

        fig.update_traces(
            line=dict(
                color="#145A32",
                width=3
            ),
            marker=dict(
                size=8,
                color="#FF8C00",
                line=dict(
                    color="#145A32",
                    width=2
                )
            )
        )

        fig.update_layout(
            height=180,
            margin=dict(l=10, r=10, t=5, b=5),
            xaxis_title="Month",
            yaxis_title="Revenue",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    with chart2:

        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
        💳 Revenue by Payment Method
        </h4>
        """, unsafe_allow_html=True)

        payment_method_df = get_billing_revenue_by_payment_method(
            st.session_state.selected_department
        )

        fig = px.bar(
            payment_method_df,
            x="Revenue",
            y="payment_method",
            orientation="h",
            text="Revenue"
        )

        fig.update_traces(
            marker=dict(
                color="#145A32",
                line=dict(
                    color="#FF8C00",
                    width=1
                )
            ),
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        fig.update_layout(
            height=180,
            margin=dict(l=10, r=30, t=5, b=5),
            xaxis_title="Revenue",
            yaxis_title="",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    chart3, chart4 = st.columns(2)
    with chart3:

        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
        🏥 Revenue by Hospital
        </h4>
        """, unsafe_allow_html=True)

        hospital_revenue_df = get_billing_revenue_by_hospital(
            st.session_state.selected_department
        )

        fig = px.bar(
            hospital_revenue_df,
            x="Revenue",
            y="hospital_branch",
            orientation="h",
            text="Revenue"
        )

        fig.update_traces(
            marker=dict(
                color="#145A32",
                line=dict(
                    color="#FF8C00",
                    width=1
                )
            ),
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        fig.update_layout(
            height=180,
            margin=dict(l=10, r=30, t=5, b=5),
            xaxis_title="Revenue",
            yaxis_title="",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    with chart4:

        st.markdown("""
        <h4 style="
            color:#145A32;
            margin-top:5px;
            margin-bottom:5px;
            font-weight:700;
        ">
        💊 Revenue by Treatment Type
        </h4>
        """, unsafe_allow_html=True)

        treatment_revenue_df = get_billing_revenue_by_treatment_type(
            st.session_state.selected_department
        )

        fig = px.bar(
            treatment_revenue_df,
            x="Revenue",
            y="treatment_type",
            orientation="h",
            text="Revenue"
        )

        fig.update_traces(
            marker=dict(
                color="#145A32",
                line=dict(
                    color="#FF8C00",
                    width=1
                )
            ),
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        fig.update_layout(
            height=180,
            margin=dict(l=10, r=30, t=5, b=5),
            xaxis_title="Revenue",
            yaxis_title="",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    st.markdown(
        """
        <h4 style="
            color:#145A32;
            margin-top:8px;
            margin-bottom:5px;
            font-weight:700;
        ">
            ⚠️ Pending Bills — Patient Details
        </h4>
        """,
        unsafe_allow_html=True
    )

    pending_table = get_pending_bill_details(
        st.session_state.selected_department
    )

    html_table = """
            <div style="
                max-height:180px;
                overflow-y:auto;
                border:1px solid #145A32;
            ">
            <table style="
                width:100%;
                border-collapse:collapse;
                text-align:center;
                font-family:Arial;
                font-size:13px;
            ">
            <thead>
            <tr style="
                background-color:#145A32;
                color:white;
            ">
            <th>Patient ID</th>
            <th>Patient Name</th>
            <th>Pending Amount</th>
            <th>Treatment Type</th>
            <th>Treatment Date</th>
            <th>Address</th>
            <th>Phone</th>
            </tr>
            </thead>
            <tbody>
            """

    for _, row in pending_table.iterrows():
        html_table += (
            "<tr>"
            f"<td>{row['patient_id']}</td>"
            f"<td>{row['first_name']} {row['last_name']}</td>"
            f"<td>₹{float(row['amount']):,.0f}</td>"
            f"<td>{row['treatment_type']}</td>"
            f"<td>{row['Treatment Date']}</td>"
            f"<td>{row['address']}</td>"
            f"<td>{row['contact_number']}</td>"
            "</tr>"
        )

    html_table += """
            </tbody>
            </table>
            </div>
            """

    st.markdown(
        html_table,
        unsafe_allow_html=True
    )