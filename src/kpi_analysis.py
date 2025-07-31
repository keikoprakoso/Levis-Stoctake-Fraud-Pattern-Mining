"""
LEVIS Stocktake KPI Analysis
Professional KPI monitoring and performance analysis for retail inventory management.

Author: Data Analytics Professional
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class StocktakeKPIAnalysis:
    """
    Professional KPI analysis for retail stocktake data.
    Provides comprehensive inventory performance metrics and monitoring.
    """
    
    def __init__(self, cleaned_data):
        """
        Initialize KPI analysis with cleaned data.
        
        Args:
            cleaned_data (pd.DataFrame): Cleaned stocktake data
        """
        self.data = cleaned_data
        self.kpi_results = {}
        
    def calculate_core_kpis(self):
        """
        Calculate core retail inventory KPIs.
        
        Returns:
            dict: Core KPI metrics
        """
        df = self.data.copy()
        
        # 1. Inventory Accuracy
        df['Inventory_Accuracy'] = (1 - abs(df['Inventory_Discrepancy']) / 
                                   (df['Beginning Inventory'] + df['Shipment'] + df['Transfer In']).replace(0, 1)) * 100
        
        # 2. Shrinkage Rate
        df['Shrinkage_Rate'] = (df['Inventory_Discrepancy'] / 
                               (df['Beginning Inventory'] + df['Shipment'] + df['Transfer In']).replace(0, 1)) * 100
        
        # 3. Inventory Turnover
        df['Inventory_Turnover'] = df['Sales'] / ((df['Beginning Inventory'] + df['Ending Inventory']) / 2).replace(0, 1)
        
        # 4. Days Sales in Inventory
        df['Days_Sales_Inventory'] = 365 / df['Inventory_Turnover'].replace([np.inf, -np.inf], np.nan)
        
        # 5. RTV Rate
        df['RTV_Rate'] = (df['RTV'] / (df['Beginning Inventory'] + df['Shipment'] + df['Transfer In']).replace(0, 1)) * 100
        
        # 6. Transfer Efficiency
        df['Transfer_Efficiency'] = (df['Transfer In'] / (df['Transfer In'] + df['Transfer Out'] + 0.001)) * 100
        
        # 7. Sales Velocity
        df['Sales_Velocity'] = df['Sales'] / df['Period_Days']
        
        # 8. Inventory Health Score (Composite) - Improved calculation
        df['Inventory_Health_Score'] = (
            df['Inventory_Accuracy'].clip(0, 100) * 0.3 +
            (100 - abs(df['Shrinkage_Rate'])).clip(0, 100) * 0.3 +
            (df['Inventory_Turnover'] * 2).clip(0, 100) * 0.2 +
            (100 - df['RTV_Rate'].clip(0, 100)) * 0.2
        )
        
        self.data = df
        
        # Store KPI results
        self.kpi_results['core_kpis'] = {
            'avg_inventory_accuracy': df['Inventory_Accuracy'].mean(),
            'avg_shrinkage_rate': df['Shrinkage_Rate'].mean(),
            'avg_inventory_turnover': df['Inventory_Turnover'].mean(),
            'avg_days_sales_inventory': df['Days_Sales_Inventory'].mean(),
            'avg_rtv_rate': df['RTV_Rate'].mean(),
            'avg_transfer_efficiency': df['Transfer_Efficiency'].mean(),
            'avg_sales_velocity': df['Sales_Velocity'].mean(),
            'avg_inventory_health_score': df['Inventory_Health_Score'].mean()
        }
        
        return self.kpi_results['core_kpis']
    
    def analyze_store_performance(self):
        """
        Analyze performance by store.
        
        Returns:
            pd.DataFrame: Store performance summary
        """
        df = self.data.copy()
        
        store_performance = df.groupby('Store').agg({
            'Inventory_Accuracy': 'mean',
            'Shrinkage_Rate': 'mean',
            'Inventory_Turnover': 'mean',
            'RTV_Rate': 'mean',
            'Sales_Velocity': 'mean',
            'Inventory_Health_Score': 'mean',
            'Sales': 'sum',
            'Inventory_Discrepancy': 'sum',
            'Period_Days': 'sum'
        }).round(2)
        
        # Add rankings
        store_performance['Health_Score_Rank'] = store_performance['Inventory_Health_Score'].rank(ascending=False)
        store_performance['Sales_Rank'] = store_performance['Sales'].rank(ascending=False)
        store_performance['Shrinkage_Rank'] = store_performance['Shrinkage_Rate'].rank(ascending=True)
        
        self.kpi_results['store_performance'] = store_performance
        
        return store_performance
    
    def analyze_temporal_trends(self):
        """
        Analyze KPI trends over time.
        
        Returns:
            dict: Temporal analysis results
        """
        df = self.data.copy()
        
        # Monthly trends
        monthly_trends = df.groupby(['Year', 'Month']).agg({
            'Inventory_Accuracy': 'mean',
            'Shrinkage_Rate': 'mean',
            'Inventory_Turnover': 'mean',
            'RTV_Rate': 'mean',
            'Sales_Velocity': 'mean',
            'Inventory_Health_Score': 'mean'
        }).reset_index()
        
        # Quarterly trends
        quarterly_trends = df.groupby(['Year', 'Quarter']).agg({
            'Inventory_Accuracy': 'mean',
            'Shrinkage_Rate': 'mean',
            'Inventory_Turnover': 'mean',
            'RTV_Rate': 'mean',
            'Sales_Velocity': 'mean',
            'Inventory_Health_Score': 'mean'
        }).reset_index()
        
        self.kpi_results['temporal_trends'] = {
            'monthly': monthly_trends,
            'quarterly': quarterly_trends
        }
        
        return self.kpi_results['temporal_trends']
    
    def identify_anomalies(self, threshold_std=2):
        """
        Identify anomalous periods using statistical methods.
        
        Args:
            threshold_std (float): Standard deviation threshold for anomalies
            
        Returns:
            pd.DataFrame: Anomalous records
        """
        df = self.data.copy()
        
        # Calculate z-scores for key metrics
        metrics = ['Inventory_Accuracy', 'Shrinkage_Rate', 'Inventory_Turnover', 'RTV_Rate']
        
        for metric in metrics:
            z_score = np.abs((df[metric] - df[metric].mean()) / df[metric].std())
            df[f'{metric}_Anomaly'] = z_score > threshold_std
        
        # Identify records with multiple anomalies
        anomaly_columns = [col for col in df.columns if 'Anomaly' in col]
        df['Total_Anomalies'] = df[anomaly_columns].sum(axis=1)
        
        # Filter anomalous records
        anomalies = df[df['Total_Anomalies'] > 0].copy()
        
        self.kpi_results['anomalies'] = anomalies
        
        return anomalies
    
    def generate_kpi_report(self):
        """
        Generate comprehensive KPI report.
        
        Returns:
            dict: Complete KPI report
        """
        # Calculate all KPIs
        self.calculate_core_kpis()
        store_perf = self.analyze_store_performance()
        temporal_trends = self.analyze_temporal_trends()
        anomalies = self.identify_anomalies()
        
        # Compile report
        report = {
            'summary': {
                'total_records': len(self.data),
                'total_stores': self.data['Store'].nunique(),
                'date_range': f"{self.data['Period Start'].min().strftime('%Y-%m-%d')} to {self.data['Period End'].max().strftime('%Y-%m-%d')}"
            },
            'core_kpis': self.kpi_results['core_kpis'],
            'store_performance': store_perf,
            'temporal_trends': temporal_trends,
            'anomalies': {
                'total_anomalous_records': len(anomalies),
                'anomaly_rate': len(anomalies) / len(self.data) * 100,
                'anomalous_records': anomalies
            },
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self):
        """
        Generate actionable recommendations based on KPI analysis.
        
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        # Analyze core KPIs
        core_kpis = self.kpi_results['core_kpis']
        
        if core_kpis['avg_shrinkage_rate'] > 1.5:
            recommendations.append({
                'category': 'Shrinkage Control',
                'priority': 'High',
                'recommendation': f"Shrinkage rate ({core_kpis['avg_shrinkage_rate']:.2f}%) exceeds industry standard. Implement enhanced inventory controls and staff training."
            })
        
        if core_kpis['avg_inventory_turnover'] < 4:
            recommendations.append({
                'category': 'Inventory Efficiency',
                'priority': 'Medium',
                'recommendation': f"Low inventory turnover ({core_kpis['avg_inventory_turnover']:.2f}) indicates potential overstocking. Review purchasing patterns."
            })
        
        if core_kpis['avg_rtv_rate'] > 2:
            recommendations.append({
                'category': 'Vendor Management',
                'priority': 'Medium',
                'recommendation': f"High RTV rate ({core_kpis['avg_rtv_rate']:.2f}%) suggests quality issues. Review vendor relationships and product quality."
            })
        
        # Store-specific recommendations
        store_perf = self.kpi_results['store_performance']
        worst_performing = store_perf[store_perf['Inventory_Health_Score'] < store_perf['Inventory_Health_Score'].quantile(0.25)]
        
        if len(worst_performing) > 0:
            recommendations.append({
                'category': 'Store Performance',
                'priority': 'High',
                'recommendation': f"Focus on {len(worst_performing)} underperforming stores: {', '.join(worst_performing.index.tolist())}"
            })
        
        return recommendations
    
    def create_kpi_dashboard_data(self):
        """
        Prepare data for KPI dashboard visualization.
        
        Returns:
            dict: Dashboard-ready data
        """
        df = self.data.copy()
        
        # Ensure KPIs are calculated
        if 'Inventory_Accuracy' not in df.columns:
            self.calculate_core_kpis()
        
        dashboard_data = {
            'summary_metrics': {
                'total_stores': df['Store'].nunique(),
                'total_periods': len(df),
                'avg_health_score': df['Inventory_Health_Score'].mean(),
                'total_sales': df['Sales'].sum(),
                'total_shrinkage': df['Inventory_Discrepancy'].sum()
            },
            'store_performance': self.analyze_store_performance(),
            'monthly_trends': df.groupby(['Year', 'Month']).agg({
                'Inventory_Health_Score': 'mean',
                'Shrinkage_Rate': 'mean',
                'Sales': 'sum'
            }).reset_index(),
            'top_performers': df.groupby('Store')['Inventory_Health_Score'].mean().nlargest(5),
            'bottom_performers': df.groupby('Store')['Inventory_Health_Score'].mean().nsmallest(5),
            'anomaly_data': self.identify_anomalies()
        }
        
        return dashboard_data
    
    def export_kpi_report(self, filename='kpi_analysis_report.xlsx'):
        """
        Export KPI analysis to Excel with multiple sheets.
        
        Args:
            filename (str): Output filename
        """
        report = self.generate_kpi_report()
        
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Summary sheet
            summary_df = pd.DataFrame([report['summary']])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Core KPIs sheet
            kpi_df = pd.DataFrame([report['core_kpis']])
            kpi_df.to_excel(writer, sheet_name='Core_KPIs', index=False)
            
            # Store performance sheet
            report['store_performance'].to_excel(writer, sheet_name='Store_Performance')
            
            # Temporal trends sheet
            report['temporal_trends']['monthly'].to_excel(writer, sheet_name='Monthly_Trends', index=False)
            report['temporal_trends']['quarterly'].to_excel(writer, sheet_name='Quarterly_Trends', index=False)
            
            # Anomalies sheet
            if len(report['anomalies']['anomalous_records']) > 0:
                report['anomalies']['anomalous_records'].to_excel(writer, sheet_name='Anomalies', index=False)
            
            # Recommendations sheet
            rec_df = pd.DataFrame(report['recommendations'])
            rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
        
        print(f"KPI report exported to: {filename}")

# Example usage
if __name__ == "__main__":
    # Load cleaned data (assuming data_pipeline.py has been run)
    try:
        from data_pipeline import StocktakeDataPipeline
        
        # Initialize and process data
        pipeline = StocktakeDataPipeline('LEVISSTOCKTAKE.csv')
        pipeline.load_data()
        cleaned_data = pipeline.clean_data()
        
        # Perform KPI analysis
        kpi_analyzer = StocktakeKPIAnalysis(cleaned_data)
        report = kpi_analyzer.generate_kpi_report()
        
        print("=== KPI ANALYSIS COMPLETE ===")
        print(f"Total stores analyzed: {report['summary']['total_stores']}")
        print(f"Average health score: {report['core_kpis']['avg_inventory_health_score']:.2f}")
        print(f"Anomaly rate: {report['anomalies']['anomaly_rate']:.2f}%")
        
        # Export report
        kpi_analyzer.export_kpi_report()
        
    except Exception as e:
        print(f"Error running KPI analysis: {e}") 