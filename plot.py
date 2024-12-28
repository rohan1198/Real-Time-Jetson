import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StressTestAnalyzer:
    def __init__(self, directory: str):
        """Initialize the analyzer with the directory containing test results."""
        self.directory = directory
        self.data = self._load_data()
        self.output_dir = f"{directory}_analysis"
        os.makedirs(self.output_dir, exist_ok=True)

    def _load_data(self) -> Dict[str, pd.DataFrame]:
        """Load and preprocess all CSV files from the directory."""
        data = {}
        try:
            for filename in os.listdir(self.directory):
                if filename.endswith('.csv'):
                    test_name = filename.replace('_results.csv', '').replace('_', ' ').title()
                    df = pd.read_csv(os.path.join(self.directory, filename))
                    df['time'] = df['time'] / 60  # Convert time to minutes

                    # Add additional statistical columns
                    df['latency_range'] = df['max'] - df['min']
                    df['std_dev'] = df[['min', 'avg', 'max']].std(axis=1)

                    data[test_name] = df
            logger.info(f"Loaded data from {len(data)} test files")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def create_individual_plots(self):
        """Create detailed individual plots for each test."""
        for test_name, df in self.data.items():
            try:
                # Create subplots: main latency plot and statistics
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=(f'{test_name} Latency Measurements', 'Statistical Metrics'),
                    row_heights=[0.7, 0.3]
                )

                # Latency traces
                for metric in ['min', 'avg', 'max']:
                    fig.add_trace(
                        go.Scatter(x=df['time'], y=df[metric], 
                                 name=metric.capitalize(),
                                 mode='lines'),
                        row=1, col=1
                    )

                # Statistics traces
                fig.add_trace(
                    go.Scatter(x=df['time'], y=df['latency_range'],
                             name='Latency Range',
                             line=dict(dash='dash')),
                    row=2, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df['time'], y=df['std_dev'],
                             name='Standard Deviation',
                             line=dict(dash='dot')),
                    row=2, col=1
                )

                # Update layout
                fig.update_layout(
                    height=800,
                    title=f'{test_name} Detailed Analysis',
                    hovermode='x unified',
                    showlegend=True
                )

                # Update axes
                fig.update_yaxes(title_text='Latency (µs)', type='log', row=1, col=1)
                fig.update_yaxes(title_text='Value (µs)', row=2, col=1)
                fig.update_xaxes(title_text='Time (minutes)', row=2, col=1)

                # Save plots
                output_base = os.path.join(self.output_dir, f'{test_name.lower().replace(" ", "_")}')
                fig.write_html(f'{output_base}_detailed.html')
                fig.write_image(f'{output_base}_detailed.png')

                logger.info(f"Generated detailed plot for {test_name}")
            except Exception as e:
                logger.error(f"Error creating plot for {test_name}: {str(e)}")

    def create_summary_statistics(self):
        """Create a summary statistics table."""
        stats = []
        for test_name, df in self.data.items():
            stats.append({
                'Test': test_name,
                'Min Latency': df['min'].min(),
                'Avg Latency': df['avg'].mean(),
                'Max Latency': df['max'].max(),
                'Std Dev': df['std_dev'].mean(),
                '99th Percentile': df['max'].quantile(0.99),
                'Latency Range': df['latency_range'].mean()
            })

        stats_df = pd.DataFrame(stats)
        stats_df.to_csv(os.path.join(self.output_dir, 'summary_statistics.csv'), index=False)
        return stats_df

    def create_comparison_plot(self):
        """Create a comprehensive comparison plot."""
        fig = go.Figure()

        # Create violin plots for each test
        for test_name, df in self.data.items():
            for metric in ['min', 'avg', 'max']:
                fig.add_trace(
                    go.Violin(
                        x=[f"{test_name} ({metric})"] * len(df),
                        y=df[metric],
                        name=f"{test_name} {metric}",
                        box_visible=True,
                        meanline_visible=True
                    )
                )

        fig.update_layout(
            title='Distribution Comparison Across All Tests',
            yaxis_title='Latency (µs)',
            yaxis_type='log',
            showlegend=False,
            height=800,
            width=1200
        )

        fig.write_html(os.path.join(self.output_dir, 'comparison_plot.html'))
        fig.write_image(os.path.join(self.output_dir, 'comparison_plot.png'))

def main():
    # Replace with your actual results directory
    results_dir = 'stress_test_results_20241226_210525'

    try:
        analyzer = StressTestAnalyzer(results_dir)
        analyzer.create_individual_plots()
        stats_df = analyzer.create_summary_statistics()
        analyzer.create_comparison_plot()

        print("\nSummary Statistics:")
        print(stats_df.to_string(index=False))
        print(f"\nAll analysis results have been saved to: {analyzer.output_dir}")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()

