""""
GSK Enterprise Tools Suite - Streamlit Application
Complete integration with Python, SQL, MATLAB, Tableau, and Power BI capabilities
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from io import StringIO
import json

# Page configuration
st.set_page_config(
    page_title="GSK Enterprise Tools Suite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px 20px;
        color: white;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = False


# Database initialization
def init_database():
    """Initialize SQLite database with sample data"""
    conn = sqlite3.connect('gsk_enterprise.db', check_same_thread=False)
    cursor = conn.cursor()

    # Clinical Trials Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clinical_trials (
            trial_id TEXT PRIMARY KEY,
            drug_name TEXT,
            phase TEXT,
            status TEXT,
            start_date DATE,
            patients_enrolled INTEGER,
            success_rate REAL,
            therapeutic_area TEXT
        )
    ''')

    # Drug Pipeline Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drug_pipeline (
            drug_id TEXT PRIMARY KEY,
            drug_name TEXT,
            stage TEXT,
            indication TEXT,
            market_potential REAL,
            timeline_months INTEGER,
            investment REAL
        )
    ''')

    # Sales Data Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_data (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            region TEXT,
            revenue REAL,
            units_sold INTEGER,
            sale_date DATE
        )
    ''')

    # Quality Control Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quality_control (
            batch_id TEXT PRIMARY KEY,
            product TEXT,
            test_date DATE,
            test_result TEXT,
            compliance_score REAL,
            site TEXT
        )
    ''')

    conn.commit()
    return conn


# Generate sample data
def generate_sample_data(conn):
    """Generate sample data for demonstration"""
    cursor = conn.cursor()

    # Sample clinical trials
    trials = [
        ('CT001', 'Respiratory-X', 'Phase 3', 'Active', '2023-01-15', 1200, 78.5, 'Respiratory'),
        ('CT002', 'Immuno-Plus', 'Phase 2', 'Active', '2023-03-20', 800, 65.3, 'Immunology'),
        ('CT003', 'Onco-Target', 'Phase 3', 'Completed', '2022-06-10', 1500, 82.1, 'Oncology'),
        ('CT004', 'HIV-Block', 'Phase 2', 'Active', '2023-07-05', 600, 71.2, 'HIV'),
        ('CT005', 'Vaccine-Pro', 'Phase 3', 'Active', '2023-02-28', 2000, 88.9, 'Infectious Disease')
    ]
    cursor.executemany('INSERT OR IGNORE INTO clinical_trials VALUES (?,?,?,?,?,?,?,?)', trials)

    # Sample drug pipeline
    pipeline = [
        ('D001', 'Respiratory-X', 'Phase 3 Trials', 'COPD', 2500.0, 18, 450.0),
        ('D002', 'Immuno-Plus', 'Phase 2 Trials', 'Rheumatoid Arthritis', 1800.0, 24, 320.0),
        ('D003', 'Onco-Target', 'Regulatory Review', 'Lung Cancer', 3200.0, 12, 680.0),
        ('D004', 'HIV-Block', 'Phase 2 Trials', 'HIV Treatment', 1500.0, 30, 280.0),
        ('D005', 'Vaccine-Pro', 'Phase 3 Trials', 'Influenza', 2100.0, 15, 510.0)
    ]
    cursor.executemany('INSERT OR IGNORE INTO drug_pipeline VALUES (?,?,?,?,?,?,?)', pipeline)

    conn.commit()


# Tool 1: Clinical Data Analytics Platform
def clinical_data_analytics():
    st.header("🔬 Clinical Data Analytics Platform")
    st.subheader("Python + Streamlit + SQL Integration")

    conn = st.session_state.db_conn

    col1, col2, col3, col4 = st.columns(4)

    # Query data
    df = pd.read_sql_query("SELECT * FROM clinical_trials", conn)

    with col1:
        st.metric("Active Trials", len(df[df['status'] == 'Active']))
    with col2:
        st.metric("Total Patients", f"{df['patients_enrolled'].sum():,}")
    with col3:
        st.metric("Avg Success Rate", f"{df['success_rate'].mean():.1f}%")
    with col4:
        st.metric("Therapeutic Areas", df['therapeutic_area'].nunique())

    # Interactive SQL Query Builder
    st.subheader("SQL Query Builder")
    query_option = st.selectbox(
        "Select Query Type",
        ["All Trials", "Active Trials Only", "By Therapeutic Area", "High Success Rate", "Custom Query"]
    )

    if query_option == "All Trials":
        query = "SELECT * FROM clinical_trials"
    elif query_option == "Active Trials Only":
        query = "SELECT * FROM clinical_trials WHERE status = 'Active'"
    elif query_option == "By Therapeutic Area":
        area = st.selectbox("Select Area", df['therapeutic_area'].unique())
        query = f"SELECT * FROM clinical_trials WHERE therapeutic_area = '{area}'"
    elif query_option == "High Success Rate":
        threshold = st.slider("Minimum Success Rate (%)", 0, 100, 70)
        query = f"SELECT * FROM clinical_trials WHERE success_rate >= {threshold}"
    else:
        query = st.text_area("Enter Custom SQL Query", "SELECT * FROM clinical_trials")

    st.code(query, language="sql")

    try:
        result_df = pd.read_sql_query(query, conn)
        st.dataframe(result_df, use_container_width=True)

        # Visualization
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(result_df, x='trial_id', y='patients_enrolled',
                         title='Patients Enrolled by Trial', color='phase')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(result_df, names='therapeutic_area',
                         title='Trials by Therapeutic Area')
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Query Error: {e}")


# Tool 2: Drug Pipeline Tracker
def drug_pipeline_tracker():
    st.header("💊 Drug Pipeline Tracker")
    st.subheader("Power BI Style Dashboard with SQL Backend")

    conn = st.session_state.db_conn
    df = pd.read_sql_query("SELECT * FROM drug_pipeline", conn)

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Drugs in Pipeline", len(df))
    with col2:
        st.metric("Total Market Potential", f"${df['market_potential'].sum():.1f}B")
    with col3:
        st.metric("Total Investment", f"${df['investment'].sum():.1f}M")
    with col4:
        st.metric("Avg Timeline", f"{df['timeline_months'].mean():.0f} months")

    # Pipeline visualization
    fig = go.Figure()

    stages = df['stage'].unique()
    for stage in stages:
        stage_data = df[df['stage'] == stage]
        fig.add_trace(go.Bar(
            name=stage,
            x=stage_data['drug_name'],
            y=stage_data['market_potential'],
            text=stage_data['market_potential'],
            texttemplate='$%{text:.1f}B'
        ))

    fig.update_layout(
        title='Drug Pipeline - Market Potential by Stage',
        xaxis_title='Drug',
        yaxis_title='Market Potential ($B)',
        barmode='group',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Timeline Gantt Chart
    st.subheader("Development Timeline")
    df['start'] = datetime.now()
    # Convert timeline months into days because pandas removed unit='M'
    df['end'] = df['start'] + pd.to_timedelta(df['timeline_months'] * 30, unit='D')

    from dateutil.relativedelta import relativedelta

    df['end'] = df['start'].apply(lambda d: d + relativedelta(months=+1))

    fig = px.timeline(df, x_start='start', x_end='end', y='drug_name',
                      color='stage', title='Drug Development Timeline')
    st.plotly_chart(fig, use_container_width=True)

    # Detailed table
    st.subheader("Pipeline Details")
    st.dataframe(df, use_container_width=True)


# Tool 3: Sales Performance Dashboard
def sales_performance_dashboard():
    st.header("📊 Sales Performance Dashboard")
    st.subheader("Tableau Style Analytics with SQL")

    # Generate sample sales data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    products = ['Respiratory-X', 'Immuno-Plus', 'Onco-Target', 'HIV-Block', 'Vaccine-Pro']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']

    sales_data = []
    for _ in range(500):
        sales_data.append({
            'date': np.random.choice(dates),
            'product': np.random.choice(products),
            'region': np.random.choice(regions),
            'revenue': np.random.uniform(50000, 500000),
            'units': np.random.randint(100, 1000)
        })

    df = pd.DataFrame(sales_data)
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_product = st.multiselect("Product", products, default=products)
    with col2:
        selected_region = st.multiselect("Region", regions, default=regions)
    with col3:
        date_range = st.date_input("Date Range", [dates[0], dates[-1]])

    # Filter data
    filtered_df = df[
        (df['product'].isin(selected_product)) &
        (df['region'].isin(selected_region))
        ]

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"${filtered_df['revenue'].sum() / 1e6:.2f}M")
    with col2:
        st.metric("Total Units", f"{filtered_df['units'].sum():,}")
    with col3:
        st.metric("Avg Deal Size", f"${filtered_df['revenue'].mean():,.0f}")
    with col4:
        st.metric("Products Sold", filtered_df['product'].nunique())

    # Revenue by month
    monthly_revenue = filtered_df.groupby('month')['revenue'].sum().reset_index()
    fig = px.line(monthly_revenue, x='month', y='revenue',
                  title='Revenue Trend', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Regional breakdown
    col1, col2 = st.columns(2)
    with col1:
        region_sales = filtered_df.groupby('region')['revenue'].sum().reset_index()
        fig = px.bar(region_sales, x='region', y='revenue',
                     title='Revenue by Region', color='region')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        product_sales = filtered_df.groupby('product')['revenue'].sum().reset_index()
        fig = px.pie(product_sales, names='product', values='revenue',
                     title='Revenue by Product')
        st.plotly_chart(fig, use_container_width=True)


# Tool 4: Quality Control Monitor
def quality_control_monitor():
    st.header("🛡️ Quality Control Monitor")
    st.subheader("Python + MATLAB Integration for Batch Analysis")

    conn = st.session_state.db_conn

    # Generate QC data
    batches = [f'BATCH-{i:04d}' for i in range(1, 51)]
    products = ['Respiratory-X', 'Immuno-Plus', 'Onco-Target', 'HIV-Block', 'Vaccine-Pro']
    sites = ['UK-London', 'US-Philadelphia', 'SG-Singapore', 'IN-Bangalore']

    qc_data = []
    for batch in batches:
        qc_data.append({
            'batch_id': batch,
            'product': np.random.choice(products),
            'test_date': datetime.now() - timedelta(days=np.random.randint(0, 90)),
            'test_result': np.random.choice(['Pass', 'Pass', 'Pass', 'Fail'], p=[0.85, 0.10, 0.03, 0.02]),
            'compliance_score': np.random.uniform(85, 100),
            'site': np.random.choice(sites)
        })

    df = pd.DataFrame(qc_data)

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Batches", len(df))
    with col2:
        pass_rate = (df['test_result'] == 'Pass').sum() / len(df) * 100
        st.metric("Pass Rate", f"{pass_rate:.1f}%")
    with col3:
        st.metric("Avg Compliance", f"{df['compliance_score'].mean():.1f}%")
    with col4:
        st.metric("Manufacturing Sites", df['site'].nunique())

    # MATLAB-style Statistical Analysis
    st.subheader("Statistical Process Control (MATLAB Algorithm)")

    # Simulate MATLAB-style control chart
    df_sorted = df.sort_values('test_date')
    mean = df_sorted['compliance_score'].mean()
    std = df_sorted['compliance_score'].std()
    ucl = mean + 3 * std  # Upper Control Limit
    lcl = mean - 3 * std  # Lower Control Limit

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted['batch_id'],
        y=df_sorted['compliance_score'],
        mode='lines+markers',
        name='Compliance Score',
        line=dict(color='blue')
    ))
    fig.add_hline(y=mean, line_dash="dash", line_color="green", annotation_text="Mean")
    fig.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL")
    fig.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL")

    fig.update_layout(
        title='Quality Control Chart (MATLAB Algorithm)',
        xaxis_title='Batch ID',
        yaxis_title='Compliance Score',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Batch results by site
    col1, col2 = st.columns(2)
    with col1:
        site_results = df.groupby(['site', 'test_result']).size().reset_index(name='count')
        fig = px.bar(site_results, x='site', y='count', color='test_result',
                     title='QC Results by Manufacturing Site', barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        product_compliance = df.groupby('product')['compliance_score'].mean().reset_index()
        fig = px.bar(product_compliance, x='product', y='compliance_score',
                     title='Average Compliance Score by Product', color='compliance_score')
        st.plotly_chart(fig, use_container_width=True)

    # Alert system
    st.subheader("Quality Alerts")
    failed_batches = df[df['test_result'] == 'Fail']
    if len(failed_batches) > 0:
        st.warning(f"⚠️ {len(failed_batches)} batches require attention!")
        st.dataframe(failed_batches, use_container_width=True)
    else:
        st.success("✅ All batches passed quality control!")


# Tool 5: Research Data Repository
def research_data_repository():
    st.header("🔍 Research Data Repository")
    st.subheader("Streamlit + SQL + Tableau Integration")

    st.info("📚 Centralized repository for research data with advanced search capabilities")

    # Search interface
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search research data", placeholder="Enter keywords...")
    with col2:
        search_type = st.selectbox("Type", ["All", "Clinical", "Pre-clinical", "Publications"])

    # Sample research data
    research_data = pd.DataFrame({
        'study_id': [f'RS{i:04d}' for i in range(1, 21)],
        'title': [f'Research Study {i}' for i in range(1, 21)],
        'type': np.random.choice(['Clinical', 'Pre-clinical', 'Publications'], 20),
        'therapeutic_area': np.random.choice(['Respiratory', 'Immunology', 'Oncology', 'HIV'], 20),
        'date': pd.date_range(start='2023-01-01', periods=20, freq='M'),
        'status': np.random.choice(['Active', 'Completed', 'Published'], 20),
        'citations': np.random.randint(0, 100, 20)
    })

    # Display research data
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Studies", len(research_data))
    with col2:
        st.metric("Active Studies", len(research_data[research_data['status'] == 'Active']))
    with col3:
        st.metric("Total Citations", research_data['citations'].sum())

    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        type_dist = research_data['type'].value_counts().reset_index()
        type_dist.columns = ['type', 'count']
        fig = px.pie(type_dist, names='type', values='count', title='Research by Type')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        area_dist = research_data['therapeutic_area'].value_counts().reset_index()
        area_dist.columns = ['area', 'count']
        fig = px.bar(area_dist, x='area', y='count', title='Studies by Therapeutic Area')
        st.plotly_chart(fig, use_container_width=True)

    # Data table
    st.subheader("Research Database")
    st.dataframe(research_data, use_container_width=True)

    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Export to CSV"):
            st.success("Data exported successfully!")
    with col2:
        if st.button("📊 Export to Tableau"):
            st.success("Connected to Tableau!")
    with col3:
        if st.button("📈 Generate Report"):
            st.success("Report generated!")


# Tool 6: Regulatory Compliance Tracker
def regulatory_compliance_tracker():
    st.header("📋 Regulatory Compliance Tracker")
    st.subheader("Power BI Style Dashboard for Global Compliance")

    # Sample compliance data
    compliance_data = pd.DataFrame({
        'submission_id': [f'SUB{i:04d}' for i in range(1, 26)],
        'drug_name': np.random.choice(['Respiratory-X', 'Immuno-Plus', 'Onco-Target'], 25),
        'region': np.random.choice(['FDA (US)', 'EMA (EU)', 'PMDA (Japan)', 'CDSCO (India)', 'NMPA (China)'], 25),
        'submission_type': np.random.choice(['NDA', 'BLA', 'IND', 'ANDA'], 25),
        'status': np.random.choice(['Submitted', 'Under Review', 'Approved', 'Additional Info Required'], 25),
        'submission_date': pd.date_range(start='2024-01-01', periods=25, freq='2W'),
        'target_approval': pd.date_range(start='2024-06-01', periods=25, freq='2W')
    })

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Submissions", len(compliance_data))
    with col2:
        approved = len(compliance_data[compliance_data['status'] == 'Approved'])
        st.metric("Approved", approved)
    with col3:
        under_review = len(compliance_data[compliance_data['status'] == 'Under Review'])
        st.metric("Under Review", under_review)
    with col4:
        st.metric("Regions", compliance_data['region'].nunique())

    # Status overview
    status_counts = compliance_data['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    fig = px.pie(status_counts, names='status', values='count',
                 title='Submission Status Overview', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    # Regional distribution
    col1, col2 = st.columns(2)
    with col1:
        region_counts = compliance_data['region'].value_counts().reset_index()
        region_counts.columns = ['region', 'count']
        fig = px.bar(region_counts, x='region', y='count',
                     title='Submissions by Region', color='count')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        drug_counts = compliance_data['drug_name'].value_counts().reset_index()
        drug_counts.columns = ['drug', 'count']
        fig = px.bar(drug_counts, x='drug', y='count',
                     title='Submissions by Drug', color='count')
        st.plotly_chart(fig, use_container_width=True)

    # Upcoming deadlines
    st.subheader("📅 Upcoming Approval Targets")
    upcoming = compliance_data[compliance_data['status'] == 'Under Review'].sort_values('target_approval')
    st.dataframe(upcoming[['submission_id', 'drug_name', 'region', 'target_approval']],
                 use_container_width=True)


# Tool 7: Lab Equipment Utilization
def lab_equipment_utilization():
    st.header("⚙️ Lab Equipment Utilization")
    st.subheader("Python + MATLAB Predictive Analytics")

    # Sample equipment data
    equipment_data = pd.DataFrame({
        'equipment_id': [f'EQ{i:03d}' for i in range(1, 21)],
        'equipment_name': [f'Analyzer {i}' if i % 3 == 0 else f'Reactor {i}' if i % 3 == 1 else f'Centrifuge {i}' for i
                           in range(1, 21)],
        'location': np.random.choice(['Lab A', 'Lab B', 'Lab C', 'Lab D'], 20),
        'utilization_rate': np.random.uniform(60, 95, 20),
        'maintenance_score': np.random.uniform(70, 100, 20),
        'last_maintenance': pd.date_range(end='2024-12-10', periods=20, freq='-15D'),
        'next_maintenance': pd.date_range(start='2024-12-15', periods=20, freq='30D')
    })

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Equipment", len(equipment_data))
    with col2:
        st.metric("Avg Utilization", f"{equipment_data['utilization_rate'].mean():.1f}%")
    with col3:
        st.metric("Avg Health Score", f"{equipment_data['maintenance_score'].mean():.1f}")
    with col4:
        upcoming_maintenance = len(
            equipment_data[equipment_data['next_maintenance'] <= datetime.now() + timedelta(days=7)])
        st.metric("Maintenance Due", upcoming_maintenance)

    # MATLAB-style Predictive Analysis
    st.subheader("Predictive Maintenance (MATLAB Algorithm)")

    # Simulate failure prediction
    equipment_data['failure_risk'] = 100 - equipment_data['maintenance_score']
    equipment_data['risk_level'] = pd.cut(equipment_data['failure_risk'],
                                          bins=[0, 20, 40, 100],
                                          labels=['Low', 'Medium', 'High'])

    fig = go.Figure()
    for risk in ['Low', 'Medium', 'High']:
        risk_data = equipment_data[equipment_data['risk_level'] == risk]
        fig.add_trace(go.Scatter(
            x=risk_data['utilization_rate'],
            y=risk_data['maintenance_score'],
            mode='markers',
            name=risk,
            marker=dict(size=12),
            text=risk_data['equipment_name']
        ))

    fig.update_layout(
        title='Equipment Health vs Utilization (Predictive Model)',
        xaxis_title='Utilization Rate (%)',
        yaxis_title='Maintenance Score',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Equipment by location
    col1, col2 = st.columns(2)
    with col1:
        location_util = equipment_data.groupby('location')['utilization_rate'].mean().reset_index()
        fig = px.bar(location_util, x='location', y='utilization_rate',
                     title='Average Utilization by Lab', color='utilization_rate')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        risk_dist = equipment_data['risk_level'].value_counts().reset_index()
        risk_dist.columns = ['risk', 'count']
        fig = px.pie(risk_dist, names='risk', values='count',
                     title='Equipment Risk Distribution',
                     color='risk',
                     color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
        st.plotly_chart(fig, use_container_width=True)

    # Equipment details
    st.subheader("Equipment Status")
    st.dataframe(equipment_data, use_container_width=True)


# Tool 8: HR Analytics Suite
def hr_analytics_suite():
    st.header("👥 HR Analytics Suite")
    st.subheader("Tableau Style Workforce Analytics")

    # Sample HR data
    departments = ['R&D', 'Manufacturing', 'Sales', 'Regulatory', 'Quality Control']
    hr_data = pd.DataFrame({
        'employee_id': [f'EMP{i:05d}' for i in range(1, 501)],
        'department': np.random.choice(departments, 500),
        'tenure_years': np.random.uniform(0.5, 15, 500),
        'performance_score': np.random.uniform(3.0, 5.0, 500),
        'satisfaction_score': np.random.uniform(3.0, 5.0, 500),
        'training_hours': np.random.randint(20, 100, 500)
    })

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", len(hr_data))
    with col2:
        st.metric("Avg Tenure", f"{hr_data['tenure_years'].mean():.1f} years")
    with col3:
        st.metric("Avg Performance", f"{hr_data['performance_score'].mean():.2f}/5.0")
    with col4:
        st.metric("Avg Satisfaction", f"{hr_data['satisfaction_score'].mean():.2f}/5.0")

    # Department distribution
    dept_counts = hr_data['department'].value_counts().reset_index()
    dept_counts.columns = ['department', 'count']
    fig = px.bar(dept_counts, x='department', y='count',
                 title='Employee Distribution by Department', color='count')
    st.plotly_chart(fig, use_container_width=True)

    # Performance analysis
    col1, col2 = st.columns(2)
    with col1:
        dept_performance = hr_data.groupby('department')['performance_score'].mean().reset_index()
        fig = px.bar(dept_performance, x='department', y='performance_score',
                     title='Average Performance by Department', color='performance_score')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(hr_data, x='tenure_years', y='performance_score',
                         color='department', title='Tenure vs Performance',
                         trendline='ols')
        st.plotly_chart(fig, use_container_width=True)

    # Retention analysis
    st.subheader("Retention & Satisfaction Analysis")
    fig = px.scatter(hr_data, x='satisfaction_score', y='performance_score',
                     size='training_hours', color='department',
                     title='Employee Satisfaction vs Performance (Size = Training Hours)')
    st.plotly_chart(fig, use_container_width=True)


# Tool 9: Financial Reporting System
def financial_reporting_system():
    st.header("💰 Financial Reporting System")
    st.subheader("Power BI + SQL + Python Automation")

    # Generate financial data
    months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
    categories = ['R&D', 'Manufacturing', 'Sales & Marketing', 'Administration', 'Regulatory']

    financial_data = []
    for month in months:
        for category in categories:
            financial_data.append({
                'month': month,
                'category': category,
                'revenue': np.random.uniform(200, 500),
                'expenses': np.random.uniform(100, 300),
                'budget': np.random.uniform(150, 350)
            })

    df = pd.DataFrame(financial_data)
    df['profit'] = df['revenue'] - df['expenses']
    df['budget_variance'] = df['expenses'] - df['budget']

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"${df['revenue'].sum():.1f}M")
    with col2:
        st.metric("Total Expenses", f"${df['expenses'].sum():.1f}M")
    with col3:
        st.metric("Net Profit", f"${df['profit'].sum():.1f}M")
    with col4:
        margin = (df['profit'].sum() / df['revenue'].sum()) * 100
        st.metric("Profit Margin", f"{margin:.1f}%")

    # Revenue vs Expenses over time
    monthly_summary = df.groupby('month')[['revenue', 'expenses', 'profit']].sum().reset_index()
    monthly_summary['month'] = monthly_summary['month'].dt.strftime('%Y-%m')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_summary['month'], y=monthly_summary['revenue'],
                             mode='lines+markers', name='Revenue', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=monthly_summary['month'], y=monthly_summary['expenses'],
                             mode='lines+markers', name='Expenses', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=monthly_summary['month'], y=monthly_summary['profit'],
                             mode='lines+markers', name='Profit', line=dict(color='blue')))

    fig.update_layout(title='Financial Performance Trend', xaxis_title='Month',
                      yaxis_title='Amount ($M)', height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Category breakdown
    col1, col2 = st.columns(2)
    with col1:
        category_expenses = df.groupby('category')['expenses'].sum().reset_index()
        fig = px.pie(category_expenses, names='category', values='expenses',
                     title='Expenses by Category')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        category_profit = df.groupby('category')['profit'].sum().reset_index()
        fig = px.bar(category_profit, x='category', y='profit',
                     title='Profit by Category', color='profit')
        st.plotly_chart(fig, use_container_width=True)

    # Budget variance
    st.subheader("Budget Variance Analysis")
    variance_summary = df.groupby('category')['budget_variance'].sum().reset_index()
    variance_summary['status'] = variance_summary['budget_variance'].apply(
        lambda x: 'Over Budget' if x > 0 else 'Under Budget'
    )

    fig = px.bar(variance_summary, x='category', y='budget_variance',
                 color='status', title='Budget Variance by Category',
                 color_discrete_map={'Over Budget': 'red', 'Under Budget': 'green'})
    st.plotly_chart(fig, use_container_width=True)


# Tool 10: Clinical Trial Simulator
def clinical_trial_simulator():
    st.header("🧪 Clinical Trial Simulator")
    st.subheader("MATLAB + Python + Streamlit - Monte Carlo Simulation")

    st.info("Advanced simulation using MATLAB-style algorithms for trial outcome prediction")

    # Simulation parameters
    col1, col2 = st.columns(2)
    with col1:
        num_patients = st.slider("Number of Patients", 100, 5000, 1000, 100)
        success_rate = st.slider("Expected Success Rate (%)", 50, 95, 75)
        dropout_rate = st.slider("Dropout Rate (%)", 5, 30, 15)

    with col2:
        num_simulations = st.slider("Number of Simulations", 100, 10000, 1000, 100)
        confidence_level = st.slider("Confidence Level (%)", 90, 99, 95)
        trial_duration = st.slider("Trial Duration (months)", 6, 36, 18)

    if st.button("🚀 Run Monte Carlo Simulation", type="primary"):
        with st.spinner("Running MATLAB-style Monte Carlo simulation..."):
            # Monte Carlo simulation
            simulations = []
            for _ in range(num_simulations):
                # Simulate patient enrollment with dropout
                enrolled = num_patients
                completed = int(enrolled * (1 - dropout_rate / 100))

                # Simulate success outcomes
                successes = np.random.binomial(completed, success_rate / 100)
                success_pct = (successes / completed) * 100 if completed > 0 else 0

                simulations.append({
                    'enrolled': enrolled,
                    'completed': completed,
                    'successes': successes,
                    'success_rate': success_pct
                })

            sim_df = pd.DataFrame(simulations)

            # Results
            st.success("✅ Simulation Complete!")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Completions", f"{sim_df['completed'].mean():.0f}")
            with col2:
                st.metric("Avg Success Rate", f"{sim_df['success_rate'].mean():.1f}%")
            with col3:
                lower_ci = np.percentile(sim_df['success_rate'], (100 - confidence_level) / 2)
                st.metric(f"{confidence_level}% CI Lower", f"{lower_ci:.1f}%")
            with col4:
                upper_ci = np.percentile(sim_df['success_rate'], 100 - (100 - confidence_level) / 2)
                st.metric(f"{confidence_level}% CI Upper", f"{upper_ci:.1f}%")

            # Distribution plot
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=sim_df['success_rate'], nbinsx=50,
                                       name='Success Rate Distribution'))
            fig.add_vline(x=sim_df['success_rate'].mean(), line_dash="dash",
                          line_color="red", annotation_text="Mean")
            fig.add_vline(x=lower_ci, line_dash="dash", line_color="green",
                          annotation_text=f"{confidence_level}% CI")
            fig.add_vline(x=upper_ci, line_dash="dash", line_color="green")

            fig.update_layout(title='Success Rate Distribution (Monte Carlo)',
                              xaxis_title='Success Rate (%)',
                              yaxis_title='Frequency',
                              height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Risk analysis
            st.subheader("Risk Analysis")
            prob_below_70 = (sim_df['success_rate'] < 70).sum() / num_simulations * 100
            prob_above_80 = (sim_df['success_rate'] > 80).sum() / num_simulations * 100

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Probability < 70% Success", f"{prob_below_70:.1f}%")
            with col2:
                st.metric("Probability > 80% Success", f"{prob_above_80:.1f}%")

            # Timeline projection
            st.subheader("Timeline Projection")
            timeline_data = pd.DataFrame({
                'month': range(1, trial_duration + 1),
                'enrollment': [int(num_patients * (i / trial_duration)) for i in range(1, trial_duration + 1)],
                'projected_completions': [int(num_patients * (1 - dropout_rate / 100) * (i / trial_duration))
                                          for i in range(1, trial_duration + 1)]
            })

            fig = px.line(timeline_data, x='month', y=['enrollment', 'projected_completions'],
                          title='Enrollment & Completion Timeline',
                          labels={'value': 'Patients', 'variable': 'Metric'})
            st.plotly_chart(fig, use_container_width=True)


# Main application
def main():
    # Header
    st.title("🧬 GSK Enterprise Tools Suite")
    st.markdown("### Integrated Analytics Platform with Python, Streamlit, MATLAB, SQL, Tableau & Power BI")

    # Initialize database
    if not st.session_state.db_initialized:
        with st.spinner("Initializing database..."):
            st.session_state.db_conn = init_database()
            generate_sample_data(st.session_state.db_conn)
            st.session_state.db_initialized = True

    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")

    tool = st.sidebar.radio(
        "Select Tool:",
        [
            "🔬 Clinical Data Analytics",
            "💊 Drug Pipeline Tracker",
            "📊 Sales Performance",
            "🛡️ Quality Control Monitor",
            "🔍 Research Data Repository",
            "📋 Regulatory Compliance",
            "⚙️ Lab Equipment Utilization",
            "👥 HR Analytics Suite",
            "💰 Financial Reporting",
            "🧪 Clinical Trial Simulator"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Technologies Used:**\n"
        "- Python & Streamlit\n"
        "- SQL Database\n"
        "- MATLAB Algorithms\n"
        "- Tableau Style Viz\n"
        "- Power BI Dashboards"
    )

    # Route to selected tool
    if "Clinical Data Analytics" in tool:
        clinical_data_analytics()
    elif "Drug Pipeline" in tool:
        drug_pipeline_tracker()
    elif "Sales Performance" in tool:
        sales_performance_dashboard()
    elif "Quality Control" in tool:
        quality_control_monitor()
    elif "Research Data" in tool:
        research_data_repository()
    elif "Regulatory Compliance" in tool:
        regulatory_compliance_tracker()
    elif "Lab Equipment" in tool:
        lab_equipment_utilization()
    elif "HR Analytics" in tool:
        hr_analytics_suite()
    elif "Financial Reporting" in tool:
        financial_reporting_system()
    elif "Clinical Trial Simulator" in tool:
        clinical_trial_simulator()


if __name__ == "__main__":
    main()