import os
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from analysis import (
    CATEGORIES,
    clean_expense_data,
    detect_anomalies,
    generate_financial_advice,
    get_summary,
    guru_comparison,
    parse_transaction_text,
    predict_next_month,
)

DATA_FILE = "expenses.csv"
SAMPLE_FILE = "sample_expenses.csv"

st.set_page_config(page_title="Financial Advisor AI", page_icon="💰", layout="wide")

st.markdown("""
<style>
:root { --ink:#111827; --muted:#374151; --blue:#2563eb; --violet:#7c3aed; --green:#059669; --card:#ffffff; }
.stApp { background: radial-gradient(circle at top left,#dbeafe 0,#f8fafc 30%,#fff7ed 100%); color: var(--ink) !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#ffffff,#eef6ff); border-right: 1px solid #dbeafe; }
h1,h2,h3,h4,h5,h6,p,label,span,div,.stMarkdown,.stTextInput label,.stNumberInput label,.stSelectbox label,.stDateInput label,.stFileUploader label { color: var(--ink) !important; }
.hero-card { background: linear-gradient(135deg,#ffffff 0%,#eff6ff 52%,#fdf2f8 100%); padding: 28px 32px; border-radius: 28px; border:1px solid #dbeafe; box-shadow:0 18px 45px rgba(30,64,175,.13); margin-bottom: 18px; }
.main-title { font-size: 42px; font-weight: 900; letter-spacing: -.04em; color:#0f172a !important; margin:0; }
.subtitle { font-size: 17px; color:#334155 !important; margin-top:8px; }
.badge { display:inline-block; padding:8px 14px; border-radius:999px; background:#dbeafe; color:#1e3a8a !important; font-weight:800; font-size:13px; margin-bottom:12px; }
.card { background:rgba(255,255,255,.94); border:1px solid #e5e7eb; border-radius:22px; padding:20px; box-shadow:0 12px 30px rgba(15,23,42,.08); margin-bottom:16px; }
.agent-box { background:#fff; color:#111827 !important; padding:15px 16px; border-radius:16px; margin-bottom:12px; border-left:7px solid #2563eb; box-shadow:0 8px 18px rgba(37,99,235,.10); font-size:15.5px; }
.agent-box b { color:#0f172a !important; }
.workflow-pill { display:inline-block; background:#fef3c7; border:1px solid #fde68a; padding:7px 11px; border-radius:999px; color:#78350f !important; font-weight:800; margin:3px; }
.security-note { background:#ecfdf5; border:1px solid #bbf7d0; border-radius:16px; padding:14px 16px; color:#064e3b !important; }
div[data-testid="stMetric"] { background:rgba(255,255,255,.96); border:1px solid #e5e7eb; padding:16px; border-radius:20px; box-shadow:0 10px 22px rgba(15,23,42,.08); }
div[data-testid="stMetricLabel"] p { color:#374151 !important; font-weight:800; }
div[data-testid="stMetricValue"] { color:#0f172a !important; font-weight:900; }
.stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"] button { background:linear-gradient(135deg,#2563eb,#7c3aed) !important; color:white !important; border:none !important; border-radius:12px !important; font-weight:800 !important; padding:.55rem 1rem !important; box-shadow:0 10px 18px rgba(37,99,235,.22); }
.stButton>button:hover, .stDownloadButton>button:hover, div[data-testid="stFormSubmitButton"] button:hover { color:white !important; filter:brightness(.95); }
button p, button span, button div { color:white !important; }
/* Keep every clickable button/dropdown option readable */
.stButton>button *, .stDownloadButton>button *, div[data-testid="stFormSubmitButton"] button *,
[data-testid="stFileUploader"] button *, [data-testid="baseButton-secondary"] *, [data-testid="baseButton-primary"] * {
    color:white !important;
}
[data-testid="stFileUploader"] button,
[data-testid="baseButton-secondary"], [data-testid="baseButton-primary"] {
    background:linear-gradient(135deg,#2563eb,#7c3aed) !important;
    color:white !important;
    border:none !important;
    border-radius:12px !important;
    font-weight:800 !important;
}
/* Selectbox closed state */
div[data-baseweb="select"] > div {
    background:linear-gradient(135deg,#2563eb,#7c3aed) !important;
    border:1px solid #c7d2fe !important;
    border-radius:12px !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="select"] svg {
    color:white !important;
    fill:white !important;
}
/* Dropdown menu options */
ul[role="listbox"], div[role="listbox"] {
    background:#1e293b !important;
    border-radius:12px !important;
}
li[role="option"], div[role="option"] {
    background:#1e293b !important;
    color:white !important;
}
li[role="option"] *, div[role="option"] * {
    color:white !important;
}
li[role="option"]:hover, div[role="option"]:hover {
    background:#2563eb !important;
}
/* Tabs are also buttons in Streamlit, so make tab text visible too */
[data-testid="stTabs"] button { background:linear-gradient(135deg,#dbeafe,#ede9fe) !important; border-radius:12px 12px 0 0 !important; }
[data-testid="stTabs"] button p { color:#111827 !important; font-weight:900; }
[data-testid="stDataFrame"] { background:white; border-radius:16px; }

/* FINAL READABILITY FIXES FOR FILE UPLOADER, INPUTS, DATE PICKER, AND NUMBER CONTROLS */
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {
    background:#ffffff !important;
    border:2px dashed #7c3aed !important;
    border-radius:18px !important;
}
[data-testid="stFileUploader"] section *,
[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] div {
    color:#111827 !important;
    opacity:1 !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"] {
    background:linear-gradient(135deg,#2563eb,#7c3aed) !important;
    color:#ffffff !important;
    border:none !important;
    border-radius:14px !important;
    font-weight:900 !important;
}
[data-testid="stFileUploader"] button *,
[data-testid="stFileUploaderDropzone"] button *,
button[kind="secondary"] *, button[kind="primary"] * {
    color:#ffffff !important;
    opacity:1 !important;
}
/* Text/date/number input boxes */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
input, textarea {
    background:#ffffff !important;
    color:#111827 !important;
    -webkit-text-fill-color:#111827 !important;
    border:1.5px solid #c7d2fe !important;
    border-radius:12px !important;
}
input::placeholder, textarea::placeholder {
    color:#4b5563 !important;
    opacity:1 !important;
}
/* Number input plus/minus buttons */
[data-testid="stNumberInput"] button,
[data-testid="stNumberInput"] button:hover,
[data-testid="stNumberInput"] button:focus {
    background:#2563eb !important;
    color:#ffffff !important;
    border:1px solid #93c5fd !important;
}
[data-testid="stNumberInput"] button *,
[data-testid="stNumberInput"] button svg {
    color:#ffffff !important;
    fill:#ffffff !important;
    stroke:#ffffff !important;
    opacity:1 !important;
}
/* Date picker popover/calendar readability */
div[data-baseweb="popover"],
div[data-baseweb="calendar"],
div[data-baseweb="calendar"] *,
div[role="dialog"],
div[role="dialog"] * {
    color:#111827 !important;
    opacity:1 !important;
}
div[data-baseweb="popover"] > div,
div[data-baseweb="calendar"],
div[role="dialog"] {
    background:#ffffff !important;
}
div[data-baseweb="calendar"] button,
div[data-baseweb="calendar"] button *,
div[role="dialog"] button,
div[role="dialog"] button * {
    color:#111827 !important;
    fill:#111827 !important;
    stroke:#111827 !important;
    opacity:1 !important;
}
div[data-baseweb="calendar"] button[aria-selected="true"],
div[data-baseweb="calendar"] button[aria-selected="true"] *,
div[role="dialog"] button[aria-selected="true"],
div[role="dialog"] button[aria-selected="true"] * {
    background:#ef4444 !important;
    color:#ffffff !important;
    fill:#ffffff !important;
    stroke:#ffffff !important;
}
/* Select dropdown readable while still aesthetic */
div[data-baseweb="select"] > div {
    background:#ffffff !important;
    color:#111827 !important;
    border:1.5px solid #c7d2fe !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color:#111827 !important;
    opacity:1 !important;
}
div[data-baseweb="select"] svg {
    fill:#111827 !important;
    color:#111827 !important;
}
ul[role="listbox"], div[role="listbox"] {
    background:#ffffff !important;
    border:1px solid #c7d2fe !important;
}
li[role="option"], div[role="option"], li[role="option"] *, div[role="option"] * {
    background:#ffffff !important;
    color:#111827 !important;
    opacity:1 !important;
}
li[role="option"]:hover, div[role="option"]:hover,
li[role="option"][aria-selected="true"], div[role="option"][aria-selected="true"] {
    background:#dbeafe !important;
    color:#111827 !important;
}
/* Keep normal action buttons with white text */
.stButton button, .stDownloadButton button, div[data-testid="stFormSubmitButton"] button {
    color:#ffffff !important;
}
.stButton button *, .stDownloadButton button *, div[data-testid="stFormSubmitButton"] button * {
    color:#ffffff !important;
    opacity:1 !important;
}


/* STRONG CALENDAR FIX: force the date picker header, month/year row, weekday row, and footer to light readable colors */
div[data-baseweb="popover"] *,
div[data-baseweb="calendar"] *,
div[data-baseweb="datepicker"] *,
div[role="dialog"] * {
    color:#111827 !important;
    -webkit-text-fill-color:#111827 !important;
    opacity:1 !important;
}
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="calendar"],
div[data-baseweb="calendar"] > div,
div[data-baseweb="datepicker"],
div[role="dialog"] {
    background:#ffffff !important;
    background-color:#ffffff !important;
}
div[data-baseweb="calendar"] div,
div[data-baseweb="datepicker"] div,
div[role="dialog"] div {
    background-color:#ffffff !important;
}
div[data-baseweb="calendar"] button,
div[data-baseweb="datepicker"] button,
div[role="dialog"] button {
    background:#ffffff !important;
    background-color:#ffffff !important;
    color:#111827 !important;
    -webkit-text-fill-color:#111827 !important;
    border:none !important;
    box-shadow:none !important;
}
div[data-baseweb="calendar"] svg,
div[data-baseweb="datepicker"] svg,
div[role="dialog"] svg {
    fill:#111827 !important;
    stroke:#111827 !important;
    color:#111827 !important;
}
/* currently selected date remains highlighted but readable */
div[data-baseweb="calendar"] button[aria-selected="true"],
div[data-baseweb="datepicker"] button[aria-selected="true"],
div[role="dialog"] button[aria-selected="true"] {
    background:#ef4444 !important;
    background-color:#ef4444 !important;
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    border-radius:999px !important;
}
div[data-baseweb="calendar"] button[aria-selected="true"] *,
div[data-baseweb="datepicker"] button[aria-selected="true"] *,
div[role="dialog"] button[aria-selected="true"] * {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}

</style>
""", unsafe_allow_html=True)


def load_data() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.read_csv(SAMPLE_FILE)
        df.to_csv(DATA_FILE, index=False)
    return clean_expense_data(df)


def save_data(df: pd.DataFrame) -> None:
    output = clean_expense_data(df).copy()
    output["date"] = output["date"].dt.strftime("%Y-%m-%d")
    output.to_csv(DATA_FILE, index=False)


def extract_pdf_text(uploaded) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(uploaded)
        return "\n".join(page.extract_text() or "" for page in reader.pages[:5])
    except Exception as exc:
        return f"PDF could not be processed automatically: {exc}"


df = load_data()

st.markdown("""
<div class="hero-card">
  <div class="main-title">Financial Advisor & Expense Manager</div>
  <div class="subtitle">A polished AI finance dashboard for expense tracking, OCR-style transaction parsing, Indian finance guidance, goal planning, financial health scoring, and advanced insights.</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("👤 User Profile")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=45000, step=1000)
    budget = st.number_input("Monthly Budget (₹)", min_value=0, value=28000, step=1000)
    savings_goal = st.number_input("Savings Goal (₹)", min_value=0, value=10000, step=500)
    philosophy = st.selectbox("Advice Style", ["Balanced", "Warren Buffett", "Robert Kiyosaki", "Ramit Sethi", "Indian Personal Finance"])

    st.divider()
    st.header("📥 Data Sources")
    uploaded_file = st.file_uploader("Upload expense/bank CSV", type=["csv"])
    if uploaded_file is not None:
        uploaded_df = clean_expense_data(pd.read_csv(uploaded_file))
        save_data(pd.concat([df, uploaded_df], ignore_index=True))
        st.success("CSV added. Refresh to view updated data.")

    splitwise_file = st.file_uploader("Upload Splitwise-style CSV", type=["csv"], key="splitwise")
    if splitwise_file is not None:
        sw = pd.read_csv(splitwise_file)
        sw.columns = [c.lower().strip() for c in sw.columns]
        mapped = pd.DataFrame({
            "date": sw.get("date", pd.Timestamp.today()),
            "category": sw.get("category", "UPI Transfer"),
            "amount": sw.get("amount", sw.get("cost", 0)),
            "description": sw.get("description", sw.get("details", "Splitwise expense")),
            "source": "Splitwise CSV"
        })
        save_data(pd.concat([df, clean_expense_data(mapped)], ignore_index=True))
        st.success("Splitwise data added. Refresh to view updated data.")

    if st.button("Reset to Sample Data"):
        save_data(pd.read_csv(SAMPLE_FILE))
        st.success("Data reset completed. Refresh the page.")

summary = get_summary(df, income, budget, savings_goal)
predicted_next = predict_next_month(df)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Expense", f"₹{summary['total_expense']:,.0f}")
col2.metric("Current Savings", f"₹{summary['savings']:,.0f}")
col3.metric("Budget Left", f"₹{summary['budget_left']:,.0f}")
col4.metric("Health Score", f"{summary['health_score']}/100")
col5.metric("Next Month Forecast", f"₹{predicted_next:,.0f}")

st.markdown("<div class='security-note'>🔐 Privacy note: This demo uses mock/local data. Avoid uploading real sensitive bank data unless proper security, encryption, and access control are added.</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Add & Extract", "AI Advisor", "Goals & Budget", "Reports"])

with tab1:
    st.subheader("📊 Advanced Financial Dashboard")
    c1, c2 = st.columns([1.15, .85])
    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("Category-wise Spending")
        category_total = summary["category_total"]
        if not category_total.empty:
            st.bar_chart(category_total)
        else:
            st.info("No spending data available.")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("Expense Distribution")
        if not category_total.empty:
            fig, ax = plt.subplots()
            ax.pie(category_total.values, labels=category_total.index, autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig)
        else:
            st.info("No data available.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("📈 Monthly Trend")
    if not summary["monthly_total"].empty:
        st.line_chart(summary["monthly_total"])

    anomalies = detect_anomalies(df)
    st.subheader("⚠️ High-Spend / Anomaly Detection")
    if anomalies.empty:
        st.success("No unusual high-spend transactions detected.")
    else:
        st.dataframe(anomalies, use_container_width=True)

with tab2:
    l, r = st.columns(2)
    with l:
        st.subheader("➕ Manual Expense Entry")
        with st.form("expense_form", clear_on_submit=True):
            expense_date = st.date_input("Date", value=date.today())
            category = st.selectbox("Category", CATEGORIES)
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
            description = st.text_input("Description")
            submitted = st.form_submit_button("Add Expense")
            if submitted:
                new_row = pd.DataFrame({"date": [pd.to_datetime(expense_date)], "category": [category], "amount": [amount], "description": [description], "source": ["Manual"]})
                save_data(pd.concat([df, new_row], ignore_index=True))
                st.success("Expense added. Refresh to update charts.")
    with r:
        st.subheader("🧾 Payment Message / OCR Text Parser")
        st.caption("Paste text copied from UPI SMS, receipt OCR, or payment screenshot text.")
        raw_text = st.text_area("Example: 2026-07-04 Paid ₹450 to Swiggy", height=160)
        image_file = st.file_uploader("Optional: upload screenshot for record keeping", type=["png", "jpg", "jpeg"], key="image")
        if image_file:
            st.image(image_file, caption="Uploaded payment screenshot preview", use_container_width=True)
            st.info("For full OCR, connect Google Vision, Amazon Textract, Azure Vision, or Tesseract.")
        if st.button("Extract Transactions from Text"):
            parsed = parse_transaction_text(raw_text)
            if parsed.empty:
                st.error("No transaction amount found. Try including ₹ amount and description.")
            else:
                save_data(pd.concat([df, parsed], ignore_index=True))
                st.success(f"Extracted {len(parsed)} transaction(s). Refresh to view them.")
                st.dataframe(parsed, use_container_width=True)

with tab3:
    st.subheader("🤖 Agentic AI Workflow")
    st.markdown('<span class="workflow-pill">Input Sources</span><span class="workflow-pill">Expense Agent</span><span class="workflow-pill">Budget Agent</span><span class="workflow-pill">Advisor Agent</span><span class="workflow-pill">Goal Agent</span><span class="workflow-pill">Report Agent</span>', unsafe_allow_html=True)
    st.markdown('<div class="agent-box"><b>Expense Agent:</b> extracts, cleans, and categorizes manual entries, CSV uploads, Splitwise-style data, and payment text.</div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-box"><b>Budget Agent:</b> compares spending with monthly budget and finds overspending zones.</div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-box"><b>Advisor Agent:</b> generates financial suggestions using selected financial philosophy.</div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-box"><b>Goal Agent:</b> tracks savings progress and financial health score.</div>', unsafe_allow_html=True)

    st.subheader("✨ Personalized Financial Advice")
    for item in generate_financial_advice(df, income, budget, savings_goal, philosophy):
        st.info(item)

    st.subheader("📚 Multi-Guru Financial Philosophy Comparison")
    st.dataframe(guru_comparison(summary["top_category"]), use_container_width=True)

    st.subheader("📄 Upload Financial Book / Article Notes")
    article = st.file_uploader("Upload PDF/TXT notes for advice context", type=["pdf", "txt"])
    if article:
        if article.name.lower().endswith(".pdf"):
            text = extract_pdf_text(article)
        else:
            text = article.read().decode("utf-8", errors="ignore")
        st.text_area("Extracted Content Preview", text[:2000], height=180)
        st.success("Content uploaded. In a full LLM version, this text becomes the advice knowledge base.")

with tab4:
    st.subheader("🎯 Budget, Savings & Indian Finance Planning")
    progress = 0 if savings_goal == 0 else max(0, min(1, summary["savings"] / savings_goal))
    st.progress(progress)
    st.write(f"Savings goal progress: {progress * 100:.1f}%")

    needs_limit = income * 0.5
    wants_limit = income * 0.3
    save_limit = income * 0.2
    plan = pd.DataFrame({
        "Bucket": ["Needs", "Wants", "Savings/Investment"],
        "Recommended Limit": [needs_limit, wants_limit, save_limit],
        "Indian Examples": ["Rent, bills, groceries", "Dining, shopping, entertainment", "SIP, PPF, ELSS, emergency fund"]
    })
    st.dataframe(plan, use_container_width=True)

    st.subheader("🇮🇳 Indian Personal Finance Suggestions")
    st.write("• Build an emergency fund before aggressive investing.")
    st.write("• Explore SIPs for disciplined monthly investing.")
    st.write("• For tax planning, learn about PPF, ELSS, NPS, and 80C options.")
    st.write("• This app gives educational guidance, not certified investment advice.")

with tab5:
    st.subheader("📄 Reports & Export")
    st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
    csv_download = df.copy()
    csv_download["date"] = csv_download["date"].dt.strftime("%Y-%m-%d")
    st.download_button("Download Expense Report CSV", csv_download.to_csv(index=False), "expense_report.csv", "text/csv")

    report_text = f"""Financial Advisor & Expense Manager Report\n\nTotal Expense: ₹{summary['total_expense']:,.0f}\nCurrent Savings: ₹{summary['savings']:,.0f}\nBudget Left: ₹{summary['budget_left']:,.0f}\nHealth Score: {summary['health_score']}/100\nTop Category: {summary['top_category']}\nNext Month Forecast: ₹{predicted_next:,.0f}\n\nAdvice:\n- """ + "\n- ".join(generate_financial_advice(df, income, budget, savings_goal, philosophy))
    st.download_button("Download Financial Summary TXT", report_text, "financial_summary.txt", "text/plain")
