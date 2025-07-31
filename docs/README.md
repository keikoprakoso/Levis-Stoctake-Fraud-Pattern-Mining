# LEVIS Stocktake Analysis & Fraud Pattern Mining

## 📊 Professional Retail Analytics Project

A comprehensive end-to-end data analytics solution for retail stocktake management, KPI monitoring, and forensic fraud pattern mining. This project demonstrates advanced data mining techniques and professional-grade analytics capabilities suitable for top-tier consulting firms.

## 🎯 Project Overview

This project analyzes LEVIS retail stocktake data to provide:
- **Inventory Performance Monitoring**: Real-time KPI tracking and health scoring
- **Fraud Detection**: Advanced pattern mining using Association Rules (Apriori & FP-Growth)
- **Forensic Auditing**: Professional-grade anomaly detection and risk assessment
- **Interactive Dashboards**: Streamlit-based visualization and reporting

## 🏗️ Project Structure

```
LEVIS Stocktake & Fraud Pattern Mining/
├── data/                           # Raw and processed data
│   └── LEVISSTOCKTAKE.csv         # Raw stocktake data
├── src/                            # Source code modules
│   ├── __init__.py                # Package initialization
│   ├── data_pipeline.py           # Data cleaning and preprocessing
│   ├── kpi_analysis.py            # KPI calculation and monitoring
│   ├── fraud_pattern_mining.py    # Association rule mining
│   ├── dashboard.py               # Streamlit interactive dashboard
│   └── main_analysis.py           # End-to-end analysis orchestrator
├── reports/                        # Generated analysis reports
│   ├── LEVIS_KPI_Analysis_Report.xlsx
│   ├── LEVIS_Fraud_Pattern_Analysis.xlsx
│   ├── LEVIS_Cleaned_Stocktake_Data.csv
│   └── LEVIS_Executive_Summary.txt
├── docs/                           # Documentation
│   ├── README.md                  # Project documentation
│   └── PROJECT_SUMMARY.md         # Project summary
├── requirements.txt                # Python dependencies
├── run_analysis.py                 # Main analysis runner
├── run_dashboard.py                # Dashboard launcher
└── README.md                       # Quick start guide
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Complete Analysis

```bash
python run_analysis.py
```

This will:
- Clean and validate the data
- Calculate comprehensive KPIs
- Perform fraud pattern mining
- Generate Excel reports
- Create executive summary

### 3. Launch Interactive Dashboard

```bash
python run_dashboard.py
```

Or directly:
```bash
streamlit run src/dashboard.py
```

## 📈 Key Features

### Data Pipeline (`data_pipeline.py`)
- **Professional Data Cleaning**: Handles European number formatting, date parsing, and data validation
- **Quality Assurance**: Comprehensive data quality checks and validation reports
- **Derived Metrics**: Calculates inventory discrepancies, shrinkage rates, and health scores
- **Export Capabilities**: Clean data export for further analysis

### KPI Analysis (`kpi_analysis.py`)
- **Core Retail KPIs**: Inventory accuracy, shrinkage rate, turnover, RTV rate
- **Performance Scoring**: Composite inventory health score
- **Store Comparison**: Ranking and benchmarking across locations
- **Temporal Analysis**: Trend analysis and seasonal patterns
- **Anomaly Detection**: Statistical outlier identification

### Fraud Pattern Mining (`fraud_pattern_mining.py`)
- **Association Rule Mining**: Apriori and FP-Growth algorithms
- **Fraud Indicators**: 12+ binary fraud indicators
- **Risk Scoring**: Composite fraud risk assessment
- **Pattern Discovery**: Suspicious transaction pattern identification
- **Forensic Analysis**: Professional-grade fraud detection

### Interactive Dashboard (`dashboard.py`)
- **Executive Summary**: Key metrics and alerts
- **KPI Visualization**: Interactive charts and performance tracking
- **Fraud Analysis**: Risk distribution and pattern visualization
- **Association Rules**: Rule quality metrics and insights
- **Actionable Recommendations**: Priority-based recommendations

## 📊 Sample Outputs

### Generated Reports
- `LEVIS_KPI_Analysis_Report.xlsx` - Comprehensive KPI analysis
- `LEVIS_Fraud_Pattern_Analysis.xlsx` - Fraud detection results
- `LEVIS_Cleaned_Stocktake_Data.csv` - Processed data for further analysis
- `LEVIS_Executive_Summary.txt` - Executive-level insights

### Dashboard Features
- **Real-time Metrics**: Live KPI monitoring
- **Interactive Charts**: Plotly-based visualizations
- **Filtering Capabilities**: Date range and store selection
- **Risk Alerts**: Automated fraud risk notifications

## 🎯 Key Performance Indicators

### Inventory Health Metrics
- **Inventory Accuracy**: Percentage accuracy of stock counts
- **Shrinkage Rate**: Loss percentage from theft/damage
- **Inventory Turnover**: Sales velocity relative to inventory
- **RTV Rate**: Return to vendor percentage
- **Health Score**: Composite performance indicator

### Fraud Detection Metrics
- **Fraud Score**: Composite risk assessment (0-7 scale)
- **Risk Rate**: Percentage of high-risk periods
- **Pattern Confidence**: Association rule reliability
- **Lift Score**: Rule significance measure

## 🔍 Fraud Detection Methodology

### Association Rule Mining
1. **Data Preparation**: Convert inventory movements to binary transactions
2. **Pattern Discovery**: Apply Apriori and FP-Growth algorithms
3. **Rule Generation**: Extract high-confidence association rules
4. **Risk Assessment**: Score periods based on fraud indicators
5. **Alert Generation**: Identify high-risk patterns and periods

### Fraud Indicators
- High shrinkage periods (>2%)
- Large inventory discrepancies (>100 units)
- Unusual RTV patterns (>3%)
- Zero sales periods
- Abnormal transfer patterns
- Store-specific anomalies
- Temporal patterns (weekends, month-end)

## 💼 Professional Applications

### For Data Analysts
- **Portfolio Project**: Demonstrates advanced analytics skills
- **Interview Preparation**: Shows real-world problem-solving
- **Skill Development**: Association rule mining and fraud detection

### For Retail Managers
- **Inventory Optimization**: Data-driven stock management
- **Loss Prevention**: Proactive fraud detection
- **Performance Monitoring**: KPI-based store management

### For Consulting Firms
- **Client Deliverables**: Professional-grade analysis reports
- **Methodology Demonstration**: Industry-standard approaches
- **Value Proposition**: Tangible business impact

## 🛠️ Technical Implementation

### Data Processing Pipeline
```python
# Initialize pipeline
pipeline = StocktakeDataPipeline('LEVISSTOCKTAKE.csv')
pipeline.load_data()
cleaned_data = pipeline.clean_data()
pipeline.validate_data_quality()
```

### KPI Analysis
```python
# Perform KPI analysis
kpi_analyzer = StocktakeKPIAnalysis(cleaned_data)
kpi_report = kpi_analyzer.generate_kpi_report()
```

### Fraud Pattern Mining
```python
# Detect fraud patterns
fraud_miner = FraudPatternMining(cleaned_data)
fraud_report = fraud_miner.generate_fraud_report()
```

## 📋 Requirements

### Python Packages
- `pandas==2.1.4` - Data manipulation
- `numpy==1.24.3` - Numerical computing
- `matplotlib==3.7.2` - Static plotting
- `seaborn==0.12.2` - Statistical visualization
- `plotly==5.17.0` - Interactive charts
- `streamlit==1.28.1` - Web dashboard
- `mlxtend==0.22.0` - Association rule mining
- `scikit-learn==1.3.0` - Machine learning utilities
- `openpyxl==3.1.2` - Excel file handling
- `xlsxwriter==3.1.9` - Excel report generation

### System Requirements
- Python 3.8+
- 4GB RAM minimum
- 500MB disk space

## 🎓 Learning Outcomes

### Technical Skills
- **Data Mining**: Association rule mining implementation
- **Fraud Detection**: Pattern-based anomaly identification
- **KPI Development**: Retail-specific performance metrics
- **Dashboard Creation**: Interactive data visualization
- **Report Generation**: Professional Excel reporting

### Business Skills
- **Retail Analytics**: Industry-specific knowledge
- **Risk Assessment**: Fraud and loss prevention
- **Performance Management**: KPI-based decision making
- **Executive Communication**: Clear insights presentation

## 🔧 Customization

### Adding New KPIs
```python
# In kpi_analysis.py
def calculate_custom_kpi(self):
    df['Custom_KPI'] = (df['Sales'] / df['Beginning_Inventory']) * 100
    return df
```

### Modifying Fraud Indicators
```python
# In fraud_pattern_mining.py
def create_custom_fraud_indicators(self):
    df['Custom_Fraud_Indicator'] = df['Sales'] < df['Sales'].quantile(0.1)
    return df
```

### Extending Dashboard
```python
# In dashboard.py
def render_custom_section(self):
    st.subheader("Custom Analysis")
    # Add your custom visualizations
```

## 📚 Best Practices

### Data Quality
- Always validate data before analysis
- Document data cleaning steps
- Handle missing values appropriately
- Check for data consistency

### Analysis Methodology
- Use industry-standard KPIs
- Apply appropriate statistical methods
- Document assumptions and limitations
- Provide actionable recommendations

### Reporting
- Create executive summaries
- Use clear visualizations
- Prioritize recommendations
- Include methodology documentation

## 🤝 Contributing

This project serves as a template for retail analytics. To extend:

1. **Add New Data Sources**: Integrate additional retail data
2. **Enhance Algorithms**: Implement advanced fraud detection
3. **Improve Visualizations**: Add new dashboard features
4. **Extend KPIs**: Develop industry-specific metrics

## 📄 License

This project is for educational and professional development purposes. The analysis methodology and code structure can be adapted for commercial use with appropriate modifications.

## 🎯 Success Metrics

### For Job Applications
- **Technical Demonstration**: Shows advanced analytics skills
- **Business Impact**: Demonstrates value creation
- **Professional Quality**: Industry-standard deliverables
- **Communication**: Clear insights presentation

### For Business Use
- **Risk Reduction**: Proactive fraud detection
- **Performance Improvement**: Data-driven optimization
- **Cost Savings**: Reduced inventory losses
- **Operational Efficiency**: Streamlined monitoring

---

**Built with ❤️ for professional data analytics and retail excellence** 