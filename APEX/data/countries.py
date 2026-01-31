"""
RISK_INTELLIGENCE // APEX
Global Watchlist - 25 Sovereign Entities

Categories:
- G7: Major advanced economies
- BRICS: Emerging market powers  
- Frontier High-Risk: Elevated sovereign stress profiles
"""

from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class Country:
    """Sovereign entity data model."""
    code: str           # ISO 3-letter code
    name: str
    category: str       # G7, BRICS, FRONTIER
    debt_to_gdp: float  # Solvency metric (%)
    fx_reserves_months: float  # Liquidity - months of import cover
    inflation_rate: float  # CPI YoY (%)
    yield_10y: float    # 10Y govt bond yield (%)
    yield_spread: float  # Spread vs US 10Y (bps)

# US 10Y Treasury baseline (for spread calculation)
US_10Y_YIELD = 4.25

def get_global_watchlist() -> List[Country]:
    """
    Returns the Global Watchlist of 25 sovereign entities.
    Data approximates Q4 2025 / Q1 2026 conditions.
    """
    return [
        # ═══════════════════════════════════════════════════════════════
        # G7 - FORTRESS ECONOMIES
        # ═══════════════════════════════════════════════════════════════
        Country("USA", "United States", "G7", 122.0, 3.2, 3.1, 4.25, 0),
        Country("JPN", "Japan", "G7", 263.0, 18.5, 2.8, 1.05, -320),
        Country("DEU", "Germany", "G7", 66.0, 2.8, 2.4, 2.35, -190),
        Country("GBR", "United Kingdom", "G7", 101.0, 3.1, 4.0, 4.15, -10),
        Country("FRA", "France", "G7", 112.0, 2.5, 2.6, 3.05, -120),
        Country("ITA", "Italy", "G7", 140.0, 2.9, 1.8, 3.85, -40),
        Country("CAN", "Canada", "G7", 107.0, 2.4, 2.9, 3.25, -100),
        
        # ═══════════════════════════════════════════════════════════════
        # BRICS - EMERGING POWERS
        # ═══════════════════════════════════════════════════════════════
        Country("BRA", "Brazil", "BRICS", 88.0, 14.2, 4.5, 12.80, 855),
        Country("RUS", "Russia", "BRICS", 20.0, 24.0, 8.5, 16.50, 1225),
        Country("IND", "India", "BRICS", 83.0, 10.8, 5.2, 7.15, 290),
        Country("CHN", "China", "BRICS", 77.0, 16.5, 0.3, 2.65, -160),
        Country("ZAF", "South Africa", "BRICS", 73.0, 5.8, 5.8, 10.25, 600),
        
        # ═══════════════════════════════════════════════════════════════
        # FRONTIER - HIGH RISK SOVEREIGNS
        # ═══════════════════════════════════════════════════════════════
        Country("LBN", "Lebanon", "FRONTIER", 180.0, 0.8, 210.0, 45.00, 4075),
        Country("ARG", "Argentina", "FRONTIER", 89.0, 2.1, 140.0, 38.50, 3425),
        Country("EGY", "Egypt", "FRONTIER", 92.0, 4.5, 28.5, 27.80, 2355),
        Country("TUR", "Turkey", "FRONTIER", 35.0, 4.2, 48.5, 28.50, 2425),
        Country("PAK", "Pakistan", "FRONTIER", 78.0, 2.8, 24.5, 18.75, 1450),
        Country("NGA", "Nigeria", "FRONTIER", 38.0, 5.1, 28.8, 18.50, 1425),
        Country("GHA", "Ghana", "FRONTIER", 88.0, 2.2, 22.5, 28.00, 2375),
        Country("LKA", "Sri Lanka", "FRONTIER", 115.0, 3.5, 8.5, 24.50, 2025),
        Country("UKR", "Ukraine", "FRONTIER", 85.0, 4.8, 12.5, 19.50, 1525),
        Country("VEN", "Venezuela", "FRONTIER", 350.0, 0.5, 185.0, 55.00, 5075),
        Country("KEN", "Kenya", "FRONTIER", 68.0, 4.1, 6.8, 16.25, 1200),
        Country("TUN", "Tunisia", "FRONTIER", 82.0, 3.2, 9.2, 14.50, 1025),
        Country("SLV", "El Salvador", "FRONTIER", 85.0, 2.8, 1.5, 12.80, 855),
    ]

def get_country_by_code(code: str) -> Country:
    """Retrieve a country by its ISO code."""
    for country in get_global_watchlist():
        if country.code == code:
            return country
    raise ValueError(f"Country code {code} not found in watchlist")

def get_countries_by_category(category: str) -> List[Country]:
    """Filter countries by category."""
    return [c for c in get_global_watchlist() if c.category == category]
