# Financial Advisor & Expense Manager - Agentic AI Project

A polished fintech AI agent project that tracks expenses, analyzes spending, gives financial advice, supports Indian personal finance planning, and includes Track B-style advanced features.

## Project Overview

This project is an AI-powered financial advisor and expense manager. It helps users:

- Add daily expenses manually
- Upload expense or bank-statement CSV files
- Upload Splitwise-style CSV data
- Paste UPI/payment message text and extract transactions
- Preview payment screenshots for OCR-ready workflow
- Analyze category-wise spending
- Track savings goals and budget limits
- Detect unusually high expenses
- Forecast next-month spending
- Compare financial advice styles from different financial philosophies
- Export expense reports and financial summaries

## Track B Requirements Covered

|---|---|
| 3-4 integrated tools | CSV upload, Splitwise-style upload, payment text parser, PDF/TXT content upload, analytics engine |
| Advanced financial analysis | Health score, anomaly detection, category trend, next-month forecast |
| Multi-guru financial analysis | Warren Buffett, Robert Kiyosaki, Ramit Sethi, Indian Personal Finance comparison |
| Automated categorization | Keyword-based category learning for payment text and descriptions |
| Goal tracking | Savings goal progress, budget left, 50-30-20 planning |
| Advanced dashboard | Streamlit tabs, cards, charts, reports, aesthetic UI |
| Security basics | Privacy note, local mock data, safe demo-first workflow |
| Export functionality | CSV report and TXT financial summary |

## Tech Stack

- Frontend/Dashboard: Streamlit
- Data Processing: Python, Pandas
- Visualization: Matplotlib, Streamlit charts
- Document Processing: pypdf
- Local Storage: CSV file

## Folder Structure

```text
financial_advisor_ai/
├── app.py
├── analysis.py
├── sample_expenses.csv
├── requirements.txt
└── README.md
```

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
streamlit run app.py
```

## CSV Format

Use this structure:

```csv
date,category,amount,description,source
2026-06-01,Food,250,Lunch,Manual
2026-06-02,Travel,120,Metro recharge,CSV
```

If category is empty, the system tries to categorize it using keywords.

## Payment Text Example

Paste text like:

```text
2026-07-04 Paid ₹450 to Swiggy
2026-07-05 UPI payment Rs 1200 to Amazon
2026-07-06 Metro recharge INR 300
```

The parser extracts amount, date, category, description, and source.

## Agentic AI Workflow

```text
User Data Sources
       ↓
Expense Agent - cleans and categorizes data
       ↓
Budget Agent - checks overspending
       ↓
Advisor Agent - gives financial suggestions
       ↓
Goal Agent - tracks savings and health score
       ↓
Report Agent - exports dashboard reports
```

## Financial Advice Disclaimer

This app gives educational financial guidance only. It does not provide certified investment advice. Users should consult qualified financial advisors before making major investment, tax, or insurance decisions.

## Future Enhancements

- Connect real OCR APIs such as Google Vision, Amazon Textract, Azure Vision, or Tesseract
- Add secure login and encrypted database storage
- Add FastAPI backend and PostgreSQL database
- Build React/Next.js frontend for full Track B deployment
- Add live Splitwise API integration
- Add investment portfolio simulator
- Add feedback system to evaluate advice usefulness

8. Guru comparison
9. Report download
10. Project requirements tab
