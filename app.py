import streamlit as st
import pandas as pd
import requests

# إعداد الصفحة بواجهة عريضة وتدعم الاتجاهين
st.set_page_config(page_title="المحلل المالي العالمي AI", layout="wide")

# تصميم الواجهة
st.markdown("""
    <style>
    .main {
        text-align: right;
    }
    </style>
    """, unsafe_allow_status=True)

st.title("🌐 المحلل المالي الذكي (عربي - English)")
st.write("ارفع ملفاتك المالية بأي لغة، وسأقوم بتحليلها لك باللغة العربية باحترافية.")

# القائمة الجانبية للإعدادات
st.sidebar.header("⚙️ الإعدادات / Settings")
api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك / Enter API Key", type="password")

# مركز رفع الملفات
uploaded_file = st.file_uploader("اختر ملف الإكسل (xlsx)", type="xlsx")

if uploaded_file and api_key:
    # قراءة البيانات
    df = pd.read_excel(uploaded_file)
    st.write("### 📋 معاينة البيانات المرفوعة / Data Preview:")
    st.dataframe(df.head(10))

    if st.button("بدء التحليل المالي الاحترافي 🚀"):
        # تحويل البيانات لنص ليقرأها الذكاء الاصطناعي
        data_summary = df.to_string(index=False)
        
        # رابط الموديل (تأكد من استخدام الموديل الذي نجح في حسابك)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        # صياغة الطلب الذكي (البرومبت) ليكون ثنائي اللغة
        prompt = f"""
        System Instruction:
        You are an expert Senior Financial Auditor and Consultant. 
        You will receive financial data that might contain accounting terms in either Arabic, English, or both.
        Your task:
        1. Identify the type of document (Income Statement, Balance Sheet, Trial Balance, etc.).
        2. Understand all professional accounting terms (e.g., Assets, Liabilities, Revenue, COGS, Accruals, Depreciation).
        3. Perform a deep financial analysis including Profitability, Liquidity, and Debt ratios if applicable.
        4. ALWAYS provide the final report in PROFESSIONAL ARABIC language.

        Data to analyze:
        {data_summary}

        التقرير المطلوب باللغة العربية:
        - ملخص سريع للحالة المالية.
        - تحليل أهم النسب المالية المكتشفة.
        - نقاط القوة ونقاط الضعف.
        - توصيات مالية استراتيجية للمدير المالي.
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        with st.spinner('جاري تحليل البيانات وفهم المصطلحات...'):
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    ai_text = result['candidates'][0]['content']['parts'][0]['text']
                    
                    st.success("✅ اكتمل التحليل بنجاح")
                    st.markdown("---")
                    st.markdown("### 📝 التقرير المالي التحليلي:")
                    st.info(ai_text)
                    
                    # محاولة رسم بياني بسيط إذا وجدت بيانات رقمية
                    st.markdown("### 📊 ملخص بياني سريع:")
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) >= 1:
                        st.bar_chart(df[numeric_cols].sum())
                else:
                    st.error(f"خطأ في الاتصال: {response.status_code}")
            except Exception as e:
                st.error("حدث خطأ غير متوقع. يرجى مراجعة مفتاح الـ API.")
