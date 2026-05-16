import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 1. إعدادات الصفحة الفاخرة
st.set_page_config(page_title="Financial AI Auditor | نظام التدقيق الذكي", layout="wide")

# 2. حقن التنسيقات الفاخرة (Luxury Custom CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Poppins:wght@400;600&display=swap');
    
    /* تنسيق الجسم العام */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
        background-color: #f8f9fa;
    }

    /* العناوين */
    h1, h2, h3 {
        color: #0d1b2a !important;
        font-weight: 700 !important;
    }

    /* تنسيق بطاقات المؤشرات (Metric Cards) */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        border-right: 6px solid #d4af37 !important; /* لمسة ذهبية */
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 18px !important;
        color: #415a77 !important;
    }

    /* تنسيق صندوق التقرير الذكي */
    .report-container {
        background-color: #0d1b2a;
        color: #e0e1dd;
        padding: 30px;
        border-radius: 20px;
        border-right: 8px solid #d4af37;
        margin-top: 20px;
        line-height: 1.8;
        font-size: 18px;
        box-shadow: 0 10px 30px rgba(13, 27, 42, 0.2);
    }

    /* الأزرار */
    .stButton>button {
        background-color: #d4af37 !important;
        color: #0d1b2a !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 25px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
    }

    /* شريط الجانب */
    .css-1d391kg { background-color: #0d1b2a !important; }
    .sidebar .sidebar-content { color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- وظائف المحرك المالي ---
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
    net_profit = get_financial_value(df, ['net profit', 'net income', 'صافي الربح', 'صافي الدخل', 'الربح الصافي'])
    assets = get_financial_value(df, ['assets', 'total assets', 'أصول', 'إجمالي الأصول'])
    liabilities = get_financial_value
