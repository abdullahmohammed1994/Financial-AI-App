import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 1. إعدادات الصفحة والجماليات
st.set_page_config(page_title="المحلل المالي الاحترافي v3", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 نظام الرقابة والتحليل المالي المتكامل")
st.write("تحليل احترافي، رسوم بيانية مقارنة، وحساب تلقائي للمؤشرات المالية.")

# 2. القائمة الجانبية
api_key = st.sidebar.text_input("🔑 مفتاح API الخاص بك", type="password")
st.sidebar.markdown("---")
st.sidebar.info("هذا النظام يدعم مقارنة فترتين زمنيتين واستخراج نسب الربحية والسيولة تلقائياً.")

# 3. وظائف الحسابات المالية الذكية
def get_financial_value(df, keywords):
    """البحث عن قيم مالية بناءً على كلمات دلالية بالعربي والإنجليزي"""
    df_lower = df.copy()
    df_lower.iloc[:, 0] = df_lower.iloc[:, 0].astype(str).str.lower()
    for word in keywords:
        mask = df_lower.iloc[:, 0].str.contains(word.lower(), na=False)
        if mask.any():
            # البحث عن أول قيمة رقمية في السطر
            row = df.loc[mask].iloc[0]
            for val in row:
                if isinstance(val, (int, float)) and val != 0:
                    return val
    return 0

def calculate_ratios(df):
    rev = get_financial_value(df, ['revenue', 'sales', 'إيرادات', 'مبيعات'])
    net_profit = get_financial_value(df, ['net profit', 'net income', 'صافي الربح', 'صافي الدخل'])
    assets = get_financial_value(df, ['assets', 'total assets', 'أصول', 'إجمالي الأصول'])
    liabilities = get_financial_value(df, ['liabilities', 'خصوم', 'التزامات'])
    
    ratios = {
        "Revenue": rev,
        "Net Profit": net_profit,
        "Profit Margin": (net_profit / rev * 100) if rev != 0 else 0,
        "Current Ratio": (assets / liabilities) if liabilities != 0 else 0,
        "Debt Ratio": (liabilities / assets * 100) if assets != 0 else 0
    }
    return ratios

# 4. رفع الملفات
col_f1, col_f2 = st.columns(2)
with col_f1:
    file1 = st.file_uploader("📂 ملف الفترة السابقة (مثلاً 2024)", type="xlsx", key="f1")
with col_f2:
    file2 = st.file_uploader("📂 ملف الفترة الحالية (مثلاً 2025)", type="xlsx", key="f2")

if file1 and file2 and api_key:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    # حساب النسب للفترتين
    r1 = calculate_ratios(df1)
    r2 = calculate_ratios(df2)
    
    # 5. عرض بطاقات المؤشرات (Metric Cards)
    st.markdown("### 📈 المؤشرات المالية الرئيسية (Key Metrics)")
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric("هامش الربح", f"{r2['Profit Margin']:.1f}%", f"{r2['Profit Margin'] - r1['Profit Margin']:.1f}%")
    m2.metric("نسبة السيولة", f"{r2['Current Ratio']:.2f}", f"{r2['Current Ratio'] - r1['Current Ratio']:.2f}")
    m3.metric("نسبة المديونية", f"{r2['Debt Ratio']:.1f}%", f"{r2['Debt Ratio'] - r1['Debt Ratio']:.1f}%", delta_color="inverse")
    m4.metric("صافي الربح", f"{r2['Net Profit']:,.0f}", f"{r2['Net Profit'] - r1['Net Profit']:,.0f}")

    # 6. الرسوم البيانية المقارنة
    st.markdown("---")
    st.markdown("### 📊 التحليل البياني المقارن")
    
    compare_data = pd.DataFrame({
        'المؤشر': ['الإيرادات', 'صافي الربح'],
        'الفترة السابقة': [r1['Revenue'], r1['Net Profit']],
        'الفترة الحالية': [r2['Revenue'], r2['Net Profit']]
    }).melt(id_vars='المؤشر', var_name='الفترة', value_name='المبلغ')
    
    fig = px.bar(compare_data, x='المؤشر', y='المبلغ', color='الفترة', barmode='group', 
                 text_auto='.2s', color_discrete_sequence=['#AEC6CF', '#1f77b4'])
    st.plotly_chart(fig, use_container_width=True)

    # 7. تحليل الذكاء الاصطناعي العميق
    if st.button("توليد التقرير الاستراتيجي بواسطة Gemini 🤖"):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        prompt = f"""
        أنت مستشار مالي (CFO). حلل هذه النسب المحسوبة بدقة وقارن بين الفترتين:
        
        الفترة السابقة: ربح {r1['Net Profit']}، هامش ربح {r1['Profit Margin']:.1f}%، سيولة {r1['Current Ratio']:.2f}، مديونية {r1['Debt Ratio']:.1f}%.
        الفترة الحالية: ربح {r2['Net Profit']}، هامش ربح {r2['Profit Margin']:.1f}%، سيولة {r2['Current Ratio']:.2f}، مديونية {r2['Debt Ratio']:.1f}%.
        
        المطلوب:
        - تحليل أداء الربحية والنمو.
        - تقييم المخاطر بناءً على نسب السيولة والمديونية.
        - نصيحة استراتيجية واحدة للمستقبل.
        - اجعل التقرير باللغة العربية، احترافياً ومختصراً.
        """
        
        with st.spinner('جاري صياغة التقرير الاستراتيجي...'):
            try:
                response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if response.status_code == 200:
                    st.markdown("---")
                    st.subheader("📝 رؤية الخبير (AI Insights)")
                    st.info(response.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error("فشل الاتصال بـ Gemini. يرجى التحقق من المفتاح.")
            except:
                st.error("حدث خطأ فني في الاتصال.")
