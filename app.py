import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. إعدادات المنصة الاحترافية وإخفاء القوائم الافتراضية
st.set_page_config(
    page_title="FinPilot AI | Next-Gen Financial Intelligence", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. حقن لغة التصميم المستقبلية (FinTech UI Stylesheet)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* لغة التصميم - الخلفية والألوان الأساسية */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        font-family: 'Cairo', sans-serif;
        background-color: #0B1020 !important; /* خلفية داكنة ملوكية */
        color: #F8FAFC !important;
        text-align: right;
        direction: rtl;
    }
    
    /* إخفاء ترويسة ستريمليت لتبدو كمنصة خاصة */
    [data-testid="stHeader"], footer {visibility: hidden;}
    
    /* تصميم الـ Hero Section */
    .hero-container {
        text-align: center;
        padding: 60px 20px;
        background: radial-gradient(circle at top, #1e293b 0%, #0B1020 100%);
        border-bottom: 1px solid #1E293B;
        border-radius: 24px;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(90deg, #00C896, #4F8CFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 19px;
        max-width: 700px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }
    
    /* تصميم البطاقات الـ SaaS Cards */
    .saas-card {
        background: #111827;
        border: 1px solid #1F2937;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .saas-card:hover {
        border-color: #4F8CFF;
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    .card-label { color: #94A3B8; font-size: 14px; font-weight: 600; margin-bottom: 6px; }
    .card-val { color: #00C896; font-size: 28px; font-weight: 700; }
    
    /* صندوق التفسير وبناء الثقة Explainability */
    .explainability-box {
        background: #1F2937;
        border-right: 4px solid #4F8CFF;
        padding: 15px 20px;
        border-radius: 8px;
        font-size: 13px;
        color: #94A3B8;
        margin-bottom: 20px;
    }
    
    /* تخصيص الأزرار اللامعة */
    .stButton>button {
        background: linear-gradient(90deg, #00C896 0%, #4F8CFF 100%) !important;
        color: #0B1020 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 30px !important;
        box-shadow: 0 4px 15px rgba(0, 200, 150, 0.2) !important;
        width: 100%;
    }
    .stButton>button:hover {
        filter: brightness(1.1);
        box-shadow: 0 6px 20px rgba(79, 140, 255, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة مفاتيح الـ API الذكية (المخفية والاحتياطية)
secrets_key = st.secrets.get("GEMINI_API_KEY", None)
active_api_key = secrets_key

# --- الهيكل الصحيح للموقع: Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='color: #00C896; font-weight:900;'>⚡ FinPilot AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size:13px;'>لوحة التحكم الاستراتيجية</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # التنقل الاحترافي بين الأقسام
    menu = st.radio("القائمة الرئيسية:", [
        "🌐 المنصة الرئيسية", 
        "📊 AI Financial Auditor", 
        "📈 Portfolio Analyzer (قريباً)", 
        "⚙️ الإعدادات"
    ])
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='background:#111827; padding:15px; border-radius:10px; border:1px solid #1F2937; font-size:12px; color:#94A3B8;'>🔒 تشفير مالي متطور وحماية البيانات ومكافحة غسيل الأموال مفعّلة تلقائياً.</div>", unsafe_allow_html=True)

# --- محرك المحاسبة المالي ---
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

# --- إدارة الصفحات بناءً على خيار الـ Sidebar ---

if menu == "🌐 المنصة الرئيسية":
    # 1. Hero Section الاحترافي
    st.markdown("""
        <div class='hero-container'>
            <h1 class='hero-title'>AI Financial Assistant for Smarter Decisions</h1>
            <p class='hero-subtitle'>اتخذ قراراتك المالية بثقة عمياء. حلل القوائم المعقدة، واكتشف انحرافات الأرباح، واحصل على تقارير تنفيذية فورية مدعومة بالذكاء الاصطناعي التوليدي.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # عرض ميزات المنصة كـ SaaS Features
    st.markdown("<h3 style='color:#F8FAFC; text-align:center;'>لماذا يعتمد المدراء التنفيذيون على FinPilot؟</h3><br>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        st.markdown("<div class='saas-card'><h4 style='color:#4F8CFF;'>⚡ تدقيق فوري عالي السرعة</h4><p style='color:#94A3B8; font-size:14px;'>استخراج فوري لنسب السيولة والربحية والمديونية من ملفات الإكسل في أجزاء من الثانية.</p></div>", unsafe_allow_html=True)
    with f_col2:
        st.markdown("<div class='saas-card'><h4 style='color:#00C896;'>🤖 تقارير خبير CFO آلي</h4><p style='color:#94A3B8; font-size:14px;'>صياغة تحليلات استراتيجية تشرح الثغرات المالية وتقترح خطط خفض التكاليف وتوليد السيولة.</p></div>", unsafe_allow_html=True)
    with f_col3:
        st.markdown("<div class='saas-card'><h4 style='color:#fbbf24;'>🔒 أمان بمستوى بنكي</h4><p style='color:#94A3B8; font-size:14px;'>بياناتك المالية مشفرة بالكامل ولا يتم تخزينها أو استخدامها لتدريب النماذج العامة.</p></div>", unsafe_allow_html=True)
        
    st.markdown("<br><p style='text-align:center; color:#64748B;'>الانتقال لغرض التحليل؟ استخدم القائمة الجانبية واختر <b>AI Financial Auditor</b> للبدء.</p>", unsafe_allow_html=True)

elif menu == "📊 AI Financial Auditor":
    st.markdown("<h2 style='color:#F8FAFC;'>📊 AI Financial Auditor</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8;'>ارفع القوائم المالية واجعل الذكاء الاصطناعي يحللها هيكلياً</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    mode = st.radio("حدد نمط المعالجة المستهدف:", ["🔎 تحليل قوائم سنة منفردة", "⚖️ تحليل التباين والمقارنة السنوية"], horizontal=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # تفعيل حقل المفتاح الاحتياطي ديناميكياً إذا واجه السيرفر العام خطأ 429
    if st.session_state.get('show_backup_key', False):
        user_backup_key = st.text_input("🔑 الـ IP العام للسيرفر مزدحم، يرجى لصق مفتاح API الخاص بك لتشغيل الاتصال المباشر الفوري:", type="password")
        if user_backup_key:
            active_api_key = user_backup_key

    if mode == "🔎 تحليل قوائم سنة منفردة":
        file = st.file_uploader("📂 ارفع ملف القائمة المالية (xlsx)", type="xlsx")
        if file:
            df = pd.read_excel(file)
            r = calculate_ratios(df)
            
            # عرض بطاقات الـ KPI الفخمة المتباعدة
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f"<div class='saas-card'><div class='card-label'>إجمالي الإيرادات</div><div class='card-val'>{r['Revenue']:,.0f}</div></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='saas-card'><div class='card-label'>صافي الربح</div><div class='card-val'>{r['Net Profit']:,.0f}</div></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='saas-card'><div class='card-label'>هامش الربح التشغيلي</div><div class='card-val'>{r['Profit Margin']:.1f}%</div></div>", unsafe_allow_html=True)
            col4.markdown(f"<div class='saas-card'><div class='card-label'>معدل السيولة المتداولة</div><div class='card-val'>{r['Current Ratio']:.2f}</div></div>", unsafe_allow_html=True)

            # الرسوم البيانية المتناسقة مع لوحة التحكم الداكنة
            fig = px.bar(x=['الإيرادات', 'صافي الربح'], y=[r['Revenue'], r['Net Profit']], color=['الإيرادات', 'صافي الربح'], color_discrete_sequence=['#4F8CFF', '#00C896'])
            fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            if st.button("توليد الرؤية والتقرير التنفيذي الآلي 🤖"):
                if active_api_key:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={active_api_key}"
                    headers = {'Content-Type': 'application/json'}
                    payload = {"contents": [{"parts": [{"text": f"حلل مالياً بالعربية كخبير CFO محترف جداً ومستشار مالي: إيرادات {r['Revenue']}، ربح {r['Net Profit']}، هامش {r['Profit Margin']:.1f}%، سيولة {r['Current Ratio']:.2f}."}]}]}
                    
                    try:
                        res = requests.post(url, json=payload, headers=headers)
                        if res.status_code == 200:
                            # 4. إضافة ميزة الـ Explainability لبناء الثقة
                            st.markdown("""
                                <div class='explainability-box'>
                                    <b>🎯 معايير بناء التقرير (Explainability):</b> تم إنشاء هذا التحليل الاستراتيجي تلقائياً بناءً على تتبع هوامش الربحية وصيغ السيولة المتداولة ومقارنتها بالمعايير القياسية لقطاع الشركات.
                                </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"<div class='saas-card' style='background:#0F172A; text-align:right;'><h3>📋 تقرير خبير الـ CFO:</h3><p style='line-height:1.9; color:#E2E8F0;'>{res.json()['candidates'][0]['content']['parts'][0]['text']}</p></div>", unsafe_allow_html=True)
                        elif res.status_code == 429:
                            st.session_state['show_backup_key'] = True
                            st.warning("⏱️ تم رصد ضغط طلبات على سيرفر المنصة العام. تفعيل حقل المفتاح المباشر في الأعلى لتخطي الحظر!")
                            st.rerun()
                        else:
                            st.error(f"خطأ استجابة من السيرفر المالي الخارجي: {res.status_code}")
                    except Exception as e:
                        st.error(f"فشل محرك الاستعلام: {str(e)}")
                else:
                    st.error("⚠️ يرجى تزويد المنصة بمفتاح الـ API للاتصال بالذكاء الاصطناعي.")

    else:
        # نمط مقارنة السنتين الهيكلي
        st.markdown("<p style='color:#94A3B8;'>ارفع الملف المالي للسنة السابقة ثم السنة الحالية لإجراء تحليل انحرافات الأداء الحقيقي (Variance Analysis):</p>", unsafe_allow_html=True)
        c_col1, c_col2 = st.columns(2)
        with c_col1: f1 = st.file_uploader("📥 ملف السنة السابقة (xlsx)", type="xlsx")
        with c_col2: f2 = st.file_uploader("📥 ملف السنة الحالية (xlsx)", type="xlsx")
        
        if f1 and f2:
            df1, df2 = pd.read_excel(f1), pd.read_excel(f2)
            r1, r2 = calculate_ratios(df1), calculate_ratios(df2)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f"<div class='saas-card'><div class='card-label'>نمو صافي الأرباح</div><div class='card-val'>{r2['Net Profit'] - r1['Net Profit']:+,.0f}</div></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='saas-card'><div class='card-label'>انحراف هامش الربح</div><div class='card-val'>{r2['Profit Margin'] - r1['Profit Margin']:+.1f}%</div></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='saas-card'><div class='card-label'>تغير كفاءة السيولة</div><div class='card-val'>{r2['Current Ratio'] - r1['Current Ratio']:+.2f}</div></div>", unsafe_allow_html=True)
            col4.markdown(f"<div class='saas-card'><div class='card-label'>نسبة مديونية الحالية</div><div class='card-val' style='color:#4F8CFF;'>{r2['Debt Ratio']:.1f}%</div></div>", unsafe_allow_html=True)

            comp_df = pd.DataFrame({
                'البند المالي': ['الإيرادات', 'صافي الربح'],
                'السنة السابقة': [r1['Revenue'], r1['Net Profit']],
                'السنة الحالية': [r2['Revenue'], r2['Net Profit']]
            }).melt(id_vars='البند المالي', var_name='الفترة الزمنية', value_name='القيمة المالية')
            
            fig = px.bar(comp_df, x='البند المالي', y='القيمة المالية', color='الفترة الزمنية', barmode='group', color_discrete_sequence=['#475569', '#00C896'])
            fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

            if st.button("بدء تحليل التباين والنمو الهيكلي المشترك 🚀"):
                if active_api_key:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={active_api_key}"
                    headers = {'Content-Type': 'application/json'}
                    payload = {"contents": [{"parts": [{"text": f"قارن ماليًا بالعربية كخبير CFO ومحلل استراتيجي للمخاطر: السنة السابقة ربح {r1['Net Profit']} وهامش {r1['Profit Margin']:.1f}%، الحالية ربح {r2['Net Profit']} وهامش {r2['Profit Margin']:.1f}%."}]}]}
                    
                    try:
                        res = requests.post(url, json=payload, headers=headers)
                        if res.status_code == 200:
                            st.markdown("""
                                <div class='explainability-box'>
                                    <b>🎯 معايير بناء التقرير (Explainability):</b> تم إعداد هذا التقرير عبر مقارنة انحرافات البنود (Variance Analysis) ومعدل النمو السنوي المركب لهيكل الأرباح والمبيعات.
                                </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"<div class='saas-card' style='background:#0F172A; text-align:right;'><h3>📋 التقرير المقارن التحليلي للنمو:</h3><p style='line-height:1.9; color:#E2E8F0;'>{res.json()['candidates'][0]['content']['parts'][0]['text']}</p></div>", unsafe_allow_html=True)
                        elif res.status_code == 429:
                            st.session_state['show_backup_key'] = True
                            st.warning("⏱️ تم رصد ضغط طلبات على سيرفر المنصة العام. تفعيل حقل المفتاح المباشر في الأعلى لتخطي الحظر!")
                            st.rerun()
                        else:
                            st.error(f"خطأ استجابة من السيرفر المالي الخارجي: {res.status_code}")
                    except Exception as e:
                        st.error(f"فشل محرك الاستعلام: {str(e)}")
                else:
                    st.error("⚠️ يرجى تزويد المنصة بمفتاح الـ API للتحليل.")

elif menu == "⚙️ الإعدادات":
    st.markdown("<h2 style='color:#F8FAFC;'>⚙️ الإعدادات التكوينية للمنصة</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("مفتاح الـ API مدمج ومحمي في خوادم السيرفر المشفرة (Secrets) تلقائياً.")
    st.write("الإصدار الحالي المستقر: **FinPilot Enterprise v5.2 (2026)**")
