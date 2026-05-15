import streamlit as st
import pandas as pd
import requests
import json

# إعدادات الواجهة
st.set_page_config(page_title="المحاسب الذكي AI", layout="centered")
st.title("📊 نظام التحليل المالي الذكي (Gemini 2.5)")
st.write("قم برفع ملف الإكسل الخاص بك للحصول على تحليل فوري")

# إدخال مفتاح الـ API بشكل آمن
api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك", type="password")

uploaded_file = st.file_uploader("اختر ملف الإكسل (xlsx)", type="xlsx")

if uploaded_file and api_key:
    df = pd.read_excel(uploaded_file)
    st.write("### معاينة البيانات:", df.head())
    
    if st.button("تحليل البيانات الآن 🚀"):
        rev = df['الدائن'].sum()
        exp = df['المدين'].sum()
        
        # الاتصال المباشر الذي نجحنا فيه سابقا
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": f"أنت مستشار مالي خبير. حلل هذه الأرقام بالعربي بـ 3 نقاط مختصرة: إيرادات {rev}، مصاريف {exp}."}]}]
        }
        
        with st.spinner('جاري التحليل...'):
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                ai_text = result['candidates'][0]['content']['parts'][0]['text']
                st.success("✅ تم التحليل بنجاح")
                st.info(ai_text)
                
                # رسم بياني بسيط
                chart_data = pd.DataFrame({'المبلغ': [rev, exp]}, index=['الإيرادات', 'المصاريف'])
                st.bar_chart(chart_data)
            else:
                st.error("فشل الاتصال بالذكاء الاصطناعي. تأكد من المفتاح أو الكوتا.")