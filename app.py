import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 1. إعدادات المنصة الحديثة والمستقرة
st.set_page_config(
    page_title="Financial AI Auditor v5", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. حقن تصميم مستقبلي فاخر مستقر (SaaS Dashboard Aesthetics)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
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

# 3. جلب المفتاح بأمان من الـ Secrets
api_key = st.secrets.get("GEMINI_API_KEY", None)

# ترويسة المنصة الفاخرة
st.markdown("<h1 style='text-align: center; color: #fbbf24; font-weight: 800; margin-top: 20px;'>📊 Financial AI Auditor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>الجيل الخامس والحديث للمراجعة المالية والتحليل الإحصائي الآلي</p>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# كبسولات الاختيار الأنيقة الحديثة
mode = st.radio("حدد نطاق التحليل المطلوب:", ["🔎 معالجة كشوفات سنة منفردة", "⚖️ المقارنة الهيكلية وتحليل التباين بين سنتين"], horizontal=True)
st.markdown("<br>", unsafe_allow_html=True)

# وظائف محرك المعالجة المالي بالبايثون
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

# --- تشغيل الأنماط المحدثة ---
if mode == "🔎 معالجة كشوفات سنة منفردة":
    file = st.file_uploader("📂 ارفع ملف القائمة المالية", type="xlsx")
    if file:
        df = pd.read_excel(file)
        r = calculate_ratios(df)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f"<div class='dashboard-card'><div class='card-title'>إجمالي الإيرادات</div><div class='card-value'>{r['Revenue']:,.0f}</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='dashboard-card'><div class='card-title'>صافي الربح</div><div class='card-value'>{r['Net Profit']:,.0f}</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='dashboard-card'><div class='card-title'>هامش الربح التشغيلي</div><div class='card-value'>{r['Profit Margin']:.1f}%</div></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='dashboard-card'><div class='card-title'>معدل السيولة المتداولة</div><div class='card-value'>{r['Current Ratio']:.2f}</div></div>", unsafe_allow_html=True)

        fig = px.bar(x=['الإيرادات', 'صافي الربح'], y=[r['Revenue'], r['Net Profit']], color=['الإيرادات', 'صافي الربح'], color_discrete_sequence=['#475569', '#fbbf24'])
        fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        if st.button("توليد الرؤية والتحليل الاستراتيجي الفوري 🤖"):
            if api_key:
                # الرابط الرسمي المصحح والمحدث لتجنب خطأ 404
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                payload = {"contents": [{"parts": [{"text": f"حلل مالياً بالعربية كخبير CFO محترف جداً: إيرادات {r['Revenue']}، ربح {r['Net Profit']}، هامش {r['Profit Margin']:.1f}%."}]}]}
                
                try:
                    res = requests.post(url, json=payload, headers=headers)
                    if res.status_code == 200:
                        st.markdown(f"<div class='ai-insight-box'><h3>📋 مخرجات تقرير الذكاء الاصطناعي:</h3>{res.json()['candidates'][0]['content']['parts'][0]['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"جوجل ترفض المفتاح. رمز الخطأ من السيرفر: {res.status_code}. يرجى مراجعة إعدادات Secrets.")
                except:
                    st.error("فشل محرك الاستعلام المالي، يرجى مراجعة الاتصال.")
            else:
                st.error("⚠️ لم يتم العثور على مفتاح الـ API المشفر في إعدادات السيرفر السريّة.")

else:
    c_col1, c_col2 = st.columns(2)
    with c_col1: f1 = st.file_uploader("📂 ملف السنة السابقة", type="xlsx", key="prev_year")
    with c_col2: f2 = st.file_uploader("📂 ملف السنة الحالية", type="xlsx", key="curr_year")
    
    if f1 and f2:
        df1, df2 = pd.read_excel(f1), pd.read_excel(f2)
        r1, r2 = calculate_ratios(df1), calculate_ratios(df2)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f"<div class='dashboard-card'><div class='card-title'>نمو صافي الأرباح</div><div class='card-value'>{r2['Net Profit'] - r1['Net Profit']:+,.0f}</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='dashboard-card'><div class='card-title'>انحراف هامش الربح</div><div class='card-value'>{r2['Profit Margin'] - r1['Profit Margin']:+.1f}%</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='dashboard-card'><div class='card-title'>تغير كفاءة السيولة</div><div class='card-value'>{r2['Current Ratio'] - r1['Current Ratio']:+.2f}</div></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='dashboard-card'><div class='card-title'>معدل مديونية الحالية</div><div class='card-value'>{r2['Debt Ratio']:.1f}%</div></div>", unsafe_allow_html=True)

        comp_df = pd.DataFrame({
            'البند المالي': ['الإيرادات', 'صافي الربح'],
            'السنة السابقة': [r1['Revenue'], r1['Net Profit']],
            'السنة الحالية': [r2['Revenue'], r2['Net Profit']]
        }).melt(id_vars='البند المالي', var_name='الفترة الزمنية', value_name='القيمة المالية')
        
        fig = px.bar(comp_df, x='البند المالي', y='القيمة المالية', color='الفترة الزمنية', barmode='group', color_discrete_sequence=['#475569', '#fbbf24'])
        fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        if st.button("بدء تحليل التباين والنمو الهيكلي 🚀"):
            if api_key:
                # الرابط الرسمي المصحح والمحدث لتجنب خطأ 404
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                payload = {"contents": [{"parts": [{"text": f"قارن بالعربية كخبير CFO: السنة الماضية ربح {r1['Net Profit']} الحالية {r2['Net Profit']}."}]}]}
                
                try:
                    res = requests.post(url, json=payload, headers=headers)
                    if res.status_code == 200:
                        st.markdown(f"<div class='ai-insight-box'><h3>📋 التقرير المقارن التحليلي للنمو:</h3>{res.json()['candidates'][0]['content']['parts'][0]['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"جوجل ترفض المفتاح. رمز الخطأ من السيرفر: {res.status_code}. يرجى مراجعة إعدادات Secrets.")
                except:
                    st.error("فشل محرك الاستعلام المالي، يرجى مراجعة الاتصال.")
            else:
                st.error("⚠️ لم يتم العثور على مفتاح الـ API المشفر في إعدادات السيرفر السريّة.")
