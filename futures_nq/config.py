"""
Configuration settings for the Futures NQ data fetcher
"""

# Databento API Configuration
API_KEY = "db-gTHu98jipf8fqeHuVjsDxhdSGM9YR"
DATASET = "GLBX.MDP3"  # Global Exchange Market Data Protocol 3

# Schema Configuration
SCHEMA = "ohlcv-1m"            # 1-minute OHLCV data
SCHEMA_STATS = "definition"    # Statistics/Reference data
SCHEMA_TRADES = "trades"       # Trade data
SCHEMA_MBP = "mbp-10"         # Market by Price (10 levels)

# Symbol Configuration
SYMBOL = "NQM5"  # E-mini NASDAQ-100 Futures June 2025 contract
SYMBOL_DESCRIPTION = "E-mini NASDAQ-100 Futures (June 2025)"

# Default time range (with timezone)
from datetime import datetime, timezone
DEFAULT_START_TIME = datetime(2025, 3, 21, tzinfo=timezone.utc)
DEFAULT_END_TIME = datetime(2025, 3, 22, tzinfo=timezone.utc)

# Output configuration
OUTPUT_DIR = "data"
OUTPUT_FILE = f"{OUTPUT_DIR}/nq_futures_data.csv"