import streamlit as st
import sqlite3
from datetime import datetime

# ---------------------------
# Database setup
# ---------------------------
conn = sqlite3.connect("atlasog.db", check_same_thread=False)
c = conn.cursor()

# Investments table
c.execute('''CREATE TABLE IF NOT EXISTS investments
             (id INTEGER PRIMARY KEY, name TEXT, amount REAL, date TEXT)''')
# Projects table
c.execute('''CREATE TABLE IF NOT EXISTS projects
             (id INTEGER PRIMARY KEY, name TEXT, status TEXT, date TEXT)''')
# Ideas table
c.execute('''CREATE TABLE IF NOT EXISTS ideas
             (id INTEGER PRIMARY KEY, content TEXT, date TEXT)''')
conn.commit()

# ---------------------------
# Helper functions
# ---------------------------
def add_investment(name, amount):
    c.execute("INSERT INTO investments (name, amount, date) VALUES (?, ?, ?)", (name, amount, datetime.now().isoformat()))
    conn.commit()

def add_project(name, status):
    c.execute("INSERT INTO projects (name, status, date) VALUES (?, ?, ?)", (name, status, datetime.now().isoformat()))
    conn.commit()

def add_idea(content):
    c.execute("INSERT INTO ideas (content, date) VALUES (?, ?)", (content, datetime.now().isoformat()))
    conn.commit()

def fetch_all(table):
    c.execute(f"SELECT * FROM {table} ORDER BY date DESC")
    return c.fetchall()

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="AtlasOG", layout="wide")
st.title("🌍 AtlasOG Dashboard")
st.markdown("Your live Atlas Operating System (AOG) — real-world ready.")

tab = st.sidebar.radio("Navigate", ["Wealth & Investments", "Homestead & Lifestyle", "Ideas & Research"])

if tab == "Wealth & Investments":
    st.header("📊 Wealth & Investments")
    name = st.text_input("Investment Name")
    amount = st.number_input("Amount", min_value=0.0)
    if st.button("Add Investment"):
        add_investment(name, amount)
        st.success("Investment added!")
    st.subheader("Your Investments")
    for inv in fetch_all("investments"):
        st.write(f"{inv[1]}: ${inv[2]:,.2f} ({inv[3][:19]})")

elif tab == "Homestead & Lifestyle":
    st.header("🏡 Homestead & Lifestyle")
    project_name = st.text_input("Project Name")
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
    if st.button("Add Project"):
        add_project(project_name, status)
        st.success("Project added!")
    st.subheader("Your Projects")
    for proj in fetch_all("projects"):
        st.write(f"{proj[1]} - {proj[2]} ({proj[3][:19]})")

elif tab == "Ideas & Research":
    st.header("🧠 Ideas & Research")
    idea = st.text_area("New Idea")
    if st.button("Save Idea"):
        add_idea(idea)
        st.success("Idea saved!")
    st.subheader("Saved Ideas")
    for i in fetch_all("ideas"):
        st.write(f"- {i[1]} ({i[2][:19]})")

st.success("✅ AtlasOG is live and storing data in real time!")