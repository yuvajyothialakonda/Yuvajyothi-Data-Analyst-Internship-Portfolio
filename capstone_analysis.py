# capstone_analysis.py
# Task 5 - Capstone Integration & Portfolio Finalization
#
# What this script does:
# 1. Loads the cleaned sales dataset
# 2. Calculates the key numbers (revenue, orders, customers, etc.)
# 3. Shows top categories, products, cities, and age groups
# 4. Builds one summary dashboard image with 4 charts
#
# How to run:
#   pip install pandas matplotlib openpyxl
#   python capstone_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data
data = pd.read_excel("Cleaned_Sales_Dataset.xlsx")

print("Dataset shape:", data.shape)
print("Missing values:", data.isnull().sum().sum())

# 2. Basic KPIs
total_revenue = data["Total_Sales"].sum()
total_orders = data["Order_ID"].nunique()
total_customers = data["Customer_ID"].nunique()
avg_order_value = data["Total_Sales"].mean()

print("\n--- Key Numbers ---")
print("Total Revenue:", round(total_revenue, 2))
print("Total Orders:", total_orders)
print("Unique Customers:", total_customers)
print("Average Order Value:", round(avg_order_value, 2))

# 3. Revenue by category, product, city, age group
by_category = data.groupby("Category")["Total_Sales"].sum().sort_values(ascending=False)
by_product = data.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False).head(5)
by_city = data.groupby("City")["Total_Sales"].sum().sort_values(ascending=False).head(5)
by_age_group = data.groupby("Age_Group")["Total_Sales"].sum().sort_values(ascending=False)

months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
by_month = data.groupby("Order_Month")["Total_Sales"].sum().reindex(months)

print("\n--- Revenue by Category ---")
print(by_category)

print("\n--- Top 5 Products ---")
print(by_product)

print("\n--- Top 5 Cities ---")
print(by_city)

print("\n--- Revenue by Age Group ---")
print(by_age_group)

print("\nBest month:", by_month.idxmax(), "-", round(by_month.max(), 2))
print("Weakest month:", by_month.idxmin(), "-", round(by_month.min(), 2))

# 4. Build a simple 4-chart dashboard and save it as an image
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("Sales Performance - Capstone Summary Dashboard", fontsize=16, fontweight="bold")

axes[0, 0].bar(by_category.index, by_category.values / 1e6, color="#2E5EAA")
axes[0, 0].set_title("Revenue by Category")
axes[0, 0].set_ylabel("Revenue (Millions)")
axes[0, 0].tick_params(axis="x", rotation=30)

axes[0, 1].plot(by_month.index, by_month.values / 1e6, marker="o", color="#D9822B")
axes[0, 1].set_title("Monthly Revenue Trend")
axes[0, 1].set_ylabel("Revenue (Millions)")
axes[0, 1].tick_params(axis="x", rotation=45)

axes[1, 0].barh(by_city.index[::-1], by_city.values[::-1] / 1e6, color="#3F9C6D")
axes[1, 0].set_title("Top 5 Cities by Revenue")
axes[1, 0].set_xlabel("Revenue (Millions)")

axes[1, 1].pie(by_age_group.values, labels=by_age_group.index, autopct="%1.0f%%")
axes[1, 1].set_title("Revenue Share by Age Group")

plt.tight_layout()
plt.savefig("assets/capstone_dashboard.png", dpi=150, bbox_inches="tight")

print("\nDashboard saved to assets/capstone_dashboard.png")
