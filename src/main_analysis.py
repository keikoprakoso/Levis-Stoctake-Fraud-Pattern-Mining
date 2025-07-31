"""
LEVIS Stocktake Main Analysis Script
End-to-end analysis pipeline for retail inventory management and fraud detection.

Author: Data Analytics Professional
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import our analysis modules
from data_pipeline import StocktakeDataPipeline
from kpi_analysis import StocktakeKPIAnalysis
from fraud_pattern_mining import FraudPatternMining

class LEVISStocktakeAnalysis:
    """
    Main analysis orchestrator for LEVIS stocktake data.
    Provides end-to-end analysis pipeline with comprehensive reporting.
    """
    
    def __init__(self, data_file='data/LEVISSTOCKTAKE.csv'):
        """
        Initialize the main analysis pipeline.
        
        Args:
            data_file (str): Path to the stocktake data file
        """
        self.data_file = data_file
        self.pipeline = None
        self.kpi_analyzer = None
        self.fraud_miner = None
        self.cleaned_data = None
        self.analysis_results = {}
        
    def run_complete_analysis(self):
        """
        Run the complete end-to-end analysis pipeline.
        
        Returns:
            dict: Complete analysis results
        """
        print("=" * 80)
        print("LEVIS STOCKTAKE ANALYSIS - PROFESSIONAL RETAIL ANALYTICS")
        print("=" * 80)
        print(f"Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Step 1: Data Pipeline
        print("STEP 1: DATA PIPELINE & PREPROCESSING")
        print("-" * 50)
        self._run_data_pipeline()
        
        # Step 2: KPI Analysis
        print("\nSTEP 2: KPI PERFORMANCE ANALYSIS")
        print("-" * 50)
        self._run_kpi_analysis()
        
        # Step 3: Fraud Pattern Mining
        print("\nSTEP 3: FRAUD PATTERN MINING")
        print("-" * 50)
        self._run_fraud_analysis()
        
        # Step 4: Generate Reports
        print("\nSTEP 4: REPORT GENERATION")
        print("-" * 50)
        self._generate_reports()
        
        # Step 5: Summary
        print("\nSTEP 5: ANALYSIS SUMMARY")
        print("-" * 50)
        self._print_summary()
        
        return self.analysis_results
    
    def _run_data_pipeline(self):
        """Execute data pipeline and preprocessing."""
        try:
            # Initialize pipeline
            self.pipeline = StocktakeDataPipeline(self.data_file)
            
            # Load data
            print("Loading data...")
            self.pipeline.load_data()
            
            # Clean data
            print("Cleaning and preprocessing data...")
            self.cleaned_data = self.pipeline.clean_data()
            
            # Validate data quality
            print("Validating data quality...")
            validation_report = self.pipeline.validate_data_quality()
            
            # Get summary statistics
            summary_stats = self.pipeline.get_summary_statistics()
            
            self.analysis_results['data_pipeline'] = {
                'validation_report': validation_report,
                'summary_statistics': summary_stats
            }
            
            print("✅ Data pipeline completed successfully")
            print(f"   - Records processed: {summary_stats['total_records']:,}")
            print(f"   - Stores analyzed: {summary_stats['stores']['total']}")
            print(f"   - Date range: {summary_stats['date_range']['start']} to {summary_stats['date_range']['end']}")
            
        except Exception as e:
            print(f"❌ Error in data pipeline: {e}")
            raise
    
    def _run_kpi_analysis(self):
        """Execute KPI analysis."""
        try:
            # Initialize KPI analyzer
            self.kpi_analyzer = StocktakeKPIAnalysis(self.cleaned_data)
            
            # Generate KPI report
            print("Calculating core KPIs...")
            kpi_report = self.kpi_analyzer.generate_kpi_report()
            
            # Store results
            self.analysis_results['kpi_analysis'] = kpi_report
            
            print("✅ KPI analysis completed successfully")
            print(f"   - Average health score: {kpi_report['core_kpis']['avg_inventory_health_score']:.2f}%")
            print(f"   - Average shrinkage rate: {kpi_report['core_kpis']['avg_shrinkage_rate']:.2f}%")
            print(f"   - Average inventory turnover: {kpi_report['core_kpis']['avg_inventory_turnover']:.2f}")
            print(f"   - Anomaly rate: {kpi_report['anomalies']['anomaly_rate']:.2f}%")
            
        except Exception as e:
            print(f"❌ Error in KPI analysis: {e}")
            raise
    
    def _run_fraud_analysis(self):
        """Execute fraud pattern mining."""
        try:
            # Initialize fraud miner
            self.fraud_miner = FraudPatternMining(self.cleaned_data)
            
            # Generate fraud report
            print("Performing fraud pattern mining...")
            fraud_report = self.fraud_miner.generate_fraud_report()
            
            # Store results
            self.analysis_results['fraud_analysis'] = fraud_report
            
            print("✅ Fraud analysis completed successfully")
            print(f"   - High-risk records: {fraud_report['summary']['high_risk_records']}")
            print(f"   - High-risk rate: {fraud_report['summary']['high_risk_rate']:.2f}%")
            print(f"   - Average fraud score: {fraud_report['summary']['avg_fraud_score']:.2f}")
            print(f"   - Stores with high risk: {fraud_report['summary']['stores_with_high_risk']}")
            
        except Exception as e:
            print(f"❌ Error in fraud analysis: {e}")
            raise
    
    def _generate_reports(self):
        """Generate comprehensive reports."""
        try:
            print("Generating Excel reports...")
            
            # Export KPI report
            self.kpi_analyzer.export_kpi_report('reports/LEVIS_KPI_Analysis_Report.xlsx')
            
            # Export fraud report
            self.fraud_miner.export_fraud_report('reports/LEVIS_Fraud_Pattern_Analysis.xlsx')
            
            # Export cleaned data
            self.pipeline.export_cleaned_data('reports/LEVIS_Cleaned_Stocktake_Data.csv')
            
            print("✅ Reports generated successfully")
            print("   - KPI Analysis Report: LEVIS_KPI_Analysis_Report.xlsx")
            print("   - Fraud Pattern Analysis: LEVIS_Fraud_Pattern_Analysis.xlsx")
            print("   - Cleaned Data: LEVIS_Cleaned_Stocktake_Data.csv")
            
        except Exception as e:
            print(f"❌ Error generating reports: {e}")
            raise
    
    def _print_summary(self):
        """Print analysis summary."""
        print("\n📊 ANALYSIS SUMMARY")
        print("=" * 50)
        
        # Data summary
        data_summary = self.analysis_results['data_pipeline']['summary_statistics']
        print(f"📈 Data Coverage:")
        print(f"   - Total records: {data_summary['total_records']:,}")
        print(f"   - Stores analyzed: {data_summary['stores']['total']}")
        print(f"   - Date range: {data_summary['date_range']['start']} to {data_summary['date_range']['end']}")
        
        # KPI summary
        kpi_summary = self.analysis_results['kpi_analysis']['core_kpis']
        print(f"\n🎯 Key Performance Indicators:")
        print(f"   - Inventory Health Score: {kpi_summary['avg_inventory_health_score']:.2f}%")
        print(f"   - Shrinkage Rate: {kpi_summary['avg_shrinkage_rate']:.2f}%")
        print(f"   - Inventory Turnover: {kpi_summary['avg_inventory_turnover']:.2f}")
        print(f"   - RTV Rate: {kpi_summary['avg_rtv_rate']:.2f}%")
        
        # Fraud summary
        fraud_summary = self.analysis_results['fraud_analysis']['summary']
        print(f"\n🔍 Fraud Detection Results:")
        print(f"   - High-risk periods: {fraud_summary['high_risk_records']}")
        print(f"   - Risk rate: {fraud_summary['high_risk_rate']:.2f}%")
        print(f"   - Average fraud score: {fraud_summary['avg_fraud_score']:.2f}")
        
        # Recommendations count
        kpi_recs = len(self.analysis_results['kpi_analysis']['recommendations'])
        fraud_recs = len(self.analysis_results['fraud_analysis']['recommendations'])
        print(f"\n💡 Actionable Insights:")
        print(f"   - KPI recommendations: {kpi_recs}")
        print(f"   - Fraud prevention recommendations: {fraud_recs}")
        
        print(f"\n✅ Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
    
    def get_key_insights(self):
        """
        Extract key business insights from the analysis.
        
        Returns:
            dict: Key insights and recommendations
        """
        insights = {
            'critical_findings': [],
            'performance_highlights': [],
            'risk_alerts': [],
            'action_items': []
        }
        
        # Critical findings
        kpi_data = self.analysis_results['kpi_analysis']
        fraud_data = self.analysis_results['fraud_analysis']
        
        # High shrinkage alert
        if kpi_data['core_kpis']['avg_shrinkage_rate'] > 1.5:
            insights['critical_findings'].append({
                'type': 'High Shrinkage',
                'value': f"{kpi_data['core_kpis']['avg_shrinkage_rate']:.2f}%",
                'impact': 'Financial loss and inventory accuracy issues',
                'priority': 'High'
            })
        
        # High fraud risk alert
        if fraud_data['summary']['high_risk_rate'] > 10:
            insights['critical_findings'].append({
                'type': 'High Fraud Risk',
                'value': f"{fraud_data['summary']['high_risk_rate']:.2f}%",
                'impact': 'Potential fraud and operational risks',
                'priority': 'Critical'
            })
        
        # Performance highlights
        store_performance = kpi_data['store_performance']
        top_performers = store_performance.nlargest(3, 'Inventory_Health_Score')
        bottom_performers = store_performance.nsmallest(3, 'Inventory_Health_Score')
        
        insights['performance_highlights'].extend([
            {
                'type': 'Top Performers',
                'stores': top_performers.index.tolist(),
                'avg_score': top_performers['Inventory_Health_Score'].mean()
            },
            {
                'type': 'Bottom Performers',
                'stores': bottom_performers.index.tolist(),
                'avg_score': bottom_performers['Inventory_Health_Score'].mean()
            }
        ])
        
        # Risk alerts
        if len(fraud_data['high_risk_periods']) > 0:
            insights['risk_alerts'].append({
                'type': 'High-Risk Periods',
                'count': len(fraud_data['high_risk_periods']),
                'description': f"{len(fraud_data['high_risk_periods'])} periods require immediate attention"
            })
        
        # Action items from recommendations
        all_recommendations = (kpi_data['recommendations'] + 
                             fraud_data['recommendations'])
        
        high_priority = [rec for rec in all_recommendations if rec['priority'] == 'High']
        insights['action_items'] = high_priority[:5]  # Top 5 high-priority items
        
        return insights
    
    def create_executive_summary(self):
        """
        Create an executive summary report.
        
        Returns:
            str: Executive summary text
        """
        insights = self.get_key_insights()
        
        summary = f"""
EXECUTIVE SUMMARY - LEVIS STOCKTAKE ANALYSIS
{'='*60}

OVERVIEW:
This analysis examined {self.analysis_results['data_pipeline']['summary_statistics']['total_records']:,} 
stocktake records across {self.analysis_results['data_pipeline']['summary_statistics']['stores']['total']} 
stores from {self.analysis_results['data_pipeline']['summary_statistics']['date_range']['start']} 
to {self.analysis_results['data_pipeline']['summary_statistics']['date_range']['end']}.

KEY FINDINGS:

1. INVENTORY HEALTH:
   - Overall Health Score: {self.analysis_results['kpi_analysis']['core_kpis']['avg_inventory_health_score']:.1f}%
   - Shrinkage Rate: {self.analysis_results['kpi_analysis']['core_kpis']['avg_shrinkage_rate']:.2f}%
   - Inventory Turnover: {self.analysis_results['kpi_analysis']['core_kpis']['avg_inventory_turnover']:.2f}

2. FRAUD RISK ASSESSMENT:
   - High-Risk Periods: {self.analysis_results['fraud_analysis']['summary']['high_risk_records']}
   - Risk Rate: {self.analysis_results['fraud_analysis']['summary']['high_risk_rate']:.2f}%
   - Average Fraud Score: {self.analysis_results['fraud_analysis']['summary']['avg_fraud_score']:.2f}

3. CRITICAL ALERTS:
"""
        
        for finding in insights['critical_findings']:
            summary += f"   - {finding['type']}: {finding['value']} ({finding['priority']} Priority)\n"
        
        summary += f"""
4. PERFORMANCE HIGHLIGHTS:
   - Top Performing Stores: {', '.join(insights['performance_highlights'][0]['stores'][:3])}
   - Stores Requiring Attention: {', '.join(insights['performance_highlights'][1]['stores'][:3])}

5. IMMEDIATE ACTION ITEMS:
"""
        
        for i, action in enumerate(insights['action_items'][:3], 1):
            summary += f"   {i}. {action['recommendation']}\n"
        
        summary += f"""
RECOMMENDATIONS:
- Implement enhanced inventory controls for high-risk stores
- Review and optimize counting procedures
- Establish regular fraud monitoring protocols
- Focus on stores with poor performance metrics

This analysis provides a foundation for data-driven inventory management 
and fraud prevention strategies aligned with industry best practices.
"""
        
        return summary

# Main execution
if __name__ == "__main__":
    # Initialize and run analysis
    analyzer = LEVISStocktakeAnalysis('data/LEVISSTOCKTAKE.csv')
    
    try:
        # Run complete analysis
        results = analyzer.run_complete_analysis()
        
        # Generate executive summary
        print("\n" + "="*80)
        print("EXECUTIVE SUMMARY")
        print("="*80)
        executive_summary = analyzer.create_executive_summary()
        print(executive_summary)
        
        # Save executive summary to file
        with open('reports/LEVIS_Executive_Summary.txt', 'w') as f:
            f.write(executive_summary)
        
        print("\n✅ Analysis completed successfully!")
        print("📁 Generated files:")
        print("   - reports/LEVIS_KPI_Analysis_Report.xlsx")
        print("   - reports/LEVIS_Fraud_Pattern_Analysis.xlsx")
        print("   - reports/LEVIS_Cleaned_Stocktake_Data.csv")
        print("   - reports/LEVIS_Executive_Summary.txt")
        
        print("\n🚀 To run the interactive dashboard:")
        print("   streamlit run src/dashboard.py")
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        print("Please check the data file and dependencies.") 