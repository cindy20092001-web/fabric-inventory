import streamlit as st
import pandas as pd
import io

# 網頁基礎設定
st.set_page_config(page_title="Xpore BMC 庫存管理系統", layout="wide")

# --- 1. 資料初始化 ---
if 'inventory' not in st.session_state:
    # 這裡放您的初始資料 (P&P, ARCTERYX 等)
    initial_data = [
        ["P&P", "2024/07/17", "XP2202-601", "G-228", "D240327-01", "L001", "D.NAVY", 27.5, 4.3, "7A-01"],
        ["ARCTERYX", "2024/07/24", "XP2202-401", "Xpore Pro", "D240327-02", "L002", "BLACK", 15.2, 3.1, "7A-02"]
    ]
    st.session_state.inventory = pd.DataFrame(initial_data, columns=[
        "客戶", "日期", "品號", "Model Name", "缸號", "LOT", "顏色", "碼數(YDS)", "淨重(NW)", "庫位"
    ])

# --- 2. 側邊欄 ---
with st.sidebar:
    st.title("🟢 Xpore BMC")
    menu = st.radio("功能選單", ["📊 庫存看板與編輯", "📤 批量匯入 CSV", "💾 備份資料庫"])

# --- 3. 庫存看板與手動編輯 ---
if menu == "📊 庫存看板與編輯":
    st.header("庫存實時看板 (可直接雙擊單格進行修改)")
    
    # 顯示編輯器
    edited_df = st.data_editor(
        st.session_state.inventory, 
        num_rows="dynamic", 
        use_container_width=True,
        key="main_editor"
    )
    
    # 更新暫存
    if st.button("確認保存修改 (暫存至網頁)"):
        st.session_state.inventory = edited_df
        st.success("暫存成功！注意：若伺服器重啟，請確保您已執行『備份資料庫』。")

    # 快速統計
    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("總碼數 (YDS)", f"{pd.to_numeric(edited_df['碼數(YDS)'], errors='coerce').sum():,.1f}")
    c2.metric("總淨重 (NW)", f"{pd.to_numeric(edited_df['淨重(NW)'], errors='coerce').sum():,.1f}")

# --- 4. 備份功能 (取代 Google Drive) ---
elif menu == "💾 備份資料庫":
    st.header("資料持久化備份")
    st.info("由於公司系統攔截雲端硬碟，請定期將編輯後的資料下載備份。")
    
    # 將 DataFrame 轉為 CSV 字串
    csv = st.session_state.inventory.to_csv(index=False).encode('utf-8-sig')
    
    st.download_button(
        label="📥 下載目前最新庫存表 (.csv)",
        data=csv,
        file_name=f"BMC_Inventory_Backup_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
    st.write("💡 下次開啟網頁時，您可以透過『批量匯入』功能將此檔案傳回系統。")

# --- 5. 批量匯入 ---
elif menu == "📤 批量匯入 CSV":
    st.header("匯入舊有/備份資料")
    uploaded_file = st.file_uploader("選擇之前的備份檔或新的庫存表", type="csv")
    if uploaded_file:
        imported_df = pd.read_csv(uploaded_file)
        if st.button("覆蓋並更新系統資料"):
            st.session_state.inventory = imported_df
            st.success("資料庫已更新！")
