"""
COMMAND MAP
World Choropleth Visualization with Interactive Selection

Color scale: Deep Blue (#002B36) → Electric Cyan (#00E5FF)
Click selection updates primary_country in session state
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Optional
from data.countries import get_global_watchlist, Country
from scoring.apex_score import calculate_all_scores, APEXResult

# ═══════════════════════════════════════════════════════════════════════════════
# DARK NEON COLOR SCALE
# Sequential: Deep Black (#050A0E) → Electric Cyan (#00E5FF)
# ═══════════════════════════════════════════════════════════════════════════════

APEX_COLORSCALE = [
    [0.0, '#050A0E'],    # FORTRESS - Deep Black (lowest stress)
    [0.25, '#0A2530'],
    [0.5, '#0A4A60'],    # ELEVATED
    [0.75, '#00A0C0'],
    [1.0, '#00E5FF'],    # CRITICAL - Electric Cyan (highest stress)
]

def create_command_map_data() -> pd.DataFrame:
    """
    Generate DataFrame for the Command Map choropleth.
    
    Returns:
        DataFrame with country codes, names, scores, and metadata
    """
    scores = calculate_all_scores()
    countries = get_global_watchlist()
    country_map = {c.code: c for c in countries}
    
    data = []
    for s in scores:
        c = country_map[s.country_code]
        # Invert score for color mapping (high risk = bright)
        stress_level = 100 - s.apex_score
        data.append({
            'code': s.country_code,
            'name': s.country_name,
            'apex_score': s.apex_score,
            'stress_level': stress_level,
            'risk_tier': s.risk_tier,
            'debt_gdp': c.debt_to_gdp,
            'fx_reserves': c.fx_reserves_months,
            'inflation': c.inflation_rate,
            'yield_10y': c.yield_10y,
            'category': c.category
        })
    
    return pd.DataFrame(data)

def create_command_map(selected_country: Optional[str] = None) -> go.Figure:
    """
    Generate the APEX Command Map using plotly.express.choropleth.
    
    Args:
        selected_country: ISO code of currently selected country (for highlighting)
    
    Returns:
        Plotly Figure with interactive choropleth map
    """
    df = create_command_map_data()
    
    # Build custom hover template
    custom_data = ['name', 'apex_score', 'risk_tier', 'debt_gdp', 'fx_reserves', 'inflation', 'yield_10y']
    
    fig = px.choropleth(
        df,
        locations='code',
        color='stress_level',
        hover_name='name',
        hover_data={
            'code': False,
            'stress_level': False,
            'apex_score': ':.1f',
            'risk_tier': True,
            'debt_gdp': ':.0f',
            'fx_reserves': ':.1f',
            'inflation': ':.1f',
            'yield_10y': ':.2f',
            'category': True
        },
        color_continuous_scale=APEX_COLORSCALE,
        range_color=[0, 100],
        labels={
            'apex_score': 'APEX Score',
            'risk_tier': 'Risk Tier',
            'debt_gdp': 'Debt/GDP (%)',
            'fx_reserves': 'FX Reserves (months)',
            'inflation': 'Inflation (%)',
            'yield_10y': '10Y Yield (%)',
            'category': 'Category'
        }
    )
    
    # Update colorbar
    fig.update_coloraxes(
        colorbar=dict(
            title=dict(
                text='SOVEREIGN<br>STRESS',
                font=dict(family='JetBrains Mono, SF Mono, monospace', size=11, color='#E0E0E0')
            ),
            tickfont=dict(family='JetBrains Mono, SF Mono, monospace', size=10, color='#6B7280'),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#1A1A2E',
            borderwidth=1,
            tickvals=[0, 25, 50, 75, 100],
            ticktext=['FORTRESS', 'STABLE', 'ELEVATED', 'HIGH', 'CRITICAL'],
            len=0.5,
            x=1.02,
            y=0.5
        )
    )
    
    # Update geo styling
    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor='#1A1A2E',
        showland=True,
        landcolor='#0A0A0F',
        showocean=True,
        oceancolor='#000000',
        showlakes=False,
        showcountries=True,
        countrycolor='#1A1A2E',
        projection_type='natural earth',
        bgcolor='#000000',
    )
    
    # Update layout
    fig.update_layout(
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(
            text='COMMAND MAP // GLOBAL SOVEREIGN EXPOSURE',
            font=dict(family='JetBrains Mono, SF Mono, monospace', size=14, color='#00E5FF'),
            x=0.5,
            xanchor='center'
        ),
        height=450,
    )
    
    # Update trace for consistent styling
    fig.update_traces(
        marker_line_color='#1A1A2E',
        marker_line_width=0.5,
    )
    
    return fig

def get_country_from_selection(selection_data: dict) -> Optional[str]:
    """
    Extract country code from plotly selection event.
    
    Args:
        selection_data: The selection event data from st.plotly_chart
        
    Returns:
        ISO country code or None if no valid selection
    """
    if selection_data is None:
        return None
    
    # Handle different selection event structures
    if 'selection' in selection_data:
        sel = selection_data['selection']
        if 'points' in sel and len(sel['points']) > 0:
            point = sel['points'][0]
            if 'location' in point:
                return point['location']
    
    # Alternative structure
    if 'points' in selection_data and len(selection_data['points']) > 0:
        point = selection_data['points'][0]
        if 'location' in point:
            return point['location']
    
    return None
