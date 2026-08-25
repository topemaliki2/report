import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import streamlit as st
import matplotlib.patches as mpatches
from datetime import datetime

# Load the cleaned data
q1_data = pd.read_excel(r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\q1_2026_school_charges_cleaned.xlsx")
q2_data = pd.read_excel(r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\q2_2026_school_charges_cleaned.xlsx")

# Create PDF report with timestamp to avoid permission conflicts
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
pdf_path = rf"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\School_Charges_Analysis_Report_2026_{timestamp}.pdf"
pdf = PdfPages(pdf_path)

# Helper function to create text pages
def create_text_page(fig, text_lines, title):
    fig.text(0.5, 0.95, title, ha='center', va='top', fontsize=16, fontweight='bold')
    y_pos = 0.90
    for line in text_lines:
        fig.text(0.1, y_pos, line, fontsize=9, va='top')
        y_pos -= 0.035
    fig.text(0.5, 0.05, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
             ha='center', fontsize=8, style='italic')

# Page 1: Title and Executive Summary
fig = plt.figure(figsize=(8.5, 11))
create_text_page(fig, [
    "",
    "SCHOOL CHARGES ANALYSIS REPORT - FIRST HALF 2026",
    "",
    "Executive Summary:",
    "",
    "This report presents a comprehensive analysis of school charges data for the first half",
    "of 2026 (January to June). The analysis includes student enrollment patterns across",
    "different academic levels, status categories (Indigene/Non-Indigene), and program types",
    "(Science/Non-Science).",
    "",
    "Data Sources:",
    "- PDF files for each month (January - June 2026)",
    "- Total records processed: 192 (96 Q1 + 96 Q2)",
    "- Total students analyzed: 27,336 (26,004 Q1 + 1,332 Q2)",
    "",
    "Key Findings:",
    "- Q1 2026 showed significantly higher enrollment compared to Q2 2026",
    "- Indigene students consistently outnumber Non-Indigene students",
    "- Non-Science programs have higher enrollment than Science programs",
    "- NDFTII and HNDFTI are the most populated levels across both quarters"
], "SCHOOL CHARGES ANALYSIS REPORT - 2026")
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 2: Q1 2026 Summary
fig = plt.figure(figsize=(8.5, 11))
q1_monthly = q1_data.groupby('MONTH')['NO OF STUDENTS'].sum()
q1_status = q1_data.groupby('STATUS')['NO OF STUDENTS'].sum()
q1_science = q1_data.groupby('SCIENCE/NON-SCIENCE')['NO OF STUDENTS'].sum()
q1_level = q1_data.groupby('LEVEL')['NO OF STUDENTS'].sum().sort_values(ascending=False)

# Build complete text including level breakdown
q1_text_lines = [
    "",
    "Q1 2026 (JANUARY - MARCH) SUMMARY",
    "",
    "Monthly Breakdown:",
    f"- January: {q1_monthly.get('January', 0):,} students",
    f"- February: {q1_monthly.get('February', 0):,} students", 
    f"- March: {q1_monthly.get('March', 0):,} students",
    f"- Total Q1: {q1_monthly.sum():,} students",
    "",
    "Status Distribution:",
    f"- Indigene: {q1_status.get('INDIGENE', 0):,} students ({q1_status.get('INDIGENE', 0)/q1_status.sum()*100:.1f}%)",
    f"- Non-Indigene: {q1_status.get('NON-INDIGENE', 0):,} students ({q1_status.get('NON-INDIGENE', 0)/q1_status.sum()*100:.1f}%)",
    "",
    "Program Type Distribution:",
    f"- Non-Science: {q1_science.get('NON-SCIENCE', 0):,} students ({q1_science.get('NON-SCIENCE', 0)/q1_science.sum()*100:.1f}%)",
    f"- Science: {q1_science.get('SCIENCE', 0):,} students ({q1_science.get('SCIENCE', 0)/q1_science.sum()*100:.1f}%)",
    "",
    "Level Distribution (Top 5):",
]

# Add level breakdown to text lines
for level, count in q1_level.head(5).items():
    q1_text_lines.append(f"- {level}: {count:,} students")

create_text_page(fig, q1_text_lines, "Q1 2026 SUMMARY STATISTICS")
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 3: Q2 2026 Summary
fig = plt.figure(figsize=(8.5, 11))
q2_monthly = q2_data.groupby('MONTH')['NO OF STUDENTS'].sum()
q2_status = q2_data.groupby('STATUS')['NO OF STUDENTS'].sum()
q2_science = q2_data.groupby('SCIENCE/NON-SCIENCE')['NO OF STUDENTS'].sum()
q2_level = q2_data.groupby('LEVEL')['NO OF STUDENTS'].sum().sort_values(ascending=False)

# Build complete text including level breakdown
q2_text_lines = [
    "",
    "Q2 2026 (APRIL - JUNE) SUMMARY",
    "",
    "Monthly Breakdown:",
    f"- April: {q2_monthly.get('April', 0):,} students",
    f"- May: {q2_monthly.get('May', 0):,} students",
    f"- June: {q2_monthly.get('June', 0):,} students",
    f"- Total Q2: {q2_monthly.sum():,} students",
    "",
    "Status Distribution:",
    f"- Indigene: {q2_status.get('INDIGENE', 0):,} students ({q2_status.get('INDIGENE', 0)/q2_status.sum()*100:.1f}%)",
    f"- Non-Indigene: {q2_status.get('NON-INDIGENE', 0):,} students ({q2_status.get('NON-INDIGENE', 0)/q2_status.sum()*100:.1f}%)",
    "",
    "Program Type Distribution:",
    f"- Non-Science: {q2_science.get('NON-SCIENCE', 0):,} students ({q2_science.get('NON-SCIENCE', 0)/q2_science.sum()*100:.1f}%)",
    f"- Science: {q2_science.get('SCIENCE', 0):,} students ({q2_science.get('SCIENCE', 0)/q2_science.sum()*100:.1f}%)",
    "",
    "Level Distribution (Top 5):",
]

# Add level breakdown to text lines
for level, count in q2_level.head(5).items():
    q2_text_lines.append(f"- {level}: {count:,} students")

create_text_page(fig, q2_text_lines, "Q2 2026 SUMMARY STATISTICS")
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 4: Q1 Charts - Status and Level
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 11))

# Q1 Status Pie Chart
q1_status.plot(kind='pie', ax=ax1, autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4'], 
               startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax1.set_title('Q1 2026 - Students by Status', fontsize=12, fontweight='bold')
ax1.set_ylabel('')

# Q1 Level Bar Chart
q1_level.plot(kind='bar', ax=ax2, color='steelblue')
ax2.set_title('Q1 2026 - Students by Level', fontsize=12, fontweight='bold')
ax2.set_xlabel('Level', fontsize=10)
ax2.set_ylabel('Number of Students', fontsize=10)
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 5: Q1 Charts - Science and Monthly
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 11))

# Q1 Science Pie Chart
q1_science.plot(kind='pie', ax=ax1, autopct='%1.1f%%', colors=['#45B7D1', '#96CEB4'],
                startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax1.set_title('Q1 2026 - Students by Program Type', fontsize=12, fontweight='bold')
ax1.set_ylabel('')

# Q1 Monthly Bar Chart
q1_monthly = q1_monthly.reindex(['January', 'February', 'March'])
q1_monthly.plot(kind='bar', ax=ax2, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax2.set_title('Q1 2026 - Monthly Student Distribution', fontsize=12, fontweight='bold')
ax2.set_xlabel('Month', fontsize=10)
ax2.set_ylabel('Number of Students', fontsize=10)
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 6: Q2 Charts - Status and Level
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 11))

# Q2 Status Pie Chart
q2_status.plot(kind='pie', ax=ax1, autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4'],
               startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax1.set_title('Q2 2026 - Students by Status', fontsize=12, fontweight='bold')
ax1.set_ylabel('')

# Q2 Level Bar Chart
q2_level.plot(kind='bar', ax=ax2, color='steelblue')
ax2.set_title('Q2 2026 - Students by Level', fontsize=12, fontweight='bold')
ax2.set_xlabel('Level', fontsize=10)
ax2.set_ylabel('Number of Students', fontsize=10)
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 7: Q2 Charts - Science and Monthly
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 11))

# Q2 Science Pie Chart
q2_science.plot(kind='pie', ax=ax1, autopct='%1.1f%%', colors=['#45B7D1', '#96CEB4'],
                startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax1.set_title('Q2 2026 - Students by Program Type', fontsize=12, fontweight='bold')
ax1.set_ylabel('')

# Q2 Monthly Bar Chart
q2_monthly = q2_monthly.reindex(['April', 'May', 'June'])
q2_monthly.plot(kind='bar', ax=ax2, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
ax2.set_title('Q2 2026 - Monthly Student Distribution', fontsize=12, fontweight='bold')
ax2.set_xlabel('Month', fontsize=10)
ax2.set_ylabel('Number of Students', fontsize=10)
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 8: Comparative Analysis
fig = plt.figure(figsize=(8.5, 11))

# Combine data for comparison
combined_monthly = pd.concat([
    q1_data.groupby('MONTH')['NO OF STUDENTS'].sum(),
    q2_data.groupby('MONTH')['NO OF STUDENTS'].sum()
])

combined_status = pd.DataFrame({
    'Q1': q1_status,
    'Q2': q2_status
})

combined_science = pd.DataFrame({
    'Q1': q1_science,
    'Q2': q2_science
})

create_text_page(fig, [
    "",
    "COMPARATIVE ANALYSIS: Q1 vs Q2 2026",
    "",
    "Quarterly Comparison:",
    f"- Q1 2026 Total: {q1_data['NO OF STUDENTS'].sum():,} students",
    f"- Q2 2026 Total: {q2_data['NO OF STUDENTS'].sum():,} students",
    f"- Difference: {q1_data['NO OF STUDENTS'].sum() - q2_data['NO OF STUDENTS'].sum():,} students",
    f"- Q2 is {(q2_data['NO OF STUDENTS'].sum()/q1_data['NO OF STUDENTS'].sum()*100):.1f}% of Q1 enrollment",
    "",
    "Status Comparison:",
    f"- Q1 Indigene: {q1_status.get('INDIGENE', 0):,} ({q1_status.get('INDIGENE', 0)/q1_status.sum()*100:.1f}%)",
    f"- Q2 Indigene: {q2_status.get('INDIGENE', 0):,} ({q2_status.get('INDIGENE', 0)/q2_status.sum()*100:.1f}%)",
    "",
    f"- Q1 Non-Indigene: {q1_status.get('NON-INDIGENE', 0):,} ({q1_status.get('NON-INDIGENE', 0)/q1_status.sum()*100:.1f}%)",
    f"- Q2 Non-Indigene: {q2_status.get('NON-INDIGENE', 0):,} ({q2_status.get('NON-INDIGENE', 0)/q2_status.sum()*100:.1f}%)",
    "",
    "Program Type Comparison:",
    f"- Q1 Non-Science: {q1_science.get('NON-SCIENCE', 0):,} ({q1_science.get('NON-SCIENCE', 0)/q1_science.sum()*100:.1f}%)",
    f"- Q2 Non-Science: {q2_science.get('NON-SCIENCE', 0):,} ({q2_science.get('NON-SCIENCE', 0)/q2_science.sum()*100:.1f}%)",
    "",
    f"- Q1 Science: {q1_science.get('SCIENCE', 0):,} ({q1_science.get('SCIENCE', 0)/q1_science.sum()*100:.1f}%)",
    f"- Q2 Science: {q2_science.get('SCIENCE', 0):,} ({q2_science.get('SCIENCE', 0)/q2_science.sum()*100:.1f}%)"
], "COMPARATIVE ANALYSIS")

pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 9: Key Insights and Recommendations
fig = plt.figure(figsize=(8.5, 11))
create_text_page(fig, [
    "",
    "KEY INSIGHTS AND RECOMMENDATIONS",
    "",
    "Key Insights:",
    "",
    "1. Enrollment Trends:",
    "   - Q1 shows significantly higher enrollment than Q2",
    "   - March has the highest enrollment in Q1 (12,323 students)",
    "   - June has the highest enrollment in Q2 (724 students)",
    "",
    "2. Demographic Patterns:",
    "   - Indigene students consistently outnumber Non-Indigene students",
    "   - The ratio remains consistent across both quarters (~58:42)",
    "",
    "3. Program Preferences:",
    "   - Non-Science programs are more popular than Science programs",
    "   - The preference ratio is approximately 59:41 across both quarters",
    "",
    "4. Level Distribution:",
    "   - NDFTII and HNDFTI are the most populated levels",
    "   - Higher diploma levels (HND) show strong enrollment",
    "",
    "Recommendations:",
    "",
    "1. Investigate the significant drop in enrollment from Q1 to Q2",
    "2. Consider strategies to boost Science program enrollment",
    "3. Maintain the strong Indigene student representation",
    "4. Focus recruitment efforts on underrepresented levels",
    "5. Monitor monthly enrollment patterns for better resource planning"
], "KEY INSIGHTS AND RECOMMENDATIONS")

pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Page 10: Data Quality and Methodology
fig = plt.figure(figsize=(8.5, 11))
create_text_page(fig, [
    "",
    "DATA QUALITY AND METHODOLOGY",
    "",
    "Data Sources:",
    "- PDF files extracted from desktop for each month (Jan-Jun 2026)",
    "- Original file names: JAN 2026 SCHOOL CHARGE.pdf through JUNE 2026 SCHOOL CHARGE.pdf",
    "",
    "Data Cleaning Process:",
    "- Used PyMuPDF library to extract text from PDF files",
    "- Implemented pattern recognition to parse structured data",
    "- Handled both separate and combined S/N and LEVEL formatting",
    "- Removed duplicate and empty records",
    "- Standardized data types and formats",
    "",
    "Data Validation:",
    "- All numeric fields validated for proper formatting",
    "- Missing values handled appropriately",
    "- Consistency checks performed across months",
    "- Total student counts verified against PDF totals",
    "",
    "Analysis Methods:",
    "- Descriptive statistics and frequency analysis",
    "- Cross-tabulation by level, status, and program type",
    "- Visual analysis using pie charts and bar graphs",
    "- Comparative analysis between quarters",
    "",
    "Limitations:",
    "- Analysis based on enrollment counts only",
    "- No demographic or socioeconomic data available",
    "- Monthly variations may reflect seasonal patterns",
    "- Q2 data shows significantly lower enrollment"
], "DATA QUALITY AND METHODOLOGY")

pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Close the PDF
pdf.close()

print(f"PDF report successfully generated: {pdf_path}")
print("The report contains 10 pages with comprehensive analysis and visualizations.")

# Generate CSV summary report
csv_path = rf"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\School_Charges_Analysis_Report_2026_{timestamp}.csv"
summary_data = []

# Q1 Summary
summary_data.append(['Q1 2026 SUMMARY', '', '', ''])
summary_data.append(['Metric', 'Category', 'Count', 'Percentage'])
summary_data.append(['Monthly', 'January', f"{q1_monthly.get('January', 0):,}", ''])
summary_data.append(['Monthly', 'February', f"{q1_monthly.get('February', 0):,}", ''])
summary_data.append(['Monthly', 'March', f"{q1_monthly.get('March', 0):,}", ''])
summary_data.append(['Monthly', 'Total Q1', f"{q1_monthly.sum():,}", ''])
summary_data.append(['Status', 'Indigene', f"{q1_status.get('INDIGENE', 0):,}", f"{q1_status.get('INDIGENE', 0)/q1_status.sum()*100:.1f}%"])
summary_data.append(['Status', 'Non-Indigene', f"{q1_status.get('NON-INDIGENE', 0):,}", f"{q1_status.get('NON-INDIGENE', 0)/q1_status.sum()*100:.1f}%"])
summary_data.append(['Program Type', 'Non-Science', f"{q1_science.get('NON-SCIENCE', 0):,}", f"{q1_science.get('NON-SCIENCE', 0)/q1_science.sum()*100:.1f}%"])
summary_data.append(['Program Type', 'Science', f"{q1_science.get('SCIENCE', 0):,}", f"{q1_science.get('SCIENCE', 0)/q1_science.sum()*100:.1f}%"])
summary_data.append(['', '', '', ''])

# Q2 Summary
summary_data.append(['Q2 2026 SUMMARY', '', '', ''])
summary_data.append(['Metric', 'Category', 'Count', 'Percentage'])
summary_data.append(['Monthly', 'April', f"{q2_monthly.get('April', 0):,}", ''])
summary_data.append(['Monthly', 'May', f"{q2_monthly.get('May', 0):,}", ''])
summary_data.append(['Monthly', 'June', f"{q2_monthly.get('June', 0):,}", ''])
summary_data.append(['Monthly', 'Total Q2', f"{q2_monthly.sum():,}", ''])
summary_data.append(['Status', 'Indigene', f"{q2_status.get('INDIGENE', 0):,}", f"{q2_status.get('INDIGENE', 0)/q2_status.sum()*100:.1f}%"])
summary_data.append(['Status', 'Non-Indigene', f"{q2_status.get('NON-INDIGENE', 0):,}", f"{q2_status.get('NON-INDIGENE', 0)/q2_status.sum()*100:.1f}%"])
summary_data.append(['Program Type', 'Non-Science', f"{q2_science.get('NON-SCIENCE', 0):,}", f"{q2_science.get('NON-SCIENCE', 0)/q2_science.sum()*100:.1f}%"])
summary_data.append(['Program Type', 'Science', f"{q2_science.get('SCIENCE', 0):,}", f"{q2_science.get('SCIENCE', 0)/q2_science.sum()*100:.1f}%"])
summary_data.append(['', '', '', ''])

# Comparative Analysis
summary_data.append(['COMPARATIVE ANALYSIS', '', '', ''])
summary_data.append(['Metric', 'Q1', 'Q2', 'Difference'])
summary_data.append(['Total Students', f"{q1_data['NO OF STUDENTS'].sum():,}", f"{q2_data['NO OF STUDENTS'].sum():,}", f"{q1_data['NO OF STUDENTS'].sum() - q2_data['NO OF STUDENTS'].sum():,}"])
summary_data.append(['Indigene', f"{q1_status.get('INDIGENE', 0):,}", f"{q2_status.get('INDIGENE', 0):,}", f"{q1_status.get('INDIGENE', 0) - q2_status.get('INDIGENE', 0):,}"])
summary_data.append(['Non-Indigene', f"{q1_status.get('NON-INDIGENE', 0):,}", f"{q2_status.get('NON-INDIGENE', 0):,}", f"{q1_status.get('NON-INDIGENE', 0) - q2_status.get('NON-INDIGENE', 0):,}"])
summary_data.append(['Non-Science', f"{q1_science.get('NON-SCIENCE', 0):,}", f"{q2_science.get('NON-SCIENCE', 0):,}", f"{q1_science.get('NON-SCIENCE', 0) - q2_science.get('NON-SCIENCE', 0):,}"])
summary_data.append(['Science', f"{q1_science.get('SCIENCE', 0):,}", f"{q2_science.get('SCIENCE', 0):,}", f"{q1_science.get('SCIENCE', 0) - q2_science.get('SCIENCE', 0):,}"])

# Create CSV
import csv
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(summary_data)

print(f"CSV report successfully generated: {csv_path}")

# Generate Excel summary report
excel_path = rf"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\School_Charges_Analysis_Report_2026_{timestamp}.xlsx"
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    # Q1 Summary Sheet
    q1_summary_df = pd.DataFrame({
        'Metric': ['Monthly', 'Monthly', 'Monthly', 'Monthly', 'Status', 'Status', 'Program Type', 'Program Type'],
        'Category': ['January', 'February', 'March', 'Total Q1', 'Indigene', 'Non-Indigene', 'Non-Science', 'Science'],
        'Count': [q1_monthly.get('January', 0), q1_monthly.get('February', 0), q1_monthly.get('March', 0), 
                 q1_monthly.sum(), q1_status.get('INDIGENE', 0), q1_status.get('NON-INDIGENE', 0),
                 q1_science.get('NON-SCIENCE', 0), q1_science.get('SCIENCE', 0)],
        'Percentage': ['', '', '', '', 
                      f"{q1_status.get('INDIGENE', 0)/q1_status.sum()*100:.1f}%", 
                      f"{q1_status.get('NON-INDIGENE', 0)/q1_status.sum()*100:.1f}%",
                      f"{q1_science.get('NON-SCIENCE', 0)/q1_science.sum()*100:.1f}%", 
                      f"{q1_science.get('SCIENCE', 0)/q1_science.sum()*100:.1f}%"]
    })
    q1_summary_df.to_excel(writer, sheet_name='Q1 2026 Summary', index=False)
    
    # Q2 Summary Sheet
    q2_summary_df = pd.DataFrame({
        'Metric': ['Monthly', 'Monthly', 'Monthly', 'Monthly', 'Status', 'Status', 'Program Type', 'Program Type'],
        'Category': ['April', 'May', 'June', 'Total Q2', 'Indigene', 'Non-Indigene', 'Non-Science', 'Science'],
        'Count': [q2_monthly.get('April', 0), q2_monthly.get('May', 0), q2_monthly.get('June', 0), 
                 q2_monthly.sum(), q2_status.get('INDIGENE', 0), q2_status.get('NON-INDIGENE', 0),
                 q2_science.get('NON-SCIENCE', 0), q2_science.get('SCIENCE', 0)],
        'Percentage': ['', '', '', '', 
                      f"{q2_status.get('INDIGENE', 0)/q2_status.sum()*100:.1f}%", 
                      f"{q2_status.get('NON-INDIGENE', 0)/q2_status.sum()*100:.1f}%",
                      f"{q2_science.get('NON-SCIENCE', 0)/q2_science.sum()*100:.1f}%", 
                      f"{q2_science.get('SCIENCE', 0)/q2_science.sum()*100:.1f}%"]
    })
    q2_summary_df.to_excel(writer, sheet_name='Q2 2026 Summary', index=False)
    
    # Comparative Analysis Sheet
    comparative_df = pd.DataFrame({
        'Metric': ['Total Students', 'Indigene', 'Non-Indigene', 'Non-Science', 'Science'],
        'Q1': [q1_data['NO OF STUDENTS'].sum(), q1_status.get('INDIGENE', 0), q1_status.get('NON-INDIGENE', 0),
              q1_science.get('NON-SCIENCE', 0), q1_science.get('SCIENCE', 0)],
        'Q2': [q2_data['NO OF STUDENTS'].sum(), q2_status.get('INDIGENE', 0), q2_status.get('NON-INDIGENE', 0),
              q2_science.get('NON-SCIENCE', 0), q2_science.get('SCIENCE', 0)],
        'Difference': [q1_data['NO OF STUDENTS'].sum() - q2_data['NO OF STUDENTS'].sum(),
                       q1_status.get('INDIGENE', 0) - q2_status.get('INDIGENE', 0),
                       q1_status.get('NON-INDIGENE', 0) - q2_status.get('NON-INDIGENE', 0),
                       q1_science.get('NON-SCIENCE', 0) - q2_science.get('NON-SCIENCE', 0),
                       q1_science.get('SCIENCE', 0) - q2_science.get('SCIENCE', 0)]
    })
    comparative_df.to_excel(writer, sheet_name='Comparative Analysis', index=False)
    
    # Level Distribution Sheet
    level_df = pd.DataFrame({
        'Level': q1_level.index.tolist(),
        'Q1 Count': q1_level.values.tolist(),
        'Q2 Count': [q2_level.get(level, 0) for level in q1_level.index],
        'Q1 Percentage': [f"{count/q1_level.sum()*100:.1f}%" for count in q1_level.values],
        'Q2 Percentage': [f"{q2_level.get(level, 0)/q2_level.sum()*100:.1f}%" if q2_level.sum() > 0 else "0%" for level in q1_level.index]
    })
    level_df.to_excel(writer, sheet_name='Level Distribution', index=False)

print(f"Excel report successfully generated: {excel_path}")
print("All reports (PDF, CSV, Excel) have been generated successfully.")
