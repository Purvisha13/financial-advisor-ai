import re
from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd

CATEGORIES = [
    "Food", "Travel", "Shopping", "Bills", "Entertainment", "Education", "Health",
    "Groceries", "Rent", "Investment", "Savings", "UPI Transfer", "Other"
]

KEYWORD_CATEGORY = {
    "food": "Food", "swiggy": "Food", "zomato": "Food", "restaurant": "Food", "cafe": "Food",
    "grocery": "Groceries", "dmart": "Groceries", "mart": "Groceries", "supermarket": "Groceries",
    "uber": "Travel", "ola": "Travel", "metro": "Travel", "bus": "Travel", "fuel": "Travel", "petrol": "Travel",
    "amazon": "Shopping", "flipkart": "Shopping", "myntra": "Shopping", "mall": "Shopping", "shoes": "Shopping",
    "electricity": "Bills", "bill": "Bills", "recharge": "Bills", "wifi": "Bills", "rent": "Rent",
    "movie": "Entertainment", "netflix": "Entertainment", "spotify": "Entertainment", "game": "Entertainment",
    "school": "Education", "course": "Education", "book": "Education", "college": "Education",
    "doctor": "Health", "medical": "Health", "pharmacy": "Health", "medicine": "Health",
    "sip": "Investment", "mutual": "Investment", "zerodha": "Investment", "groww": "Investment",
}

GURU_RULES = {
    "Warren Buffett": [
        "Avoid impulse purchases; buy only what gives long-term value.",
        "Keep emergency money before taking risky investment decisions.",
        "Prefer simple, understandable investment habits over complicated choices."
    ],
    "Robert Kiyosaki": [
        "Separate needs, wants, assets, and liabilities before spending.",
        "Try building assets like SIPs, skills, or side-income tools.",
        "Reduce lifestyle expenses that do not improve your future cashflow."
    ],
    "Ramit Sethi": [
        "Create a conscious spending plan: save first, then spend guilt-free.",
        "Automate savings and bill payments where possible.",
        "Cut costs aggressively on things you do not value, not everything."
    ],
    "Indian Personal Finance": [
        "For India, consider SIPs, PPF, ELSS, emergency fund, and insurance basics.",
        "Use INR budgets by category: food, travel, groceries, bills, health, education.",
        "For tax-saving, explore ELSS, PPF, NPS, and 80C options with professional guidance."
    ],
}


def guess_category(text: str) -> str:
    lower = str(text).lower()
    for key, category in KEYWORD_CATEGORY.items():
        if key in lower:
            return category
    return "Other"


def clean_expense_data(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = ["date", "category", "amount", "description", "source"]
    for col in required_columns:
        if col not in df.columns:
            if col == "amount":
                df[col] = 0
            elif col == "source":
                df[col] = "Manual/CSV"
            else:
                df[col] = ""

    df = df[required_columns].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["description"] = df["description"].fillna("").astype(str)
    df["category"] = df["category"].fillna("").astype(str)
    df.loc[df["category"].str.strip().eq(""), "category"] = df["description"].apply(guess_category)
    df["source"] = df["source"].fillna("Manual/CSV").astype(str)
    df = df.dropna(subset=["date"])
    return df


def get_summary(df: pd.DataFrame, income: float, budget: float, savings_goal: float) -> dict:
    total_expense = float(df["amount"].sum()) if not df.empty else 0.0
    savings = float(income - total_expense)
    budget_left = float(budget - total_expense)
    goal_gap = float(savings_goal - savings)
    saving_rate = (savings / income * 100) if income else 0
    spend_rate = (total_expense / income * 100) if income else 0

    if not df.empty:
        category_total = df.groupby("category")["amount"].sum().sort_values(ascending=False)
        monthly_total = df.assign(month=df["date"].dt.to_period("M").astype(str)).groupby("month")["amount"].sum()
        top_category = category_total.index[0]
        top_amount = float(category_total.iloc[0])
    else:
        category_total = pd.Series(dtype=float)
        monthly_total = pd.Series(dtype=float)
        top_category = "No data"
        top_amount = 0.0

    health_score = calculate_health_score(income, total_expense, budget, savings_goal)

    return {
        "total_expense": total_expense,
        "savings": savings,
        "budget_left": budget_left,
        "goal_gap": goal_gap,
        "saving_rate": saving_rate,
        "spend_rate": spend_rate,
        "category_total": category_total,
        "monthly_total": monthly_total,
        "top_category": top_category,
        "top_amount": top_amount,
        "health_score": health_score,
    }


def calculate_health_score(income: float, total: float, budget: float, goal: float) -> int:
    score = 100
    if income <= 0:
        return 50
    saving_rate = (income - total) / income
    if saving_rate < 0:
        score -= 35
    elif saving_rate < 0.1:
        score -= 25
    elif saving_rate < 0.2:
        score -= 12
    if budget > 0 and total > budget:
        score -= 20
    if goal > 0 and (income - total) < goal:
        score -= 15
    return max(0, min(100, int(score)))


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or len(df) < 4:
        return pd.DataFrame(columns=df.columns)
    mean = df["amount"].mean()
    std = df["amount"].std() or 0
    threshold = mean + 1.5 * std
    return df[df["amount"] > threshold].sort_values("amount", ascending=False)


def predict_next_month(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    monthly = df.assign(month=df["date"].dt.to_period("M").astype(str)).groupby("month")["amount"].sum()
    if len(monthly) == 1:
        return float(monthly.iloc[-1])
    weights = range(1, len(monthly) + 1)
    return float(sum(v * w for v, w in zip(monthly.values, weights)) / sum(weights))


def parse_transaction_text(text: str) -> pd.DataFrame:
    rows = []
    lines = [line.strip() for line in str(text).splitlines() if line.strip()]
    amount_re = re.compile(r"(?:₹|rs\.?|inr)?\s*([0-9]+(?:,[0-9]{2,3})*(?:\.[0-9]{1,2})?)", re.I)
    date_re = re.compile(r"(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")
    for line in lines:
        amt_match = amount_re.search(line.replace(",", ""))
        if not amt_match:
            continue
        amount = float(amt_match.group(1).replace(",", ""))
        dt_match = date_re.search(line)
        date_value = pd.to_datetime(dt_match.group(1), errors="coerce") if dt_match else pd.Timestamp.today()
        rows.append({
            "date": date_value,
            "category": guess_category(line),
            "amount": amount,
            "description": line[:120],
            "source": "Payment Text/OCR"
        })
    return clean_expense_data(pd.DataFrame(rows)) if rows else pd.DataFrame(columns=["date", "category", "amount", "description", "source"])


def generate_financial_advice(df: pd.DataFrame, income: float, budget: float, savings_goal: float, philosophy: str = "Balanced") -> List[str]:
    summary = get_summary(df, income, budget, savings_goal)
    advice = []
    if df.empty:
        return ["Add expenses, upload CSV, or paste payment text to get personalized advice."]

    total = summary["total_expense"]
    savings = summary["savings"]
    top_category = summary["top_category"]
    top_amount = summary["top_amount"]

    if budget > 0 and total > budget:
        advice.append(f"Budget Agent: You crossed your budget by ₹{total - budget:,.0f}. Reduce flexible expenses first.")
    elif budget > 0:
        advice.append(f"Budget Agent: You are within budget with ₹{budget - total:,.0f} left.")

    if income > 0:
        saving_rate = (savings / income) * 100
        if saving_rate < 20:
            advice.append("Advisor Agent: Your saving rate is below 20%. Try a 50-30-20 style split: needs, wants, savings.")
        else:
            advice.append(f"Advisor Agent: Good progress. Your saving rate is around {saving_rate:.1f}%.")

    advice.append(f"Expense Agent: Highest spending is {top_category} with ₹{top_amount:,.0f}. Set a weekly cap for this category.")

    if savings_goal > 0:
        if savings >= savings_goal:
            advice.append("Goal Agent: You achieved your savings goal for this month.")
        else:
            advice.append(f"Goal Agent: You need ₹{savings_goal - savings:,.0f} more to reach your savings goal.")

    if philosophy != "Balanced" and philosophy in GURU_RULES:
        advice.extend([f"{philosophy} Lens: {line}" for line in GURU_RULES[philosophy][:2]])
    return advice


def guru_comparison(top_category: str) -> pd.DataFrame:
    data = []
    for guru, rules in GURU_RULES.items():
        data.append({
            "Financial Philosophy": guru,
            "Advice for Your Spending": f"Since your key category is {top_category}, {rules[0]}",
            "Best For": "Long-term wealth" if guru == "Warren Buffett" else "Cashflow mindset" if guru == "Robert Kiyosaki" else "Practical budgeting" if guru == "Ramit Sethi" else "Indian finance planning"
        })
    return pd.DataFrame(data)
