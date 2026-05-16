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
    liabilities = get_financial_value(df, ['liabilities', 'خصوم', 'التزامات'])
    return {
        "Revenue": rev, "Net Profit": net_profit,
        "Profit Margin": (net_profit / rev * 100) if rev != 0 else 0,
        "Current Ratio": (assets / liabilities) if liabilities != 0 else 0,
        "Debt Ratio": (liabilities / assets * 100) if assets != 0 else 0
    }

# --- واجهة المستخدم ---
st.title("🏦 Financial AI Auditor")
st.subheader("نظام الرقابة المالية الذكي | الاستشارات الاستراتيجية الآلية")
st.markdown("---")

# القائمة الجانبية الفاخرة
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100)
    st.header("لوحة التحكم")
    api_key = st.text_input("🔑 مفتاح API الخاص بك", type="password")
    mode = st.radio("📊 نمط العمل:", ["تحليل مفرد", "مقارنة سنتين"])
    st.markdown("---")
    st.info("النظام يدعم تحليل كشوف الدخل والميزانيات باللغتين العربية والإنجليزية.")

if mode == "تحليل مفرد":
    file = st.file_uploader("📂 ارفع القائمة المالية (xlsx)", type="xlsx")
    if file and api_key:
        df = pd.read_excel(file)
        r = calculate_ratios(df)
        
        # عرض المؤشرات في بطاقات فاخرة
        st.markdown("### 📈 نبذة عن الأداء المالي")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("الإيرادات", f"{r['Revenue']:,.0f}")
        c2.metric("صافي الربح", f"{r['Net Profit']:,.0f}")
        c3.metric("هامش الربح", f"{r['Profit Margin']:.1f}%")
        c4.metric("نسبة السيولة", f"{r['Current Ratio']:.2f}")

        # الرسم البياني الفاخر
        fig = px.bar(x=['الإيرادات', 'صافي الربح'], y=[r['Revenue'], r['Net Profit']], 
                     color=['إيرادات', 'ربح'], color_discrete_map={'إيرادات':'#415a77', 'ربح':'#d4af37'})
        fig.update_layout(plot_bgcolor='white', title="هيكل الأرباح والإيرادات")
        st.plotly_chart(fig, use_container_width=True)

        if st.button("توليد التقرير التنفيذي 🤖"):
            # طلب Gemini
            prompt = f"حلل مالياً بالعربية كخبير CFO: إيرادات {r['Revenue']}، ربح {r['Net Profit']}، هامش {r['Profit Margin']:.1f}%."
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
            st.markdown(f"<div class='report-container'><h3>📝 تقرير الخبير المالي:</h3>{res.json()['candidates'][0]['content']['parts'][0]['text']}</div>", unsafe_allow_html=True)

else:
    # نمط المقارنة
    col1, col2 = st.columns(2)
    with col1: f1 = st.file_uploader("📂 ملف السنة السابقة", type="xlsx")
    with col2: f2 = st.file_uploader("📂 ملف السنة الحالية", type="xlsx")
    
    if f1 and f2 and api_key:
        df1, df2 = pd.read_excel(f1), pd.read_excel(f2)
        r1, r2 = calculate_ratios(df1), calculate_ratios(df2)
        
        st.markdown("### ⚖️ مقارنة الأداء السنوي (Variance Analysis)")
        m1, m
