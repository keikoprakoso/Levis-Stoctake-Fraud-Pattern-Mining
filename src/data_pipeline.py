"""
LEVIS Stocktake Data Pipeline
Professional-grade data preprocessing for retail inventory analysis and fraud detection.

Author: Data Analytics Professional
Date: 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class StocktakeDataPipeline:
    """
    Professional data pipeline for LEVIS stocktake analysis.
    Handles data cleaning, validation, and preprocessing for fraud detection.
    """
    
    def __init__(self, file_path):
        """
        Initialize the data pipeline.
        
        Args:
            file_path (str): Path to the CSV file
        """
        self.file_path = file_path
        self.raw_data = None
        self.cleaned_data = None
        self.validation_report = {}
        
    def load_data(self):
        """
        Load and perform initial data inspection.
        
        Returns:
            pd.DataFrame: Raw data with basic info
        """
        try:
            # Load data with proper encoding
            self.raw_data = pd.read_csv(self.file_path, encoding='utf-8')
            
            # Basic data info
            print("=== DATA LOADING SUMMARY ===")
            print(f"Records loaded: {len(self.raw_data):,}")
            print(f"Columns: {list(self.raw_data.columns)}")
            print(f"Date range: {self.raw_data['Period Start'].min()} to {self.raw_data['Period End'].max()}")
            print(f"Stores: {self.raw_data['Store'].nunique()}")
            
            return self.raw_data
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self):
        """
        Clean and preprocess the stocktake data.
        
        Returns:
            pd.DataFrame: Cleaned data ready for analysis
        """
        if self.raw_data is None:
            print("No data loaded. Run load_data() first.")
            return None
            
        df = self.raw_data.copy()
        
        # 1. Convert date columns
        df['Period Start'] = pd.to_datetime(df['Period Start'], format='%d/%m/%Y')
        df['Period End'] = pd.to_datetime(df['Period End'], format='%d/%m/%Y')
        
        # 2. Clean numeric columns (handle European number format)
        numeric_columns = ['Beginning Inventory', 'Shipment', 'Transfer In', 
                          'Transfer Out', 'RTV', 'Sales', 'Ending Inventory']
        
        for col in numeric_columns:
            # Handle European format: "3.343,00" -> 3343.00
            df[col] = df[col].astype(str).str.replace('"', '')
            # Replace dots with empty string first, then commas with dots
            df[col] = df[col].str.replace('.', '', regex=False)
            df[col] = df[col].str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 3. Calculate derived metrics
        df['Period_Days'] = (df['Period End'] - df['Period Start']).dt.days + 1
        df['Calculated_Ending'] = (df['Beginning Inventory'] + df['Shipment'] + 
                                  df['Transfer In'] - df['Transfer Out'] - 
                                  df['RTV'] - df['Sales'])
        
        # 4. Calculate discrepancies
        df['Inventory_Discrepancy'] = df['Ending Inventory'] - df['Calculated_Ending']
        df['Shrinkage_Rate'] = (df['Inventory_Discrepancy'] / 
                               (df['Beginning Inventory'] + df['Shipment'] + df['Transfer In'])) * 100
        
        # 5. Add time-based features
        df['Year'] = df['Period Start'].dt.year
        df['Month'] = df['Period Start'].dt.month
        df['Quarter'] = df['Period Start'].dt.quarter
        df['Week_of_Year'] = df['Period Start'].dt.isocalendar().week
        
        # 6. Store categorization
        df['Store_Category'] = df['Store'].apply(self._categorize_store)
        
        # 7. Flag potential issues
        df['High_Shrinkage_Flag'] = df['Shrinkage_Rate'] > 2.0
        df['Large_Discrepancy_Flag'] = abs(df['Inventory_Discrepancy']) > 100
        df['Zero_Sales_Flag'] = df['Sales'] == 0
        
        self.cleaned_data = df
        
        print("=== DATA CLEANING COMPLETE ===")
        print(f"Records processed: {len(df):,}")
        print(f"Date range: {df['Period Start'].min().strftime('%Y-%m-%d')} to {df['Period End'].max().strftime('%Y-%m-%d')}")
        print(f"Stores: {df['Store'].nunique()}")
        
        return df
    
    def _categorize_store(self, store_name):
        """
        Categorize stores based on naming patterns.
        
        Args:
            store_name (str): Store name
            
        Returns:
            str: Store category
        """
        if 'MSI' in store_name:
            return 'MSI_Store'
        elif 'SOGO' in store_name:
            return 'SOGO_Store'
        elif 'GALERIES' in store_name:
            return 'GALERIES_Store'
        else:
            return 'Other'
    
    def validate_data_quality(self):
        """
        Perform comprehensive data quality validation.
        
        Returns:
            dict: Validation report
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Run clean_data() first.")
            return {}
            
        df = self.cleaned_data
        report = {}
        
        # 1. Missing values check
        missing_data = df.isnull().sum()
        report['missing_values'] = missing_data[missing_data > 0].to_dict()
        
        # 2. Data consistency checks
        report['negative_values'] = {
            'Beginning_Inventory': (df['Beginning Inventory'] < 0).sum(),
            'Ending_Inventory': (df['Ending Inventory'] < 0).sum(),
            'Sales': (df['Sales'] < 0).sum(),
            'RTV': (df['RTV'] < 0).sum()
        }
        
        # 3. Logical consistency
        report['inventory_imbalance'] = (abs(df['Inventory_Discrepancy']) > 50).sum()
        report['period_consistency'] = (df['Period_Days'] <= 0).sum()
        
        # 4. Store coverage
        report['store_coverage'] = df.groupby('Store').size().to_dict()
        
        # 5. Date coverage
        report['date_coverage'] = {
            'start_date': df['Period Start'].min().strftime('%Y-%m-%d'),
            'end_date': df['Period End'].max().strftime('%Y-%m-%d'),
            'total_periods': len(df)
        }
        
        self.validation_report = report
        
        print("=== DATA QUALITY VALIDATION ===")
        print(f"Missing values: {sum(report['missing_values'].values())}")
        print(f"Negative values: {sum(report['negative_values'].values())}")
        print(f"Large discrepancies: {report['inventory_imbalance']}")
        print(f"Period issues: {report['period_consistency']}")
        
        return report
    
    def get_summary_statistics(self):
        """
        Generate comprehensive summary statistics.
        
        Returns:
            dict: Summary statistics
        """
        if self.cleaned_data is None:
            print("No cleaned data available. Run clean_data() first.")
            return {}
            
        df = self.cleaned_data
        
        summary = {
            'total_records': len(df),
            'date_range': {
                'start': df['Period Start'].min().strftime('%Y-%m-%d'),
                'end': df['Period End'].max().strftime('%Y-%m-%d')
            },
            'stores': {
                'total': df['Store'].nunique(),
                'list': df['Store'].unique().tolist()
            },
            'inventory_metrics': {
                'avg_beginning_inventory': df['Beginning Inventory'].mean(),
                'avg_ending_inventory': df['Ending Inventory'].mean(),
                'total_shipments': df['Shipment'].sum(),
                'total_sales': df['Sales'].sum(),
                'total_rtv': df['RTV'].sum(),
                'total_transfers_in': df['Transfer In'].sum(),
                'total_transfers_out': df['Transfer Out'].sum()
            },
            'discrepancy_analysis': {
                'avg_discrepancy': df['Inventory_Discrepancy'].mean(),
                'max_discrepancy': df['Inventory_Discrepancy'].max(),
                'min_discrepancy': df['Inventory_Discrepancy'].min(),
                'std_discrepancy': df['Inventory_Discrepancy'].std()
            },
            'shrinkage_analysis': {
                'avg_shrinkage_rate': df['Shrinkage_Rate'].mean(),
                'max_shrinkage_rate': df['Shrinkage_Rate'].max(),
                'high_shrinkage_periods': df['High_Shrinkage_Flag'].sum()
            }
        }
        
        return summary
    
    def export_cleaned_data(self, output_path='cleaned_stocktake_data.csv'):
        """
        Export cleaned data to CSV.
        
        Args:
            output_path (str): Output file path
        """
        if self.cleaned_data is not None:
            self.cleaned_data.to_csv(output_path, index=False)
            print(f"Cleaned data exported to: {output_path}")
        else:
            print("No cleaned data available to export.")

# Example usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = StocktakeDataPipeline('LEVISSTOCKTAKE.csv')
    
    # Load and process data
    pipeline.load_data()
    pipeline.clean_data()
    pipeline.validate_data_quality()
    
    # Get summary
    summary = pipeline.get_summary_statistics()
    print("\n=== SUMMARY STATISTICS ===")
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Export cleaned data
    pipeline.export_cleaned_data() 