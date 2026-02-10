import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Admin Database Viewer", layout="wide")

DB_FILE = "english_learning_db/users_chat.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

st.title("📂 Database Administrator")

if not os.path.exists(DB_FILE):
    st.error(f"Database file not found at {DB_FILE}")
    st.stop()

# 1. Select Table
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]
conn.close()

if not tables:
    st.warning("No tables found in database.")
    st.stop()

table = st.selectbox("Select Table", tables)

# 2. View Data
conn = get_connection()
df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
conn.close()

st.subheader(f"Data in '{table}'")
st.dataframe(df)

# 3. SQL Execution (Advanced)
st.markdown("---")
st.subheader("⚡ Execute SQL Command")
sql_query = st.text_area("SQL Query", f"SELECT * FROM {table} WHERE id = 1")

if st.button("Execute SQL"):
    try:
        conn = get_connection()
        if sql_query.strip().upper().startswith("SELECT"):
            result = pd.read_sql_query(sql_query, conn)
            st.dataframe(result)
        else:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.commit()
            st.success("Query executed successfully!")
            st.rerun()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")
