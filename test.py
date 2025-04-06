import pandas as pd
import streamlit as st
import plotly.express as px

# Load the CSV file
@st.cache_data
def load_data():
    df = pd.read_csv("student_performance.csv")
    df.dropna(subset=["Marks"], inplace=True)
    df["Marks"] = pd.to_numeric(df["Marks"], errors='coerce')
    df.dropna(subset=["Marks"], inplace=True)
    return df

df = load_data()

st.title("📊 Student Performance Dashboard")

# Sidebar filters
students = df['Name'].unique()
classes = df['Class'].unique()
subjects = df['Subject'].unique()

selected_student = st.sidebar.selectbox("Select Student", options=students)
selected_class = st.sidebar.selectbox("Select Class", options=classes)
subject_options = ['All Subjects'] + list(subjects)
selected_subject = st.sidebar.selectbox("Select Subject", options=subject_options)

filtered_df = df[df['Name'] == selected_student]

if selected_subject != "All Subjects":
    filtered_df = filtered_df[filtered_df['Subject'] == selected_subject]

if selected_class:
    filtered_df = filtered_df[filtered_df['Class'] == selected_class]

# Exam Comparison within selected class and subject
st.header("📌 Exam-wise Performance")
if not filtered_df.empty:
    exam_summary = filtered_df.groupby("Exam")["Marks"].mean().reset_index()
    fig = px.bar(exam_summary, x="Exam", y="Marks", title=f"Exam-wise Marks for {selected_student} ({selected_subject})")
    st.plotly_chart(fig)
else:
    st.info("No data available for the selected options.")

# Class Comparison for a given subject
st.header("📚 Class-wise Comparison")
comparison_df = df[(df['Name'] == selected_student)]
if selected_subject != "All Subjects":
    comparison_df = comparison_df[comparison_df['Subject'] == selected_subject]

if not comparison_df.empty:
    class_comparison = comparison_df.groupby("Class")["Marks"].mean().reset_index()
    fig = px.bar(class_comparison, x="Class", y="Marks", title=f"Class-wise Average Marks for {selected_student} ({selected_subject})")
    st.plotly_chart(fig)
else:
    st.info("No data available for class comparison.")

# Overall performance comparison between class 8 and 9 (all subjects)
st.header("📈 Overall Class Performance (All Subjects)")
overall_comparison = df[df['Name'] == selected_student].groupby(["Class"])["Marks"].mean().reset_index()
if not overall_comparison.empty:
    fig = px.pie(overall_comparison, names='Class', values='Marks', title=f"Overall Class Performance for {selected_student}")
    st.plotly_chart(fig)
else:
    st.info("No data available for overall class performance.")
