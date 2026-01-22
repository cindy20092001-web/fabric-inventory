import streamlit as st
import pandas as pd

# 設定網頁標籤
st.set_page_config(page_title="Xpore BMC 庫存管理系統", layout="wide")

# 自定義 CSS (保留您 HTML 中的專業配色)
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    .stMetric { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-bottom: 4px solid #10b981; }
    </style>
    """, unsafe_allow_html=True)

# 1. 初始化資料庫 (欄位對齊您的 HTML/Excel 邏輯)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=[
        "客戶", "日期", "品號", "Model Name", "缸號", "LOT", "顏色", "碼數(YDS)", "淨重(NW)", "庫位"
    ])

# --- 側邊欄 ---
with st.sidebar:
    st.title("🟢 Xpore BMC")
    st.write("成布庫存數位化系統")
    st.divider()
    menu = st.radio("功能選單", ["庫存實時看板", "手動入庫/出庫", "批量 CSV 匯入"])

# --- 主畫面邏輯 ---
if menu == "庫存實時看板":
    st.header("📊 庫存實時看板")
    
    # 搜尋功能
    search_col1, search_col2 = st.columns([2, 1])
    query = search_col1.text_input("🔍 搜尋客戶、品號、缸號或顏色...")
    
    # 過濾資料
    df = st.session_state.inventory
    if query:
        df = df[df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]

    # 數據看板 (對齊您的 4 個 Card)
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("搜尋結果總疋數", len(df))
    s2.metric("總碼數 (Yds)", f"{df['碼數(YDS)'].sum():,.1f}")
    s3.metric("總淨重 (NW/kg)", f"{df['淨重(NW)'].sum():,.1f}")
    s4.metric("品項總數", len(df['Model Name'].unique()))

    st.divider()
    st.dataframe(df, use_container_width=True, height=500)

elif menu == "手動入庫/出庫":
    st.header("📦 庫存異動操作")
    with st.form("manual_form"):
        c1, c2, c3 = st.columns(3)
        cust = c1.text_input("客戶")
        model = c2.text_input("Model Name")
        color = c3.text_input("顏色")
        
        c4, c5, c6 = st.columns(3)
        lot = c4.text_input("LOT 號")
        yds = c5.number_input("碼數 (YDS)", min_value=0.0)
        nw = c6.number_input("淨重 (NW)", min_value=0.0)
        
        op = st.selectbox("操作類型", ["新增入庫", "出庫扣除"])
        submit = st.form_submit_button("確認執行")
        
        if submit:
            if op == "新增入庫":
                new_data = {
                    "客戶": cust, "日期": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "Model Name": model, "顏色": color, "LOT": lot, 
                    "碼數(YDS)": yds, "淨重(NW)": nw
                }
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_data])], ignore_index=True)
                st.success("入庫成功！")
            else:
                st.warning("出庫功能將根據 LOT 號比對扣除（開發中）")

elif menu == "批量 CSV 匯入":
    st.header("📤 匯入 CSV 庫存表")
    uploaded_file = st.file_uploader("請選擇 CSV 檔案", type="csv")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        # 這裡可以根據您 HTML 中的 cols[0], cols[11] 等邏輯進行欄位映射
        st.write("預覽匯入資料：")
        st.dataframe(new_df.head())
        if st.button("確認合併至系統"):
            st.session_state.inventory = pd.concat([st.session_state.inventory, new_df], ignore_index=True)
            st.success("資料已匯入！")
