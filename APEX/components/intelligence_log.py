"""
INTELLIGENCE LOG
Auto-updating sidebar with system messages

Simulates real-time intelligence updates
"""

import random
from datetime import datetime
from typing import List
from data.countries import get_global_watchlist

# ═══════════════════════════════════════════════════════════════════════════════
# LOG MESSAGE TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════════

ROUTINE_MESSAGES = [
    "APEX Score synchronized with World Bank & IMF parameters... OK",
    "Global watchlist updated: 25 sovereigns active",
    "FX volatility scan complete... NOMINAL",
    "Bond yield data refreshed from Bloomberg API... OK",
    "Inflation metrics synchronized... OK",
    "Credit default swap spreads updated... OK",
    "Sovereign rating crosscheck complete... OK",
    "Debt sustainability analysis running... OK",
]

COUNTRY_SCAN_MESSAGES = [
    "Recalculating default probability for {code}... OK",
    "Scanning FX volatility spreads for {code}... {status}",
    "Analyzing yield curve inversion for {code}... {status}",
    "Debt rollover risk assessment for {code}... {status}",
    "External financing gap calculated for {code}... OK",
    "Current account deficit monitored for {code}... {status}",
]

ALERT_MESSAGES = [
    "ALERT: {code} yield spread exceeds 2000bps threshold",
    "ALERT: {code} inflation rate critical (>100%)",
    "ALERT: {code} FX reserves below 3-month import cover",
    "WARNING: {code} APEX score declined 5pts in 24h",
    "ALERT: {code} sovereign CDS spread widening detected",
]

HIGH_RISK_CODES = ['LBN', 'ARG', 'VEN', 'GHA', 'EGY', 'TUR', 'PAK']
STABLE_CODES = ['USA', 'DEU', 'JPN', 'GBR', 'FRA', 'CAN']

def _get_timestamp() -> str:
    """Generate formatted timestamp."""
    return datetime.now().strftime("%H:%M:%S")

def generate_log_messages(count: int = 8) -> List[str]:
    """
    Generate a list of simulated intelligence log messages.
    
    Args:
        count: Number of messages to generate
        
    Returns:
        List of formatted log strings
    """
    messages = []
    countries = get_global_watchlist()
    all_codes = [c.code for c in countries]
    
    for _ in range(count):
        roll = random.random()
        
        if roll < 0.4:
            # Routine message
            msg = random.choice(ROUTINE_MESSAGES)
            messages.append(f"[{_get_timestamp()}] > {msg}")
            
        elif roll < 0.75:
            # Country-specific scan
            code = random.choice(all_codes)
            status = "ALERT" if code in HIGH_RISK_CODES and random.random() < 0.3 else "NOMINAL"
            template = random.choice(COUNTRY_SCAN_MESSAGES)
            msg = template.format(code=code, status=status)
            messages.append(f"[{_get_timestamp()}] > {msg}")
            
        else:
            # Alert message (only for high-risk countries)
            code = random.choice(HIGH_RISK_CODES)
            template = random.choice(ALERT_MESSAGES)
            msg = template.format(code=code)
            messages.append(f"[{_get_timestamp()}] >> {msg}")
    
    return messages

def get_boot_sequence() -> List[str]:
    """
    Generate startup boot sequence messages.
    """
    return [
        f"[{_get_timestamp()}] RISK_INTELLIGENCE // APEX v2.1.0",
        f"[{_get_timestamp()}] ═══════════════════════════════════════",
        f"[{_get_timestamp()}] > Initializing sovereign risk engine...",
        f"[{_get_timestamp()}] > Loading Global Watchlist (25 entities)... OK",
        f"[{_get_timestamp()}] > APEX scoring algorithm online... OK",
        f"[{_get_timestamp()}] > World Bank API connection... ESTABLISHED",
        f"[{_get_timestamp()}] > IMF WEO data synchronized... OK",
        f"[{_get_timestamp()}] > Bloomberg terminal link... ACTIVE",
        f"[{_get_timestamp()}] ═══════════════════════════════════════",
        f"[{_get_timestamp()}] SYSTEM STATUS: OPERATIONAL",
    ]
