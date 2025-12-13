# Interactive Data Visualization Dashboard
# Featuring: Stream Graph, Scatter Plot, Heatmaps, and Violin Chart

import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================
# SAMPLE DATA GENERATION
# ============================================

np.random.seed(42)

# Generate date range for 52 weeks
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(weeks=i) for i in range(52)]
weeks = list(range(1, 53))

# Stream Graph Data (multiple categories over time)
categories = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer']
stream_data = pd.DataFrame({
    'Week': weeks * len(categories),
    'Date': dates * len(categories),
    'Category': np.repeat(categories, 52),
    'Value': np.concatenate([
        50 + np.cumsum(np.random.randn(52) * 5 + 2),  # Technology - upward trend
        30 + np.cumsum(np.random.randn(52) * 3 + 1),  # Healthcare - moderate growth
        40 + np.cumsum(np.random.randn(52) * 4),       # Finance - volatile
        25 + np.cumsum(np.random.randn(52) * 3 - 0.5), # Energy - slight decline
        35 + np.cumsum(np.random.randn(52) * 3 + 0.5)  # Consumer - stable growth
    ])
})

# Scatter Plot Data
n_points = 200
scatter_data = pd.DataFrame({
    'X_Value': np.random.randn(n_points) * 20 + 50,
    'Y_Value': np.random.randn(n_points) * 15 + 40,
    'Size': np.random.uniform(10, 50, n_points),
    'Category': np.random.choice(categories, n_points),
    'Performance': np.random.uniform(0, 100, n_points)
})
scatter_data['Y_Value'] = scatter_data['X_Value'] * 0.6 + np.random.randn(n_points) * 10 + 10

# Heatmap Data (4 different correlation matrices)
def generate_heatmap_data(n=8, seed=None):
    if seed:
        np.random.seed(seed)
    data = np.random.randn(100, n)
    corr = np.corrcoef(data.T)
    return corr

heatmap1 = generate_heatmap_data(8, 1)
heatmap2 = generate_heatmap_data(8, 2)
heatmap3 = generate_heatmap_data(8, 3)
heatmap4 = generate_heatmap_data(8, 4)

heatmap_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Violin Chart Data
violin_data = pd.DataFrame({
    'Category': np.repeat(categories, 100),
    'Value': np.concatenate([
        np.random.normal(60, 15, 100),   # Technology
        np.random.normal(45, 10, 100),   # Healthcare
        np.random.normal(55, 20, 100),   # Finance
        np.random.normal(40, 12, 100),   # Energy
        np.random.normal(50, 8, 100)     # Consumer
    ]),
    'Quarter': np.tile(np.repeat(['Q1', 'Q2', 'Q3', 'Q4'], 25), 5)
})

# ============================================
# COLOR SCHEMES
# ============================================

# Dark theme colors
colors = {
    'bg': '#0f0f1a',
    'card_bg': 'rgba(30, 30, 50, 0.8)',
    'text': '#ffffff',
    'text_secondary': '#a0a0b0',
    'accent': '#6366f1',
    'grid': 'rgba(255, 255, 255, 0.1)'
}

# Vibrant color palette for charts
chart_colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b']
heatmap_colorscale = [
    [0, '#1e1e3c'],
    [0.25, '#3b3b6d'],
    [0.5, '#6366f1'],
    [0.75, '#8b5cf6'],
    [1, '#c4b5fd']
]

# ============================================
# PLOTLY FIGURE TEMPLATE
# ============================================

plotly_template = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': colors['text'], 'family': 'Inter, sans-serif'},
        'xaxis': {
            'gridcolor': colors['grid'],
            'zerolinecolor': colors['grid'],
            'tickfont': {'color': colors['text_secondary']}
        },
        'yaxis': {
            'gridcolor': colors['grid'],
            'zerolinecolor': colors['grid'],
            'tickfont': {'color': colors['text_secondary']}
        },
        'colorway': chart_colors,
        'hoverlabel': {
            'bgcolor': colors['card_bg'],
            'font': {'color': colors['text'], 'family': 'Inter'}
        }
    }
}

# ============================================
# INITIALIZE DASH APP
# ============================================

app = dash.Dash(
    __name__,
    title="Data Visualization Dashboard",
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

# ============================================
# CREATE FIGURES
# ============================================

def create_stream_graph(week_range):
    """Create stream graph with line overlay"""
    filtered = stream_data[(stream_data['Week'] >= week_range[0]) & (stream_data['Week'] <= week_range[1])]
    
    fig = go.Figure()
    
    # Add stacked area (stream) for each category
    for i, cat in enumerate(categories):
        cat_data = filtered[filtered['Category'] == cat]
        fig.add_trace(go.Scatter(
            x=cat_data['Week'],
            y=cat_data['Value'],
            name=cat,
            mode='lines',
            stackgroup='one',
            fillcolor=f'rgba{tuple(list(px.colors.hex_to_rgb(chart_colors[i])) + [0.6])}',
            line=dict(width=0.5, color=chart_colors[i]),
            hovertemplate=f'<b>{cat}</b><br>Week: %{{x}}<br>Value: %{{y:.1f}}<extra></extra>'
        ))
    
    # Add trend line (average across categories)
    avg_by_week = filtered.groupby('Week')['Value'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=avg_by_week['Week'],
        y=avg_by_week['Value'],
        name='Trend',
        mode='lines',
        line=dict(color='#ffffff', width=3, dash='dot'),
        hovertemplate='<b>Average Trend</b><br>Week: %{x}<br>Value: %{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        template=plotly_template,
        height=450,
        margin=dict(l=50, r=30, t=30, b=50),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11)
        ),
        xaxis_title='Week Number',
        yaxis_title='Value',
        hovermode='x unified'
    )
    
    return fig


def create_scatter_plot():
    """Create interactive scatter plot"""
    fig = px.scatter(
        scatter_data,
        x='X_Value',
        y='Y_Value',
        color='Category',
        size='Size',
        hover_data=['Performance'],
        color_discrete_sequence=chart_colors
    )
    
    fig.update_traces(
        marker=dict(opacity=0.7, line=dict(width=1, color='white')),
        hovertemplate='<b>%{customdata[0]:.1f}% Performance</b><br>X: %{x:.1f}<br>Y: %{y:.1f}<extra></extra>'
    )
    
    fig.update_layout(
        template=plotly_template,
        height=450,
        margin=dict(l=50, r=30, t=30, b=50),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=10)
        ),
        xaxis_title='X Value',
        yaxis_title='Y Value'
    )
    
    return fig


def create_heatmap(data, title):
    """Create a single heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=heatmap_labels,
        y=heatmap_labels,
        colorscale=heatmap_colorscale,
        showscale=False,
        hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>'
    ))
    
    # Add correlation values as text
    annotations = []
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            annotations.append(dict(
                x=heatmap_labels[j],
                y=heatmap_labels[i],
                text=f'{val:.2f}',
                showarrow=False,
                font=dict(color='white' if abs(val) > 0.5 else '#a0a0b0', size=9)
            ))
    
    fig.update_layout(
        template=plotly_template,
        height=250,
        margin=dict(l=40, r=20, t=40, b=40),
        title=dict(text=title, font=dict(size=14), x=0.5),
        annotations=annotations
    )
    
    return fig


def create_violin_chart(selected_quarter=None):
    """Create violin chart"""
    data = violin_data if selected_quarter is None else violin_data[violin_data['Quarter'] == selected_quarter]
    
    fig = go.Figure()
    
    for i, cat in enumerate(categories):
        cat_data = data[data['Category'] == cat]['Value']
        fig.add_trace(go.Violin(
            y=cat_data,
            name=cat,
            box_visible=True,
            meanline_visible=True,
            fillcolor=f'rgba{tuple(list(px.colors.hex_to_rgb(chart_colors[i])) + [0.6])}',
            line_color=chart_colors[i],
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Value: %{y:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        template=plotly_template,
        height=400,
        margin=dict(l=50, r=30, t=30, b=50),
        showlegend=False,
        xaxis_title='Category',
        yaxis_title='Distribution Value',
        violinmode='group'
    )
    
    return fig


# ============================================
# APP LAYOUT
# ============================================

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Data Analysis & Visualization Dashboard"),
        html.P("Explore interactive visualizations with real-time data insights")
    ], className='dashboard-header'),
    
    # Main Container
    html.Div([
        # Top Row: Stream Graph + Scatter Plot
        html.Div([
            # Main Stream Graph Card
            html.Div([
                html.Div([
                    html.H3("Stream Graph with Trend Analysis"),
                    html.P("Stacked area visualization showing category performance over time"),
                ]),
                dcc.Graph(id='stream-graph', figure=create_stream_graph([1, 52]), config={'responsive': False}, style={'height': '450px'}),
                html.Div([
                    html.Label("Select Week Range:", style={'color': '#a0a0b0', 'marginBottom': '10px', 'display': 'block'}),
                    dcc.RangeSlider(
                        id='week-slider',
                        min=1,
                        max=52,
                        step=1,
                        value=[1, 52],
                        marks={i: {'label': f'W{i}', 'style': {'color': '#6b7280', 'fontSize': '10px'}} 
                               for i in range(1, 53, 4)},
                        tooltip={'placement': 'bottom', 'always_visible': False}
                    )
                ], style={'marginTop': '20px', 'padding': '0 10px'})
            ], className='graph-card'),
            
            # Scatter Plot Card
            html.Div([
                html.Div([
                    html.H3("Scatter Plot Analysis"),
                    html.P("Correlation between variables by category"),
                ]),
                dcc.Graph(id='scatter-plot', figure=create_scatter_plot(), config={'responsive': False}, style={'height': '450px'})
            ], className='graph-card')
        ], className='top-row'),
        
        # Heatmaps Section
        html.Div([
            html.Div([
                html.H3("Correlation Heatmaps"),
                html.P("Four correlation matrices showing relationships between variables"),
            ]),
            html.Div([
                html.Div([
                    dcc.Graph(id='heatmap-1', figure=create_heatmap(heatmap1, 'Dataset A'), config={'responsive': False}, style={'height': '250px'})
                ], className='heatmap-card'),
                html.Div([
                    dcc.Graph(id='heatmap-2', figure=create_heatmap(heatmap2, 'Dataset B'), config={'responsive': False}, style={'height': '250px'})
                ], className='heatmap-card'),
                html.Div([
                    dcc.Graph(id='heatmap-3', figure=create_heatmap(heatmap3, 'Dataset C'), config={'responsive': False}, style={'height': '250px'})
                ], className='heatmap-card'),
                html.Div([
                    dcc.Graph(id='heatmap-4', figure=create_heatmap(heatmap4, 'Dataset D'), config={'responsive': False}, style={'height': '250px'})
                ], className='heatmap-card'),
            ], className='heatmaps-container')
        ], className='graph-card'),
        
        # Violin Chart Section
        html.Div([
            html.Div([
                html.H3("Distribution Analysis - Violin Chart"),
                html.P("Value distribution across categories with box plot overlay"),
            ]),
            html.Div([
                html.Label("Filter by Quarter:", style={'color': '#a0a0b0', 'marginRight': '15px'}),
                dcc.Dropdown(
                    id='quarter-dropdown',
                    options=[
                        {'label': 'All Quarters', 'value': 'all'},
                        {'label': 'Q1', 'value': 'Q1'},
                        {'label': 'Q2', 'value': 'Q2'},
                        {'label': 'Q3', 'value': 'Q3'},
                        {'label': 'Q4', 'value': 'Q4'}
                    ],
                    value='all',
                    clearable=False,
                    style={
                        'width': '200px',
                        'backgroundColor': '#1a1a2e',
                        'color': '#ffffff'
                    }
                )
            ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            dcc.Graph(id='violin-chart', figure=create_violin_chart(), config={'responsive': False}, style={'height': '400px'})
        ], className='graph-card'),
        
    ], className='main-container'),
    
    # Footer
    html.Div([
        html.P(["Data Visualization Project - Group 65 | Built with ", 
                html.A("Dash & Plotly", href="https://plotly.com/dash/", target="_blank")])
    ], className='dashboard-footer')
    
], style={'backgroundColor': '#0f0f1a', 'minHeight': '100vh'})


# ============================================
# CALLBACKS FOR INTERACTIVITY
# ============================================

@callback(
    Output('stream-graph', 'figure'),
    Input('week-slider', 'value')
)
def update_stream_graph(week_range):
    """Update stream graph based on slider selection"""
    return create_stream_graph(week_range)


@callback(
    Output('violin-chart', 'figure'),
    Input('quarter-dropdown', 'value')
)
def update_violin_chart(quarter):
    """Update violin chart based on quarter selection"""
    if quarter == 'all':
        return create_violin_chart()
    return create_violin_chart(quarter)


# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    app.run(debug=True, port=8050)
