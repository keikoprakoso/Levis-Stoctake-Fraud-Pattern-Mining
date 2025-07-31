#!/usr/bin/env python3
"""
LEVIS Stocktake Analysis - Main Entry Point
Run the complete analysis pipeline from the project root.

Usage:
    python run_analysis.py
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main_analysis import LEVISStocktakeAnalysis

if __name__ == "__main__":
    # Run the complete analysis
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