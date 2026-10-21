
import pandas as pd

# Load the HR Analytics dataset
df = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")

# Display first five rows
print("First 5 rows:")
print(df.head())

# Display dataset dimensions
print("\nDataset Shape:")
print(df.shape)



# Step 2: Understanding the dataset

# Display all column names
print("\nColumn Names:")
print(df.columns.tolist())

# Check data types and non-null values
print("\nDataset Information:")
df.info()

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())



# Step 3: Data Cleaning

# Check total missing values
print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

# Check duplicate rows
print("\nTotal Duplicate Rows:")
print(df.duplicated().sum())

# Identify columns with only one unique value
print("\nConstant Columns:")
print(df.columns[df.nunique() == 1].tolist())



# Step 3 - Part 2: Cleaning the dataset

# Create a copy of the original dataset
cleaned_df = df.copy()

# Remove constant columns
columns_to_remove = [
    "EmployeeCount",
    "Over18",
    "StandardHours"
]

cleaned_df = cleaned_df.drop(columns=columns_to_remove)

# Remove duplicate records, if any
cleaned_df = cleaned_df.drop_duplicates()

# Display cleaned dataset dimensions
print("\nCleaned Dataset Shape:")
print(cleaned_df.shape)

# Check remaining missing values
print("\nRemaining Missing Values:")
print(cleaned_df.isnull().sum().sum())

# Save the cleaned dataset
cleaned_df.to_csv("data/cleaned_hr_data.csv", index=False)

print("\nCleaned dataset saved successfully!")
