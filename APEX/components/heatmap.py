"""
SOVEREIGN STRESS HEATMAP
Vertical ranking of all 25 countries by stress level

Features:
- Monochromatic scale matching Command Map
- Highlight effect for selected country
"""

import plotly.graph_objects as go
import numpy as np
from typing import Optional
from data.countries import get_global_watchlist
from scoring.apex_score import get_stress_ranked_countries, APEXResult

# ═══════════════════════════════════════════════════════════════════════════════
# HEATMAP COLOR SCALE (matches Command Map)
# ═══════════════════════════════════════════════════════════════════════════════

STRESS_COLORSCALE = [
    [0.0, '#002B36'],    # Low stress (high APEX) - Deep Blue
    [0.25, '#004855'],
    [0.5, '#006B7A'],
    [0.75, '#00A8BD'],
    [1.0, '#00E5FF'],    # High stress (low APEX) - Electric Cyan
]

def create_stress_heatmap(selected_country: Optional[str] = None) -> go.Figure:
    """
    Generate vertical heatmap of sovereign stress levels.
    Countries sorted by stress (lowest APEX score at top).
    
    Args:
        selected_country: ISO code of country to highlight
    
    Returns:
        Plotly Figure with annotated heatmap
    """
    # Get stress-ranked countries
    ranked = get_stress_ranked_countries()
    countries = get_global_watchlist()
    country_map = {c.code: c for c in countries}
    
    # Prepare data
    codes = [r.country_code for r in ranked]
    full_names = [r.country_name for r in ranked]
    apex_scores = [r.apex_score for r in ranked]
    tiers = [r.risk_tier for r in ranked]
    
    # Invert for stress (100 - APEX)
    stress_levels = [100 - s for s in apex_scores]
    
    # Create heatmap matrix (single column)
    z = [[s] for s in stress_levels]
    
    # Build hover text
    hover_texts = []
    for r in ranked:
        c = country_map[r.country_code]
        hover_texts.append([
            f"<b>{r.country_name}</b><br>"
            f"APEX: {r.apex_score:.1f}<br>"
            f"Tier: {r.risk_tier}<br>"
            f"Debt/GDP: {c.debt_to_gdp:.0f}%<br>"
            f"Inflation: {c.inflation_rate:.1f}%"
        ])
    
    # Create y-axis labels with highlight marker for selected country
    y_labels = []
    for code in codes:
        if selected_country and code == selected_country:
            y_labels.append(f"▶ {code}")  # Highlight marker
        else:
            y_labels.append(code)
    
    fig = go.Figure(data=go.Heatmap(
        z=z,
        y=y_labels,
        x=['STRESS'],
        colorscale=STRESS_COLORSCALE,
        showscale=True,
        hovertext=hover_texts,
        hovertemplate='%{hovertext}<extra></extra>',
        colorbar=dict(
            title=dict(
                text='STRESS<br>INDEX',
                font=dict(family='JetBrains Mono, SF Mono, monospace', size=10, color='#E0E0E0')
            ),
            tickfont=dict(family='JetBrains Mono, SF Mono, monospace', size=9, color='#6B7280'),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#1A1A2E',
            borderwidth=1,
            len=0.4,
            thickness=15,
        ),
    ))
    
    # Add APEX score annotations with highlight for selected
    for i, (code, score, tier, y_label) in enumerate(zip(codes, apex_scores, tiers, y_labels)):
        is_selected = selected_country and code == selected_country
        
        # Score text - use different style for selected country
        font_color = '#00E5FF' if is_selected else ('#000000' if score < 50 else '#E0E0E0')
        font_weight = 'bold' if is_selected else 'normal'
        
        fig.add_annotation(
            x=0,
            y=y_label,
            text=f"<b>{score:.0f}</b>" if is_selected else f"{score:.0f}",
            showarrow=False,
            font=dict(
                family='JetBrains Mono, SF Mono, monospace',
                size=12 if is_selected else 11,
                color=font_color
            ),
            xshift=0
        )
    
    # Define y-axis tick colors (highlight selected)
    tickcolors = []
    for code in codes:
        if selected_country and code == selected_country:
            tickcolors.append('#00E5FF')
        else:
            tickcolors.append('#E0E0E0')
    
    fig.update_layout(
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        title=dict(
            text='SOVEREIGN STRESS RANKING',
            font=dict(family='JetBrains Mono, SF Mono, monospace', size=14, color='#00E5FF'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            tickfont=dict(family='JetBrains Mono, SF Mono, monospace', size=10, color='#E0E0E0'),
            showgrid=False,
            zeroline=False,
            autorange='reversed',  # Highest stress at top
        ),
        margin=dict(l=60, r=80, t=50, b=20),
        height=650,
    )
    
    # Add highlight rectangle for selected country
    if selected_country and selected_country in codes:
        idx = codes.index(selected_country)
        y_label = y_labels[idx]
        
        fig.add_shape(
            type="rect",
            x0=-0.5,
            x1=0.5,
            y0=idx - 0.5,
            y1=idx + 0.5,
            line=dict(color="#00E5FF", width=2),
            fillcolor="rgba(0, 229, 255, 0.15)",
            layer="below"
        )
    
    return fig
