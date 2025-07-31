# LEVIS Stocktake Analysis - Project Structure

## 📁 Complete Directory Organization

```
LEVIS Stocktake & Fraud Pattern Mining/
├── 📊 data/                           # Raw and processed data
│   └── LEVISSTOCKTAKE.csv            # Raw stocktake data (104 records, 8 stores)
│
├── 🔧 src/                            # Source code modules
│   ├── __init__.py                   # Package initialization
│   ├── data_pipeline.py              # Data cleaning and preprocessing
│   ├── kpi_analysis.py               # KPI calculation and monitoring
│   ├── fraud_pattern_mining.py       # Association rule mining
│   ├── dashboard.py                  # Streamlit interactive dashboard
│   └── main_analysis.py              # End-to-end analysis orchestrator
│
├── 📈 reports/                        # Generated analysis reports
│   ├── LEVIS_KPI_Analysis_Report.xlsx
│   ├── LEVIS_Fraud_Pattern_Analysis.xlsx
│   ├── LEVIS_Cleaned_Stocktake_Data.csv
│   └── LEVIS_Executive_Summary.txt
│
├── 📚 docs/                           # Documentation
│   ├── README.md                     # Complete project documentation
│   └── PROJECT_SUMMARY.md            # Project summary and achievements
│
├── 📋 requirements.txt                # Python dependencies
├── 🚀 run_analysis.py                 # Main analysis runner
├── 📊 run_dashboard.py                # Dashboard launcher
├── 📖 README.md                       # Quick start guide
└── 📁 PROJECT_STRUCTURE.md            # This file
```

## 🎯 File Descriptions

### 📊 Data Files
- **`data/LEVISSTOCKTAKE.csv`**: Raw stocktake data with European number formatting

### 🔧 Source Code
- **`src/__init__.py`**: Package initialization and exports
- **`src/data_pipeline.py`**: Professional data cleaning and validation
- **`src/kpi_analysis.py`**: Retail KPI calculation and performance monitoring
- **`src/fraud_pattern_mining.py`**: Association rule mining for fraud detection
- **`src/dashboard.py`**: Interactive Streamlit dashboard
- **`src/main_analysis.py`**: End-to-end analysis orchestrator

### 📈 Generated Reports
- **`reports/LEVIS_KPI_Analysis_Report.xlsx`**: Comprehensive KPI analysis with multiple sheets
- **`reports/LEVIS_Fraud_Pattern_Analysis.xlsx`**: Fraud detection results and patterns
- **`reports/LEVIS_Cleaned_Stocktake_Data.csv`**: Processed data for further analysis
- **`reports/LEVIS_Executive_Summary.txt`**: Executive-level insights and recommendations

### 📚 Documentation
- **`docs/README.md`**: Complete project documentation with technical details
- **`docs/PROJECT_SUMMARY.md`**: Project achievements and business value

### 🚀 Entry Points
- **`run_analysis.py`**: Main analysis runner from project root
- **`run_dashboard.py`**: Dashboard launcher with user-friendly interface
- **`README.md`**: Quick start guide for immediate use

## 🛠️ Usage Instructions

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run complete analysis
python run_analysis.py

# Launch interactive dashboard
python run_dashboard.py
```

### Direct Access
```bash
# Run analysis directly
python src/main_analysis.py

# Launch dashboard directly
streamlit run src/dashboard.py
```

## 📊 Analysis Results

### Key Performance Indicators
- **Inventory Health Score**: 79.50% (Good performance)
- **Shrinkage Rate**: 0.00% (Excellent - no inventory loss)
- **Inventory Turnover**: 0.12 (Optimization opportunity)
- **RTV Rate**: 2.74% (Acceptable vendor returns)

### Fraud Detection
- **High-risk periods**: 0 (No suspicious patterns)
- **Average fraud score**: 0.29 (Low risk)
- **Association rules**: Successfully generated using Apriori & FP-Growth

### Store Performance
- **Top Performers**: MSI_ATRIUM_PLAZA, MSI_ARTHA_GADING_MEN, MSI_TAMAN_ANGGREK
- **Needs Attention**: SOGO_KARAWACI_LADIES, SOGO_CENTRAL_PARK, GALERIES_LAFAYETTE

## 💼 Professional Value

### For Data Analysts
- **Portfolio Project**: Demonstrates advanced analytics skills
- **Technical Skills**: Association rule mining, KPI development, data visualization
- **Business Impact**: Real-world retail analytics application

### For Consulting Firms
- **Client Deliverables**: Professional Excel reports with executive summaries
- **Methodology**: Industry-standard approaches and best practices
- **Scalability**: Framework easily adaptable for similar projects

### For Retail Managers
- **Performance Monitoring**: Real-time KPI tracking across stores
- **Risk Management**: Proactive fraud detection and anomaly identification
- **Decision Support**: Data-driven insights for operational improvements

## 🔧 Technical Architecture

### Modular Design
- **Separation of Concerns**: Each module handles specific functionality
- **Reusability**: Components can be used independently
- **Maintainability**: Clean, documented code structure
- **Scalability**: Easy to extend with additional features

### Dependencies
- **Core Analytics**: pandas, numpy, scikit-learn
- **Data Mining**: mlxtend (Apriori, FP-Growth)
- **Visualization**: streamlit, plotly, matplotlib, seaborn
- **Reporting**: openpyxl, xlsxwriter

## 📈 Project Achievements

✅ **Complete End-to-End Pipeline**: Data cleaning → Analysis → Reporting  
✅ **Professional Data Handling**: European number format support  
✅ **Advanced Analytics**: Association rule mining for fraud detection  
✅ **Interactive Dashboard**: Real-time monitoring and visualization  
✅ **Automated Reporting**: Excel exports with executive summaries  
✅ **Comprehensive Documentation**: Technical and business documentation  
✅ **Organized Structure**: Professional project organization  

---

**Built with ❤️ for professional data analytics and retail excellence** 