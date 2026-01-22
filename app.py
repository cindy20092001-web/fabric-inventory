import streamlit as st
import pandas as pd

# 網頁基礎設定
st.set_page_config(page_title="機能織材庫存系統", layout="wide")

# 1. 模擬資料庫 (未來可擴充為真實資料庫)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "客戶": ["Nike", "Adidas", "A公司", "B貿易"],
        "款式編號": ["WP-01", "GT-02", "SL-03", "WP-02"],
        "布料描述": ["3層貼合防水", "彈性透氣網布", "平織防潑水", "2.5層輕量防水"],
        "顏色": ["海軍藍", "黑色", "白色", "深灰"],
        "疋數(Rolls)": [10, 5, 12, 8],
        "總碼數(Yds)": [500, 250, 600, 400],
        "規格(WP/MVP)": ["10k/10k", "N/A", "5k/5k", "20k/15k"]
    })

# 2. 標題與側邊欄搜尋
st.title("🧵 機能織材與團服庫存管理系統")

st.sidebar.header("🔍 搜尋篩選")
search_cust = st.sidebar.text_input("搜尋客戶")
search_fabric = st.sidebar.text_input("搜尋款式/描述")
search_color = st.sidebar.text_input("搜尋顏色")

# 執行過濾
df = st.session_state.data
if search_cust: df = df[df['客戶'].str.contains(search_cust)]
if search_fabric: df = df[df['款式編號'].str.contains(search_fabric) | df['布料描述'].str.contains(search_fabric)]
if search_color: df = df[df['顏色'].str.contains(search_color)]

# 3. 視覺化統計卡片
c1, c2, c3 = st.columns(3)
c1.metric("在庫款式數", len(df))
c2.metric("布疋總數 (Rolls)", int(df["疋數(Rolls)"].sum()))
c3.metric("總碼數 (Yds)", f"{df['總碼數(Yds)'].sum():,.0f}")

st.divider()

# 4. 功能分頁
tab1, tab2, tab3 = st.tabs(["📋 庫存明細", "📦 出入庫作業", "📥 批量匯入"])

with tab1:
    st.dataframe(df, use_container_width=True)

with tab2:
    with st.form("inventory_form"):
        col1, col2, col3 = st.columns(3)
        action = col1.selectbox("操作類型", ["入庫", "出庫"])
        item = col2.selectbox("選擇款式", st.session_state.data["款式編號"].unique())
        qty = col3.number_input("變更疋數", min_value=1)
        if st.form_submit_button("確認提交"):
            st.success(f"已完成 {item} 的 {action} 作業 ({qty} 疋)")

with tab3:
    st.file_uploader("匯入 Packing List (Excel/CSV)", type=["xlsx", "csv"])
