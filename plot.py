import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data(directory):
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            test_name = filename.replace('_results.csv', '').replace('_', ' ').title()
            df = pd.read_csv(os.path.join(directory, filename))
            df['time'] = df['time'] / 60  # Convert time to minutes
            data[test_name] = df
    return data

def create_individual_plots(data):
    for test_name, df in data.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['time'], y=df['min'], mode='lines', name='Min'))
        fig.add_trace(go.Scatter(x=df['time'], y=df['avg'], mode='lines', name='Avg'))
        fig.add_trace(go.Scatter(x=df['time'], y=df['max'], mode='lines', name='Max'))
        
        fig.update_layout(
            title=f'{test_name} Results',
            xaxis_title='Time (minutes)',
            yaxis_title='Latency (µs)',
            yaxis_type='log',
            legend_title='Metric',
            hovermode='x unified'
        )
        
        fig.write_html(f'{test_name.lower().replace(" ", "_")}_plot.html')
        fig.write_image(f'{test_name.lower().replace(" ", "_")}_plot.png')

def create_combined_plot(data):
    fig = make_subplots(rows=len(data), cols=1, subplot_titles=list(data.keys()), shared_xaxes=True)
    
    for i, (test_name, df) in enumerate(data.items(), start=1):
        fig.add_trace(go.Scatter(x=df['time'], y=df['min'], mode='lines', name=f'{test_name} Min'), row=i, col=1)
        fig.add_trace(go.Scatter(x=df['time'], y=df['avg'], mode='lines', name=f'{test_name} Avg'), row=i, col=1)
        fig.add_trace(go.Scatter(x=df['time'], y=df['max'], mode='lines', name=f'{test_name} Max'), row=i, col=1)
        
        fig.update_yaxes(title_text='Latency (µs)', type='log', row=i, col=1)
    
    fig.update_layout(
        height=300 * len(data),
        title_text='Combined Stress Test Results',
        showlegend=True,
        legend_tracegroupgap=5,
        hovermode='x unified'
    )
    fig.update_xaxes(title_text='Time (minutes)', row=len(data), col=1)
    
    fig.write_html('combined_plot.html')
    fig.write_image('combined_plot.png')

def create_boxplot(data):
    fig = go.Figure()
    
    for test_name, df in data.items():
        fig.add_trace(go.Box(y=df['max'], name=f'{test_name} Max', boxpoints='all', jitter=0.3, pointpos=-1.8))
        fig.add_trace(go.Box(y=df['avg'], name=f'{test_name} Avg', boxpoints='all', jitter=0.3, pointpos=-1.8))
        fig.add_trace(go.Box(y=df['min'], name=f'{test_name} Min', boxpoints='all', jitter=0.3, pointpos=-1.8))
    
    fig.update_layout(
        title='Distribution of Latencies Across All Tests',
        yaxis_title='Latency (µs)',
        yaxis_type='log',
        showlegend=True,
        boxmode='group'
    )
    
    fig.write_html('latency_distribution_boxplot.html')
    fig.write_image('latency_distribution_boxplot.png')

def main():
    # Replace with your actual results directory
    results_dir = 'stress_test_results_20241017_203959'
    
    data = load_data(results_dir)
    create_individual_plots(data)
    create_combined_plot(data)
    create_boxplot(data)
    
    print("All plots have been generated and saved.")

if __name__ == "__main__":
    main()
