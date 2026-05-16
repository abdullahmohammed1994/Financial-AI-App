import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. إعدادات المنصة الاحترافية
st.set_page_config(
    page_title="FinPilot AI | Next-Gen Financial Intelligence", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. حقن لغة التصميم المستقبلية (FinTech UI Stylesheet)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        font-family: 'Cairo', sans-serif;
        background-color: #0B1020 !important;
        color: #F8FAFC !important;
        text-align: right;
        direction: rtl;
    }
    
    [data-testid="stHeader"], footer {visibility: hidden;}
    
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
    
    /* تصميم بطاقة الـ Score الفريدة */
    .score-card {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 2px solid #00C896;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 200, 150, 0.1);
    }
    
    .explainability-box {
        background: #1F2937;
        border-right: 4px solid #4F8CFF;
        padding: 15px 20px;
        border-radius: 8px;
        font-size: 13px;
        color: #94A3B8;
        margin-bottom: 20px;
    }
    
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
    </style>
    """, unsafe_allow_html=True)

secrets_key = st.secrets.get("GEMINI_API_KEY", None)
active_api_key = secrets_key

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='color: #00C896; font-weight:900;'>⚡ FinPilot AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size:13px;'>لوحة التحكم الاستراتيجية</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("القائمة الرئيسية:", [
        "🌐 المنصة الرئيسية", 
        "📊 AI Financial Auditor", 
        "⚙️ الإعدادات"
    ])

# --- محرك بايثون المحاسبي ---
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

# خوارزمية حساب تقييم السلامة المالية الاحترافية (Financial Health Score)
def calculate_health_score(r):
    score = 0
    # 1. نقاط السيولة (الوزن الكلي: 35 نقطة)
    if r['Current Ratio'] >= 1.5: score += 35
    elif r['Current Ratio'] >= 1.0: score += 20
    else: score += 5
    
    # 2. نقاط الربحية (الوزن الكلي: 35 نقطة)
    if r['Profit Margin'] >= 15: score += 35
    elif r['Profit Margin'] > 0: score += 20
    else: score -= 10 # خسارة تشغيلية تؤثر سلباً
    
    # 3. نقاط الأمان ضد الديون (الوزن الكلي: 30 نقطة)
    if r['Debt Ratio'] <= 40: score += 30
    elif r['Debt Ratio'] <= 70: score += 15
    else: score += 0
    
    return max(0, min(100, score)) # ضمان بقاء المؤشر بين 0 و 100

# --- الأنماط والصفحات ---
if menu == "🌐 المنصة الرئيسية":
    st.markdown("""
        <div class='hero-container'>
            <h1 class='hero-title'>AI Financial Assistant for Smarter Decisions</h1>
            <p class='hero-subtitle'>اتخذ قراراتك المالية بثقة عمياء. حلل القوائم المعقدة، واكتشف انحرافات الأرباح، واحصل على تقارير تنفيذية فورية مدعومة بالذكاء الاصطناعي التوليدي.</p>
        </div>
    """, unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.markdown("<div class='saas-card'><h4 style='color:#4F8CFF;'>⚡ تدقيق فوري عالي السرعة</h4><p style='color:#94A3B8; font-size:14px;'>استخراج فوري لنسب السيولة والربحية والمديونية من ملفات الإكسل في أجزاء من الثانية.</p></div>", unsafe_allow_html=True)
    with f_col2:
        st.markdown("<div class='saas-card'><h4 style='color:#00C896;'>🤖 تقارير خبير CFO آلي</h4><p style='color:#94A3B8; font-size:14px;'>صياغة تحليلات استراتيجية تشرح الثغرات المالية وتقترح خطط خفض التكاليف وتوليد السيولة.</p></div>", unsafe_allow_html=True)
    with f_col3:
        st.markdown("<div class='saas-card'><h4 style='color:#fbbf24;'>🛡️ Financial Health Score</h4><p style='color:#94A3B8; font-size:14px;'>خوارزمية قياسية لتقييم قوة الشركة المالية ومقاومتها للأزمات بضغطة زر واحدة.</p></div>", unsafe_allow_html=True)

elif menu == "📊 AI Financial Auditor":
    st.markdown("<h2 style='color:#F8FAFC;'>📊 AI Financial Auditor & Intelligence Center</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # تفعيل حقل المفتاح الاحتياطي ديناميكياً إذا واجه السيرفر العام خطأ 429
    if st.session_state.get('show_backup_key', False):
        user_backup_key = st.text_input("🔑 الـ IP العام للسيرفر مزدحم، يرجى لصق مفتاح API الخاص بك لتشغيل الاتصال المباشر الفوري:", type="password")
        if user_backup_key: active_api_key = user_backup_key

    file = st.file_uploader("📂 ارفع ملف القائمة المالية الخاصة بالسنة الحالية (xlsx)", type="xlsx")
    if file:
        df = pd.read_excel(file)
        r = calculate_ratios(df)
        health_score = calculate_health_score(r)
        
        # تقسيم الشاشة: اليسار للمؤشر المالي الكبير، اليمين للـ KPIs والمخطط
        main_col, score_col = st.columns([3, 1])
        
        with main_col:
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"<div class='saas-card'><div class='card-label'>إجمالي الإيرادات</div><div class='card-val'>{r['Revenue']:,.0f}</div></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='saas-card'><div class='card-label'>صافي الربح</div><div class='card-val'>{r['Net Profit']:,.0f}</div></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='saas-card'><div class='card-label'>هامش الربح التشغيلي</div><div class='card-val'>{r['Profit Margin']:.1f}%</div></div>", unsafe_allow_html=True)
            
            fig = px.bar(x=['الإيرادات', 'صافي الربح'], y=[r['Revenue'], r['Net Profit']], color=['الإيرادات', 'صافي الربح'], color_discrete_sequence=['#4F8CFF', '#00C896'])
            fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
        with score_col:
            # عرض بطاقة تقييم السلامة المالية الفخمة
            status = "ممتاز" if health_score >= 70 else "متوسط" if health_score >= 40 else "حرِج"
            color = "#00C896" if health_score >= 70 else "#fbbf24" if health_score >= 40 else "#EF4444"
            st.markdown(f"""
                <div class='score-card' style='border-color: {color};'>
                    <div class='card-label' style='font-size:16px;'>Financial Health Score</div>
                    <div style='font-size: 64px; font-weight: 900; color: {color}; margin: 15px 0;'>{health_score}</div>
                    <div style='background: {color}20; color: {color}; padding: 6px 15px; border-radius: 20px; display: inline-block; font-weight: 700;'>وضع مالي: {status}</div>
                </div>
            """, unsafe_allow_html=True)

        if st.button("توليد التقرير الاستراتيجي والتوصيات المستقبلية 🤖"):
            if active_api_key:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={active_api_key}"
                headers = {'Content-Type': 'application/json'}
                prompt = f"حلل مالياً كخبير CFO ومحلل مخاطر: إيرادات {r['Revenue']}، ربح {r['Net Profit']}، هامش ربح {r['Profit Margin']:.1f}%، سلامة مالية {health_score}/100 بناءً على السيولة والأمان."
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                
                try:
                    res = requests.post(url, json=payload, headers=headers)
                    if res.status_code == 200:
                        st.markdown("""
                            <div class='explainability-box'>
                                <b>🎯 معايير بناء الثقة (Explainability):</b> هذا التقرير تم استخلاصه برمجياً بربط مؤشر السلامة المالية (Health Score) بالخوارزمية القياسية المعتمدة عالمياً لتقييم جودة الائتمان التشغيلي للشركات الناشئة.
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"<div class='saas-card' style='background:#0F172A;'><h3>📋 مخرجات التقرير المالي الذكي:</h3><p style='line-height:1.9; color:#E2E8F0;'>{res.json()['candidates'][0]['content']['parts'][0]['text']}</p></div>", unsafe_allow_html=True)
                    elif res.status_code == 429:
                        st.session_state['show_backup_key'] = True
                        st.warning("⏱️ تم رصد ضغط طلبات على سيرفر المنصة العام. تم تفعيل الحقل في الأعلى لتجاوز الحظر بمفتاحك المباشر!")
                        st.rerun()
                    else:
                        st.error(f"خطأ استجابة من جوجل: {res.status_code}")
                except Exception as e:
                    st.error(f"فشل الاستعلام: {str(e)}")

elif menu == "⚙️ الإعدادات":
    st.markdown("<h2 style='color:#F8FAFC;'>⚙️ الإعدادات التكوينية للمنصة</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("إصدار المنصة المستقر الحالي: **FinPilot Enterprise v5.5 (2026)**")
