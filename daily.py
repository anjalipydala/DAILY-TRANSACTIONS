import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# load data set
df=pd.read_csv(r"C:\Users\ANJU\Downloads\Daily Household Transactions.csv")
#print first few rows
print(df.head())
#print last few rows
print(df.tail())
#printing all the column names
print(df.columns)
#size of data
print(df.shape)
#checking for null values
print(df.isnull().sum())
#CONVERT 'AMOUNT' TO NUMERIC
df['Amount']=pd.to_numeric(df['Amount'],errors='coerce')
#convert 'date' column to datetime format
df['Date']=pd.to_datetime(df['Date'],errors='coerce')
#BASIC INSIGHTS
#total transactions,income,expense,savings
total_transactions=len(df)
total_income=df[df['Income/Expense'].str.lower()=='income']['Amount'].sum()
total_expense=df[df['Income/Expense'].str.lower()=='expense']['Amount'].sum()
net_savings=total_income -total_expense
average_transaction=df['Amount'].mean()
#print all statements
print("total transactions:",total_transactions)
print("total income:",total_income)
print("total expenses:",total_expense)
print("net savings:",net_savings)
print("average transaction value:",round(average_transaction,2))
#  Extract month and year for grouping
df['Month'] = df['Date'].dt.to_period('M')

#  Monthly summary
monthly_summary = df.groupby(['Month', 'Income/Expense'])['Amount'].sum().unstack(fill_value=0)
monthly_summary['Net Savings'] = monthly_summary.get('Income', 0) - monthly_summary.get('Expense', 0)

# Visualization 1: Monthly Income vs Expense
plt.figure(figsize=(10, 5))
monthly_summary[['Income', 'Expense']].plot(kind='bar', figsize=(10, 5))
plt.title("Monthly Income vs Expense")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.legend(["Income", "Expense"])
plt.grid(True)
plt.show()

#  Visualization 2: Net Savings Trend
plt.figure(figsize=(10, 5))
plt.plot(monthly_summary.index.astype(str), monthly_summary['Net Savings'], marker='o', color='green')
plt.title("Monthly Net Savings Trend")
plt.xlabel("Month")
plt.ylabel("Net Savings")
plt.grid(True)
plt.show()

# Visualization 3: Income vs Expense Pie Chart
plt.figure(figsize=(5, 5))
plt.pie(
    [total_income, total_expense],
    labels=["Income", "Expense"],
    autopct='%1.1f%%',
    colors=['#66b3ff', '#ff9999'],
    startangle=90
)
plt.title("Overall Income vs Expense Distribution")
plt.show()
# Ensure Amount is numeric
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# Clean Income/Expense column
df["Income/Expense"] = df["Income/Expense"].str.strip().str.lower()

# ------------------------------
#  EXPENSE BY CATEGORY
# ------------------------------
expense_df = df[df["Income/Expense"] == "expense"]

expense_by_category = expense_df.groupby("Category")["Amount"].sum()

print("\n💸 Expense by Category:\n", expense_by_category)

# Visualization – Expense by Category
plt.figure(figsize=(10,5))
plt.bar(expense_by_category.index, expense_by_category.values)
plt.title("Expenses by Category")
plt.xlabel("Category")
plt.ylabel("Total Expense")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# CATEGORY WISE ANALYSIS
# ------------------------------
#  COSTLIEST EXPENSE CATEGORY
# ------------------------------
max_category = expense_by_category.idxmax()
max_value = expense_by_category.max()

print("\n🔥 Highest Expense Category:", max_category, "→", max_value)


# ------------------------------
#  SUBCATEGORY BREAKDOWN
# ------------------------------
subcategory_breakdown = expense_df.groupby(["Category", "Subcategory"])["Amount"].sum()

print("\n📂 Subcategory Breakdown:\n", subcategory_breakdown)

# Visualization – Subcategory per Category (one graph)
subcategory_breakdown.unstack(fill_value=0).plot(kind="bar", figsize=(12,6))
plt.title("Subcategory-wise Expense Breakdown")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------
#  INCOME BY SOURCE
# ------------------------------
income_df = df[df["Income/Expense"] == "income"]

income_by_source = income_df.groupby("Category")["Amount"].sum()

print("\n💰 Income by Source:\n", income_by_source)

# Visualization – Income by Category
plt.figure(figsize=(10,5))
plt.bar(income_by_source.index, income_by_source.values)
plt.title("Income by Source")
plt.xlabel("Income Category")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ------------------------------
#  PIE CHART (Income vs Expense Categories)
# ------------------------------
plt.figure(figsize=(6,6))
plt.pie(
    expense_by_category.values,
    labels=expense_by_category.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Expense Distribution by Category")
plt.show()
#MODE OF PAYMENT ANALYSIS
# Make sure Amount is numeric
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# Clean Mode column
df["Mode"] = df["Mode"].str.strip().str.title()

# -------------------------------
#  MOST USED PAYMENT MODE
# -------------------------------
mode_counts = df["Mode"].value_counts()

print("\n💳 Payment Mode Usage Count:\n", mode_counts)

most_used_mode = mode_counts.idxmax()
print("\n⭐ Most Used Payment Mode:", most_used_mode)


# Visualization — Count of transactions by mode
plt.figure(figsize=(8,5))
plt.bar(mode_counts.index, mode_counts.values)
plt.title("Most Frequently Used Payment Modes")
plt.xlabel("Payment Mode")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# -------------------------------
#  AMOUNT SPENT PER PAYMENT MODE
# -------------------------------
expense_df = df[df["Income/Expense"].str.lower() == "expense"]

amount_by_mode = expense_df.groupby("Mode")["Amount"].sum()

print("\n💸 Amount Spent via Each Payment Mode:\n", amount_by_mode)


# Visualization — Total amount spent per mode
plt.figure(figsize=(8,5))
plt.bar(amount_by_mode.index, amount_by_mode.values)
plt.title("Total Amount Spent via Each Payment Mode")
plt.xlabel("Payment Mode")
plt.ylabel("Total Expense")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#SAVINGS PATTERN
# Clean income/expense column
df["Income/Expense"] = df["Income/Expense"].str.strip().str.lower()

# Extract month period
df["Month"] = df["Date"].dt.to_period("M")

# ----------------------------
#  Monthly Income & Expense
# ----------------------------
monthly = df.groupby(["Month", "Income/Expense"])["Amount"].sum().unstack(fill_value=0)

# Ensure both columns exist even if missing in data
monthly["Income"] = monthly.get("income", 0)
monthly["Expense"] = monthly.get("expense", 0)

print("\n📅 Monthly Income & Expense:\n", monthly)

# ----------------------------
#  Monthly Savings
# ----------------------------
monthly["Savings"] = monthly["Income"] - monthly["Expense"]

print("\n💰 Monthly Savings:\n", monthly["Savings"])

# ----------------------------
#  Savings Rate (%)
# ----------------------------
monthly["Savings Rate (%)"] = (monthly["Savings"] / monthly["Income"].replace(0, pd.NA)) * 100

print("\n📈 Savings Rate (%):\n", monthly["Savings Rate (%)"])

# ----------------------------
#  Identify Overspending Months
# ----------------------------
overspending_months = monthly[monthly["Expense"] > monthly["Income"]]

print("\n⚠️ Months with Overspending:\n", overspending_months)





