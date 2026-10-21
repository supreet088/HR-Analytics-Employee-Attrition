# 📊 HR Analytics | Employee Attrition Dashboard


## 🌐 Live Dashboard

🚀 [Click Here to Explore the HR Analytics Dashboard](https://supreet-hr-analytics.streamlit.app/)


## Project Overview

An interactive HR Analytics Dashboard developed using Python, Pandas, Plotly, and Streamlit to analyze employee attrition patterns and explore workforce trends.

The project uses the IBM HR Analytics Employee Attrition dataset containing 1,470 employee records.

## Objectives

- Analyze overall employee attrition.
- Identify departments and job roles with higher attrition rates.
- Explore relationships between attrition, overtime, income, job satisfaction, and work-life balance.
- Build an interactive dashboard with dynamic filters.
- Support data-driven HR decision-making.

## Technologies Used

- **Python** — Data analysis and application development
- **Pandas** — Data cleaning and manipulation
- **NumPy** — Numerical operations
- **Plotly** — Interactive data visualizations
- **Streamlit** — Interactive dashboard development
- **VS Code** — Development environment
- **Git & GitHub** — Version control and project hosting

## Dashboard Features

- Four KPI metrics
- Ten interactive visualizations
- Seven interactive filters
- Reset All Filters functionality
- Download filtered employee data as CSV
- Department and overtime comparison charts

## Key Findings

| Metric | Result |
|---|---|
| Total Employees | 1,470 |
| Employees Who Left | 237 |
| Overall Attrition Rate | 16.12% |
| Sales Department Attrition | 20.63% |
| Overtime Employees Attrition | 30.53% |
| Non-Overtime Employees Attrition | 10.44% |

Employees working overtime showed a higher attrition rate than employees not working overtime. Sales had the highest attrition rate among the three departments.

These findings describe associations in the dataset and do not establish causation.

## How to Run the Project

1. Clone or download the repository.
2. Open the project folder in VS Code.
3. Install the required libraries:

   `python -m pip install -r requirements.txt`

4. Launch the dashboard:

   `python -m streamlit run dashboard.py`

5. Open the local URL displayed in your terminal.

## Dataset

IBM HR Analytics Employee Attrition Dataset.

## Future Improvements

- Employee attrition prediction using machine learning
- Additional HR performance indicators
- More advanced dashboard comparisons

## Project Status

Completed interactive dashboard with tested filtering, reset, and CSV download functionality.
