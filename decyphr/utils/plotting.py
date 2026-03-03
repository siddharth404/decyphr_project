
import plotly.graph_objects as go
from typing import Optional, Dict, Any

# --- ANTIGRAVITY THEME DEFINITIONS ---
THEME_COLORS = {
    "background": "#FFFFFF",
    "text": "#121317",
    "secondary_text": "#5F6368",
    "grid": "#F1F3F4",
    "primary_accent": "#1a73e8",    # Google Blue
    "secondary_accent": "#AECBFA",  # Light Blue
    "tertiary_accent": "#E8F0FE",   # Very Light Blue
    "success": "#137333",
    "warning": "#EA8600",
    "error": "#C5221F"
}

ANTIGRAVITY_FONT = "Outfit, sans-serif"

def apply_antigravity_theme(fig: go.Figure, height: int = 350) -> go.Figure:
    """
    Applies the standardized Decyphr Antigravity aesthetic to a Plotly figure.
    
    Features:
    - Transparent backgrounds (paper and plot)
    - 'Outfit' font family
    - Minimalist grid lines
    - No surrounding legends/clutter by default (can be overridden)
    """
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family=ANTIGRAVITY_FONT,
            size=12,
            color=THEME_COLORS['text']
        ),
        margin=dict(l=0, r=0, t=30, b=20),
        height=height,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family=ANTIGRAVITY_FONT
        ),
        # Minimalist Axis
        xaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor=THEME_COLORS['grid'],
            tickfont=dict(color=THEME_COLORS['secondary_text'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=THEME_COLORS['grid'],
            showline=False,
            zeroline=False,
            tickfont=dict(color=THEME_COLORS['secondary_text'])
        )
    )
    return fig

def get_theme_colors() -> Dict[str, str]:
    """Returns the dictionary of theme colors for use in specific plot traces."""
    return THEME_COLORS
