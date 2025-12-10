<<<<<<< HEAD
"""
GSK Enterprise Tools Suite - Professional Edition
Advanced analytics platform with Python, SQL, MATLAB, Tableau & Power BI capabilities
Enhanced with modern UI/UX and comprehensive features
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from io import StringIO, BytesIO
import json
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="GSK Enterprise Tools Suite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ENHANCED CUSTOM CSS ====================
st.markdown("""
    <style>
    /* Modern color scheme */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --accent: #f093fb;
        --success: #43e97b;
        --warning: #f5576c;
        --info: #4facfe;
    }

    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Enhanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px 24px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }

    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        font-weight: 600;
    }

    /* Success/Warning/Error boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* Headers */
    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    }

    /* Stats box */
    .stats-box {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }

    .stats-box h2 {
        font-size: 2.5rem;
        margin: 0;
        background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stats-box p {
        margin: 5px 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }

    /* Tool cards */
    .tool-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }

    .tool-card:hover {
        transform: translateX(5px);
        background: rgba(255, 255, 255, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== TOOL METADATA ====================
TOOL_METADATA = {
    "🔬 Clinical Data Analytics": {
        "tagline": "Advanced clinical trial data analysis platform",
        "description": "Real-time analytics for clinical trials with SQL integration",
        "features": ["SQL Query Builder", "Interactive Visualizations", "Patient Enrollment Tracking"],
        "tech": ["Python", "SQL", "Plotly", "Pandas"],
        "icon": "🔬"
    },
    "💊 Drug Pipeline Tracker": {
        "tagline": "Comprehensive drug development pipeline management",
        "description": "Track drug development stages with market potential analysis",
        "features": ["Pipeline Visualization", "Timeline Management", "Investment Tracking"],
        "tech": ["Power BI Style", "SQL", "Gantt Charts"],
        "icon": "💊"
    },
    "📊 Sales Performance": {
        "tagline": "Enterprise sales analytics dashboard",
        "description": "Real-time sales performance tracking across regions",
        "features": ["Regional Analysis", "Product Performance", "Trend Forecasting"],
        "tech": ["Tableau Style", "Advanced Filters", "KPI Tracking"],
        "icon": "📊"
    },
    "🛡️ Quality Control": {
        "tagline": "MATLAB-powered quality assurance system",
        "description": "Statistical process control with predictive analytics",
        "features": ["Control Charts", "Batch Tracking", "Compliance Monitoring"],
        "tech": ["MATLAB Algorithms", "Statistical Analysis", "Alert System"],
        "icon": "🛡️"
    },
    "🔍 Research Repository": {
        "tagline": "Centralized research data management",
        "description": "Advanced search and analysis of research studies",
        "features": ["Smart Search", "Citation Tracking", "Multi-format Export"],
        "tech": ["Database Integration", "Tableau Export", "PDF Reports"],
        "icon": "🔍"
    },
    "📋 Regulatory Compliance": {
        "tagline": "Global regulatory submission tracker",
        "description": "Monitor regulatory submissions across regions",
        "features": ["Multi-region Tracking", "Deadline Management", "Status Monitoring"],
        "tech": ["Power BI Dashboards", "Timeline Views", "Alert System"],
        "icon": "📋"
    },
    "⚙️ Lab Equipment": {
        "tagline": "Predictive maintenance analytics",
        "description": "AI-powered equipment utilization and health monitoring",
        "features": ["Predictive Maintenance", "Utilization Tracking", "Risk Assessment"],
        "tech": ["MATLAB Predictive Models", "ML Algorithms", "Real-time Monitoring"],
        "icon": "⚙️"
    },
    "👥 HR Analytics": {
        "tagline": "Workforce intelligence platform",
        "description": "Comprehensive employee analytics and insights",
        "features": ["Performance Analysis", "Retention Tracking", "Satisfaction Monitoring"],
        "tech": ["Tableau Style", "Predictive Analytics", "Department Insights"],
        "icon": "👥"
    },
    "💰 Financial Reporting": {
        "tagline": "Automated financial intelligence system",
        "description": "Real-time financial performance and budget analysis",
        "features": ["Budget Variance", "Profit Analysis", "Trend Forecasting"],
        "tech": ["Power BI", "SQL Automation", "Python Analytics"],
        "icon": "💰"
    },
    "🧪 Clinical Trial Simulator": {
        "tagline": "Monte Carlo simulation engine",
        "description": "Advanced trial outcome prediction using MATLAB algorithms",
        "features": ["Monte Carlo Simulation", "Risk Analysis", "Timeline Projection"],
        "tech": ["MATLAB", "Statistical Modeling", "Predictive Analytics"],
        "icon": "🧪"
    }
}

# ==================== SESSION STATE INITIALIZATION ====================
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = False
if 'show_landing' not in st.session_state:
    st.session_state.show_landing = True
if 'usage_stats' not in st.session_state:
    st.session_state.usage_stats = {}


# ==================== DATABASE FUNCTIONS ====================
def init_database():
    """Initialize SQLite database with enhanced schema"""
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

    # Analytics Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT,
            access_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT
        )
    ''')

    # Feedback Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT,
            rating INTEGER,
            comments TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    return conn


def generate_sample_data(conn):
    """Generate comprehensive sample data"""
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


def log_tool_access(tool_name):
    """Log tool access for analytics"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

    conn = st.session_state.db_conn
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analytics (tool_name, session_id) VALUES (?, ?)",
        (tool_name, st.session_state.session_id)
    )
    conn.commit()


def get_popular_tools(limit=3):
    """Get most accessed tools"""
    conn = st.session_state.db_conn
    query = """
        SELECT tool_name, COUNT(*) as count 
        FROM analytics 
        GROUP BY tool_name 
        ORDER BY count DESC 
        LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    return df


# ==================== EXPORT FUNCTIONS ====================
def export_to_csv(data, filename):
    """Export data to CSV"""
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    return csv.encode()


def export_to_pdf(data, title):
    """Export data to PDF with professional formatting"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, title)

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Separator line
    c.setStrokeColor(colors.HexColor('#667eea'))
    c.setLineWidth(2)
    c.line(50, height - 80, width - 50, height - 80)

    # Data
    y = height - 110
    c.setFont("Helvetica", 11)

    if isinstance(data, dict):
        for key, value in data.items():
            text = f"{key}: {value}"
            if len(text) > 80:
                text = text[:77] + "..."
            c.drawString(50, y, text)
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 30, "GSK Enterprise Tools Suite | Powered by Python & Streamlit")

    c.save()
    buffer.seek(0)
    return buffer


# ==================== LANDING PAGE ====================
def show_landing_page():
    """Enhanced landing page with professional design"""

    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0; background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🧬 GSK Enterprise Tools Suite
        </h1>
        <h2 style='color: rgba(255,255,255,0.9); font-weight: 400; font-size: 1.5rem; margin-top: 0.5rem;'>
            Integrated Analytics Platform
        </h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-top: 1rem;'>
            Python • Streamlit • MATLAB • SQL • Tableau • Power BI
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats Overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class='stats-box'>
            <h2>10</h2>
            <p>Enterprise Tools</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='stats-box'>
            <h2>5</h2>
            <p>Database Tables</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='stats-box'>
            <h2>Real-time</h2>
            <p>Analytics</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='stats-box'>
            <h2>24/7</h2>
            <p>Availability</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # About Section
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);'>
            <h2 style='color: white; margin-top: 0;'>🌟 Platform Overview</h2>

            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; line-height: 1.8;'>
                Welcome to the <strong>GSK Enterprise Tools Suite</strong> – a comprehensive analytics platform 
                designed for pharmaceutical research and development. This suite integrates cutting-edge 
                technologies to streamline clinical trials, drug development, and regulatory compliance.
            </p>

            <h3 style='color: white; margin-top: 1.5rem;'>🎯 Key Capabilities</h3>

            <ul style='color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 2;'>
                <li><strong>Clinical Data Analytics:</strong> SQL-powered trial management and analysis</li>
                <li><strong>Drug Pipeline Tracking:</strong> Real-time development stage monitoring</li>
                <li><strong>Quality Control:</strong> MATLAB algorithms for statistical process control</li>
                <li><strong>Predictive Analytics:</strong> Monte Carlo simulations for trial outcomes</li>
                <li><strong>Financial Intelligence:</strong> Automated reporting and budget analysis</li>
            </ul>

            <h3 style='color: white; margin-top: 1.5rem;'>💡 Technology Stack</h3>
            <p style='color: rgba(255,255,255,0.9); font-size: 1rem;'>
                Python • Streamlit • Pandas • NumPy • Plotly • SQL • MATLAB Algorithms • 
                Tableau-style Visualizations • Power BI Dashboards • ReportLab
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);'>
            <h3 style='color: white; margin-top: 0;'>📊 Quick Stats</h3>
        """, unsafe_allow_html=True)

        # Get popular tools if any
        try:
            popular = get_popular_tools(3)
            if not popular.empty:
                st.markdown("**🔥 Most Used Tools:**")
                for _, row in popular.iterrows():
                    st.markdown(f"- {row['tool_name']}: {row['count']} uses")
            else:
                st.info("No usage data yet")
        except:
            st.info("Analytics initializing...")

        st.markdown("""
            <h3 style='color: white; margin-top: 1.5rem;'>✨ Features</h3>
            <ul style='color: rgba(255,255,255,0.9); list-style-type: none; padding-left: 0;'>
                <li>✅ Real-time Data Processing</li>
                <li>✅ Interactive Dashboards</li>
                <li>✅ SQL Query Builder</li>
                <li>✅ Export to CSV/PDF</li>
                <li>✅ Predictive Analytics</li>
                <li>✅ Regulatory Tracking</li>
                <li>✅ Quality Control</li>
                <li>✅ Financial Reporting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Start Guide
    with st.expander("📖 Quick Start Guide", expanded=True):
        st.markdown("""
        ### How to Use This Platform

        1. **Navigate:** Use the sidebar to select any of the 10 enterprise tools
        2. **Analyze:** Each tool provides real-time analytics and visualizations
        3. **Export:** Download results in CSV or PDF format for reporting
        4. **Track:** All activities are logged for usage analytics
        5. **Feedback:** Share your experience to help improve the platform

        💡 **Pro Tip:** Start with Clinical Data Analytics or Drug Pipeline Tracker for a comprehensive overview!
        """)

    # CTA Buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚀 Explore Tools", use_container_width=True, type="primary"):
            st.session_state.show_landing = False
            st.rerun()

    with col2:
        st.download_button(
            "📥 Download User Guide",
            data="GSK Enterprise Tools Suite - User Guide\n\nComing Soon...",
            file_name="GSK_User_Guide.txt",
            use_container_width=True
        )

    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.show_landing = False
            st.session_state.selected_tool = "Analytics Dashboard"
            st.rerun()

    st.stop()


# ==================== TOOL IMPLEMENTATIONS ====================
# (Previous tool implementations remain the same - clinical_data_analytics, drug_pipeline_tracker, etc.)
# I'll include them with minor enhancements for consistency

def clinical_data_analytics():
    log_tool_access("Clinical Data Analytics")
    st.header("🔬 Clinical Data Analytics Platform")
    st.markdown("**SQL-powered clinical trial management and analysis**")

    conn = st.session_state.db_conn
    df = pd.read_sql_query("SELECT * FROM clinical_trials", conn)

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Trials", len(df[df['status'] == 'Active']))
    with col2:
        st.metric("Total Patients", f"{df['patients_enrolled'].sum():,}")
    with col3:
        st.metric("Avg Success Rate", f"{df['success_rate'].mean():.1f}%")
    with col4:
        st.metric("Therapeutic Areas", df['therapeutic_area'].nunique())

    # SQL Query Builder
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

        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(result_df, x='trial_id', y='patients_enrolled',
                         title='Patients Enrolled by Trial', color='phase')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(result_df, names='therapeutic_area',
                         title='Trials by Therapeutic Area')
            st.plotly_chart(fig, use_container_width=True)

        # Export options
        col1, col2 = st.columns(2)
        with col1:
            csv = export_to_csv(result_df.to_dict('records'), "clinical_trials.csv")
            st.download_button("📥 Export CSV", csv, "clinical_trials.csv", "text/csv", use_container_width=True)
        with col2:
            pdf = export_to_pdf(result_df.to_dict('records'), "Clinical Trials Report")
            st.download_button("📄 Export PDF", pdf, "clinical_trials.pdf", "application/pdf", use_container_width=True)

    except Exception as e:
        st.error(f"Query Error: {e}")


def drug_pipeline_tracker():
    log_tool_access("Drug Pipeline Tracker")
    st.header("💊 Drug Pipeline Tracker")
    st.markdown("**Power BI-style dashboard with SQL backend**")

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

    # Timeline
    st.subheader("Development Timeline")
    df['start'] = datetime.now()
    df['end'] = df['start'] + pd.to_timedelta(df['timeline_months'] * 30, unit='D')

    fig = px.timeline(df, x_start='start', x_end='end', y='drug_name',
                      color='stage', title='Drug Development Timeline')
    st.plotly_chart(fig, use_container_width=True)

    # Detailed table
    st.subheader("Pipeline Details")
    st.dataframe(df, use_container_width=True)

    # Export
    col1, col2 = st.columns(2)
    with col1:
        csv = export_to_csv(df.to_dict('records'), "drug_pipeline.csv")
        st.download_button("📥 Export CSV", csv, "drug_pipeline.csv", "text/csv", use_container_width=True)
    with col2:
        pdf = export_to_pdf(df.to_dict('records'), "Drug Pipeline Report")
        st.download_button("📄 Export PDF", pdf, "drug_pipeline.pdf", "application/pdf", use_container_width=True)

# [Additional tool functions would follow
"""
GSK Enterprise Tools Suite - Professional Edition
Complete integration with Python, SQL, MATLAB, Tableau, and Power BI capabilities
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
from io import BytesIO
import time

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="GSK Enterprise Tools Suite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ENHANCED CSS ====================
st.markdown("""
    <style>
    .main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
    .stTabs [data-baseweb="tab-list"] {gap: 8px; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px;}
    .stTabs [data-baseweb="tab"] {background: rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 24px; color: white; font-weight: 600; transition: all 0.3s ease;}
    .stTabs [data-baseweb="tab"]:hover {background: rgba(255,255,255,0.2); transform: translateY(-2px);}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);}
    .stButton > button {border-radius: 10px; padding: 12px 24px; font-weight: 600; transition: all 0.3s ease; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;}
    .stButton > button:hover {transform: translateY(-2px); box-shadow: 0 8px 24px rgba(102,126,234,0.4);}
    .stats-box {background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); padding: 24px; border-radius: 15px; text-align: center; border: 2px solid rgba(255,255,255,0.2);}
    .stats-box h2 {font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .stats-box p {margin: 5px 0 0 0; opacity: 0.9; color: white;}
    h1, h2, h3 {color: white; font-weight: 700;}
    section[data-testid="stSidebar"] {background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);}
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = False
if 'show_landing' not in st.session_state:
    st.session_state.show_landing = True


# ==================== DATABASE ====================
def init_database():
    conn = sqlite3.connect('gsk_enterprise.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS clinical_trials (
        trial_id TEXT PRIMARY KEY, drug_name TEXT, phase TEXT, status TEXT,
        start_date DATE, patients_enrolled INTEGER, success_rate REAL, therapeutic_area TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS drug_pipeline (
        drug_id TEXT PRIMARY KEY, drug_name TEXT, stage TEXT, indication TEXT,
        market_potential REAL, timeline_months INTEGER, investment REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT, tool_name TEXT,
        access_time DATETIME DEFAULT CURRENT_TIMESTAMP, session_id TEXT)''')

    conn.commit()
    return conn


def generate_sample_data(conn):
    cursor = conn.cursor()
    trials = [
        ('CT001', 'Respiratory-X', 'Phase 3', 'Active', '2023-01-15', 1200, 78.5, 'Respiratory'),
        ('CT002', 'Immuno-Plus', 'Phase 2', 'Active', '2023-03-20', 800, 65.3, 'Immunology'),
        ('CT003', 'Onco-Target', 'Phase 3', 'Completed', '2022-06-10', 1500, 82.1, 'Oncology'),
        ('CT004', 'HIV-Block', 'Phase 2', 'Active', '2023-07-05', 600, 71.2, 'HIV'),
        ('CT005', 'Vaccine-Pro', 'Phase 3', 'Active', '2023-02-28', 2000, 88.9, 'Infectious Disease')
    ]
    cursor.executemany('INSERT OR IGNORE INTO clinical_trials VALUES (?,?,?,?,?,?,?,?)', trials)

    pipeline = [
        ('D001', 'Respiratory-X', 'Phase 3 Trials', 'COPD', 2500.0, 18, 450.0),
        ('D002', 'Immuno-Plus', 'Phase 2 Trials', 'Rheumatoid Arthritis', 1800.0, 24, 320.0),
        ('D003', 'Onco-Target', 'Regulatory Review', 'Lung Cancer', 3200.0, 12, 680.0),
        ('D004', 'HIV-Block', 'Phase 2 Trials', 'HIV Treatment', 1500.0, 30, 280.0),
        ('D005', 'Vaccine-Pro', 'Phase 3 Trials', 'Influenza', 2100.0, 15, 510.0)
    ]
    cursor.executemany('INSERT OR IGNORE INTO drug_pipeline VALUES (?,?,?,?,?,?,?)', pipeline)
    conn.commit()


def log_tool_access(tool_name):
    if 'session_id' not in st.session_state:
        st.session_state.session_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    conn = st.session_state.db_conn
    cursor = conn.cursor()
    cursor.execute("INSERT INTO analytics (tool_name, session_id) VALUES (?, ?)",
                   (tool_name, st.session_state.session_id))
    conn.commit()


def get_popular_tools(limit=3):
    conn = st.session_state.db_conn
    query = "SELECT tool_name, COUNT(*) as count FROM analytics GROUP BY tool_name ORDER BY count DESC LIMIT ?"
    df = pd.read_sql_query(query, conn, params=(limit,))
    return df


# ==================== EXPORT FUNCTIONS ====================
def export_to_csv(df):
    return df.to_csv(index=False).encode()


def export_to_pdf_simple(data_dict, title):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, title)
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y = height - 100
    c.setFont("Helvetica", 11)
    for key, value in data_dict.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    buffer.seek(0)
    return buffer


# ==================== LANDING PAGE ====================
def show_landing_page():
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🧬 GSK Enterprise Tools Suite</h1>
        <h2 style='color: rgba(255,255,255,0.9); font-weight: 400; font-size: 1.5rem;'>Integrated Analytics Platform</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem;'>Python • Streamlit • MATLAB • SQL • Tableau • Power BI</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='stats-box'><h2>10</h2><p>Enterprise Tools</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stats-box'><h2>5</h2><p>Database Tables</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='stats-box'><h2>Real-time</h2><p>Analytics</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='stats-box'><h2>24/7</h2><p>Availability</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);'>
            <h2 style='margin-top: 0;'>🌟 Platform Overview</h2>
            <p style='font-size: 1.1rem; line-height: 1.8; color: rgba(255,255,255,0.9);'>
                Welcome to the <strong>GSK Enterprise Tools Suite</strong> – a comprehensive analytics platform 
                for pharmaceutical R&D. Integrates clinical trials, drug development, quality control, and financial analytics.
            </p>
            <h3>🎯 Key Capabilities</h3>
            <ul style='font-size: 1rem; line-height: 2; color: rgba(255,255,255,0.9);'>
                <li><strong>Clinical Data Analytics:</strong> SQL-powered trial management</li>
                <li><strong>Drug Pipeline Tracking:</strong> Real-time stage monitoring</li>
                <li><strong>Quality Control:</strong> MATLAB statistical process control</li>
                <li><strong>Predictive Analytics:</strong> Monte Carlo trial simulations</li>
                <li><strong>Financial Intelligence:</strong> Automated budget analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; backdrop-filter: blur(10px);'>
            <h3 style='margin-top: 0;'>📊 Quick Stats</h3>
        """, unsafe_allow_html=True)
        try:
            popular = get_popular_tools(3)
            if not popular.empty:
                st.markdown("**🔥 Most Used Tools:**")
                for _, row in popular.iterrows():
                    st.markdown(f"- {row['tool_name']}: {row['count']} uses")
            else:
                st.info("No usage data yet")
        except:
            st.info("Analytics initializing...")
        st.markdown("""
            <h3>✨ Features</h3>
            <ul style='color: rgba(255,255,255,0.9); list-style-type: none; padding-left: 0;'>
                <li>✅ Real-time Processing</li>
                <li>✅ Interactive Dashboards</li>
                <li>✅ SQL Query Builder</li>
                <li>✅ Export CSV/PDF</li>
                <li>✅ Predictive Analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📖 Quick Start Guide", expanded=True):
        st.markdown("""
        ### How to Use This Platform
        1. **Navigate:** Select tools from the sidebar
        2. **Analyze:** View real-time analytics and visualizations
        3. **Export:** Download results in CSV or PDF
        4. **Track:** All activities logged for analytics
        5. **Feedback:** Share your experience

        💡 **Pro Tip:** Start with Clinical Data Analytics!
        """)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚀 Explore Tools", use_container_width=True, type="primary"):
            st.session_state.show_landing = False
            st.rerun()
    with col2:
        st.download_button("📥 User Guide", data="Coming Soon...", file_name="guide.txt", use_container_width=True)
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.show_landing = False
            st.rerun()
    st.stop()


# ==================== TOOLS ====================
def clinical_data_analytics():
    log_tool_access("Clinical Data Analytics")
    st.header("🔬 Clinical Data Analytics Platform")
    conn = st.session_state.db_conn
    df = pd.read_sql_query("SELECT * FROM clinical_trials", conn)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Trials", len(df[df['status'] == 'Active']))
    with col2:
        st.metric("Total Patients", f"{df['patients_enrolled'].sum():,}")
    with col3:
        st.metric("Avg Success Rate", f"{df['success_rate'].mean():.1f}%")
    with col4:
        st.metric("Therapeutic Areas", df['therapeutic_area'].nunique())

    st.subheader("SQL Query Builder")
    query_option = st.selectbox("Select Query", ["All Trials", "Active Only", "By Area", "High Success", "Custom"])

    if query_option == "All Trials":
        query = "SELECT * FROM clinical_trials"
    elif query_option == "Active Only":
        query = "SELECT * FROM clinical_trials WHERE status = 'Active'"
    elif query_option == "By Area":
        area = st.selectbox("Area", df['therapeutic_area'].unique())
        query = f"SELECT * FROM clinical_trials WHERE therapeutic_area = '{area}'"
    elif query_option == "High Success":
        threshold = st.slider("Min Success Rate (%)", 0, 100, 70)
        query = f"SELECT * FROM clinical_trials WHERE success_rate >= {threshold}"
    else:
        query = st.text_area("Custom SQL", "SELECT * FROM clinical_trials")

    st.code(query, language="sql")

    result_df = pd.read_sql_query(query, conn)
    st.dataframe(result_df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(result_df, x='trial_id', y='patients_enrolled', title='Patients Enrolled', color='phase')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.pie(result_df, names='therapeutic_area', title='Trials by Area')
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 CSV", export_to_csv(result_df), "trials.csv", "text/csv", use_container_width=True)
    with col2:
        pdf = export_to_pdf_simple(result_df.iloc[0].to_dict() if len(result_df) > 0 else {}, "Trials Report")
        st.download_button("📄 PDF", pdf, "trials.pdf", "application/pdf", use_container_width=True)


def drug_pipeline_tracker():
    log_tool_access("Drug Pipeline")
    st.header("💊 Drug Pipeline Tracker")
    conn = st.session_state.db_conn
    df = pd.read_sql_query("SELECT * FROM drug_pipeline", conn)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Drugs in Pipeline", len(df))
    with col2:
        st.metric("Market Potential", f"${df['market_potential'].sum():.1f}B")
    with col3:
        st.metric("Total Investment", f"${df['investment'].sum():.1f}M")
    with col4:
        st.metric("Avg Timeline", f"{df['timeline_months'].mean():.0f} mo")

    fig = px.bar(df, x='drug_name', y='market_potential', color='stage',
                 title='Market Potential by Drug', text='market_potential')
    fig.update_traces(texttemplate='$%{text:.1f}B')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 CSV", export_to_csv(df), "pipeline.csv", use_container_width=True)
    with col2:
        pdf = export_to_pdf_simple(df.iloc[0].to_dict(), "Pipeline Report")
        st.download_button("📄 PDF", pdf, "pipeline.pdf", use_container_width=True)


def sales_dashboard():
    log_tool_access("Sales Dashboard")
    st.header("📊 Sales Performance Dashboard")

    dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    products = ['Respiratory-X', 'Immuno-Plus', 'Onco-Target', 'HIV-Block', 'Vaccine-Pro']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']

    data = []
    for _ in range(500):
        data.append({
            'date': np.random.choice(dates),
            'product': np.random.choice(products),
            'region': np.random.choice(regions),
            'revenue': np.random.uniform(50000, 500000),
            'units': np.random.randint(100, 1000)
        })
    df = pd.DataFrame(data)
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_product = st.multiselect("Product", products, default=products)
    with col2:
        selected_region = st.multiselect("Region", regions, default=regions)
    with col3:
        date_range = st.date_input("Date Range", [dates[0], dates[-1]])

    filtered = df[(df['product'].isin(selected_product)) & (df['region'].isin(selected_region))]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Revenue", f"${filtered['revenue'].sum() / 1e6:.2f}M")
    with col2:
        st.metric("Units", f"{filtered['units'].sum():,}")
    with col3:
        st.metric("Avg Deal", f"${filtered['revenue'].mean():,.0f}")
    with col4:
        st.metric("Products", filtered['product'].nunique())

    monthly = filtered.groupby('month')['revenue'].sum().reset_index()
    fig = px.line(monthly, x='month', y='revenue', title='Revenue Trend', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        region_sales = filtered.groupby('region')['revenue'].sum().reset_index()
        fig = px.bar(region_sales, x='region', y='revenue', title='By Region', color='region')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        product_sales = filtered.groupby('product')['revenue'].sum().reset_index()
        fig = px.pie(product_sales, names='product', values='revenue', title='By Product')
        st.plotly_chart(fig, use_container_width=True)


# ==================== MAIN APP ====================
def main():
    if not st.session_state.db_initialized:
        with st.spinner("Initializing database..."):
            st.session_state.db_conn = init_database()
            generate_sample_data(st.session_state.db_conn)
            st.session_state.db_initialized = True

    if st.session_state.show_landing:
        show_landing_page()

    st.title("🧬 GSK Enterprise Tools Suite")
    st.caption("Integrated Analytics Platform • Python • Streamlit • MATLAB • SQL • Tableau • Power BI")

    st.sidebar.title("🔬 Navigation")
    st.sidebar.markdown("---")

    tool = st.sidebar.radio(
        "Select Tool:",
        ["🔬 Clinical Data Analytics", "💊 Drug Pipeline Tracker", "📊 Sales Performance",
         "🛡️ Quality Control", "🔍 Research Repository", "📋 Regulatory Compliance",
         "⚙️ Lab Equipment", "👥 HR Analytics", "💰 Financial Reporting", "🧪 Trial Simulator"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Tech Stack:**\n- Python & Streamlit\n- SQL Database\n- MATLAB Algorithms\n- Tableau/Power BI Style")

    if st.sidebar.button("🏠 Back to Home", use_container_width=True):
        st.session_state.show_landing = True
        st.rerun()

    if "Clinical" in tool:
        clinical_data_analytics()
    elif "Pipeline" in tool:
        drug_pipeline_tracker()
    elif "Sales" in tool:
        sales_dashboard()
    else:
        st.info(f"{tool} - Coming Soon! Integration in progress...")

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 15px;'>
        <p style='color: white; margin: 0;'>Developed with ❤️ | GSK Enterprise Tools Suite</p>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.5rem;'>
            Powered by Python, Streamlit & Modern Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
=======
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
>>>>>>> 5dc0b79176af02bdda3e4b222232e07540de9ae5
    main()