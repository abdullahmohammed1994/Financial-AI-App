import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 1. إعدادات الصفحة والتصميم اللغوي
st.set_page_config(page_title="منصة الرقابة المالية الذكية v4", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stMetric { background-color: #f8f9fa; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); border: 1px solid #e9ecef; }
    .report-box { background-color: #eef2f7; padding: 20px; border-radius: 10px; border-right: 5px solid #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 المنصة المتطورة للتدقيق والتحليل المالي")
st.write("نظام ذكي مرن يمنحك القدرة على تحليل سنة مالية منفردة أو إجراء مقارنة هيكلية بين فترتين.")

# 2. القائمة الجانبية الذكية
st.sidebar.header("🛠️ لوحة التحكم والإعدادات")
api_key = st.sidebar.text_input("🔑 مفتاح API الخاص بك (Gemini)", type="password")

st.sidebar.markdown("---")
# اختيار نمط التحليل
analysis_mode = st.sidebar.radio(
    "📊 اختر نمط التحليل المالي:",
    ["تحليل سنة واحدة فقط", "مقارنة بين سنتين ماليتين"]
)

# 3. محرك البحث الذكي عن الحسابات
def get_financial_value(df, keywords):
    df_lower = df.copy()
    df_lower.iloc[:, 0] = df_lower.iloc[:, 0].astype(str).str.lower()
    for word in keywords:
        mask = df_lower.iloc[:, 0].str.contains(word.lower(), na=False)
        if mask.any():
            row = df.loc[mask].iloc[0]
            for val in row:
                if isinstance(val, (int, float)) and val != 0:
                    return val
    return 0

def calculate_ratios(df):
    rev = get_financial_value(df, ['revenue', 'sales', 'إيرادات', 'مبيعات', 'المبيعات'])
    net_profit = get_financial_value(df, ['net profit', 'net income', 'صافي الربح', 'صافي الدخل', 'الربح الصافي'])
    assets = get_financial_value(df, ['assets', 'total assets', 'أصول', 'إجمالي الأصول', 'الأصول'])
    liabilities = get_financial_value(df, ['liabilities', 'total liabilities', 'خصوم', 'التزامات', 'إجمالي الالتزامات'])
    
    return {
        "Revenue": rev,
        "Net Profit": net_profit,
        "Profit Margin": (net_profit / rev * 100) if rev != 0 else 0,
        "Current Ratio": (assets / liabilities) if liabilities != 0 else 0,
        "Debt Ratio": (liabilities / assets * 100) if assets != 0 else 0
    }

# 4. معالجة الواجهات بناءً على النمط المختار
if analysis_mode == "تحليل سنة واحدة فقط":
    file = st.file_uploader("📂 ارفع القائمة المالية للسنة المستهدفة (xlsx)", type="xlsx")
    
    if file and api_key:
        df = pd.read_excel(file)
        r = calculate_ratios(df)
        
        tab1, tab2 = st.tabs(["📋 معاينة الجدول", "📊 المؤشرات والتقرير الذكي"])
        
        with tab1:
            st.dataframe(df.head(15), use_container_width=True)
            
        with tab2:
            st.markdown("### 📈 المؤشرات المالية المستخرجة")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("إجمالي الإيرادات", f"{r['Revenue']:,.0f}")
            m2.metric("صافي الدخل", f"{r['Net Profit']:,.0f}")
            m3.metric("هامش الربح التشغيلي", f"{r['Profit Margin']:.1f}%")
            m4.metric("نسبة السيولة الحالية", f"{r['Current Ratio']:.2f}")
            
            # رسم بياني أحادي
            st.markdown("---")
            fig = px.bar(x=['الإيرادات', 'صافي الربح'], y=[r['Revenue'], r['Net Profit']], 
                         labels={'x': 'البند المالي', 'y': 'المبلغ'}, title="حجم الأداء المالي للنظام",
                         color_discrete_sequence=['#2ca02c'])
            st.plotly_chart(fig, use_container_width=True)
            
            if st.button("توليد الاستشارة المالية الذكية 🤖"):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                prompt = f"أنت مستشار مالي خبير. حلل هذه المؤشرات لسنة واحدة وقدم نصيحة استراتيجية سريعة ونقاط القوة والضعف بالعربية: إيرادات {r['Revenue']}، صافي ربح {r['Net Profit']}، هامش {r['Profit Margin']:.1f}%، سيولة {r['Current Ratio']:.2f}."
                
                with st.spinner('جاري قراءة المعطيات وصياغة التقرير...'):
                    try:
                        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                        st.markdown("<div class='report-box'><h3>📝 التقرير الاستراتيجي للسنة المالية:</h3>" + response.json()['candidates'][0]['content']['parts'][0]['text'] + "</div>", unsafe_allow_html=True)
                    except:
                        st.error("فشل في الاتصال بمحرك الاستشارة.")

else:
    # نمط المقارنة بين سنتين
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        file1 = st.file_uploader("📂 ملف السنة السابقة (مثلاً 2024)", type="xlsx", key="f1")
    with col_f2:
        file2 = st.file_uploader("📂 ملف السنة الحالية (مثلاً 2025)", type="xlsx", key="f2")
        
    if file1 and file2 and api_key:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        r1 = calculate_ratios(df1)
        r2 = calculate_ratios(df2)
        
        tab1, tab2 = st.tabs(["📋 معاينة ومقارنة الجداول", "⚖️ لوحة مؤشرات الأداء المقارن"])
        
        with tab1:
            c1, c2 = st.columns(2)
            c1.write("### بيانات السنة السابقة:")
            c1.dataframe(df1.head(10), use_container_width=True)
            c2.write("### بيانات السنة الحالية:")
            c2.dataframe(df2.head(10), use_container_width=True)
            
        with tab2:
            st.markdown("### 📈 التغير في المؤشرات الرئيسية (Variance)")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("هامش الربح", f"{r2['Profit Margin']:.1f}%", f"{r2['Profit Margin'] - r1['Profit Margin']:.1f}%")
            m2.metric("نسبة السيولة", f"{r2['Current Ratio']:.2f}", f"{r2['Current Ratio'] - r1['Current Ratio']:.2f}")
            m3.metric("نسبة المديونية", f"{r2['Debt Ratio']:.1f}%", f"{r2['Debt Ratio'] - r1['Debt Ratio']:.1f}%", delta_color="inverse")
            m4.metric("صافي الربح", f"{r2['Net Profit']:,.0f}", f"{r2['Net Profit'] - r1['Net Profit']:,.0f}")
            
            st.markdown("---")
            compare_data = pd.DataFrame({
                'المؤشر': ['الإيرادات', 'صافي الربح'],
                'السنة السابقة': [r1['Revenue'], r1['Net Profit']],
                'السنة الحالية': [r2['Revenue'], r2['Net Profit']]
            }).melt(id_vars='المؤشر', var_name='الفترة', value_name='المبلغ')
            
            fig = px.bar(compare_data, x='المؤشر', y='المبلغ', color='الفترة', barmode='group', text_auto='.2s')
            st.plotly_chart(fig, use_container_width=True)
            
            if st.button("توليد التقرير المقارن بواسطة Gemini 🤖"):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                prompt = f"""
                أنت CFO خبير. قارن بين الفترتين مالياً باللغة العربية:
                السنة السابقة: ربح {r1['Net Profit']}، هامش {r1['Profit Margin']:.1f}%، سيولة {r1['Current Ratio']:.2f}.
                السنة الحالية: ربح {r2['Net Profit']}، هامش {r2['Profit Margin']:.1f}%، سيولة {r2['Current Ratio']:.2f}.
                ركز على تحليل الفروقات، النمو، ونقاط القوة والضعف اللحظية لكل فترة وتوصية للمستقبل.
                """
                with st.spinner('جاري تشغيل محرك المقارنة الجيو-مالي...'):
                    try:
                        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                        st.markdown("<div class='report-box'><h3>📝 التقرير التحليلي المقارن الشامل:</h3>" + response.json()['candidates'][0]['content']['parts'][0]['text'] + "</div>", unsafe_allow_html=True)
                    except:
                        st.error("فشل الاتصال الخارجي بالسيرفر.")
