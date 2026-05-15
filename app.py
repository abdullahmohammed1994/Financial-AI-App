import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="المحاسب الذكي AI", layout="centered")
st.title("📊 نظام التحليل المالي الذكي")

api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك", type="password")
uploaded_file = st.file_uploader("اختر ملف الإكسل (xlsx)", type="xlsx")

if uploaded_file and api_key:
    df = pd.read_excel(uploaded_file)
    
    # تنظيف أسماء الأعمدة من المسافات الزائدة
    df.columns = [str(col).strip() for col in df.columns]
    
    st.write("### معاينة الأعمدة التي وجدتها:")
    st.write(list(df.columns))

    # التحقق من وجود الأعمدة المطلوبة
    col_rev = 'الدائن'
    col_exp = 'المدين'

    if col_rev in df.columns and col_exp in df.columns:
        if st.button("تحليل البيانات الآن 🚀"):
            rev = pd.to_numeric(df[col_rev], errors='coerce').sum()
            exp = pd.to_numeric(df[col_exp], errors='coerce').sum()
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": f"أنت مستشار مالي. حلل الأرقام التالية بالعربي: إيرادات {rev}، مصاريف {exp}."}]}]
            }
            
            with st.spinner('جاري التحليل...'):
                try:
                    response = requests.post(url, json=payload)
                    result = response.json()
                    ai_text = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("✅ تم التحليل")
                    st.info(ai_text)
                    st.bar_chart(pd.DataFrame({'المبلغ': [rev, exp]}, index=['الإيرادات', 'المصاريف']))
                except:
                    st.error("تأكد من صحة مفتاح الـ API أو حصة الاستخدام.")
    else:
        st.error(f"لم أجد أعمدة باسم '{col_rev}' و '{col_exp}'. يرجى التأكد من تسمية الأعمدة في ملف الإكسل.")
