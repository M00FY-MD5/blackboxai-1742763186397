"""
Data fetcher module for retrieving Futures NQ data from Databento
"""

import os
from datetime import datetime
import pandas as pd
from databento import Historical
from .logger import logger
from .config import (
    API_KEY, DATASET, SCHEMA, SCHEMA_STATS, SCHEMA_TRADES, SCHEMA_MBP,
    SYMBOL, SYMBOL_DESCRIPTION
)

class NQDataFetcher:
    def __init__(self):
        """Initialize the Databento client with API credentials"""
        self.client = Historical(API_KEY)
        logger.info(f"Initialized Databento client for {DATASET}")

    def fetch_data(self, start_time: datetime, end_time: datetime) -> pd.DataFrame:
        """
        Fetch OHLCV data for NQ futures from Databento
        
        Args:
            start_time (datetime): Start time for data retrieval
            end_time (datetime): End time for data retrieval
            
        Returns:
            pd.DataFrame: DataFrame containing the OHLCV data
        """
        try:
            logger.info(f"Fetching {SYMBOL} OHLCV data from {start_time} to {end_time}")
            
            # Convert datetime to ISO format string
            start_str = start_time.isoformat()
            end_str = end_time.isoformat()
            
            # Fetch data using the Databento client
            data = self.client.timeseries.get_range(
                dataset=DATASET,
                symbols=[SYMBOL],
                schema=SCHEMA,
                start=start_str,
                end=end_str
            )
            
            # Convert to DataFrame
            df = data.to_df()
            
            # Clean up DataFrame
            if 'ts_event' in df.columns:
                df.set_index('ts_event', inplace=True)
            
            keep_cols = ['open', 'high', 'low', 'close', 'volume']
            df = df[keep_cols]
            df.index = pd.to_datetime(df.index)
            
            logger.info(f"Successfully fetched {len(df)} OHLCV records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching OHLCV data: {str(e)}")
            raise

    def fetch_statistics(self, start_time: datetime, end_time: datetime) -> pd.DataFrame:
        """
        Fetch statistics/reference data for NQ futures from Databento
        
        Args:
            start_time (datetime): Start time for data retrieval
            end_time (datetime): End time for data retrieval
            
        Returns:
            pd.DataFrame: DataFrame containing the statistics data
        """
        try:
            logger.info(f"Fetching {SYMBOL} statistics from {start_time} to {end_time}")
            
            # For statistics/reference data, we use metadata.get_definition
            data = self.client.metadata.get_definition(
                dataset=DATASET,
                symbols=[SYMBOL],
                start=start_time.date(),
                end=end_time.date()
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            logger.info(f"Successfully fetched statistics records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching statistics data: {str(e)}")
            raise

    def fetch_trades(self, start_time: datetime, end_time: datetime) -> pd.DataFrame:
        """
        Fetch trades data for NQ futures from Databento
        
        Args:
            start_time (datetime): Start time for data retrieval
            end_time (datetime): End time for data retrieval
            
        Returns:
            pd.DataFrame: DataFrame containing the trades data
        """
        try:
            logger.info(f"Fetching {SYMBOL} trades from {start_time} to {end_time}")
            
            start_str = start_time.isoformat()
            end_str = end_time.isoformat()
            
            data = self.client.timeseries.get_range(
                dataset=DATASET,
                symbols=[SYMBOL],
                schema=SCHEMA_TRADES,
                start=start_str,
                end=end_str
            )
            
            df = data.to_df()
            
            if 'ts_event' in df.columns:
                df.set_index('ts_event', inplace=True)
            
            df.index = pd.to_datetime(df.index)
            
            logger.info(f"Successfully fetched {len(df)} trade records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching trades data: {str(e)}")
            raise

    def fetch_mbp10(self, start_time: datetime, end_time: datetime) -> pd.DataFrame:
        """
        Fetch MBP-10 data for NQ futures from Databento
        
        Args:
            start_time (datetime): Start time for data retrieval
            end_time (datetime): End time for data retrieval
            
        Returns:
            pd.DataFrame: DataFrame containing the MBP-10 data
        """
        try:
            logger.info(f"Fetching {SYMBOL} MBP-10 data from {start_time} to {end_time}")
            
            start_str = start_time.isoformat()
            end_str = end_time.isoformat()
            
            data = self.client.timeseries.get_range(
                dataset=DATASET,
                symbols=[SYMBOL],
                schema=SCHEMA_MBP,
                start=start_str,
                end=end_str
            )
            
            df = data.to_df()
            
            if 'ts_event' in df.columns:
                df.set_index('ts_event', inplace=True)
            
            df.index = pd.to_datetime(df.index)
            
            logger.info(f"Successfully fetched {len(df)} MBP-10 records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching MBP-10 data: {str(e)}")
            raise

    def save_to_csv(self, df: pd.DataFrame, filepath: str):
        """
        Save the DataFrame to a CSV file
        
        Args:
            df (pd.DataFrame): DataFrame to save
            filepath (str): Path to save the CSV file
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            df_to_save = df.reset_index()
            if df_to_save.columns[0] == 'ts_event':
                df_to_save.rename(columns={'ts_event': 'timestamp'}, inplace=True)
            df_to_save.to_csv(filepath, index=False)
            logger.info(f"Data saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving data to CSV: {str(e)}")
            raise