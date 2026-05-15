import streamlit as st
import pandas as pd
import requests

# إعداد الصفحة لتكون واسعة وتدعم المقارنة
st.set_page_config(page_title="المحلل المالي - نظام المقارنة", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ منصة المقارنة والتحليل المالي الذكي")
st.write("ارفع ملفين (مثلاً: سنتين ماليتين مختلفتين) وسأقوم بتحليل النمو والفروقات بينهما.")

# القائمة الجانبية
st.sidebar.header("⚙️ الإعدادات / Settings")
api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك", type="password")

# تقسيم الشاشة لرفع ملفين
col1, col2 = st.columns(2)

with col1:
    st.subheader("الفترة الأولى (السابقة)")
    file1 = st.file_uploader("اختر الملف الأول", type="xlsx", key="file1")

with col2:
    st.subheader("الفترة الثانية (الحالية)")
    file2 = st.file_uploader("اختر الملف الثاني", type="xlsx", key="file2")

if file1 and file2 and api_key:
    # قراءة الملفين
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    tab1, tab2 = st.tabs(["📊 معاينة البيانات", "🤖 التحليل والمقارنة"])
    
    with tab1:
        c1, c2 = st.columns(2)
        c1.write("### بيانات الفترة الأولى:")
        c1.dataframe(df1.head(10))
        c2.write("### بيانات الفترة الثانية:")
        c2.dataframe(df2.head(10))

    with tab2:
        if st.button("بدء المقارنة الذكية 🚀"):
            # تحويل البيانات لنص ليقرأها الذكاء الاصطناعي
            data1_txt = df1.to_string(index=False)
            data2_txt = df2.to_string(index=False)
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            
            prompt = f"""
            أنت خبير مالي واستراتيجي CFO. لديك الآن بيانات مالية لفترتين مختلفتين (ممكن بالعربي أو الإنجليزي).
            
            بيانات الفترة الأولى:
            {data1_txt}
            
            بيانات الفترة الثانية:
            {data2_txt}
            
            المطلوب منك:
            1. قارن بين الفترتين واستخرج نسبة النمو أو التراجع في البنود الرئيسية (إيرادات، أصول، خصوم).
            2. حدد التغيرات الجوهرية (Variance) وأسبابها المحتملة.
            3. قدم تحليلاً للاتجاهات (Trend Analysis) والتوقعات للفترة القادمة.
            4. التقرير يجب أن يكون باللغة العربية المهنية.
            """
            
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            with st.spinner('جاري مقارنة القوائم المالية وتحليل الاتجاهات...'):
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        result = response.json()
                        ai_report = result['candidates'][0]['content']['parts'][0]['text']
                        
                        st.success("✅ اكتمل تحليل المقارنة بنجاح")
                        st.markdown("---")
                        st.markdown("### 📝 تقرير مقارنة الأداء المالي:")
                        st.info(ai_report)
                    else:
                        st.error("فشل الاتصال بمحرك الذكاء الاصطناعي.")
                except Exception as e:
                    st.error("حدث خطأ في معالجة البيانات.")
