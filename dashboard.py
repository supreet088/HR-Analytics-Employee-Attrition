"""Interactive HR Analytics | Employee Attrition Dashboard.

Run from the project root with: python -m streamlit run dashboard.py
Requires data/cleaned_hr_data.csv and the dependencies in requirements.txt.
"""

from pathlib import Path
import html

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="HR Analytics Dashboard", page_icon="📊", layout="wide")

PURPLE = "#7C3AED"
PINK = "#E879B9"
PALETTE = [PURPLE, "#A78BFA", "#C4B5FD", PINK, "#6D28D9", "#DDD6FE", "#9333EA", "#F0ABFC", "#8B5CF6"]
DATA_PATH = Path(__file__).resolve().parent / "data" / "cleaned_hr_data.csv"


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


if not DATA_PATH.is_file():
    st.error(f"Dataset not found: {DATA_PATH}. Keep the data folder alongside dashboard.py.")
    st.stop()

try:
    original_df = load_data(DATA_PATH)
except Exception as exc:
    st.error(f"Unable to read the HR dataset: {exc}")
    st.stop()

required_columns = {
    "Attrition", "Department", "Gender", "JobRole", "Age", "MonthlyIncome",
    "OverTime", "YearsAtCompany", "JobSatisfaction", "WorkLifeBalance",
}
missing = required_columns.difference(original_df.columns)
if missing:
    st.error("Missing dataset columns: " + ", ".join(sorted(missing)))
    st.stop()


def style_hr_chart(fig):
    """Apply the same modern light-purple styling to every Plotly chart."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial", color="#24163B", size=13),
        title=dict(font=dict(size=18, color="#24163B"), x=0.5, xanchor="center"),
        margin=dict(t=75, b=65, l=35, r=35),
        colorway=PALETTE,
    )
    fig.update_xaxes(showgrid=False, linecolor="#E9E1FA", tickfont=dict(color="#625578"))
    fig.update_yaxes(gridcolor="#EEE8F8", zeroline=False, tickfont=dict(color="#625578"))
    return fig


def kpi_card(label, value, icon, accent):
    st.markdown(
        f"""
        <div style="background:#FFFFFF;border:1px solid #E9E1FA;
            border-top:4px solid {accent};border-radius:16px;padding:22px 18px;
            box-shadow:0 4px 16px rgba(90,55,140,.07);min-height:145px;">
          <div style="color:#6B6080;font-size:14px;font-weight:500;margin-bottom:14px;">
            {html.escape(icon)} {html.escape(label)}</div>
          <div style="color:#24163B;font-size:30px;font-weight:700;">
            {html.escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def calculate_attrition(data, column):
    result = data.groupby(column, observed=True).agg(
        Total_Employees=("Attrition", "count"),
        Employees_Left=("Attrition", lambda values: (values == "Yes").sum()),
    ).reset_index()
    result["Attrition Rate (%)"] = (
        result["Employees_Left"] / result["Total_Employees"] * 100
    ).round(2)
    return result


def show_attrition_chart(data, column, title, order=None, horizontal=False):
    """Render one attrition chart. Does not create tabs or reference fig2."""
    analysis = calculate_attrition(data, column)
    if order is not None:
        analysis[column] = pd.Categorical(analysis[column], categories=order, ordered=True)
        analysis = analysis.sort_values(column)
    elif horizontal:
        analysis = analysis.sort_values("Attrition Rate (%)", ascending=False)

    if horizontal:
        fig = px.bar(
            analysis, x="Attrition Rate (%)", y=column, orientation="h",
            color="Attrition Rate (%)",
            color_continuous_scale=["#DDD6FE", "#A78BFA", PURPLE, "#5B21B6"],
            text="Attrition Rate (%)", title=title,
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
    else:
        fig = px.bar(
            analysis, x=column, y="Attrition Rate (%)", color=column,
            color_discrete_sequence=PALETTE, text="Attrition Rate (%)", title=title,
        )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside", cliponaxis=False)
    fig = style_hr_chart(fig)
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, width="stretch")


# SIDEBAR FILTERS
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    for key in (
        "department_filter", "gender_filter", "jobrole_filter", "age_filter",
        "income_filter", "overtime_filter", "tenure_filter",
    ):
        st.session_state.pop(key, None)
    st.rerun()

st.sidebar.title("HR Analytics Filters")
st.sidebar.markdown("Customize your employee analysis")
st.sidebar.divider()

department = st.sidebar.selectbox(
    "Select Department", ["All Departments"] + sorted(original_df["Department"].dropna().unique().tolist()),
    key="department_filter",
)
gender_options = sorted(original_df["Gender"].dropna().unique().tolist())
gender = st.sidebar.multiselect(
    "Select Gender", options=gender_options, default=gender_options, key="gender_filter",
)
role_options = sorted(original_df["JobRole"].dropna().unique().tolist())
job_roles = st.sidebar.multiselect(
    "Select Job Role", options=role_options, default=role_options, key="jobrole_filter",
)
age_range = st.sidebar.slider(
    "Select Age Range", min_value=int(original_df["Age"].min()),
    max_value=int(original_df["Age"].max()),
    value=(int(original_df["Age"].min()), int(original_df["Age"].max())),
    key="age_filter",
)
income_range = st.sidebar.slider(
    "Select Monthly Income", min_value=int(original_df["MonthlyIncome"].min()),
    max_value=int(original_df["MonthlyIncome"].max()),
    value=(int(original_df["MonthlyIncome"].min()), int(original_df["MonthlyIncome"].max())),
    key="income_filter",
)
overtime = st.sidebar.radio("Overtime Status", ["All", "Yes", "No"], key="overtime_filter")
tenure_range = st.sidebar.slider(
    "Years at Company", min_value=int(original_df["YearsAtCompany"].min()),
    max_value=int(original_df["YearsAtCompany"].max()),
    value=(int(original_df["YearsAtCompany"].min()), int(original_df["YearsAtCompany"].max())),
    key="tenure_filter",
)

# Filter from the unmodified dataset each time Streamlit reruns.
mask = (
    original_df["Gender"].isin(gender)
    & original_df["JobRole"].isin(job_roles)
    & original_df["Age"].between(*age_range)
    & original_df["MonthlyIncome"].between(*income_range)
    & original_df["YearsAtCompany"].between(*tenure_range)
)
if department != "All Departments":
    mask &= original_df["Department"].eq(department)
if overtime != "All":
    mask &= original_df["OverTime"].eq(overtime)

df = original_df.loc[mask].copy()
st.sidebar.divider()
st.sidebar.metric("Matching Employees", len(df))
if df.empty:
    st.warning("No employees match the selected filters. Please adjust your selections.")
    st.stop()

st.sidebar.divider()
st.sidebar.download_button(
    "📥 Download Filtered Data", data=df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_hr_analytics.csv", mime="text/csv", use_container_width=True,
)

# HEADER AND TABS
st.title("📊 HR Analytics | Employee Attrition Dashboard")
st.markdown(
    "Explore workforce trends, employee retention, salary patterns, "
    "and the factors associated with employee attrition."
)
st.caption("Interactive workforce analytics | IBM HR Employee Attrition Dataset")
st.divider()
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Attrition Analysis", "👥 Employee Insights"])

total_employees = len(df)
employees_left = int(df["Attrition"].eq("Yes").sum())
attrition_rate = employees_left / total_employees * 100
average_income = df["MonthlyIncome"].mean()

# TAB 1: OVERVIEW
with tab1:
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        kpi_card("Total Employees", f"{total_employees:,}", "👥", PURPLE)
    with col2:
        kpi_card("Employees Left", f"{employees_left:,}", "📉", "#E05C87")
    with col3:
        kpi_card("Attrition Rate", f"{attrition_rate:.2f}%", "📊", "#8B5CF6")
    with col4:
        kpi_card("Average Monthly Income", f"{average_income:,.2f}", "💰", "#6D28D9")

    st.divider()
    st.subheader("Overall Employee Attrition")
    attrition_counts = df["Attrition"].value_counts().rename_axis("Attrition").reset_index(name="Employees")
    fig = px.pie(
        attrition_counts, names="Attrition", values="Employees", hole=0.5,
        title="Employee Attrition Distribution", color="Attrition",
        color_discrete_map={"No": PURPLE, "Yes": PINK},
    )
    fig = style_hr_chart(fig)
    fig.update_traces(
        textinfo="label+percent", textposition="inside",
        marker=dict(line=dict(color="#FFFFFF", width=3)),
        textfont=dict(size=13, color="#FFFFFF"),
    )
    fig.update_layout(
        legend=dict(title="Attrition Status", orientation="h", yanchor="bottom",
                    y=-0.12, xanchor="center", x=0.5),
        margin=dict(t=65, b=70, l=20, r=20),
    )
    st.plotly_chart(fig, width="stretch")

# TAB 2: ALL ATTRITION ANALYSIS CHARTS
with tab2:
    st.subheader("Department & Overtime Analysis")
    col_dept, col_overtime = st.columns(2)
    with col_dept:
        department_analysis = calculate_attrition(df, "Department").sort_values(
            "Attrition Rate (%)", ascending=False
        )
        fig2 = px.bar(
            department_analysis, x="Department", y="Attrition Rate (%)",
            color="Department", text="Attrition Rate (%)",
            title="Department-wise Employee Attrition Rate",
            color_discrete_sequence=[PURPLE, "#A78BFA", PINK],
        )
        fig2.update_traces(texttemplate="%{text:.2f}%", textposition="outside", cliponaxis=False)
        fig2 = style_hr_chart(fig2)
        fig2.update_layout(showlegend=False, xaxis_title="Department", yaxis_title="Attrition Rate (%)")
        st.plotly_chart(fig2, width="stretch")
    with col_overtime:
        show_attrition_chart(df, "OverTime", "Overtime vs Employee Attrition Rate", order=["No", "Yes"])

    st.divider()
    st.subheader("Salary vs Employee Attrition")
    salary_analysis = df.groupby("Attrition", as_index=False)["MonthlyIncome"].mean()
    salary_analysis["MonthlyIncome"] = salary_analysis["MonthlyIncome"].round(2)
    fig_salary = px.bar(
        salary_analysis, x="Attrition", y="MonthlyIncome", color="Attrition",
        text="MonthlyIncome", title="Average Monthly Income vs Employee Attrition",
        color_discrete_map={"No": PURPLE, "Yes": PINK},
    )
    fig_salary.update_traces(texttemplate="%{text:,.2f}", textposition="outside", cliponaxis=False)
    fig_salary = style_hr_chart(fig_salary)
    fig_salary.update_layout(showlegend=False, yaxis_title="Average Monthly Income")
    st.plotly_chart(fig_salary, width="stretch")

    st.divider()
    st.subheader("Job Satisfaction vs Attrition")
    show_attrition_chart(df, "JobSatisfaction", "Job Satisfaction vs Employee Attrition Rate", order=[1, 2, 3, 4])

    st.divider()
    st.subheader("Work-Life Balance vs Attrition")
    show_attrition_chart(df, "WorkLifeBalance", "Work-Life Balance vs Employee Attrition Rate", order=[1, 2, 3, 4])

    st.divider()
    st.subheader("Years at Company vs Attrition")
    tenure_labels = ["0-2 Years", "3-5 Years", "6-10 Years", "11-20 Years", "20+ Years"]
    df["TenureGroup"] = pd.cut(
        df["YearsAtCompany"], bins=[-1, 2, 5, 10, 20, float("inf")], labels=tenure_labels,
    )
    show_attrition_chart(df, "TenureGroup", "Years at Company vs Employee Attrition Rate", order=tenure_labels)

    st.divider()
    st.subheader("Age Group vs Attrition")
    age_labels = ["18-25 Years", "26-35 Years", "36-45 Years", "46-55 Years", "56+ Years"]
    df["AgeGroup"] = pd.cut(
        df["Age"], bins=[17, 25, 35, 45, 55, float("inf")], labels=age_labels,
    )
    show_attrition_chart(df, "AgeGroup", "Age Group vs Employee Attrition Rate", order=age_labels)

    st.divider()
    st.subheader("Job Role vs Attrition")
    show_attrition_chart(df, "JobRole", "Job Role vs Employee Attrition Rate", horizontal=True)

    st.divider()
    st.subheader("Gender vs Attrition")
    show_attrition_chart(df, "Gender", "Gender vs Employee Attrition Rate", order=["Female", "Male"])

# TAB 3: EMPLOYEE INSIGHTS
with tab3:
    st.subheader("👥 Employee Insights")
    st.write("Explore key workforce findings based on the currently selected employee filters.")
    st.markdown("### 📊 Key Findings")
    st.info(
        f"Out of {total_employees:,} employees, {employees_left:,} have left the company, "
        f"resulting in an attrition rate of {attrition_rate:.2f}%."
    )
    st.markdown("### 💡 HR Recommendations")
    st.markdown(
        "- Review overtime workloads and employee well-being.\n"
        "- Improve job satisfaction and employee engagement.\n"
        "- Develop retention strategies for high-attrition groups.\n"
        "- Monitor employee turnover trends regularly."
    )

# FOOTER (shared across tabs)
st.divider()
st.markdown(
    "### HR Analytics Dashboard\n\n"
    "**Technologies:** Python | Pandas | Plotly | Streamlit\n\n"
    "**Dataset:** IBM HR Analytics Employee Attrition Dataset\n\n"
    "**Purpose:** Analyze employee attrition patterns and support data-driven HR decisions.\n\n"
    "*Note: The findings show associations, not proven causes of attrition.*"
)
