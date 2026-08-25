import pandas as pd
import numpy as np
import pymupdf  # PyMuPDF
import re
import matplotlib.pyplot as plt

# Load the March 2025 school fees charges data from PDF
pdf_path = r"C:\Users\ALH MALIK TOPE\Desktop\MARCH 2025 SCHOOL CHARGE BREAKDOWN.pdf"

print("Extracting data from PDF using PyMuPDF...")

# Open the PDF file
doc = pymupdf.open(pdf_path)

print(f"Number of pages: {len(doc)}")

# Extract text from each page
all_text = ""
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    all_text += text

doc.close()

# Parse the extracted text into structured data
print("\nParsing extracted text...")

# Split text into lines
lines = all_text.split('\n')

# Filter out empty lines and clean up
lines = [line.strip() for line in lines if line.strip()]

print(f"Total lines extracted: {len(lines)}")

# Print all lines to understand the structure better
print("\nAll extracted lines:")
for i, line in enumerate(lines):
    print(f"{i}: {line}")

# The data appears to have inconsistent formatting. Let's use a regex-based approach
# to extract the structured data pattern: S/N, LEVEL, STATUS, SCIENCE/NON-SCIENCE, NO OF STUDENTS

structured_data = []

# Look for patterns where we have a number followed by level, status, science/non-science, and student count
# Pattern: digit(s) -> level -> status -> science/non-science -> digit(s)

i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this line is a sequence number (S/N)
    if line.isdigit() and int(line) <= 50:  # Assuming max 50 records
        sn = int(line)
        
        # Look ahead for the next 4 fields
        if i + 4 < len(lines):
            level = lines[i + 1]
            status = lines[i + 2]
            science = lines[i + 3]
            students = lines[i + 4]
            
            # Track if we had combined level/status
            combined = False
            
            # Handle cases where level and status might be on the same line
            # Check if level contains status keywords
            if 'INDIGENE' in level.upper() or 'NON-INDIGENE' in level.upper():
                # Split the level line
                parts = level.split()
                if len(parts) >= 2:
                    level = parts[0]
                    status = ' '.join(parts[1:])
                    # Shift the other fields
                    science = lines[i + 2]
                    students = lines[i + 3]
                    combined = True
            
            # Validate students is a number
            if students.isdigit():
                structured_data.append({
                    'S/N': sn,
                    'LEVEL': level,
                    'STATUS': status,
                    'SCIENCE/NON-SCIENCE': science,
                    'NO OF STUDENTS': int(students)
                })
                # Skip based on whether fields were combined
                i += 4 if combined else 5
            else:
                i += 1
        else:
            i += 1
    elif 'TOTAL' in line.upper():
        # Extract the total if present
        # Look for the total number in the next line
        if i + 1 < len(lines) and lines[i + 1].isdigit():
            total_students = int(lines[i + 1])
            print(f"\nTotal students from PDF: {total_students}")
        break
    else:
        i += 1

# Create DataFrame
if structured_data:
    df = pd.DataFrame(structured_data)
    
    print("\nStructured data:")
    print(df)
    
    print(f"\nData Shape: {df.shape}")
    print("\nData types:")
    print(df.dtypes)
    
    print("\nMissing values:")
    print(df.isnull().sum())
    
    # Calculate total students
    total_students = df['NO OF STUDENTS'].sum()
    print(f"\nTotal Students: {total_students}")
    
    # Group by LEVEL and STATUS
    print("\nStudents by Level and Status:")
    summary = df.groupby(['LEVEL', 'STATUS'])['NO OF STUDENTS'].sum().reset_index()
    print(summary)
    
    # Group by LEVEL and SCIENCE/NON-SCIENCE
    print("\nStudents by Level and Science/Non-Science:")
    science_summary = df.groupby(['LEVEL', 'SCIENCE/NON-SCIENCE'])['NO OF STUDENTS'].sum().reset_index()
    print(science_summary)
    
    # Save cleaned data
    output_path = r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\march_2025_school_fees_cleaned.xlsx"
    df.to_excel(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    
    # Also save summary
    summary_path = r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\march_2025_school_fees_summary.xlsx"
    summary.to_excel(summary_path, index=False)
    print(f"Summary saved to: {summary_path}")
    
    # Create visualizations
    print("\n" + "="*50)
    print("CREATING VISUALIZATIONS")
    print("="*50)
    
    # 1. Students by Level
    print("\n1. Students by Level:")
    level_summary = df.groupby('LEVEL')['NO OF STUDENTS'].sum().sort_values(ascending=False)
    print(level_summary)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    level_summary.plot(kind='bar', color='steelblue', ax=ax)
    ax.set_xlabel('Level', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
    ax.set_title('Students by Level - March 2025', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    level_chart_path = r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\march_2025_students_by_level.png"
    plt.savefig(level_chart_path, dpi=300, bbox_inches='tight')
    print(f"Level chart saved to: {level_chart_path}")
    plt.show()
    
    # 2. Students by Status
    print("\n2. Students by Status:")
    status_summary = df.groupby('STATUS')['NO OF STUDENTS'].sum().sort_values(ascending=False)
    print(status_summary)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#FF6B6B', '#4ECDC4']
    status_summary.plot(kind='bar', color=colors, ax=ax)
    ax.set_xlabel('Status', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
    ax.set_title('Students by Status - March 2025', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    status_chart_path = r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\march_2025_students_by_status.png"
    plt.savefig(status_chart_path, dpi=300, bbox_inches='tight')
    print(f"Status chart saved to: {status_chart_path}")
    plt.show()
    
    # 3. Students by Science/Non-Science
    print("\n3. Students by Science/Non-Science:")
    science_summary = df.groupby('SCIENCE/NON-SCIENCE')['NO OF STUDENTS'].sum().sort_values(ascending=False)
    print(science_summary)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#45B7D1', '#96CEB4']
    science_summary.plot(kind='bar', color=colors, ax=ax)
    ax.set_xlabel('Program Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
    ax.set_title('Students by Science/Non-Science - March 2025', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    science_chart_path = r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\march_2025_students_by_science.png"
    plt.savefig(science_chart_path, dpi=300, bbox_inches='tight')
    print(f"Science chart saved to: {science_chart_path}")
    plt.show()
    
    # 4. Students by Level and Status (Stacked Bar)
    print("\n4. Students by Level and Status:")
    level_status_pivot = df.pivot_table(values='NO OF STUDENTS', index='LEVEL', columns='STATUS', aggfunc='sum', fill_value=0)
    print(level_status_pivot)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    level_status_pivot.plot(kind='bar', stacked=True, color=['#FF6B6B', '#4ECDC4'], ax=ax)
    ax.set_xlabel('Level', fontsize=12, fontweight='bold')
    ax.set_ylabel(' Number of Students', fontsize=12, fontweight='bold')
    ax.set_title('Students by Level and Status - March 2025', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.legend(title='Status', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    level_status_chart_path = r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\march_2025_students_by_level_status.png"
    plt.savefig(level_status_chart_path, dpi=300, bbox_inches='tight')
    print(f"Level-Status chart saved to: {level_status_chart_path}")
    plt.show()
    
    # 5. Students by Level and Science/Non-Science (Stacked Bar)
    print("\n5. Students by Level and Science/Non-Science:")
    level_science_pivot = df.pivot_table(values='NO OF STUDENTS', index='LEVEL', columns='SCIENCE/NON-SCIENCE', aggfunc='sum', fill_value=0)
    print(level_science_pivot)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    level_science_pivot.plot(kind='bar', stacked=True, color=['#45B7D1', '#96CEB4'], ax=ax)
    ax.set_xlabel('Level', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
    ax.set_title('Students by Level and Science/Non-Science - March 2025', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.legend(title='Program Type', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    level_science_chart_path = r"C:\Users\ALH MALIK TOPE\PycharmProjects\PythonProject\march_2025_students_by_level_science.png"
    plt.savefig(level_science_chart_path, dpi=300, bbox_inches='tight')
    print(f"Level-Science chart saved to: {level_science_chart_path}")
    plt.show()
    
    print("\n" + "="*50)
    print("ALL VISUALIZATIONS COMPLETED")
    print("="*50)
else:
    print("No structured data could be extracted")
