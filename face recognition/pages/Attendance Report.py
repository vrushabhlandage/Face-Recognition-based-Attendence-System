import streamlit as st
import sqlite3
import pandas as pd
import datetime

conn = sqlite3.connect('database.db', check_same_thread=False)

c = conn.cursor()

st.title("Attendance Report")

enter_date = st.date_input("Select Date", datetime.date.today())

#
# def function_delete_duplicate():
#     # c.execute('DELETE FROM attendance WHERE id NOT IN (SELECT MAX(id) id FROM attendance GROUP BY name, dt, tm)')
#     # c.execute('SELECT DISTINCT id,name,dt,tm FROM attendance;')
#     c.execute('DELETE FROM attendance WHERE id = 5')
#     # DELETE FROM DETAILS WHERE SN NOT IN(SELECT MAX(SN) FROM DETAILS GROUP BY EMPNAME, DEPT, CONTACTNO, CITY)
#     conn.commit()


def function_view_data(enter_date):
    c.execute('SELECT * FROM attendance WHERE dt = ?', (enter_date,))
    data = c.fetchall()
    # st.write(data)
    df = pd.DataFrame(data, columns=['ID', 'NAME', 'DATE', 'TIME'])
    st.dataframe(df)


if enter_date is not None:
    # function_delete_duplicate()
    function_view_data(enter_date)
