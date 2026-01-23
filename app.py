import streamlit as st
import pandas as pd

# 基礎設定
st.set_page_config(page_title="Xpore BMC", layout="wide")

# 初始化數據 (確保絕對不會報錯的寫法)
if 'inventory' not in st.session_state:
    try:
        # 直接寫入幾筆您的 CSV 內容作為預設
        data = [
            ["ZHIK", "系統", "OD007-NA", "卡其", "R1B19D", 12.0, 2.5, "F101"],
            ["宏良", "系統", "OD019-NA", "咖啡", "R1C20D", 5.0, 1.2, "F105"]
        ]
        st.session_state.inventory = pd.DataFrame(data, columns=["客戶", "日期", "Model Name", "顏色", "LOT", "碼數", "淨重", "庫位"])
    except:
        st.session_state.inventory = pd.DataFrame(columns=["客戶", "日期", "Model Name", "顏色", "LOT", "碼數", "淨重", "庫位"])

# 介面顯示
st.title("🟢 Xpore BMC 行動庫存系統")

tab1, tab2 = st.tabs(["🔍 查詢與修改", "📤 匯入/備份"])

with tab1:
    search = st.text_input("搜尋內容")
    # 使用 st.data_editor 讓手機也可以直接點擊修改
    edited = st.data_editor(st.session_state.inventory, num_rows="dynamic", use_container_width=True)
    if st.button("儲存修改"):
        st.session_state.inventory = edited
        st.success("已儲存！")

with tab2:
    up = st.file_uploader("匯入 CSV", type="csv")
    if up:
        st.session_state.inventory = pd.read_csv(up)
        st.success("匯入完成")
