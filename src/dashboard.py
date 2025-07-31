"""
LEVIS Stocktake Interactive Dashboard
Professional Streamlit dashboard for retail inventory analysis and fraud detection.

Author: Data Analytics Professional
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Import our analysis modules
from data_pipeline import StocktakeDataPipeline
from kpi_analysis import StocktakeKPIAnalysis
from fraud_pattern_mining import FraudPatternMining

class StocktakeDashboard:
    """
    Professional Streamlit dashboard for LEVIS stocktake analysis.
    Provides interactive visualizations and insights.
    """
    
    def __init__(self):
        """Initialize the dashboard."""
        st.set_page_config(
            page_title="LEVIS Stocktake Analysis Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for professional styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
        }
        .alert-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def load_data(self):
        """Load and process the stocktake data."""
        try:
            # Initialize data pipeline
            pipeline = StocktakeDataPipeline('data/LEVISSTOCKTAKE.csv')
            pipeline.load_data()
            cleaned_data = pipeline.clean_data()
            pipeline.validate_data_quality()
            
            # Initialize analysis modules
            kpi_analyzer = StocktakeKPIAnalysis(cleaned_data)
            fraud_miner = FraudPatternMining(cleaned_data)
            
            return cleaned_data, kpi_analyzer, fraud_miner
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None, None, None
    
    def render_header(self):
        """Render the dashboard header."""
        st.markdown('<h1 class="main-header">LEVIS Stocktake Analysis Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("""
        **Professional retail inventory analysis and fraud detection dashboard**  
        *Comprehensive KPI monitoring, pattern mining, and forensic auditing capabilities*
        """)
    
    def render_summary_metrics(self, data, kpi_analyzer, fraud_miner):
        """Render summary metrics cards."""
        st.subheader("📈 Executive Summary")
        
        # Calculate core metrics
        kpi_report = kpi_analyzer.generate_kpi_report()
        fraud_report = fraud_miner.generate_fraud_report()
        
        # Create metric columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Stores",
                value=kpi_report['summary']['total_stores'],
                delta=None
            )
        
        with col2:
            st.metric(
                label="Avg Health Score",
                value=f"{kpi_report['core_kpis']['avg_inventory_health_score']:.1f}%",
                delta=None
            )
        
        with col3:
            st.metric(
                label="High Risk Rate",
                value=f"{fraud_report['summary']['high_risk_rate']:.1f}%",
                delta=None
            )
        
        with col4:
            st.metric(
                label="Total Sales",
                value=f"${kpi_data['summary_metrics']['total_sales']:,.0f}",
                delta=None
            )
    
    def render_kpi_analysis(self, kpi_analyzer):
        """Render KPI analysis section."""
        st.subheader("🎯 KPI Performance Analysis")
        
        # Get KPI data
        kpi_data = kpi_analyzer.create_kpi_dashboard_data()
        
        # Store performance chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Store Performance Ranking**")
            store_perf = kpi_data['store_performance'].sort_values('Inventory_Health_Score', ascending=True)
            
            fig = px.bar(
                store_perf.tail(10), 
                x='Inventory_Health_Score', 
                y=store_perf.tail(10).index,
                orientation='h',
                title="Top 10 Stores by Health Score",
                labels={'Inventory_Health_Score': 'Health Score (%)', 'index': 'Store'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Monthly Health Score Trends**")
            monthly_trends = kpi_data['monthly_trends']
            monthly_trends['Date'] = pd.to_datetime(monthly_trends[['Year', 'Month']].assign(day=1))
            
            fig = px.line(
                monthly_trends, 
                x='Date', 
                y='Inventory_Health_Score',
                title="Monthly Inventory Health Score Trend",
                labels={'Inventory_Health_Score': 'Health Score (%)', 'Date': 'Month'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # KPI breakdown
        st.write("**Detailed KPI Metrics**")
        kpi_metrics = pd.DataFrame([
            {
                'Metric': 'Inventory Accuracy',
                'Value': f"{kpi_data['summary_metrics']['avg_health_score']:.1f}%",
                'Status': 'Good' if kpi_data['summary_metrics']['avg_health_score'] > 95 else 'Needs Attention'
            },
            {
                'Metric': 'Shrinkage Rate',
                'Value': f"{kpi_data['store_performance']['Shrinkage_Rate'].mean():.2f}%",
                'Status': 'Good' if kpi_data['store_performance']['Shrinkage_Rate'].mean() < 1.5 else 'High'
            },
            {
                'Metric': 'Inventory Turnover',
                'Value': f"{kpi_data['store_performance']['Inventory_Turnover'].mean():.2f}",
                'Status': 'Good' if kpi_data['store_performance']['Inventory_Turnover'].mean() > 4 else 'Low'
            },
            {
                'Metric': 'RTV Rate',
                'Value': f"{kpi_data['store_performance']['RTV_Rate'].mean():.2f}%",
                'Status': 'Good' if kpi_data['store_performance']['RTV_Rate'].mean() < 2 else 'High'
            }
        ])
        
        st.dataframe(kpi_metrics, use_container_width=True)
    
    def render_fraud_analysis(self, fraud_miner):
        """Render fraud analysis section."""
        st.subheader("🔍 Fraud Pattern Analysis")
        
        # Get fraud data
        fraud_report = fraud_miner.generate_fraud_report()
        
        # Fraud risk overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Fraud Risk Distribution**")
            fraud_indicators = fraud_report['fraud_indicators']
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(fraud_indicators.keys()),
                    y=list(fraud_indicators.values()),
                    marker_color=['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
                )
            ])
            fig.update_layout(
                title="Fraud Indicators Count",
                xaxis_title="Fraud Type",
                yaxis_title="Count",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Store Risk Levels**")
            store_risk = fraud_report['suspicious_patterns']['store_risk_analysis']
            
            risk_counts = store_risk['Risk_Level'].value_counts()
            fig = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Store Risk Level Distribution"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # High-risk periods
        st.write("**High-Risk Periods Analysis**")
        high_risk_periods = fraud_report['high_risk_periods']
        
        if len(high_risk_periods) > 0:
            # Filter for display
            display_periods = high_risk_periods[['Store', 'Period Start', 'Period End', 'Fraud_Score', 'Risk_Category', 'Fraud_Types']].head(10)
            st.dataframe(display_periods, use_container_width=True)
            
            # Risk trend over time
            temporal_fraud = fraud_report['suspicious_patterns']['temporal_fraud_patterns']
            temporal_fraud['Date'] = pd.to_datetime(temporal_fraud[['Year', 'Month']].assign(day=1))
            
            fig = px.line(
                temporal_fraud,
                x='Date',
                y='Fraud_Score',
                title="Fraud Risk Trend Over Time",
                labels={'Fraud_Score': 'Average Fraud Score', 'Date': 'Month'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No high-risk periods detected in the current dataset.")
    
    def render_association_rules(self, fraud_miner):
        """Render association rules analysis."""
        st.subheader("🔗 Association Rules Analysis")
        
        association_rules = fraud_miner.association_rules
        
        if len(association_rules['apriori']['rules']) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Top Apriori Rules**")
                top_rules = association_rules['apriori']['rules'].nlargest(5, 'lift')
                
                for idx, rule in top_rules.iterrows():
                    st.markdown(f"""
                    **Rule {idx + 1}:**  
                    {list(rule['antecedents'])} → {list(rule['consequents'])}  
                    **Confidence:** {rule['confidence']:.2f} | **Lift:** {rule['lift']:.2f}
                    """)
            
            with col2:
                st.write("**Rule Quality Metrics**")
                rules_df = association_rules['apriori']['rules'][['support', 'confidence', 'lift']].describe()
                st.dataframe(rules_df, use_container_width=True)
        else:
            st.info("ℹ️ No significant association rules found with current thresholds.")
    
    def render_recommendations(self, kpi_analyzer, fraud_miner):
        """Render actionable recommendations."""
        st.subheader("💡 Actionable Recommendations")
        
        # Get recommendations
        kpi_report = kpi_analyzer.generate_kpi_report()
        fraud_report = fraud_miner.generate_fraud_report()
        
        all_recommendations = kpi_report['recommendations'] + fraud_report['recommendations']
        
        if all_recommendations:
            for i, rec in enumerate(all_recommendations, 1):
                priority_color = {
                    'High': '🔴',
                    'Medium': '🟡',
                    'Low': '🟢'
                }
                
                st.markdown(f"""
                <div class="alert-box">
                    <h4>{priority_color.get(rec['priority'], '⚪')} {rec['category']} ({rec['priority']} Priority)</h4>
                    <p>{rec['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No critical recommendations at this time.")
    
    def render_sidebar(self):
        """Render sidebar controls."""
        st.sidebar.title("🎛️ Dashboard Controls")
        
        st.sidebar.subheader("Analysis Settings")
        
        # Date range filter
        st.sidebar.write("**Date Range Filter**")
        start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2023-08-01'))
        end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('2024-09-01'))
        
        # Store filter
        st.sidebar.write("**Store Filter**")
        store_filter = st.sidebar.multiselect(
            "Select Stores",
            options=['All Stores'] + ['MSI_Store', 'SOGO_Store', 'GALERIES_Store'],
            default=['All Stores']
        )
        
        # Analysis parameters
        st.sidebar.write("**Fraud Detection Parameters**")
        confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.5, 0.9, 0.7, 0.1)
        lift_threshold = st.sidebar.slider("Lift Threshold", 1.0, 3.0, 1.5, 0.1)
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'store_filter': store_filter,
            'confidence_threshold': confidence_threshold,
            'lift_threshold': lift_threshold
        }
    
    def run(self):
        """Run the complete dashboard."""
        # Render header
        self.render_header()
        
        # Load data
        with st.spinner("Loading and processing data..."):
            data, kpi_analyzer, fraud_miner = self.load_data()
        
        if data is None:
            st.error("Failed to load data. Please check the data file.")
            return
        
        # Render sidebar
        filters = self.render_sidebar()
        
        # Main dashboard content
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Executive Summary", 
            "🎯 KPI Analysis", 
            "🔍 Fraud Detection", 
            "🔗 Pattern Mining", 
            "💡 Recommendations"
        ])
        
        with tab1:
            self.render_summary_metrics(data, kpi_analyzer, fraud_miner)
        
        with tab2:
            self.render_kpi_analysis(kpi_analyzer)
        
        with tab3:
            self.render_fraud_analysis(fraud_miner)
        
        with tab4:
            self.render_association_rules(fraud_miner)
        
        with tab5:
            self.render_recommendations(kpi_analyzer, fraud_miner)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p><strong>LEVIS Stocktake Analysis Dashboard</strong> | Professional Retail Analytics & Fraud Detection</p>
            <p>Built with Streamlit, Pandas, and MLxtend | Data Analytics Professional</p>
        </div>
        """, unsafe_allow_html=True)

# Run the dashboard
if __name__ == "__main__":
    dashboard = StocktakeDashboard()
    dashboard.run() 