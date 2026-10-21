
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load cleaned HR dataset
df = pd.read_csv("data/cleaned_hr_data.csv")



# ==========================================
# STEP 7 - PROFESSIONAL DASHBOARD FILTERS
# ==========================================


# Reset all dashboard filters
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    for key in [
        "department_filter",
        "gender_filter",
        "jobrole_filter",
        "age_filter",
        "income_filter",
        "overtime_filter",
        "tenure_filter"
    ]:
        st.session_state.pop(key, None)

    st.rerun()


st.sidebar.title("HR Analytics Filters")
st.sidebar.markdown("Customize your employee analysis")
st.sidebar.divider()

# 1. Department - Dropdown
department = st.sidebar.selectbox(
    "Select Department",
    ["All Departments"] + sorted(df["Department"].unique().tolist()),
    key="department_filter"
)

# 2. Gender - Multiselect
gender = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Gender"].unique().tolist()),
    default=sorted(df["Gender"].unique().tolist()),
    key="gender_filter"
)

# 3. Job Role - Multiselect
job_roles = st.sidebar.multiselect(
    "Select Job Role",
    options=sorted(df["JobRole"].unique().tolist()),
    default=sorted(df["JobRole"].unique().tolist()),
    key="jobrole_filter"
)

# 4. Age - Range Slider
age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max())),
    key="age_filter"
)

# 5. Monthly Income - Range Slider
income_range = st.sidebar.slider(
    "Select Monthly Income",
    min_value=int(df["MonthlyIncome"].min()),
    max_value=int(df["MonthlyIncome"].max()),
    value=(
        int(df["MonthlyIncome"].min()),
        int(df["MonthlyIncome"].max())
    ),
    step=100,
    key="income_filter"
)

# 6. Overtime - Radio Buttons
overtime = st.sidebar.radio(
    "Overtime Status",
    ["All", "Yes", "No"],
    key="overtime_filter"
)

# 7. Years at Company - Range Slider
tenure_range = st.sidebar.slider(
    "Years at Company",
    min_value=int(df["YearsAtCompany"].min()),
    max_value=int(df["YearsAtCompany"].max()),
    value=(
        int(df["YearsAtCompany"].min()),
        int(df["YearsAtCompany"].max())
    ),
    key="tenure_filter"
)

# ==========================================
# APPLY ALL FILTERS
# ==========================================

filtered_df = df.copy()

if department != "All Departments":
    filtered_df = filtered_df[
        filtered_df["Department"] == department
    ]

filtered_df = filtered_df[
    filtered_df["Gender"].isin(gender)
]

filtered_df = filtered_df[
    filtered_df["JobRole"].isin(job_roles)
]

filtered_df = filtered_df[
    filtered_df["Age"].between(*age_range)
]

filtered_df = filtered_df[
    filtered_df["MonthlyIncome"].between(*income_range)
]

if overtime != "All":
    filtered_df = filtered_df[
        filtered_df["OverTime"] == overtime
    ]

filtered_df = filtered_df[
    filtered_df["YearsAtCompany"].between(*tenure_range)
]

# Display number of matching employees
st.sidebar.divider()
st.sidebar.metric(
    "Matching Employees",
    len(filtered_df)
)

# Handle empty results
if filtered_df.empty:
    st.warning(
        "No employees match the selected filters. "
        "Please adjust your selections."
    )
    st.stop()

# Use filtered data for all KPIs and charts
df = filtered_df.copy()


# Download filtered employee data
st.sidebar.divider()

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_hr_analytics.csv",
    mime="text/csv",
    use_container_width=True
)


# Dashboard title

st.title("📊 HR Analytics | Employee Attrition Dashboard")

st.markdown(
    "Explore workforce trends, employee retention, "
    "salary patterns, and the factors associated "
    "with employee attrition."
)

st.caption(
    "Interactive workforce analytics | "
    "IBM HR Employee Attrition Dataset"
)


st.divider()

# Calculate key metrics
total_employees = len(df)

employees_left = (df["Attrition"] == "Yes").sum()

employees_stayed = (df["Attrition"] == "No").sum()

attrition_rate = (employees_left / total_employees) * 100

average_income = df["MonthlyIncome"].mean()

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", f"{total_employees:,}")

with col2:
    st.metric("Employees Left", f"{employees_left:,}")

with col3:
    st.metric("Attrition Rate", f"{attrition_rate:.2f}%")

with col4:
    st.metric("Average Monthly Income", f"{average_income:,.2f}")

st.divider()

st.success("HR Analytics Dashboard loaded successfully!")



# Step 6 - Part 4: Overall Attrition Donut Chart

st.subheader("Overall Employee Attrition")

# Count employees by attrition status
attrition_counts = (
    df["Attrition"]
    .value_counts()
    .reset_index()
)

attrition_counts.columns = [
    "Attrition",
    "Employees"
]

# Create donut chart
fig = px.pie(
    attrition_counts,
    names="Attrition",
    values="Employees",
    hole=0.5,
    title="Employee Attrition Distribution",
    color="Attrition",
    color_discrete_map={
        "No": "#2ECC71",
        "Yes": "#E74C3C"
    }
)

# Display percentages
fig.update_traces(
    textinfo="label+percent",
    textposition="inside"
)

# Improve chart appearance
fig.update_layout(
    title_x=0.5,
    legend_title="Attrition Status"
)

# Display chart in Streamlit
st.plotly_chart(
    fig,
    use_container_width=True
)

# Group employees by department
department_analysis = df.groupby("Department").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition rate
department_analysis["Attrition Rate (%)"] = (
    department_analysis["Employees_Left"]
    / department_analysis["Total_Employees"] * 100
).round(2)

# Sort departments by attrition rate
department_analysis = department_analysis.sort_values(
    by="Attrition Rate (%)",
    ascending=False
)

# Create interactive bar chart
fig2 = px.bar(
    department_analysis,
    x="Department",
    y="Attrition Rate (%)",
    color="Department",
    text="Attrition Rate (%)",
    title="Department-wise Employee Attrition Rate",
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Display percentages above bars
fig2.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

# Improve chart appearance
fig2.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Department",
    yaxis_title="Attrition Rate (%)",
    showlegend=False
)

# Display chart in Streamlit


# ==========================================
# REMAINING HR ANALYTICS DASHBOARD CHARTS
# ==========================================

# Reusable function for attrition analysis
def calculate_attrition(data, column):
    result = data.groupby(column, observed=True).agg(
        Total_Employees=("Attrition", "count"),
        Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
    ).reset_index()

    result["Attrition Rate (%)"] = (
        result["Employees_Left"] /
        result["Total_Employees"] * 100
    ).round(2)

    return result


# Reusable chart function
def show_attrition_chart(column, title, order=None, horizontal=False):
    analysis = calculate_attrition(df, column)

    if order:
        analysis[column] = pd.Categorical(
            analysis[column],
            categories=order,
            ordered=True
        )
        analysis = analysis.sort_values(column)

    elif horizontal:
        analysis = analysis.sort_values(
            "Attrition Rate (%)", ascending=False
        )

    if horizontal:
        fig = px.bar(
            analysis,
            x="Attrition Rate (%)",
            y=column,
            orientation="h",
            color="Attrition Rate (%)",
            color_continuous_scale="Reds",
            text="Attrition Rate (%)",
            title=title
        )
        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )
    else:
        fig = px.bar(
            analysis,
            x=column,
            y="Attrition Rate (%)",
            color=column,
            text="Attrition Rate (%)",
            title=title
        )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        title_x=0.5,
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(t=80)
    )

    st.plotly_chart(fig, use_container_width=True)



# 3. DEPARTMENT AND OVERTIME ANALYSIS

st.divider()
st.subheader("Department & Overtime Analysis")

col_dept, col_overtime = st.columns(2)

with col_dept:
    st.plotly_chart(fig2, use_container_width=True)

with col_overtime:
    show_attrition_chart(
        "OverTime",
        "Overtime vs Employee Attrition Rate",
        order=["No", "Yes"]
    )



# 4. SALARY ANALYSIS
st.divider()
st.subheader("Salary vs Employee Attrition")

salary_analysis = df.groupby("Attrition")[
    "MonthlyIncome"
].mean().reset_index()

salary_analysis["MonthlyIncome"] = (
    salary_analysis["MonthlyIncome"].round(2)
)

fig_salary = px.bar(
    salary_analysis,
    x="Attrition",
    y="MonthlyIncome",
    color="Attrition",
    text="MonthlyIncome",
    title="Average Monthly Income vs Employee Attrition"
)

fig_salary.update_traces(
    texttemplate="%{text:,.2f}",
    textposition="outside"
)

fig_salary.update_layout(
    title_x=0.5,
    showlegend=False,
    yaxis_title="Average Monthly Income"
)

st.plotly_chart(fig_salary, use_container_width=True)


# 5. JOB SATISFACTION
st.divider()
st.subheader("Job Satisfaction vs Attrition")

show_attrition_chart(
    "JobSatisfaction",
    "Job Satisfaction vs Employee Attrition Rate",
    order=[1, 2, 3, 4]
)


# 6. WORK-LIFE BALANCE
st.divider()
st.subheader("Work-Life Balance vs Attrition")

show_attrition_chart(
    "WorkLifeBalance",
    "Work-Life Balance vs Employee Attrition Rate",
    order=[1, 2, 3, 4]
)


# 7. YEARS AT COMPANY
st.divider()
st.subheader("Years at Company vs Attrition")

df["TenureGroup"] = pd.cut(
    df["YearsAtCompany"],
    bins=[-1, 2, 5, 10, 20, float("inf")],
    labels=[
        "0-2 Years",
        "3-5 Years",
        "6-10 Years",
        "11-20 Years",
        "20+ Years"
    ]
)

show_attrition_chart(
    "TenureGroup",
    "Years at Company vs Employee Attrition Rate",
    order=[
        "0-2 Years",
        "3-5 Years",
        "6-10 Years",
        "11-20 Years",
        "20+ Years"
    ]
)


# 8. AGE GROUP ANALYSIS
st.divider()
st.subheader("Age Group vs Attrition")

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[17, 25, 35, 45, 55, float("inf")],
    labels=[
        "18-25 Years",
        "26-35 Years",
        "36-45 Years",
        "46-55 Years",
        "56+ Years"
    ]
)

show_attrition_chart(
    "AgeGroup",
    "Age Group vs Employee Attrition Rate",
    order=[
        "18-25 Years",
        "26-35 Years",
        "36-45 Years",
        "46-55 Years",
        "56+ Years"
    ]
)


# 9. JOB ROLE ANALYSIS
st.divider()
st.subheader("Job Role vs Attrition")

show_attrition_chart(
    "JobRole",
    "Job Role vs Employee Attrition Rate",
    horizontal=True
)


# 10. GENDER ANALYSIS
st.divider()
st.subheader("Gender vs Attrition")

show_attrition_chart(
    "Gender",
    "Gender vs Employee Attrition Rate",
    order=["Female", "Male"]
)


# FINAL MESSAGE
st.divider()
st.success("HR Analytics Dashboard completed successfully!")




# Dashboard Footer
st.divider()

st.markdown(
    """
    ### HR Analytics Dashboard

    **Technologies:** Python | Pandas | Plotly | Streamlit

    **Dataset:** IBM HR Analytics Employee Attrition Dataset

    **Purpose:** Analyze employee attrition patterns
    and support data-driven HR decisions.

    *Note: The findings show associations,
    not proven causes of attrition.*
    """
)
