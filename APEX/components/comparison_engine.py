"""
COMPARISON ENGINE
Side-by-Side Radar Chart Analysis

Dual polar charts revealing structural weaknesses between sovereign pairs
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple
from data.countries import get_global_watchlist, Country, get_country_by_code
from scoring.apex_score import calculate_apex_score, APEXResult

# ═══════════════════════════════════════════════════════════════════════════════
# COMPARISON AXES
# ═══════════════════════════════════════════════════════════════════════════════

RADAR_CATEGORIES = [
    'SOLVENCY',
    'LIQUIDITY', 
    'STABILITY',
    'YIELD HEALTH',
    'APEX SCORE'
]

# Color palette
ICE_BLUE = '#00E5FF'
SHARP_RED = '#FF0033'
MUTED_BLUE = 'rgba(0, 229, 255, 0.3)'
MUTED_RED = 'rgba(255, 0, 51, 0.3)'

def _get_radar_values(country: Country, result: APEXResult) -> list:
    """Extract normalized values for radar chart axes."""
    return [
        result.solvency_score,
        result.liquidity_score,
        result.pressure_score,  # Stability (inverse pressure)
        max(0, 100 - abs(country.yield_spread) / 50),  # Yield Health
        result.apex_score
    ]

def create_comparison_radar(code1: str, code2: str) -> go.Figure:
    """
    Generate side-by-side radar charts comparing two sovereigns.
    
    Args:
        code1: ISO code for first country (displayed in Ice Blue)
        code2: ISO code for second country (displayed in Sharp Red)
        
    Returns:
        Plotly Figure with dual radar traces
    """
    # Get country data and scores
    c1 = get_country_by_code(code1)
    c2 = get_country_by_code(code2)
    r1 = calculate_apex_score(c1)
    r2 = calculate_apex_score(c2)
    
    # Get radar values
    values1 = _get_radar_values(c1, r1)
    values2 = _get_radar_values(c2, r2)
    
    # Close the polygon
    values1.append(values1[0])
    values2.append(values2[0])
    categories = RADAR_CATEGORIES + [RADAR_CATEGORIES[0]]
    
    fig = go.Figure()
    
    # Country 1 trace (Ice Blue)
    fig.add_trace(go.Scatterpolar(
        r=values1,
        theta=categories,
        fill='toself',
        fillcolor=MUTED_BLUE,
        line=dict(color=ICE_BLUE, width=2),
        name=f'{c1.name} ({c1.code})',
        hovertemplate=(
            f'<b>{c1.name}</b><br>'
            '%{theta}: %{r:.1f}<extra></extra>'
        )
    ))
    
    # Country 2 trace (Sharp Red)
    fig.add_trace(go.Scatterpolar(
        r=values2,
        theta=categories,
        fill='toself',
        fillcolor=MUTED_RED,
        line=dict(color=SHARP_RED, width=2),
        name=f'{c2.name} ({c2.code})',
        hovertemplate=(
            f'<b>{c2.name}</b><br>'
            '%{theta}: %{r:.1f}<extra></extra>'
        )
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#000000',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(family='JetBrains Mono, SF Mono, monospace', size=9, color='#6B7280'),
                gridcolor='#1A1A2E',
                linecolor='#1A1A2E',
            ),
            angularaxis=dict(
                tickfont=dict(family='JetBrains Mono, SF Mono, monospace', size=10, color='#E0E0E0'),
                gridcolor='#1A1A2E',
                linecolor='#1A1A2E',
            )
        ),
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        showlegend=True,
        legend=dict(
            font=dict(family='JetBrains Mono, SF Mono, monospace', size=11, color='#E0E0E0'),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#1A1A2E',
            borderwidth=1,
            x=0.5,
            y=-0.15,
            xanchor='center',
            orientation='h'
        ),
        title=dict(
            text='COMPARISON ENGINE // STRUCTURAL ANALYSIS',
            font=dict(family='JetBrains Mono, SF Mono, monospace', size=14, color='#00E5FF'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(l=60, r=60, t=60, b=80),
        height=400,
    )
    
    return fig

def get_comparison_summary(code1: str, code2: str) -> dict:
    """
    Generate textual comparison summary between two countries.
    """
    c1 = get_country_by_code(code1)
    c2 = get_country_by_code(code2)
    r1 = calculate_apex_score(c1)
    r2 = calculate_apex_score(c2)
    
    # Determine relative strengths
    stronger = c1.name if r1.apex_score > r2.apex_score else c2.name
    weaker = c2.name if r1.apex_score > r2.apex_score else c1.name
    delta = abs(r1.apex_score - r2.apex_score)
    
    return {
        'country_1': {
            'name': c1.name,
            'code': c1.code,
            'apex': r1.apex_score,
            'tier': r1.risk_tier,
            'category': c1.category
        },
        'country_2': {
            'name': c2.name,
            'code': c2.code,
            'apex': r2.apex_score,
            'tier': r2.risk_tier,
            'category': c2.category
        },
        'stronger': stronger,
        'weaker': weaker,
        'apex_delta': round(delta, 2)
    }
