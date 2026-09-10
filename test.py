import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title="2023 Revised Budget Analysis Dashboard", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #f5f5f5;
    }
    h1 {
        color: #2c3e50;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("📊 2023 Revised Budget Analysis Dashboard")
st.markdown("---")
st.markdown("### Comprehensive analysis of the 2023 Revised Budget data")

# File upload section
st.header("📁 Upload Excel File")
st.markdown("Upload your Excel file to begin analysis. The file should contain budget data with multiple sheets.")

uploaded_file = st.file_uploader(
    "Choose an Excel file",
    type=['xlsx', 'xls'],
    help="Upload your budget Excel file (.xlsx or .xls)"
)

# Load data function
@st.cache_data
def load_budget_data(uploaded_file):
    try:
        if uploaded_file is not None:
            # Read the uploaded Excel file
            xls = pd.ExcelFile(uploaded_file)
            st.success(f"✅ Successfully loaded Excel file with {len(xls.sheet_names)} sheets")
            
            # Display available sheets
            st.info(f"Available sheets: {', '.join(xls.sheet_names)}")
            
            # Load all sheets into a dictionary
            data_dict = {}
            for sheet_name in xls.sheet_names:
                try:
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                    data_dict[sheet_name] = df
                    st.info(f"📄 Sheet '{sheet_name}': {df.shape[0]} rows, {df.shape[1]} columns")
                except Exception as e:
                    st.warning(f"⚠️ Could not load sheet '{sheet_name}': {str(e)}")
            
            return data_dict, xls.sheet_names
        else:
            return None, []
    except Exception as e:
        st.error(f"❌ Error loading Excel file: {str(e)}")
        return None, []

# Load the data only if file is uploaded
data_dict = None
sheet_names = []

if uploaded_file is not None:
    data_dict, sheet_names = load_budget_data(uploaded_file)
else:
    st.info("👆 Please upload an Excel file to begin analysis.")
    st.warning("⚠️ No file uploaded. The dashboard requires an Excel file to function.")

if data_dict and uploaded_file is not None:
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("📋 Navigation")
    analysis_option = st.sidebar.radio(
        "Select Analysis View:",
        ["Data Overview", "Statistical Summary", "Visualizations", "Comparative Analysis"]
    )
    
    # Data Overview
    if analysis_option == "Data Overview":
        st.header("📁 Data Overview")
        
        # Sheet selector
        selected_sheet = st.selectbox("Select a sheet to view:", sheet_names)
        
        if selected_sheet in data_dict:
            df = data_dict[selected_sheet]
            
            # Display basic info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", f"{df.shape[0]:,}")
            with col2:
                st.metric("Total Columns", df.shape[1])
            with col3:
                st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            st.markdown("---")
            
            # Display column information
            st.subheader("Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum(),
                'Unique Values': df.nunique()
            })
            st.dataframe(col_info, width='stretch')
            
            st.markdown("---")
            
            # Display first few rows
            st.subheader("First 10 Rows")
            st.dataframe(df.head(10), width='stretch')
            
            # Display last few rows
            st.subheader("Last 10 Rows")
            st.dataframe(df.tail(10), width='stretch')
    
    # Statistical Summary
    elif analysis_option == "Statistical Summary":
        st.header("📈 Statistical Summary")
        
        selected_sheet = st.selectbox("Select a sheet for analysis:", sheet_names)
        
        if selected_sheet in data_dict:
            df = data_dict[selected_sheet]
            
            # Numeric columns summary
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                st.subheader("Numeric Columns Statistics")
                st.dataframe(df[numeric_cols].describe(), width='stretch')
                
                # Additional statistics
                st.subheader("Additional Statistics")
                stats_df = pd.DataFrame({
                    'Column': numeric_cols,
                    'Sum': df[numeric_cols].sum(),
                    'Median': df[numeric_cols].median(),
                    'Standard Deviation': df[numeric_cols].std(),
                    'Variance': df[numeric_cols].var(),
                    'Skewness': df[numeric_cols].skew(),
                    'Kurtosis': df[numeric_cols].kurtosis()
                })
                st.dataframe(stats_df, width='stretch')
            else:
                st.warning("⚠️ No numeric columns found in this sheet")
            
            # Categorical columns summary
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if categorical_cols:
                st.subheader("Categorical Columns Statistics")
                for col in categorical_cols[:5]:  # Limit to first 5 categorical columns
                    st.write(f"**{col}**")
                    st.write(f"Unique values: {df[col].nunique()}")
                    st.write(f"Most frequent: {df[col].mode()[0] if not df[col].mode().empty else 'N/A'}")
                    st.dataframe(df[col].value_counts().head(10))
                    st.markdown("---")
    
    # Visualizations
    elif analysis_option == "Visualizations":
        st.header("📊 Visualizations")
        
        selected_sheet = st.selectbox("Select a sheet for visualization:", sheet_names)
        
        if selected_sheet in data_dict:
            df = data_dict[selected_sheet]
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if numeric_cols:
                # Chart type selector
                chart_type = st.selectbox(
                    "Select Chart Type:",
                    ["Histogram", "Box Plot", "Correlation Heatmap", "Scatter Plot", "Bar Chart"]
                )
                
                if chart_type == "Histogram":
                    col_to_plot = st.selectbox("Select column for histogram:", numeric_cols)
                    bins = st.slider("Number of bins:", 5, 50, 20)
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.hist(df[col_to_plot].dropna(), bins=bins, edgecolor='black', alpha=0.7)
                    ax.set_xlabel(col_to_plot, fontsize=12)
                    ax.set_ylabel('Frequency', fontsize=12)
                    ax.set_title(f'Histogram of {col_to_plot}', fontsize=14, fontweight='bold')
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                    plt.close()
                
                elif chart_type == "Box Plot":
                    cols_to_plot = st.multiselect("Select columns for box plot:", numeric_cols, default=numeric_cols[:4])
                    
                    if cols_to_plot:
                        fig, ax = plt.subplots(figsize=(12, 6))
                        df[cols_to_plot].boxplot(ax=ax)
                        ax.set_title('Box Plot of Selected Columns', fontsize=14, fontweight='bold')
                        ax.set_ylabel('Values', fontsize=12)
                        ax.tick_params(axis='x', rotation=45)
                        ax.grid(True, alpha=0.3, axis='y')
                        st.pyplot(fig)
                        plt.close()
                
                elif chart_type == "Correlation Heatmap":
                    if len(numeric_cols) >= 2:
                        fig, ax = plt.subplots(figsize=(12, 10))
                        correlation_matrix = df[numeric_cols].corr()
                        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                                   fmt='.2f', square=True, linewidths=1, cbar_kws={"shrink": 0.8})
                        ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold')
                        st.pyplot(fig)
                        plt.close()
                    else:
                        st.warning("⚠️ Need at least 2 numeric columns for correlation heatmap")
                
                elif chart_type == "Scatter Plot":
                    if len(numeric_cols) >= 2:
                        x_col = st.selectbox("Select X-axis:", numeric_cols, index=0)
                        y_col = st.selectbox("Select Y-axis:", numeric_cols, index=1)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.scatter(df[x_col], df[y_col], alpha=0.6, edgecolors='w', linewidth=0.5)
                        ax.set_xlabel(x_col, fontsize=12)
                        ax.set_ylabel(y_col, fontsize=12)
                        ax.set_title(f'Scatter Plot: {x_col} vs {y_col}', fontsize=14, fontweight='bold')
                        ax.grid(True, alpha=0.3)
                        st.pyplot(fig)
                        plt.close()
                    else:
                        st.warning("⚠️ Need at least 2 numeric columns for scatter plot")
                
                elif chart_type == "Bar Chart":
                    if categorical_cols and numeric_cols:
                        cat_col = st.selectbox("Select categorical column:", categorical_cols)
                        num_col = st.selectbox("Select numeric column for aggregation:", numeric_cols)
                        agg_func = st.selectbox("Aggregation function:", ["sum", "mean", "count", "max", "min"])
                        
                        grouped_data = df.groupby(cat_col)[num_col].agg(agg_func).sort_values(ascending=False).head(15)
                        
                        fig, ax = plt.subplots(figsize=(12, 6))
                        grouped_data.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
                        ax.set_xlabel(cat_col, fontsize=12)
                        ax.set_ylabel(f'{num_col} ({agg_func})', fontsize=12)
                        ax.set_title(f'Bar Chart: {num_col} by {cat_col}', fontsize=14, fontweight='bold')
                        ax.tick_params(axis='x', rotation=45)
                        ax.grid(True, alpha=0.3, axis='y')
                        st.pyplot(fig)
                        plt.close()
                    else:
                        st.warning("⚠️ Need both categorical and numeric columns for bar chart")
            else:
                st.warning("⚠️ No numeric columns available for visualization")
    
    # Comparative Analysis
    elif analysis_option == "Comparative Analysis":
        st.header("🔍 Comparative Analysis")
        
        if len(sheet_names) >= 2:
            sheet1 = st.selectbox("Select first sheet:", sheet_names, index=0)
            sheet2 = st.selectbox("Select second sheet:", sheet_names, index=1)
            
            if sheet1 in data_dict and sheet2 in data_dict:
                df1 = data_dict[sheet1]
                df2 = data_dict[sheet2]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"{sheet1} Summary")
                    st.metric("Rows", f"{df1.shape[0]:,}")
                    st.metric("Columns", df1.shape[1])
                
                with col2:
                    st.subheader(f"{sheet2} Summary")
                    st.metric("Rows", f"{df2.shape[0]:,}")
                    st.metric("Columns", df2.shape[1])
                
                st.markdown("---")
                
                # Compare numeric columns
                numeric_cols1 = df1.select_dtypes(include=[np.number]).columns.tolist()
                numeric_cols2 = df2.select_dtypes(include=[np.number]).columns.tolist()
                common_numeric = list(set(numeric_cols1) & set(numeric_cols2))
                
                if common_numeric:
                    st.subheader("Common Numeric Columns Comparison")
                    comparison_data = []
                    for col in common_numeric:
                        comparison_data.append({
                            'Column': col,
                            f'{sheet1} Mean': df1[col].mean(),
                            f'{sheet2} Mean': df2[col].mean(),
                            f'{sheet1} Sum': df1[col].sum(),
                            f'{sheet2} Sum': df2[col].sum(),
                            'Difference': df1[col].sum() - df2[col].sum()
                        })
                    
                    comparison_df = pd.DataFrame(comparison_data)
                    st.dataframe(comparison_df, width='stretch')
                    
                    # Visualization of comparison
                    if len(common_numeric) > 0:
                        st.subheader("Visual Comparison")
                        col_to_compare = st.selectbox("Select column to compare:", common_numeric)
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        x = [sheet1, sheet2]
                        y = [df1[col_to_compare].sum(), df2[col_to_compare].sum()]
                        bars = ax.bar(x, y, color=['#FF6B6B', '#4ECDC4'], edgecolor='black')
                        ax.set_ylabel(f'Total {col_to_compare}', fontsize=12)
                        ax.set_title(f'Comparison of {col_to_compare} Across Sheets', fontsize=14, fontweight='bold')
                        ax.grid(True, alpha=0.3, axis='y')
                        
                        # Add value labels on bars
                        for bar in bars:
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width()/2., height,
                                   f'{height:,.0f}',
                                   ha='center', va='bottom', fontsize=11, fontweight='bold')
                        
                        st.pyplot(fig)
                        plt.close()
                else:
                    st.info("No common numeric columns found between the selected sheets")
        else:
            st.info("Need at least 2 sheets for comparative analysis")
    
    # Data quality check
    st.markdown("---")
    st.header("🔍 Data Quality Report")
    
    selected_sheet = st.selectbox("Select sheet for quality check:", sheet_names, key="quality_check")
    
    if selected_sheet in data_dict:
        df = data_dict[selected_sheet]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_cells = df.shape[0] * df.shape[1]
            null_cells = df.isnull().sum().sum()
            completeness = ((total_cells - null_cells) / total_cells) * 100
            st.metric("Data Completeness", f"{completeness:.1f}%")
        
        with col2:
            duplicate_rows = df.duplicated().sum()
            st.metric("Duplicate Rows", f"{duplicate_rows:,}")
        
        with col3:
            total_nulls = df.isnull().sum().sum()
            st.metric("Total Null Values", f"{total_nulls:,}")
        
        with col4:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            st.metric("Numeric Columns", len(numeric_cols))
        
        # Null values by column
        st.subheader("Null Values by Column")
        null_counts = df.isnull().sum()
        null_counts = null_counts[null_counts > 0].sort_values(ascending=False)
        
        if not null_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            null_counts.plot(kind='bar', ax=ax, color='coral', edgecolor='black')
            ax.set_xlabel('Columns', fontsize=12)
            ax.set_ylabel('Null Count', fontsize=12)
            ax.set_title('Null Values by Column', fontsize=14, fontweight='bold')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3, axis='y')
            st.pyplot(fig)
            plt.close()
        else:
            st.success("✅ No null values found in this sheet!")
    
    # Export functionality
    st.markdown("---")
    st.header("💾 Export Data")
    
    export_sheet = st.selectbox("Select sheet to export:", sheet_names, key="export")
    
    if export_sheet in data_dict:
        df = data_dict[export_sheet]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export to CSV"):
                csv_filename = f"{export_sheet}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(csv_filename, index=False)
                st.success(f"✅ Data exported to {csv_filename}")
        
        with col2:
            if st.button("Export to Excel"):
                excel_filename = f"{export_sheet}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                df.to_excel(excel_filename, index=False)
                st.success(f"✅ Data exported to {excel_filename}")

else:
    st.error("❌ No data loaded. Please upload an Excel file to begin analysis.")
    st.info("💡 Tip: Upload your budget Excel file using the file uploader above.")

# Footer
st.markdown("---")
st.markdown(f"📅 Dashboard generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("🔧 Built with Streamlit, Pandas, NumPy, Matplotlib, and Seaborn")
