"""
Main entry point for the Futures NQ data fetcher application
"""

import os
import sys
from datetime import datetime, timezone
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from .data_fetcher import NQDataFetcher
from .config import DEFAULT_START_TIME, DEFAULT_END_TIME, OUTPUT_FILE, SYMBOL_DESCRIPTION
from .logger import logger

def plot_ohlcv(df: pd.DataFrame) -> go.Figure:
    """Create an OHLCV candlestick chart using Plotly"""
    fig = go.Figure()
    
    # Add candlestick trace
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='OHLC',
        increasing_line_color='#26a69a',
        decreasing_line_color='#ef5350'
    ))
    
    # Add volume trace
    colors = ['#26a69a' if row['close'] >= row['open'] else '#ef5350' for _, row in df.iterrows()]
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['volume'],
        name='Volume',
        marker_color=colors,
        opacity=0.5,
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        yaxis=dict(
            title='Price',
            side='left',
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            tickformat='.2f'
        ),
        yaxis2=dict(
            title='Volume',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        xaxis=dict(
            title='Time',
            rangeslider=dict(visible=False),
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            tickformat='%Y-%m-%d %H:%M'
        ),
        template='plotly_dark',
        height=300,
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=50, r=50, t=30, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def run_streamlit():
    """Run the Streamlit web interface"""
    # Configure the page
    st.set_page_config(
        page_title=f"{SYMBOL_DESCRIPTION} Data Viewer",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        .stButton>button:hover {
            background-color: #FF3333;
            transform: translateY(-2px);
        }
        .stDateInput>div>div {
            background-color: #262730;
            border: 1px solid #4B4B4B;
            border-radius: 0.5rem;
            padding: 0.5rem;
        }
        div[data-testid="stVerticalBlock"] > div {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
        .data-frame {
            background-color: #1a1c23;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        h1 {
            font-size: 2rem !important;
            margin-bottom: 0.5rem !important;
        }
        h3 {
            font-size: 1.2rem !important;
            margin: 0.5rem 0 !important;
        }
        .stMarkdown {
            margin-bottom: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Header section with minimal spacing
    st.title(f"{SYMBOL_DESCRIPTION} Data Viewer")
    st.markdown("Select a date range and click 'Fetch Data' to view OHLCV (Open, High, Low, Close, Volume) data.")
    
    # Info message
    st.info("📅 Data is available up to March 22, 2025")
    
    # Input section with reduced spacing
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=DEFAULT_START_TIME.date(),
            max_value=DEFAULT_END_TIME.date()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=DEFAULT_END_TIME.date(),
            max_value=DEFAULT_END_TIME.date()
        )
    with col3:
        fetch_button = st.button("🔄 Fetch Data", type="primary", use_container_width=True)
    
    # Convert dates to timezone-aware datetime
    start_time = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
    end_time = datetime.combine(end_date, datetime.min.time(), tzinfo=timezone.utc)
    
    if fetch_button:
        try:
            with st.spinner("📊 Fetching data..."):
                fetcher = NQDataFetcher()
                df = fetcher.fetch_data(start_time, end_time)
                
                if len(df) > 0:
                    # Create two columns for the main content
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Chart
                        fig = plot_ohlcv(df)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Summary Statistics
                        st.markdown("#### 📈 Summary Statistics")
                        summary = pd.DataFrame({
                            'Open': [df['open'].min(), df['open'].max(), df['open'].mean()],
                            'High': [df['high'].min(), df['high'].max(), df['high'].mean()],
                            'Low': [df['low'].min(), df['low'].max(), df['low'].mean()],
                            'Close': [df['close'].min(), df['close'].max(), df['close'].mean()],
                            'Volume': [df['volume'].min(), df['volume'].max(), df['volume'].mean()]
                        }, index=['Min', 'Max', 'Mean'])
                        
                        st.dataframe(
                            summary.style.format({
                                'Open': '{:.2f}',
                                'High': '{:.2f}',
                                'Low': '{:.2f}',
                                'Close': '{:.2f}',
                                'Volume': '{:,.0f}'
                            }),
                            use_container_width=True
                        )
                    
                    # Raw Data section
                    st.markdown("#### 📋 Raw Data")
                    st.dataframe(
                        df.style.format({
                            'open': '{:.2f}',
                            'high': '{:.2f}',
                            'low': '{:.2f}',
                            'close': '{:.2f}',
                            'volume': '{:,.0f}'
                        }),
                        use_container_width=True,
                        height=150
                    )
                    
                    # Download button
                    st.download_button(
                        "⬇️ Download CSV",
                        df.to_csv(),
                        f"nq_futures_data_{start_date}_{end_date}.csv",
                        "text/csv",
                        use_container_width=True
                    )
                else:
                    st.warning("⚠️ No data available for the selected date range.")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            logger.error(f"Error in Streamlit app: {str(e)}")

def run_cli():
    """Run the command-line interface"""
    try:
        fetcher = NQDataFetcher()
        df = fetcher.fetch_data(DEFAULT_START_TIME, DEFAULT_END_TIME)
        
        if len(df) > 0:
            fetcher.save_to_csv(df, OUTPUT_FILE)
            print(f"Data successfully saved to {OUTPUT_FILE}")
        else:
            print("No data available for the specified date range.")
        
    except Exception as e:
        logger.error(f"Error in CLI mode: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if os.environ.get('STREAMLIT_RUNNING'):
        run_streamlit()
    else:
        run_cli()