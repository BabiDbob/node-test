import streamlit as st
import pandas as pd
from pyproj import Proj, transform

# 세션 상태 확인
if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')

# CSV 파일 읽기
data = pd.read_csv("hospital.csv")

st.title('종합병원은 어디있지?')


# 데이터 전처리
data = data.copy().fillna(0)
data["size"] = 5 * data["병상수"]



# 좌표 변환 (EPSG:5179 -> EPSG:4326)
proj_src = Proj(init="epsg:5179")  # 기존 좌표계 (TM)
proj_dst = Proj(init="epsg:4326")  # 위도/경도 (WGS84)

data["latitude"], data["longitude"] = transform(
    proj_src, proj_dst,
    data["좌표정보(x)"].values, data["좌표정보(y)"].values
)

# 데이터 확인
st.dataframe(data)

data["latitude"] = pd.to_numeric(data["latitude"], errors="coerce")
data["longitude"] = pd.to_numeric(data["longitude"], errors="coerce")

# 지도 출력
st.map(data, latitude="latitude", longitude="longitude", size="size")
