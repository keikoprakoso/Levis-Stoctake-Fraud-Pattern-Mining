"""
LEVIS Stocktake Analysis Package
Professional retail analytics and fraud detection modules.
"""

__version__ = "1.0.0"
__author__ = "Data Analytics Professional"
__description__ = "End-to-end retail stocktake analysis and fraud pattern mining"

# Import main classes for easy access
from .data_pipeline import StocktakeDataPipeline
from .kpi_analysis import StocktakeKPIAnalysis
from .fraud_pattern_mining import FraudPatternMining
from .main_analysis import LEVISStocktakeAnalysis

__all__ = [
    'StocktakeDataPipeline',
    'StocktakeKPIAnalysis', 
    'FraudPatternMining',
    'LEVISStocktakeAnalysis'
] 