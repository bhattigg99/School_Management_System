import streamlit as st
import sqlite3
import pandas as pd
import os
from groq import Groq
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(page_title="School Management System", layout="wide")

# Groq API
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Database connection
conn = sqlite3.connect("school.db", check_same_thread=False)
cursor = conn.cursor()

# Login system
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("School Management Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.login = True
        else:
            st.error("Invalid Credentials")
else:
    with st.sidebar:
        selected = option_menu(
            "School System",
            ["Dashboard","Students","Teachers","Attendance","Marks","Fees","AI Assistant"]
        )

    if selected == "Dashboard":
        st.title("Dashboard")
        students = pd.read_sql("SELECT * FROM students", conn)
        teachers = pd.read_sql("SELECT * FROM teachers", conn)
        col1, col2 = st.columns(2)
        col1.metric("Total Students", len(students))
        col2.metric("Total Teachers", len(teachers))

    if selected == "Students":
        st.title("Student Management")
        name = st.text_input("Student Name")
        student_class = st.text_input("Class")
        age = st.number_input("Age", min_value=1, max_value=100)
        contact = st.text_input("Contact")
        photo = st.file_uploader("Upload Photo", type=["png","jpg","jpeg"])

        if st.button("Add Student"):
            photo_name = photo.name if photo else ""
            cursor.execute(
                "INSERT INTO students(name,class,age,contact,photo) VALUES(?,?,?,?,?)",
                (name, student_class, age, contact, photo_name)
            )
            conn.commit()
            st.success("Student Added")

        data = pd.read_sql("SELECT * FROM students", conn)
        st.dataframe(data)

    if selected == "Teachers":
        st.title("Teacher Management")
        name = st.text_input("Teacher Name")
        subject = st.text_input("Subject")
        phone = st.text_input("Phone")

        if st.button("Add Teacher"):
            cursor.execute(
                "INSERT INTO teachers(name,subject,phone) VALUES(?,?,?)",
                (name, subject, phone)
            )
            conn.commit()
            st.success("Teacher Added")

        data = pd.read_sql("SELECT * FROM teachers", conn)
        st.dataframe(data)

    if selected == "Attendance":
        st.title("Attendance")
        roll = st.number_input("Roll Number", min_value=1)
        status = st.selectbox("Status", ["Present", "Absent"])

        if st.button("Save Attendance"):
            cursor.execute(
                "INSERT INTO attendance(roll_no,date,status) VALUES(?,?,?)",
                (roll, str(pd.Timestamp.now().date()), status)
            )
            conn.commit()
            st.success("Attendance Saved")

        data = pd.read_sql("SELECT * FROM attendance", conn)
        st.dataframe(data)

    if selected == "Marks":
        st.title("Marks Management")
        roll = st.number_input("Roll Number", min_value=1)
        subject = st.text_input("Subject")
        marks = st.number_input("Marks", min_value=0, max_value=100)

        if st.button("Save Marks"):
            cursor.execute(
                "INSERT INTO marks(roll_no,subject,marks) VALUES(?,?,?)",
                (roll, subject, marks)
            )
            conn.commit()
            st.success("Marks Added")

        data = pd.read_sql("SELECT * FROM marks", conn)
        st.dataframe(data)

    if selected == "Fees":
        st.title("Fee Management")
        roll = st.number_input("Roll Number", min_value=1)
        amount = st.number_input("Amount", min_value=0)
        status = st.selectbox("Status", ["Paid", "Unpaid"])

        if st.button("Save Fee"):
            cursor.execute(
                "INSERT INTO fees(roll_no,amount,status) VALUES(?,?,?)",
                (roll, amount, status)
            )
            conn.commit()
            st.success("Fee Saved")

        data = pd.read_sql("SELECT * FROM fees", conn)
        st.dataframe(data)

    if selected == "AI Assistant":
        st.title("AI School Assistant")
        question = st.text_input("Ask anything about education")

        if st.button("Ask AI") and question:
            chat_completion = client.chat.completions.create(
                messages=[{"role":"user","content":question}],
                model="llama-3.3-70b-versatile"
            )
            st.write(chat_completion.choices[0].message.content)
