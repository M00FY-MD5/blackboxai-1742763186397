"""
Runner script for the Futures NQ Data Viewer
"""

import os
import streamlit as st
from futures_nq.main import run_streamlit

if __name__ == "__main__":
    # Set environment variable to indicate Streamlit is running
    os.environ['STREAMLIT_RUNNING'] = 'true'
    
    # Run the Streamlit application
    run_streamlit()