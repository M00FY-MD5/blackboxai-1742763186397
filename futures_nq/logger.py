"""
Logger configuration for the Futures NQ data fetcher
"""

import logging
import sys
from datetime import datetime

def setup_logger(name: str = "futures_nq") -> logging.Logger:
    """
    Configure and return a logger instance with proper formatting
    
    Args:
        name (str): Name of the logger instance
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger already exists
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Create console handler with formatting
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Create default logger instance
logger = setup_logger()