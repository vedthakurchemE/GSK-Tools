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
    main()