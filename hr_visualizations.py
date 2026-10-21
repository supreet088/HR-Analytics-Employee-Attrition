
# Step 5 - Part 1: Overall Employee Attrition Visualization

import pandas as pd
import plotly.express as px

# Load cleaned HR dataset
df = pd.read_csv("data/cleaned_hr_data.csv")

# Count employees by attrition status
attrition_counts = df["Attrition"].value_counts().reset_index()

attrition_counts.columns = ["Attrition", "Employees"]

# Create interactive donut chart
fig = px.pie(
    attrition_counts,
    names="Attrition",
    values="Employees",
    hole=0.5,
    title="Overall Employee Attrition",
    color="Attrition",
    color_discrete_map={
        "No": "#2ECC71",
        "Yes": "#E74C3C"
    }
)

# Display percentages and labels
fig.update_traces(
    textinfo="percent+label",
    textposition="inside"
)

# Improve chart layout
fig.update_layout(
    title_x=0.5,
    template="plotly_white"
)

# Display chart
fig.show()



# Step 5 - Part 2: Department-wise Attrition Visualization

# Calculate department-wise attrition
department_analysis = df.groupby("Department").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition percentage
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

# Improve chart appearance
fig2.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig2.update_layout(
    title_x=0.5,
    template="plotly_white",
    yaxis_title="Attrition Rate (%)",
    showlegend=False
)

# Display chart
fig2.show()



# Step 5 - Part 3: Overtime vs Attrition Visualization

# Group employees by overtime status
overtime_analysis = df.groupby("OverTime").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition rate
overtime_analysis["Attrition Rate (%)"] = (
    overtime_analysis["Employees_Left"]
    / overtime_analysis["Total_Employees"] * 100
).round(2)

# Create interactive bar chart
fig3 = px.bar(
    overtime_analysis,
    x="OverTime",
    y="Attrition Rate (%)",
    color="OverTime",
    text="Attrition Rate (%)",
    title="Overtime vs Employee Attrition Rate",
    color_discrete_map={
        "No": "#2ECC71",
        "Yes": "#E74C3C"
    }
)

# Display percentages above bars
fig3.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

# Improve chart appearance
fig3.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Overtime",
    yaxis_title="Attrition Rate (%)",
    showlegend=False
)

# Display chart
fig3.show()



# Step 5 - Part 4: Salary vs Attrition Visualization

# Calculate average monthly income by attrition
salary_analysis = df.groupby("Attrition").agg(
    Average_Income=("MonthlyIncome", "mean")
).reset_index()

# Round average income
salary_analysis["Average_Income"] = (
    salary_analysis["Average_Income"].round(2)
)

# Create interactive bar chart
fig4 = px.bar(
    salary_analysis,
    x="Attrition",
    y="Average_Income",
    color="Attrition",
    text="Average_Income",
    title="Average Monthly Income vs Employee Attrition",
    color_discrete_map={
        "No": "#2ECC71",
        "Yes": "#E74C3C"
    }
)

# Display salary values above bars
fig4.update_traces(
    texttemplate="%{text:,.2f}",
    textposition="outside"
)

# Improve chart appearance
fig4.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Employee Attrition",
    yaxis_title="Average Monthly Income",
    showlegend=False
)

# Display chart
fig4.show()



# Step 5 - Part 5: Job Satisfaction vs Attrition Visualization

# Group employees by job satisfaction level
satisfaction_analysis = df.groupby("JobSatisfaction").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition rate
satisfaction_analysis["Attrition Rate (%)"] = (
    satisfaction_analysis["Employees_Left"]
    / satisfaction_analysis["Total_Employees"] * 100
).round(2)

# Convert satisfaction ratings to readable labels
satisfaction_analysis["Satisfaction Level"] = (
    satisfaction_analysis["JobSatisfaction"].map({
        1: "1 - Low",
        2: "2 - Medium",
        3: "3 - High",
        4: "4 - Very High"
    })
)

# Create interactive bar chart
fig5 = px.bar(
    satisfaction_analysis,
    x="Satisfaction Level",
    y="Attrition Rate (%)",
    color="Satisfaction Level",
    text="Attrition Rate (%)",
    title="Job Satisfaction vs Employee Attrition Rate",
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Display percentages above bars
fig5.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

# Improve chart appearance
fig5.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Job Satisfaction Level",
    yaxis_title="Attrition Rate (%)",
    showlegend=False
)

# Display chart
fig5.show()



# Step 5 - Part 6: Work-Life Balance vs Attrition Visualization

# Group employees by work-life balance rating
worklife_analysis = df.groupby("WorkLifeBalance").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition rate
worklife_analysis["Attrition Rate (%)"] = (
    worklife_analysis["Employees_Left"]
    / worklife_analysis["Total_Employees"] * 100
).round(2)

# Convert ratings into readable labels
worklife_analysis["Work-Life Balance Level"] = (
    worklife_analysis["WorkLifeBalance"].map({
        1: "1 - Bad",
        2: "2 - Good",
        3: "3 - Better",
        4: "4 - Best"
    })
)

# Create interactive bar chart
fig6 = px.bar(
    worklife_analysis,
    x="Work-Life Balance Level",
    y="Attrition Rate (%)",
    color="Work-Life Balance Level",
    text="Attrition Rate (%)",
    title="Work-Life Balance vs Employee Attrition Rate",
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Display percentages above bars
fig6.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

# Improve chart appearance
fig6.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Work-Life Balance Level",
    yaxis_title="Attrition Rate (%)",
    showlegend=False
)

# Display chart
fig6.show()



# Step 5 - Part 7: Years at Company vs Attrition Visualization

# Create employee tenure groups
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

# Group employees by tenure
tenure_analysis = df.groupby(
    "TenureGroup", observed=True
).agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition rate
tenure_analysis["Attrition Rate (%)"] = (
    tenure_analysis["Employees_Left"]
    / tenure_analysis["Total_Employees"] * 100
).round(2)

# Create interactive bar chart
fig7 = px.bar(
    tenure_analysis,
    x="TenureGroup",
    y="Attrition Rate (%)",
    color="TenureGroup",
    text="Attrition Rate (%)",
    title="Years at Company vs Employee Attrition Rate",
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Display percentages above bars
fig7.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

# Improve chart appearance
fig7.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Years at Company",
    yaxis_title="Attrition Rate (%)",
    showlegend=False
)

# Display chart
fig7.show()



# Step 5 - Part 8: Age Group vs Attrition Visualization

# Create employee age groups
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

# Group employees by age
age_analysis = df.groupby(
    "AgeGroup", observed=True
).agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition rate
age_analysis["Attrition Rate (%)"] = (
    age_analysis["Employees_Left"]
    / age_analysis["Total_Employees"] * 100
).round(2)

# Create interactive bar chart
fig8 = px.bar(
    age_analysis,
    x="AgeGroup",
    y="Attrition Rate (%)",
    color="AgeGroup",
    text="Attrition Rate (%)",
    title="Age Group vs Employee Attrition Rate",
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Display percentages above bars
fig8.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

# Improve chart appearance
fig8.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Age Group",
    yaxis_title="Attrition Rate (%)",
    showlegend=False
)

# Display chart
fig8.show()



# Step 5 - Part 9: Job Role vs Attrition Visualization

# Group employees by job role
jobrole_analysis = df.groupby("JobRole").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition rate
jobrole_analysis["Attrition Rate (%)"] = (
    jobrole_analysis["Employees_Left"]
    / jobrole_analysis["Total_Employees"] * 100
).round(2)

# Sort by attrition rate
jobrole_analysis = jobrole_analysis.sort_values(
    by="Attrition Rate (%)",
    ascending=True
)

# Create interactive horizontal bar chart
fig9 = px.bar(
    jobrole_analysis,
    x="Attrition Rate (%)",
    y="JobRole",
    orientation="h",
    color="Attrition Rate (%)",
    text="Attrition Rate (%)",
    title="Job Role vs Employee Attrition Rate",
    color_continuous_scale="Reds"
)

# Display percentages outside bars
fig9.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

# Improve chart appearance
fig9.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Attrition Rate (%)",
    yaxis_title="Job Role",
    coloraxis_showscale=False,
    margin=dict(l=180, r=80, t=80, b=60)
)

# Display chart
fig9.show()



# Step 5 - Part 10: Gender vs Attrition Visualization

# Group employees by gender
gender_analysis = df.groupby("Gender").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate attrition rate
gender_analysis["Attrition Rate (%)"] = (
    gender_analysis["Employees_Left"]
    / gender_analysis["Total_Employees"] * 100
).round(2)

# Create interactive bar chart
fig10 = px.bar(
    gender_analysis,
    x="Gender",
    y="Attrition Rate (%)",
    color="Gender",
    text="Attrition Rate (%)",
    title="Gender vs Employee Attrition Rate",
    color_discrete_map={
        "Female": "#E78AC3",
        "Male": "#66C2A5"
    }
)

# Display percentages above bars
fig10.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

# Improve chart appearance
fig10.update_layout(
    title_x=0.5,
    template="plotly_white",
    xaxis_title="Gender",
    yaxis_title="Attrition Rate (%)",
    showlegend=False
)

# Display chart
fig10.show()
