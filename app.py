import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 1. إعدادات الصفحة الرسمية المستقرة
st.set_page_config(page_title="Financial AI Auditor", layout="wide")

# عنوان رئيسي واضح
st.title("🏦 Financial AI Auditor")
st.subheader("نظام الرقابة المالية الذكي | الاستشارات الاستراتيجية الآلية")
st.markdown("---")

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

# --- القائمة الجانبية المستقرة ---
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    api_key = st.text_input("🔑 مفتاح API الخاص بك", type="password")
    mode = st.radio("📊 نمط العمل المالي:", ["تحليل مفرد", "مقارنة سنتين"])
    st.markdown("---")
    st.write("يدعم القوائم باللغتين العربية والإنجليزية.")

# --- المعالجة والعرض ---
if mode == "تحليل مفرد":
    file = st.file_uploader("📂 ارفع القائمة المالية (xlsx)", type="xlsx")
    if file and api_key:
        df = pd.read_excel(file)
        r = calculate_ratios(df)
        
        st.markdown("### 📈 نبذة عن الأداء المالي")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("إجمالي الإيرادات", f"{r['Revenue']:,.0f}")
        c2.metric("صافي الربح", f"{r['Net Profit']:,.0f}")
        c3.metric("هامش الربح", f"{r['Profit Margin']:.1f}%")
        c4.metric("نسبة السيولة", f"{r['Current Ratio']:.2f}")

        # رسم بياني متناسق مع الثيم
        fig = px.bar(x=['الإيرادات', 'صافي الربح'], y=[r['Revenue'], r['Net Profit']], 
                     color=['إيرادات', 'ربح'], color_discrete_sequence=['#415a77', '#d4af37'])
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        if st.button("توليد التقرير التنفيذي 🤖"):
            prompt = f"حلل مالياً بالعربية كخبير CFO: إيرادات {r['Revenue']}، ربح {r['Net Profit']}، هامش {r['Profit Margin']:.1f}%."
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            try:
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                st.markdown("---")
                st.markdown("### 📝 تقرير الخبير المالي:")
                st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
            except:
                st.error("خطأ في الاتصال بمفتاح الـ API.")

else:
    col1, col2 = st.columns(2)
    with col1: f1 = st.file_uploader("📂 ملف السنة السابقة", type="xlsx")
    with col2: f2 = st.file_uploader("📂 ملف السنة الحالية", type="xlsx")
    
    if f1 and f2 and api_key:
        df1, df2 = pd.read_excel(f1), pd.read_excel(f2)
        r1, r2 = calculate_ratios(df1), calculate_ratios(df2)
        
        st.markdown("### ⚖️ مقارنة الأداء السنوي (Variance Analysis)")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("صافي الربح", f"{r2['Net Profit']:,.0f}", f"{r2['Net Profit'] - r1['Net Profit']:,.0f}")
        m2.metric("هامش الربح", f"{r2['Profit Margin']:.1f}%", f"{r2['Profit Margin'] - r1['Profit Margin']:.1f}%")
        m3.metric("السيولة", f"{r2['Current Ratio']:.2f}", f"{r2['Current Ratio'] - r1['Current Ratio']:.2f}")
        m4.metric("المديونية", f"{r2['Debt Ratio']:.1f}%", f"{r2['Debt Ratio'] - r1['Debt Ratio']:.1f}%", delta_color="inverse")

        # رسم بياني مقارن متناسق
        comp_df = pd.DataFrame({
            'البند': ['الإيرادات', 'صافي الربح'],
            'السابقة': [r1['Revenue'], r1['Net Profit']],
            'الحالية': [r2['Revenue'], r2['Net Profit']]
        }).melt(id_vars='البند', var_name='السنة', value_name='المبلغ')
        fig = px.bar(comp_df, x='البند', y='المبلغ', color='السنة', barmode='group', color_discrete_sequence=['#415a77', '#d4af37'])
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        if st.button("تحليل الفروقات والنمو 🚀"):
            prompt = f"قارن بالعربية كخبير CFO: السنة الماضية ربح {r1['Net Profit']} الحالية {r2['Net Profit']}."
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            try:
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                st.markdown("---")
                st.markdown("### 📝 التقرير المقارن الاستراتيجي:")
                st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
            except:
                st.error("خطأ في الاتصال بمفتاح الـ API.")
