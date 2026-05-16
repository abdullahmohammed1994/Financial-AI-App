import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. إعدادات المنصة الحديثة والمستقرة
st.set_page_config(
    page_title="Financial AI Auditor v5", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. حقن واجهة مستقبلية فاخرة مستقرة (SaaS Dashboard Aesthetics)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
        text-align: right;
        direction: rtl;
    }
    
    [data-testid="stHeader"], footer {visibility: hidden;}
    
    .dashboard-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        text-align: center;
        margin-bottom: 16px;
    }
    .card-title { color: #94a3b8; font-size: 15px; font-weight: 600; margin-bottom: 8px; }
    .card-value { color: #fbbf24; font-size: 30px; font-weight: 800; }
    
    .ai-insight-box {
        background: #0f172a;
        border-right: 5px solid #fbbf24;
        border-radius: 12px;
        padding: 25px;
        color: #e2e8f0;
        font-size: 17px;
        line-height: 1.9;
        margin-top: 25px;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #d97706 0%, #f59e0b 100%) !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 17px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 0px !important;
        width: 100%;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. جلب المفتاح التلقائي من الـ Secrets
secrets_key = st.secrets.get("GEMINI_API_KEY", None)

# ترويسة المنصة الفاخرة
st.markdown("<h1 style='text-align: center; color: #fbbf24; font-weight: 800; margin-top: 20px;'>📊 Financial AI Auditor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>الجيل الخامس والحديث للمراجعة المالية والتحليل الإحصائي الآلي</p>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# كبسولات الاختيار الأنيقة الحديثة
mode = st.radio("حدد نطاق التحليل المطلوب:", ["🔎 معالجة كشوفات سنة منفردة", "⚖️ المقارنة الهيكلية وتحليل التباين بين سنتين"], horizontal=True)
st.markdown("<br>", unsafe_allow_html=True)

def get_financial_value(df, keywords):
    df_lower = df.copy()
    df_lower.iloc[:, 0] = df_lower.iloc[:, 0].astype(str).str.lower()
    for word in keywords:
        mask = df_lower.iloc[:, 0].str.contains(word.lower(), na=False)
        if mask.any():
            row = df.loc[mask].iloc[0]
            for val in row:
                if isinstance(val, (int, float)) and val != 0: return val
    return 0

def calculate_ratios(df):
    rev = get_financial_value(df, ['revenue', 'sales', 'إيرادات', 'مبيعات', 'المبيعات'])
    net_profit = get_financial_value(df, ['net profit', 'net income', 'صافي الربح', 'صافي الدخل'])
    assets = get_financial_value(df, ['assets', 'total assets', 'أصول', 'إجمالي الأصول'])
    liabilities = get_financial_value(df, ['liabilities', 'خصوم', 'التزامات'])
    return {
        "Revenue": rev, "Net Profit": net_profit,
        "Profit Margin": (net_profit / rev * 100) if rev != 0 else 0,
        "Current Ratio": (assets / liabilities) if liabilities != 0 else 0,
        "Debt Ratio": (liabilities / assets * 100) if assets != 0 else 0
    }

# متغير لحمل المفتاح النشط
active_api_key = secrets_key

if mode == "🔎 معالجة كشوفات سنة منفردة":
    file = st.file_uploader("📂 ارفع ملف القائمة المالية", type="xlsx")
    if file:
        df = pd.read_excel(file)
        r = calculate_ratios(df)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f"<div class='dashboard-card'><div class='card-title'>إجمالي الإيرادات</div><div class='card-value'>{r['Revenue']:,.0f}</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='dashboard-card'><div class='card-title'>صافي الربح</div><div class='card-value'>{r['Net Profit']:,.0f}</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='dashboard-card'><div class='card-title'>هامش الربح التشغيلي</div><div class='card-value'>{r['Profit Margin']:.1f}%</div></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='dashboard-card'><div class='card-title'>معدل السيولة المتدا
