"""
APEX SCORE ENGINE v2.0
Proprietary Sovereign Risk Scoring Algorithm

APEX = w₁ × Solvency + w₂ × Liquidity + w₃ × Pressure

Scoring Philosophy:
- Lower APEX = Higher Risk (critical sovereigns approach 0)
- Higher APEX = Fortress Status (stable sovereigns approach 100)

Features:
- Z-Score statistical normalization for comparability
- Letter grading (AAA to D)
- Global average calculations
- Simulation mode support
- AI-style insight generation
"""

import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from data.countries import Country, get_global_watchlist

# ═══════════════════════════════════════════════════════════════════════════════
# DATA FRESHNESS TIMESTAMP
# ═══════════════════════════════════════════════════════════════════════════════

DATA_LAST_UPDATED = datetime(2026, 1, 30, 12, 0, 0)  # Jan 30, 2026 12:00 UTC

def get_data_freshness() -> str:
    """Return formatted data freshness timestamp."""
    return DATA_LAST_UPDATED.strftime("%Y-%m-%d %H:%M UTC")

# ═══════════════════════════════════════════════════════════════════════════════
# EDUCATIONAL TOOLTIPS (Glossary)
# ═══════════════════════════════════════════════════════════════════════════════

TOOLTIPS = {
    'apex_score': "A composite stress index (0-100) aggregating solvency, liquidity, and political stability to estimate the probability of a sovereign credit event.",
    'solvency': "The long-term ability of a state to meet its debt obligations, primarily measured by the Debt-to-GDP ratio. Lower debt ratios indicate stronger solvency.",
    'liquidity': "The availability of immediate foreign currency reserves to cover imports and short-term debt servicing. Measured in months of import coverage.",
    'pressure': "Combined market stress from inflation and bond yield spreads. Higher inflation and wider spreads indicate greater fiscal pressure.",
    'debt_to_gdp': "Total government debt as a percentage of GDP. A key indicator of fiscal sustainability. Levels above 100% are considered elevated.",
    'fx_reserves': "Foreign exchange reserves measured in months of import coverage. The IMF recommends a minimum of 3 months coverage.",
    'inflation': "Year-over-year change in consumer prices. High inflation erodes purchasing power and can signal monetary instability.",
    'yield_spread': "The difference between a country's 10-year bond yield and the US Treasury benchmark. Wider spreads indicate higher perceived risk.",
    'yield_10y': "The yield on 10-year government bonds. Higher yields generally indicate higher perceived credit risk or inflation expectations.",
    'z_score': "A statistical measure indicating how many standard deviations a value is from the mean. Used for metric comparability."
}

# ═══════════════════════════════════════════════════════════════════════════════
# APEX CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

WEIGHTS = {
    'solvency': 0.35,
    'liquidity': 0.30,
    'pressure': 0.35
}

BOUNDS = {
    'debt_to_gdp': (0, 350),
    'fx_reserves': (0, 24),
    'inflation': (0, 220),
    'yield_spread': (-500, 5500)
}

# ═══════════════════════════════════════════════════════════════════════════════
# Z-SCORE STATISTICAL NORMALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_global_statistics() -> Dict[str, Dict[str, float]]:
    """Calculate mean and std for all metrics across the global watchlist."""
    watchlist = get_global_watchlist()
    
    debt_values = [c.debt_to_gdp for c in watchlist]
    fx_values = [c.fx_reserves_months for c in watchlist]
    inflation_values = [c.inflation_rate for c in watchlist]
    pressure_values = [c.inflation_rate + abs(c.yield_spread) / 100 for c in watchlist]
    
    return {
        'debt_to_gdp': {'mean': np.mean(debt_values), 'std': max(np.std(debt_values), 1)},
        'fx_reserves': {'mean': np.mean(fx_values), 'std': max(np.std(fx_values), 1)},
        'inflation': {'mean': np.mean(inflation_values), 'std': max(np.std(inflation_values), 1)},
        'pressure': {'mean': np.mean(pressure_values), 'std': max(np.std(pressure_values), 1)}
    }

def z_score_normalize(value: float, mean: float, std: float, invert: bool = False) -> float:
    """Z-Score normalization with sigmoid transformation to [0, 100]."""
    z = (value - mean) / std
    if invert:
        z = -z
    normalized = 100 / (1 + np.exp(-z * 0.5))
    return float(np.clip(normalized, 0, 100))

def get_z_score(value: float, mean: float, std: float) -> float:
    """Calculate raw Z-Score for display purposes."""
    return (value - mean) / std

# ═══════════════════════════════════════════════════════════════════════════════
# LETTER GRADING SCALE
# ═══════════════════════════════════════════════════════════════════════════════

def get_letter_grade(score: float) -> str:
    """Convert APEX score to letter grade (AAA to D)."""
    if score >= 90: return "AAA"
    elif score >= 80: return "AA"
    elif score >= 70: return "A"
    elif score >= 60: return "BBB"
    elif score >= 50: return "BB"
    elif score >= 40: return "B"
    elif score >= 30: return "CCC"
    elif score >= 20: return "CC"
    elif score >= 10: return "C"
    else: return "D"

@dataclass
class APEXResult:
    """APEX scoring result for a sovereign entity."""
    country_code: str
    country_name: str
    apex_score: float
    solvency_score: float
    liquidity_score: float
    pressure_score: float
    risk_tier: str
    letter_grade: str = ""
    z_scores: Optional[Dict[str, float]] = None
    
    def __post_init__(self):
        if not self.letter_grade:
            self.letter_grade = get_letter_grade(self.apex_score)

def normalize(value: float, min_val: float, max_val: float, invert: bool = False) -> float:
    """Min-max normalization to [0, 100] scale."""
    clamped = max(min_val, min(max_val, value))
    normalized = (clamped - min_val) / (max_val - min_val) * 100
    return 100 - normalized if invert else normalized

def get_risk_tier(score: float) -> str:
    """Classify APEX score into risk tier."""
    if score >= 90: return "FORTRESS"
    elif score >= 70: return "STABLE"
    elif score >= 50: return "ELEVATED"
    elif score >= 30: return "HIGH RISK"
    else: return "CRITICAL"

def calculate_apex_score(
    country: Country,
    use_zscore: bool = True,
    override_debt: Optional[float] = None,
    override_inflation: Optional[float] = None
) -> APEXResult:
    """Calculate the proprietary APEX sovereign risk score."""
    debt_value = override_debt if override_debt is not None else country.debt_to_gdp
    inflation_value = override_inflation if override_inflation is not None else country.inflation_rate
    
    if use_zscore:
        stats = calculate_global_statistics()
        
        solvency = z_score_normalize(debt_value, stats['debt_to_gdp']['mean'], stats['debt_to_gdp']['std'], invert=True)
        liquidity = z_score_normalize(country.fx_reserves_months, stats['fx_reserves']['mean'], stats['fx_reserves']['std'], invert=False)
        
        pressure_raw = inflation_value + abs(country.yield_spread) / 100
        pressure = z_score_normalize(pressure_raw, stats['pressure']['mean'], stats['pressure']['std'], invert=True)
        
        z_scores = {
            'debt': round(get_z_score(debt_value, stats['debt_to_gdp']['mean'], stats['debt_to_gdp']['std']), 2),
            'liquidity': round(get_z_score(country.fx_reserves_months, stats['fx_reserves']['mean'], stats['fx_reserves']['std']), 2),
            'pressure': round(get_z_score(pressure_raw, stats['pressure']['mean'], stats['pressure']['std']), 2)
        }
    else:
        solvency = normalize(debt_value, BOUNDS['debt_to_gdp'][0], BOUNDS['debt_to_gdp'][1], invert=True)
        liquidity = normalize(country.fx_reserves_months, BOUNDS['fx_reserves'][0], BOUNDS['fx_reserves'][1], invert=False)
        pressure_raw = inflation_value + abs(country.yield_spread) / 100
        pressure = normalize(pressure_raw, 0, 250, invert=True)
        z_scores = None
    
    apex = WEIGHTS['solvency'] * solvency + WEIGHTS['liquidity'] * liquidity + WEIGHTS['pressure'] * pressure
    
    return APEXResult(
        country_code=country.code,
        country_name=country.name,
        apex_score=round(apex, 2),
        solvency_score=round(solvency, 2),
        liquidity_score=round(liquidity, 2),
        pressure_score=round(pressure, 2),
        risk_tier=get_risk_tier(apex),
        letter_grade=get_letter_grade(apex),
        z_scores=z_scores
    )

def simulate_apex_score(country_code: str, debt_to_gdp: Optional[float] = None, inflation_rate: Optional[float] = None) -> APEXResult:
    """Simulation mode: Calculate APEX with custom parameter overrides."""
    from data.countries import get_country_by_code
    country = get_country_by_code(country_code)
    return calculate_apex_score(country, use_zscore=True, override_debt=debt_to_gdp, override_inflation=inflation_rate)

def calculate_all_scores() -> List[APEXResult]:
    """Calculate APEX scores for entire Global Watchlist."""
    watchlist = get_global_watchlist()
    return [calculate_apex_score(c) for c in watchlist]

def get_ranked_countries() -> List[APEXResult]:
    """Return countries ranked by APEX score (highest first)."""
    return sorted(calculate_all_scores(), key=lambda x: x.apex_score, reverse=True)

def get_stress_ranked_countries() -> List[APEXResult]:
    """Return countries ranked by sovereign stress (lowest APEX first)."""
    return sorted(calculate_all_scores(), key=lambda x: x.apex_score)

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL AVERAGES
# ═══════════════════════════════════════════════════════════════════════════════

def get_global_averages() -> Dict[str, float]:
    """Calculate global average values for all key metrics."""
    watchlist = get_global_watchlist()
    scores = calculate_all_scores()
    
    return {
        'apex_score': round(np.mean([s.apex_score for s in scores]), 2),
        'solvency': round(np.mean([s.solvency_score for s in scores]), 2),
        'liquidity': round(np.mean([s.liquidity_score for s in scores]), 2),
        'pressure': round(np.mean([s.pressure_score for s in scores]), 2),
        'debt_to_gdp': round(np.mean([c.debt_to_gdp for c in watchlist]), 2),
        'fx_reserves': round(np.mean([c.fx_reserves_months for c in watchlist]), 2),
        'inflation': round(np.mean([c.inflation_rate for c in watchlist]), 2),
        'yield_10y': round(np.mean([c.yield_10y for c in watchlist]), 2),
        'Solvency': round(np.mean([s.solvency_score for s in scores]), 2),
        'Liquidity': round(np.mean([s.liquidity_score for s in scores]), 2),
        'Stability': round(np.mean([s.pressure_score for s in scores]), 2),
        'Yield Health': round(np.mean([max(0, 100 - abs(c.yield_spread) / 50) for c in watchlist]), 2),
        'Inflation': round(100 - np.mean([c.inflation_rate for c in watchlist]) / 2.5, 2),
        'APEX SCORE': round(np.mean([s.apex_score for s in scores]), 2),
    }

# ═══════════════════════════════════════════════════════════════════════════════
# AI-STYLE INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_insight(country_code: str) -> Dict[str, str]:
    """Generate AI-style analytical insight for a country."""
    from data.countries import get_country_by_code
    
    country = get_country_by_code(country_code)
    result = calculate_apex_score(country)
    averages = get_global_averages()
    
    risk_factors = {
        'Solvency (Debt/GDP)': (result.solvency_score, averages['solvency']),
        'Liquidity (FX Reserves)': (result.liquidity_score, averages['liquidity']),
        'Market Pressure': (result.pressure_score, averages['pressure'])
    }
    
    primary_risk, max_deviation = None, 0
    for factor, (score, avg) in risk_factors.items():
        deviation = avg - score
        if deviation > max_deviation:
            max_deviation, primary_risk = deviation, factor
    
    if primary_risk is None or max_deviation < 5:
        weakest = min(risk_factors.items(), key=lambda x: x[1][0])
        primary_risk = weakest[0]
    
    grade_desc = {
        'AAA': 'top-tier investment grade', 'AA': 'high investment grade',
        'A': 'upper-medium investment grade', 'BBB': 'medium investment grade',
        'BB': 'speculative grade', 'B': 'highly speculative',
        'CCC': 'substantial risk', 'CC': 'extremely speculative',
        'C': 'near-default', 'D': 'default imminent'
    }
    
    if result.apex_score >= 70: tone = "demonstrates robust fundamentals"
    elif result.apex_score >= 50: tone = "exhibits moderate vulnerability"
    elif result.apex_score >= 30: tone = "shows significant stress indicators"
    else: tone = "faces severe sovereign distress"
    
    summary = f"{result.country_name} ({result.letter_grade}) {tone}. Primary risk factor is {primary_risk} which deviates {round(abs(max_deviation), 1)}% from the global mean."
    
    if result.apex_score >= 70: recommendation = "LOW RISK: Suitable for sovereign bond allocation."
    elif result.apex_score >= 50: recommendation = "MODERATE RISK: Monitor key indicators closely."
    elif result.apex_score >= 30: recommendation = "HIGH RISK: Consider hedging or reduced exposure."
    else: recommendation = "CRITICAL: Avoid new exposure. Evaluate exit strategy."
    
    return {
        'summary': summary, 'primary_risk': primary_risk, 'deviation': round(abs(max_deviation), 1),
        'grade': result.letter_grade, 'grade_description': grade_desc.get(result.letter_grade, 'undefined'),
        'recommendation': recommendation, 'apex_score': result.apex_score, 'risk_tier': result.risk_tier
    }
