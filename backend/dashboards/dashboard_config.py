#!/usr/bin/env python3
"""
Configuration file for dashboard settings
"""

import os

# Google Maps API Key
# Replace with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyACApQn1JG2iuLby7b5rMvkLaho383a42s")

# Default map center coordinates for Kenya
DEFAULT_MAP_CENTER = [-0.0236, 37.9062]

# Default zoom level for country-wide view
DEFAULT_ZOOM_LEVEL = 7