import streamlit as st
import pandas as pd

# 網頁基礎設定
st.set_page_config(page_title="Xpore BMC 庫存管理系統", layout="wide")

# 自定義介面樣式
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    .stMetric { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-bottom: 4px solid #10b981; }
    </style>
    """, unsafe_allow_html=True)

# 1. 建立初始庫存資料庫 (從您的 CSV 提取)
if 'inventory' not in st.session_state:
    raw_data = [
        ["P&P", "2024/7/17", "XP2202-601", "G-228", "D240327-01", "D240327-01", "L001", "D.NAVY", 27.5, 4.3, "7A-01"],
        ["ARCTERYX", "2024/7/24", "XP2202-401", "Xpore Pro", "D240327-02", "D240327-02", "L002", "BLACK", 15.2, 3.1, "7A-02"],
        ["POLARTEC", "2024/8/12", "XP2401-201", "Xpore Air", "D240515-01", "D240515-01", "L003", "GREY", 45.0, 7.8, "8B-05"],
        ["P&P", "2024/9/05", "XP2202-601", "G-228", "D240601-01", "D240601-01", "L004", "D.NAVY", 30.1, 4.8, "7A-01"],
        ["SALOMON", "2024/10/20", "XP2305-110", "G-500", "D240812-05", "D240812-05", "L005", "BLUE", 55.4, 9.2, "9C-12"]
    ]
    
    st.session_state.inventory = pd.DataFrame(raw_data, columns=[
        "客戶", "日期", "品號", "Model Name", "缸號(表)", "缸號(底)", "LOT", "顏色", "碼數(YDS)", "淨重(NW)", "庫位"
    ])

# --- 側邊欄 ---
with st.sidebar:
    st.title("🟢 Xpore BMC")
    st.write("成布庫存數位化系統")
    st.divider()
    menu = st.radio("功能選單", ["📊 庫存實時看板", "📦 手動入庫/出庫", "📤 批量匯入 CSV"])

# --- 功能區：庫存實時看板 ---
if menu == "📊 庫存實時看板":
    st.header("庫存實時看板")
    
    df = st.session_state.inventory
    
    # 搜尋與過濾
    search = st.text_input("🔍 搜尋客戶、品號、缸號或顏色...", placeholder="輸入關鍵字...")
    if search:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

    # 頂部統計指標
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("搜尋結果總疋數", len(df))
    col2.metric("總碼數 (YDS)", f"{df['碼數(YDS)'].sum():,.1f}")
    col3.metric("總淨重 (NW)", f"{df['淨重(NW)'].sum():,.1f}")
    col4.metric("品項總數", len(df['Model Name'].unique()))

    st.divider()
    
    # 顯示主表格
    st.dataframe(df, use_container_width=True, height=600)

# --- 功能區：手動作業 ---
elif menu == "📦 手動入庫/出庫":
    st.header("手動更新庫存")
    with st.form("manual_entry"):
        c1, c2, c3 = st.columns(3)
        new_cust = c1.text_input("客戶名稱")
        new_model = c2.text_input("Model Name")
        new_color = c3.text_input("顏色")
        
        c4, c5, c6 = st.columns(3)
        new_yds = c4.number_input("碼數 (YDS)", min_value=0.0)
        new_nw = c5.number_input("淨重 (NW)", min_value=0.0)
        new_loc = c6.text_input("庫位")
        
        if st.form_submit_button("確認入庫"):
            new_row = pd.DataFrame([[new_cust, pd.Timestamp.now().strftime("%Y/%m/%d"), "", new_model, "", "", "", new_color, new_yds, new_nw, new_loc]], columns=df.columns)
            st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
            st.success("入庫資料已更新！")

# --- 功能區：批量匯入 ---
elif menu == "📤 批量匯入 CSV":
    st.header("CSV 批量匯入作業")
    uploaded_file = st.file_uploader("請上傳您的庫存 CSV 檔案", type="csv")
    if uploaded_file:
        st.success("檔案已讀取！(此功能可根據您的 CSV 欄位進一步客製化)")
