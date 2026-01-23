import streamlit as st
import pandas as pd
from datetime import datetime

# 網頁設定：讓表格在手機上更易閱讀
st.set_page_config(page_title="Xpore BMC 行動庫存", layout="wide")

# 強制 CSS 優化手機表格顯示
st.markdown("""
    <style>
    [data-testid="stDataEditor"] { width: 100% !important; }
    .stButton button { width: 100%; border-radius: 10px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# 1. 初始化資料 (從您提供的 BMC 表格提取核心)
if 'inventory' not in st.session_state:
    initial_data = [
        ["P&P", "2024/07/17", "XP2202-601", "G-228", "D240327-01", "L001", "D.NAVY", 27.5, 4.3, "7A-01"],
        ["ARCTERYX", "2024/07/24", "XP2202-401", "Xpore Pro", "D240327-02", "L002", "BLACK", 15.2, 3.1, "7A-02"]
    ]
    st.session_state.inventory = pd.DataFrame(initial_data, columns=[
        "客戶", "日期", "品號", "Model Name", "缸號", "LOT", "顏色", "碼數(YDS)", "淨重(NW)", "庫位"
    ])

# --- 側邊欄：手機選單 ---
with st.sidebar:
    st.title("🟢 Xpore 行動庫存")
    menu = st.radio("功能切換", ["🔍 查詢與修改", "📤 手機匯入 CSV", "💾 存檔至手機/電腦"])

# --- 功能 1：查詢與修改 ---
if menu == "🔍 查詢與修改":
    st.header("📊 庫存看板")
    
    # 搜尋框：手機輸入優化
    search = st.text_input("快速搜尋 (客戶/品號/顏色)", placeholder="輸入關鍵字...")
    
    df = st.session_state.inventory
    if search:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

    # 數據統計
    c1, c2 = st.columns(2)
    c1.metric("總碼數", f"{pd.to_numeric(df['碼數(YDS)'], errors='coerce').sum():,.1f}")
    c2.metric("總淨重", f"{pd.to_numeric(df['淨重(NW)'], errors='coerce').sum():,.1f}")

    st.subheader("點擊下方表格內容可直接修改")
    # 手動修改欄位內容 (動態表格)
    updated_df = st.data_editor(
        df, 
        num_rows="dynamic", 
        use_container_width=True,
        key="mobile_editor"
    )
    
    if st.button("✅ 確認保存所有修改"):
        st.session_state.inventory = updated_df
        st.success("修改已暫存！")

# --- 功能 2：手機匯入 CSV ---
elif menu == "📤 手機匯入 CSV":
    st.header("上傳 CSV 檔案")
    st.write("您可以從手機的『檔案』App 選擇 CSV 匯入。")
    up_file = st.file_uploader("選擇檔案", type="csv")
    if up_file:
        new_data = pd.read_csv(up_file)
        if st.button("覆蓋並更新庫存"):
            st.session_state.inventory = new_data
            st.success("匯入成功！")

# --- 功能 3：持久化存檔 ---
elif menu == "💾 存檔至手機/電腦":
    st.header("下載最新庫存表")
    st.info("因系統重啟資料會重置，請在修改後下載此檔保存。")
    csv_data = st.session_state.inventory.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下載 CSV 到手機存檔",
        data=csv_data,
        file_name=f"BMC_Stock_{datetime.now().strftime('%m%d_%H%M')}.csv",
        mime="text/csv"
    )
