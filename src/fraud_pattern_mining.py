"""
LEVIS Stocktake Fraud Pattern Mining
Advanced fraud detection using Association Rule Mining (Apriori & FP-Growth).

Author: Data Analytics Professional
Date: 2024
"""

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class FraudPatternMining:
    """
    Professional fraud pattern mining for retail inventory data.
    Uses Association Rule Mining to detect suspicious patterns and potential fraud.
    """
    
    def __init__(self, cleaned_data):
        """
        Initialize fraud pattern mining with cleaned data.
        
        Args:
            cleaned_data (pd.DataFrame): Cleaned stocktake data
        """
        self.data = cleaned_data
        self.fraud_indicators = {}
        self.association_rules = {}
        self.suspicious_patterns = {}
        
    def create_fraud_indicators(self):
        """
        Create binary fraud indicators for pattern mining.
        
        Returns:
            pd.DataFrame: Data with fraud indicators
        """
        df = self.data.copy()
        
        # Calculate KPIs if not already present
        if 'RTV_Rate' not in df.columns:
            df['RTV_Rate'] = (df['RTV'] / (df['Beginning Inventory'] + df['Shipment'] + df['Transfer In']).replace(0, 1)) * 100
        
        if 'Inventory_Accuracy' not in df.columns:
            df['Inventory_Accuracy'] = (1 - abs(df['Inventory_Discrepancy']) / 
                                       (df['Beginning Inventory'] + df['Shipment'] + df['Transfer In']).replace(0, 1)) * 100
        
        if 'Inventory_Turnover' not in df.columns:
            df['Inventory_Turnover'] = df['Sales'] / ((df['Beginning Inventory'] + df['Ending Inventory']) / 2).replace(0, 1)
        
        # 1. High shrinkage periods
        df['High_Shrinkage'] = df['Shrinkage_Rate'] > 2.0
        
        # 2. Large inventory discrepancies
        df['Large_Discrepancy'] = abs(df['Inventory_Discrepancy']) > 100
        
        # 3. Unusual RTV patterns
        df['High_RTV'] = df['RTV_Rate'] > 3.0
        
        # 4. Zero sales periods
        df['Zero_Sales'] = df['Sales'] == 0
        
        # 5. Unusual transfer patterns
        df['High_Transfer_Out'] = df['Transfer Out'] > df['Transfer Out'].quantile(0.9)
        df['High_Transfer_In'] = df['Transfer In'] > df['Transfer In'].quantile(0.9)
        
        # 6. Inventory accuracy issues
        df['Low_Accuracy'] = df['Inventory_Accuracy'] < 95.0
        
        # 7. Unusual shipment patterns
        df['High_Shipment'] = df['Shipment'] > df['Shipment'].quantile(0.9)
        df['Zero_Shipment'] = df['Shipment'] == 0
        
        # 8. Store-specific anomalies
        store_avg_shrinkage = df.groupby('Store')['Shrinkage_Rate'].mean()
        df['Store_Anomaly'] = df.apply(
            lambda x: x['Shrinkage_Rate'] > store_avg_shrinkage[x['Store']] * 2, axis=1
        )
        
        # 9. Temporal anomalies (weekend/holiday patterns)
        df['Weekend'] = df['Period Start'].dt.dayofweek >= 5
        df['Month_End'] = df['Period Start'].dt.day >= 25
        
        # 10. Composite fraud score
        fraud_columns = ['High_Shrinkage', 'Large_Discrepancy', 'High_RTV', 'Zero_Sales',
                        'High_Transfer_Out', 'Low_Accuracy', 'Store_Anomaly']
        df['Fraud_Score'] = df[fraud_columns].sum(axis=1)
        df['High_Fraud_Risk'] = df['Fraud_Score'] >= 3
        
        self.data = df
        self.fraud_indicators = df[fraud_columns + ['High_Fraud_Risk', 'Fraud_Score']]
        
        return df
    
    def prepare_transaction_data(self, min_support=0.1):
        """
        Prepare transaction data for association rule mining.
        
        Args:
            min_support (float): Minimum support threshold
            
        Returns:
            tuple: (frequent_itemsets, association_rules)
        """
        df = self.data.copy()
        
        # Select fraud indicator columns
        indicator_columns = ['High_Shrinkage', 'Large_Discrepancy', 'High_RTV', 
                           'Zero_Sales', 'High_Transfer_Out', 'High_Transfer_In',
                           'Low_Accuracy', 'High_Shipment', 'Zero_Shipment',
                           'Store_Anomaly', 'Weekend', 'Month_End']
        
        # Create binary transaction matrix
        transaction_data = df[indicator_columns].astype(int)
        
        # Add store and time period information
        transaction_data['Store'] = df['Store']
        transaction_data['Period'] = df['Period Start'].dt.strftime('%Y-%m')
        
        # Group by store and period to create transactions
        transactions = transaction_data.groupby(['Store', 'Period'])[indicator_columns].sum()
        transactions = (transactions > 0).astype(int)  # Convert to binary
        
        # Apply Apriori algorithm
        frequent_itemsets_apriori = apriori(transactions, min_support=min_support, use_colnames=True)
        
        # Apply FP-Growth algorithm
        frequent_itemsets_fpgrowth = fpgrowth(transactions, min_support=min_support, use_colnames=True)
        
        # Generate association rules
        if len(frequent_itemsets_apriori) > 0:
            rules_apriori = association_rules(frequent_itemsets_apriori, metric="confidence", min_threshold=0.5)
        else:
            rules_apriori = pd.DataFrame()
            
        if len(frequent_itemsets_fpgrowth) > 0:
            rules_fpgrowth = association_rules(frequent_itemsets_fpgrowth, metric="confidence", min_threshold=0.5)
        else:
            rules_fpgrowth = pd.DataFrame()
        
        self.association_rules = {
            'apriori': {
                'frequent_itemsets': frequent_itemsets_apriori,
                'rules': rules_apriori
            },
            'fpgrowth': {
                'frequent_itemsets': frequent_itemsets_fpgrowth,
                'rules': rules_fpgrowth
            },
            'transactions': transactions
        }
        
        return self.association_rules
    
    def analyze_suspicious_patterns(self, confidence_threshold=0.7, lift_threshold=1.5):
        """
        Analyze suspicious patterns from association rules.
        
        Args:
            confidence_threshold (float): Minimum confidence for suspicious patterns
            lift_threshold (float): Minimum lift for suspicious patterns
            
        Returns:
            dict: Suspicious pattern analysis
        """
        if not self.association_rules:
            self.prepare_transaction_data()
        
        suspicious_patterns = {}
        
        # Analyze Apriori rules
        apriori_rules = self.association_rules['apriori']['rules']
        if len(apriori_rules) > 0:
            high_confidence_rules = apriori_rules[
                (apriori_rules['confidence'] >= confidence_threshold) &
                (apriori_rules['lift'] >= lift_threshold)
            ]
            
            suspicious_patterns['apriori_high_confidence'] = high_confidence_rules
            
            # Identify most suspicious patterns
            if len(high_confidence_rules) > 0:
                suspicious_patterns['apriori_top_suspicious'] = high_confidence_rules.nlargest(10, 'lift')
        
        # Analyze FP-Growth rules
        fpgrowth_rules = self.association_rules['fpgrowth']['rules']
        if len(fpgrowth_rules) > 0:
            high_confidence_rules = fpgrowth_rules[
                (fpgrowth_rules['confidence'] >= confidence_threshold) &
                (fpgrowth_rules['lift'] >= lift_threshold)
            ]
            
            suspicious_patterns['fpgrowth_high_confidence'] = high_confidence_rules
            
            if len(high_confidence_rules) > 0:
                suspicious_patterns['fpgrowth_top_suspicious'] = high_confidence_rules.nlargest(10, 'lift')
        
        # Analyze fraud risk by store
        store_fraud_risk = self.data.groupby('Store').agg({
            'Fraud_Score': 'mean',
            'High_Fraud_Risk': 'sum',
            'High_Shrinkage': 'sum',
            'Large_Discrepancy': 'sum'
        }).round(2)
        
        store_fraud_risk['Risk_Level'] = pd.cut(
            store_fraud_risk['Fraud_Score'], 
            bins=[0, 1, 2, 3, 10], 
            labels=['Low', 'Medium', 'High', 'Very High']
        )
        
        suspicious_patterns['store_risk_analysis'] = store_fraud_risk
        
        # Analyze temporal patterns
        temporal_fraud = self.data.groupby(['Year', 'Month']).agg({
            'Fraud_Score': 'mean',
            'High_Fraud_Risk': 'sum',
            'High_Shrinkage': 'sum'
        }).reset_index()
        
        suspicious_patterns['temporal_fraud_patterns'] = temporal_fraud
        
        self.suspicious_patterns = suspicious_patterns
        
        return suspicious_patterns
    
    def identify_high_risk_periods(self):
        """
        Identify specific high-risk periods and stores.
        
        Returns:
            pd.DataFrame: High-risk periods analysis
        """
        df = self.data.copy()
        
        # Identify periods with multiple fraud indicators
        high_risk_periods = df[df['Fraud_Score'] >= 3].copy()
        
        if len(high_risk_periods) > 0:
            high_risk_periods = high_risk_periods.sort_values('Fraud_Score', ascending=False)
            
            # Add context information
            high_risk_periods['Risk_Category'] = high_risk_periods['Fraud_Score'].apply(
                lambda x: 'Critical' if x >= 5 else 'High' if x >= 4 else 'Medium'
            )
            
            # Identify specific fraud types
            fraud_types = []
            for _, row in high_risk_periods.iterrows():
                types = []
                if row['High_Shrinkage']: types.append('High_Shrinkage')
                if row['Large_Discrepancy']: types.append('Large_Discrepancy')
                if row['High_RTV']: types.append('High_RTV')
                if row['Zero_Sales']: types.append('Zero_Sales')
                if row['High_Transfer_Out']: types.append('High_Transfer_Out')
                if row['Low_Accuracy']: types.append('Low_Accuracy')
                if row['Store_Anomaly']: types.append('Store_Anomaly')
                fraud_types.append(' + '.join(types))
            
            high_risk_periods['Fraud_Types'] = fraud_types
        
        return high_risk_periods
    
    def generate_fraud_report(self):
        """
        Generate comprehensive fraud detection report.
        
        Returns:
            dict: Complete fraud analysis report
        """
        # Create fraud indicators
        self.create_fraud_indicators()
        
        # Prepare transaction data
        self.prepare_transaction_data()
        
        # Analyze suspicious patterns
        suspicious_patterns = self.analyze_suspicious_patterns()
        
        # Identify high-risk periods
        high_risk_periods = self.identify_high_risk_periods()
        
        # Compile report
        report = {
            'summary': {
                'total_records': len(self.data),
                'high_risk_records': len(high_risk_periods),
                'high_risk_rate': len(high_risk_periods) / len(self.data) * 100,
                'avg_fraud_score': self.data['Fraud_Score'].mean(),
                'stores_with_high_risk': self.data[self.data['High_Fraud_Risk']]['Store'].nunique()
            },
            'fraud_indicators': {
                'high_shrinkage_count': self.data['High_Shrinkage'].sum(),
                'large_discrepancy_count': self.data['Large_Discrepancy'].sum(),
                'high_rtv_count': self.data['High_RTV'].sum(),
                'zero_sales_count': self.data['Zero_Sales'].sum(),
                'low_accuracy_count': self.data['Low_Accuracy'].sum()
            },
            'association_rules': {
                'apriori_rules_count': len(self.association_rules['apriori']['rules']),
                'fpgrowth_rules_count': len(self.association_rules['fpgrowth']['rules']),
                'high_confidence_rules': len(suspicious_patterns.get('apriori_high_confidence', pd.DataFrame()))
            },
            'suspicious_patterns': suspicious_patterns,
            'high_risk_periods': high_risk_periods,
            'recommendations': self._generate_fraud_recommendations()
        }
        
        return report
    
    def _generate_fraud_recommendations(self):
        """
        Generate fraud prevention recommendations.
        
        Returns:
            list: Fraud prevention recommendations
        """
        recommendations = []
        
        # Analyze fraud indicators
        fraud_indicators = self.data[['High_Shrinkage', 'Large_Discrepancy', 'High_RTV', 
                                    'Zero_Sales', 'High_Transfer_Out', 'Low_Accuracy']].sum()
        
        if fraud_indicators['High_Shrinkage'] > len(self.data) * 0.1:
            recommendations.append({
                'category': 'Shrinkage Control',
                'priority': 'High',
                'recommendation': f"High shrinkage detected in {fraud_indicators['High_Shrinkage']} periods. Implement enhanced inventory controls and staff training."
            })
        
        if fraud_indicators['Large_Discrepancy'] > len(self.data) * 0.05:
            recommendations.append({
                'category': 'Inventory Accuracy',
                'priority': 'High',
                'recommendation': f"Large discrepancies found in {fraud_indicators['Large_Discrepancy']} periods. Review counting procedures and implement cycle counting."
            })
        
        if fraud_indicators['High_RTV'] > len(self.data) * 0.05:
            recommendations.append({
                'category': 'Vendor Management',
                'priority': 'Medium',
                'recommendation': f"High RTV rates in {fraud_indicators['High_RTV']} periods. Review vendor quality and return policies."
            })
        
        # Store-specific recommendations
        store_risk = self.suspicious_patterns.get('store_risk_analysis', pd.DataFrame())
        if len(store_risk) > 0:
            high_risk_stores = store_risk[store_risk['Risk_Level'].isin(['High', 'Very High'])]
            if len(high_risk_stores) > 0:
                recommendations.append({
                    'category': 'Store Monitoring',
                    'priority': 'High',
                    'recommendation': f"Focus on {len(high_risk_stores)} high-risk stores: {', '.join(high_risk_stores.index.tolist())}"
                })
        
        return recommendations
    
    def export_fraud_report(self, filename='fraud_pattern_analysis.xlsx'):
        """
        Export fraud analysis to Excel with multiple sheets.
        
        Args:
            filename (str): Output filename
        """
        report = self.generate_fraud_report()
        
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Summary sheet
            summary_df = pd.DataFrame([report['summary']])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Fraud indicators sheet
            indicators_df = pd.DataFrame([report['fraud_indicators']])
            indicators_df.to_excel(writer, sheet_name='Fraud_Indicators', index=False)
            
            # Association rules sheets
            if report['association_rules']['apriori_rules_count'] > 0:
                self.association_rules['apriori']['rules'].to_excel(writer, sheet_name='Apriori_Rules', index=False)
            
            if report['association_rules']['fpgrowth_rules_count'] > 0:
                self.association_rules['fpgrowth']['rules'].to_excel(writer, sheet_name='FPGrowth_Rules', index=False)
            
            # Store risk analysis
            if 'store_risk_analysis' in report['suspicious_patterns']:
                report['suspicious_patterns']['store_risk_analysis'].to_excel(writer, sheet_name='Store_Risk_Analysis')
            
            # High-risk periods
            if len(report['high_risk_periods']) > 0:
                report['high_risk_periods'].to_excel(writer, sheet_name='High_Risk_Periods', index=False)
            
            # Recommendations
            rec_df = pd.DataFrame(report['recommendations'])
            rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
        
        print(f"Fraud analysis report exported to: {filename}")

# Example usage
if __name__ == "__main__":
    # Load cleaned data (assuming data_pipeline.py has been run)
    try:
        from data_pipeline import StocktakeDataPipeline
        
        # Initialize and process data
        pipeline = StocktakeDataPipeline('LEVISSTOCKTAKE.csv')
        pipeline.load_data()
        cleaned_data = pipeline.clean_data()
        
        # Perform fraud pattern mining
        fraud_miner = FraudPatternMining(cleaned_data)
        report = fraud_miner.generate_fraud_report()
        
        print("=== FRAUD PATTERN MINING COMPLETE ===")
        print(f"High-risk records: {report['summary']['high_risk_records']}")
        print(f"High-risk rate: {report['summary']['high_risk_rate']:.2f}%")
        print(f"Average fraud score: {report['summary']['avg_fraud_score']:.2f}")
        print(f"Stores with high risk: {report['summary']['stores_with_high_risk']}")
        
        # Export report
        fraud_miner.export_fraud_report()
        
    except Exception as e:
        print(f"Error running fraud pattern mining: {e}") 