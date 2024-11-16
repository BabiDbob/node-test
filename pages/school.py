import streamlit as st
import pandas as pd

# import matplotlib.pyplot as plt

data = pd.read_csv("hospital2.csv")
data

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]

with st.sidebar:
    st.caption(f'{ID}님 접속중')
    
with st.form("input"):
    region = st.multiselect("지역", data['지역'].unique())
    submitted = st.form_submit_button("조회")
    
    if submitted:
        name_list = []
        result = data["병상수"].drop_duplicates().sort_values().reset_index(drop=True)
        for re in region:
            name = f"{re}_"
            name_list.append(name)
            selected_df = data[(data['지역'] == re)]
            selected_df = selected_df[["병상수","의료인수"]].rename(columns={"의료인수": name})
            result = pd.merge(result, selected_df, on='병상수').sort_values('병상수')
        
        st.line_chart(data=result, x='병상수', y=name_list,use_container_width=True)
        