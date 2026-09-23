import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Φόρτωση του επεξεργασμένου RFM
rfm = pd.read_csv('rfm_analysis.csv')

# 2. Χαρτογράφηση Segments βάσει R_Score και F_Score (Industry Standard RFM Map)
segment_map = {
    r'[1-2][1-2]': 'Hibernating / Lost',
    r'[1-2][3-4]': 'At Risk',
    r'[1-2]5': 'Cannot Lose Them',
    r'3[1-2]': 'About to Sleep',
    r'33': 'Need Attention',
    r'[3-4][4-5]': 'Loyal Customers',
    r'41': 'Promising',
    r'51': 'New Customers',
    r'[4-5][2-3]': 'Potential Loyalists',
    r'5[4-5]': 'Champions'
}

# Δημιουργία στήλης Segment
rfm['RF_String'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str)
rfm['Customer_Segment'] = rfm['RF_String'].replace(segment_map, regex=True)

# 3. Σύνοψη ανά Segment (Metrics που ενδιαφέρουν τους stakeholders)
segment_summary = rfm.groupby('Customer_Segment').agg(
    Customer_Count=('CustomerID', 'count'),
    Avg_Recency=('Recency', 'mean'),
    Avg_Frequency=('Frequency', 'mean'),
    Total_Monetary=('Monetary', 'sum'),
    Avg_Monetary=('Monetary', 'mean')
).reset_index()

# Υπολογισμός ποσοστού επί των συνολικών εσόδων
segment_summary['Revenue_Share_%'] = (segment_summary['Total_Monetary'] / segment_summary['Total_Monetary'].sum()) * 100
segment_summary['Customer_Share_%'] = (segment_summary['Customer_Count'] / segment_summary['Customer_Count'].sum()) * 100

segment_summary = segment_summary.sort_values(by='Total_Monetary', ascending=False)
print("\n--- Business Summary ανά Segment ---")
print(segment_summary[['Customer_Segment', 'Customer_Count', 'Customer_Share_%', 'Revenue_Share_%', 'Avg_Monetary']].round(2))

# Αποθήκευση της σύνοψης
segment_summary.to_csv('segment_summary.csv', index=False)

# 4. Γράφημα 1: Κατανομή Εσόδων ανά Customer Segment
plt.figure(figsize=(10, 6))
sns.barplot(
    data=segment_summary,
    x='Revenue_Share_%',
    y='Customer_Segment',
    palette='Blues_r'
)
plt.title('Share of Total Revenue by Customer Segment (%)', fontsize=14, weight='bold')
plt.xlabel('Revenue Share (%)', fontsize=12)
plt.ylabel('Customer Segment', fontsize=12)
plt.tight_layout()
plt.savefig('revenue_by_segment.png', dpi=300)
plt.close()

# 5. Γράφημα 2: Scatter / Bubble Chart (Recency vs Frequency ανά Segment)
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=segment_summary,
    x='Avg_Recency',
    y='Avg_Frequency',
    size='Customer_Count',
    hue='Customer_Segment',
    sizes=(100, 2000),
    palette='tab10',
    legend=False
)

for i in range(len(segment_summary)):
    plt.text(
        x=segment_summary['Avg_Recency'][i] + 5,
        y=segment_summary['Avg_Frequency'][i],
        s=segment_summary['Customer_Segment'][i],
        fontdict=dict(color='black', size=10)
    )

plt.title('Customer Segments: Recency vs Frequency', fontsize=14, weight='bold')
plt.xlabel('Average Days Since Last Purchase (Recency)', fontsize=12)
plt.ylabel('Average Order Frequency', fontsize=12)
plt.tight_layout()
plt.savefig('recency_vs_frequency.png', dpi=300)
plt.close()

print("\nΤα γραφήματα 'revenue_by_segment.png' και 'recency_vs_frequency.png' αποθηκεύτηκαν επιτυχώς στον φάκελο!")