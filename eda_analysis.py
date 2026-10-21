
import pandas as pd

# Load cleaned HR dataset
df = pd.read_csv("data/cleaned_hr_data.csv")

# Total employees
total_employees = len(df)

# Employees who left
employees_left = (df["Attrition"] == "Yes").sum()

# Employees who stayed
employees_stayed = (df["Attrition"] == "No").sum()

# Calculate attrition rate
attrition_rate = (employees_left / total_employees) * 100

# Display results
print("HR EMPLOYEE ATTRITION ANALYSIS")
print("-----------------------------")

print("Total Employees:", total_employees)
print("Employees Left:", employees_left)
print("Employees Stayed:", employees_stayed)
print("Attrition Rate:", round(attrition_rate, 2), "%")




# Step 4 - Part 2: Department-Wise Attrition

# Total employees in each department
department_total = df.groupby("Department").size()

# Employees who left in each department
department_left = df[df["Attrition"] == "Yes"].groupby(
    "Department"
).size()

# Combine the results
department_analysis = pd.DataFrame({
    "Total Employees": department_total,
    "Employees Left": department_left
})

# Replace missing values with zero
department_analysis["Employees Left"] = (
    department_analysis["Employees Left"].fillna(0).astype(int)
)

# Calculate department-wise attrition rate
department_analysis["Attrition Rate (%)"] = (
    department_analysis["Employees Left"]
    / department_analysis["Total Employees"] * 100
).round(2)

# Sort by highest attrition rate
department_analysis = department_analysis.sort_values(
    by="Attrition Rate (%)",
    ascending=False
)

print("\nDEPARTMENT-WISE ATTRITION ANALYSIS")
print("----------------------------------")
print(department_analysis)




# Step 4 - Part 3: Overtime vs Attrition

# Total employees by overtime status
overtime_total = df.groupby("OverTime").size()

# Employees who left by overtime status
overtime_left = df[df["Attrition"] == "Yes"].groupby(
    "OverTime"
).size()

# Combine results
overtime_analysis = pd.DataFrame({
    "Total Employees": overtime_total,
    "Employees Left": overtime_left
})

# Replace missing values
overtime_analysis["Employees Left"] = (
    overtime_analysis["Employees Left"].fillna(0).astype(int)
)

# Calculate attrition rate
overtime_analysis["Attrition Rate (%)"] = (
    overtime_analysis["Employees Left"]
    / overtime_analysis["Total Employees"] * 100
).round(2)

print("\nOVERTIME VS ATTRITION ANALYSIS")
print("------------------------------")
print(overtime_analysis)



# Step 4 - Part 4: Salary vs Attrition

# Group employees by attrition status
salary_analysis = df.groupby("Attrition")["MonthlyIncome"].agg(
    ["count", "mean", "median", "min", "max"]
)

# Rename columns
salary_analysis.columns = [
    "Total Employees",
    "Average Income",
    "Median Income",
    "Minimum Income",
    "Maximum Income"
]

# Round values
salary_analysis = salary_analysis.round(2)

# Display results
print("\nSALARY VS ATTRITION ANALYSIS")
print("---------------------------")
print(salary_analysis.to_string())



# Step 4 - Part 5: Job Satisfaction vs Attrition

# Group employees by job satisfaction level
satisfaction_analysis = df.groupby("JobSatisfaction").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
)

# Calculate attrition rate
satisfaction_analysis["Attrition Rate (%)"] = (
    satisfaction_analysis["Employees_Left"]
    / satisfaction_analysis["Total_Employees"] * 100
).round(2)

# Rename columns
satisfaction_analysis = satisfaction_analysis.rename(columns={
    "Total_Employees": "Total Employees",
    "Employees_Left": "Employees Left"
})

# Display results
print("\nJOB SATISFACTION VS ATTRITION ANALYSIS")
print("-------------------------------------")
print(satisfaction_analysis.to_string())



# Step 4 - Part 6: Work-Life Balance vs Attrition

# Group employees by work-life balance rating
worklife_analysis = df.groupby("WorkLifeBalance").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
)

# Calculate attrition rate
worklife_analysis["Attrition Rate (%)"] = (
    worklife_analysis["Employees_Left"]
    / worklife_analysis["Total_Employees"] * 100
).round(2)

# Rename columns
worklife_analysis = worklife_analysis.rename(columns={
    "Total_Employees": "Total Employees",
    "Employees_Left": "Employees Left"
})

# Display results
print("\nWORK-LIFE BALANCE VS ATTRITION ANALYSIS")
print("--------------------------------------")
print(worklife_analysis.to_string())



# Step 4 - Part 7: Years at Company vs Attrition

# Create employee tenure groups
df["TenureGroup"] = pd.cut(
    df["YearsAtCompany"],
    bins=[-1, 2, 5, 10, 20, float("inf")],
    labels=["0-2 Years", "3-5 Years", "6-10 Years",
            "11-20 Years", "20+ Years"]
)

# Group employees by tenure
tenure_analysis = df.groupby(
    "TenureGroup", observed=True
).agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
)

# Calculate attrition rate
tenure_analysis["Attrition Rate (%)"] = (
    tenure_analysis["Employees_Left"]
    / tenure_analysis["Total_Employees"] * 100
).round(2)

# Rename columns
tenure_analysis = tenure_analysis.rename(columns={
    "Total_Employees": "Total Employees",
    "Employees_Left": "Employees Left"
})

# Display results
print("\nYEARS AT COMPANY VS ATTRITION ANALYSIS")
print("--------------------------------------")
print(tenure_analysis.to_string())



# Step 4 - Part 8: Age Group vs Attrition

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
)

# Calculate attrition rate
age_analysis["Attrition Rate (%)"] = (
    age_analysis["Employees_Left"]
    / age_analysis["Total_Employees"] * 100
).round(2)

# Rename columns
age_analysis = age_analysis.rename(columns={
    "Total_Employees": "Total Employees",
    "Employees_Left": "Employees Left"
})

# Display results
print("\nAGE GROUP VS ATTRITION ANALYSIS")
print("-------------------------------")
print(age_analysis.to_string())



# Step 4 - Part 9: Job Role vs Attrition

# Group employees by job role
jobrole_analysis = df.groupby("JobRole").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
)

# Calculate attrition rate
jobrole_analysis["Attrition Rate (%)"] = (
    jobrole_analysis["Employees_Left"]
    / jobrole_analysis["Total_Employees"] * 100
).round(2)

# Rename columns
jobrole_analysis = jobrole_analysis.rename(columns={
    "Total_Employees": "Total Employees",
    "Employees_Left": "Employees Left"
})

# Sort by highest attrition rate
jobrole_analysis = jobrole_analysis.sort_values(
    by="Attrition Rate (%)",
    ascending=False
)

# Display results
print("\nJOB ROLE VS ATTRITION ANALYSIS")
print("-----------------------------")
print(jobrole_analysis.to_string())



# Step 4 - Part 10: Gender vs Attrition

# Group employees by gender
gender_analysis = df.groupby("Gender").agg(
    Total_Employees=("Attrition", "count"),
    Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
)

# Calculate attrition rate
gender_analysis["Attrition Rate (%)"] = (
    gender_analysis["Employees_Left"]
    / gender_analysis["Total_Employees"] * 100
).round(2)

# Rename columns
gender_analysis = gender_analysis.rename(columns={
    "Total_Employees": "Total Employees",
    "Employees_Left": "Employees Left"
})

# Display results
print("\nGENDER VS ATTRITION ANALYSIS")
print("---------------------------")
print(gender_analysis.to_string())
