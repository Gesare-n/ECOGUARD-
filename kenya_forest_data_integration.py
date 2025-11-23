#!/usr/bin/env python3
"""
Acoustic Guardian - Kenya Forest Data Integration

This script demonstrates how to integrate publicly available Kenyan forest datasets
into the Acoustic Guardian Digital Twin system to enhance visualization and analytics.
"""

import pandas as pd
import geopandas as gpd
import json
import requests
from datetime import datetime
import os

# Data sources for Kenyan forests
DATA_SOURCES = {
    "gazetted_forests": {
        "name": "Kenya Gazetted Forest Dataset",
        "url": "https://opendata.rcmrd.org/datasets/kenya-gazetted-forest-dataset/about",
        "type": "GIS Shapefile",
        "use_case": "Base map layers for Grafana Digital Twin"
    },
    "global_forest_watch": {
        "name": "Global Forest Watch Kenya",
        "url": "https://www.globalforestwatch.org/dashboards/country/KEN/",
        "type": "Deforestation alerts and historical data",
        "use_case": "High-risk logging model and validation context"
    },
    "openafrica_forests": {
        "name": "openAFRICA Kenyan Forestry Datasets",
        "url": "https://open.africa/dataset/kenyan-forests-datasets",
        "type": "Historical tree cover data",
        "use_case": "Baseline for impact measurement"
    },
    "icpac_forests": {
        "name": "ICPAC Geoportal - Kenya Forests",
        "url": "https://geoportal.icpac.net/layers/data0:geonode:ken_forests",
        "type": "Forest coverage data",
        "use_case": "General forest extent visualization"
    },
    "biodiversity_data": {
        "name": "Kenya Biodiversity Data",
        "url": "https://rcoe-geoportal.rcmrd.org/datasets/kenya-biodiversity-data",
        "type": "Geospatial biodiversity data",
        "use_case": "Protected areas and wildlife monitoring"
    },
    "wri_gis_data": {
        "name": "WRI Kenya GIS Data",
        "url": "https://www.wri.org/data/kenya-gis-data",
        "type": "Comprehensive GIS data",
        "use_case": "Strategic layers for risk modeling"
    }
}

def download_sample_data():
    """
    Download sample data from public sources (this is a demonstration function)
    In a real implementation, you would download the actual datasets
    """
    print("Downloading sample Kenya forest data...")
    
    # Sample forest locations in Kenya with real coordinates
    kenya_forests = [
        {"name": "Karura Forest", "lat": -1.2723, "lng": 36.8080, "area_km2": 17.5, "type": "Urban Forest"},
        {"name": "Uhuru Park", "lat": -1.3037, "lng": 36.8166, "area_km2": 0.6, "type": "Urban Park"},
        {"name": "Ngong Forest", "lat": -1.3500, "lng": 36.7000, "area_km2": 20.0, "type": "Indigenous Forest"},
        {"name": "Aberdare Forest", "lat": -0.4500, "lng": 36.5000, "area_km2": 200.0, "type": "Mountain Forest"},
        {"name": "Mt. Kenya Forest", "lat": -0.2500, "lng": 37.7500, "area_km2": 150.0, "type": "Mountain Forest"},
        {"name": "Arboretum Forest", "lat": -0.5300, "lng": 36.5300, "area_km2": 5.0, "type": "Indigenous Forest"},
        {"name": "Kakamega Forest", "lat": 0.3000, "lng": 34.7500, "area_km2": 70.0, "type": "Indigenous Forest"},
        {"name": "Mau Forest", "lat": -0.5000, "lng": 35.5000, "area_km2": 400.0, "type": "Indigenous Forest"},
        {"name": "Chyulu Hills Forest", "lat": -2.5000, "lng": 38.0000, "area_km2": 150.0, "type": "Indigenous Forest"},
        {"name": "Taita Hills Forest", "lat": -3.5000, "lng": 38.5000, "area_km2": 25.0, "type": "Indigenous Forest"}
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(kenya_forests)
    
    # Save as CSV for easy integration
    df.to_csv("kenya_forest_locations.csv", index=False)
    print("Sample Kenya forest data saved to kenya_forest_locations.csv")
    
    return df

def create_grafana_forest_layer():
    """
    Create a Grafana-compatible JSON for forest boundary layers
    This would be used to enhance the Grafana dashboard with actual forest boundaries
    """
    print("Creating Grafana forest layer...")
    
    # Sample GeoJSON structure for forest boundaries
    forest_layer = {
        "dashboard": {
            "id": None,
            "title": "Kenya Forest Boundaries",
            "tags": ["kenya-forests", "boundaries"],
            "timezone": "browser",
            "schemaVersion": 16,
            "version": 0,
            "panels": [
                {
                    "id": 100,
                    "type": "geomap",
                    "title": "Kenya Gazetted Forests",
                    "gridPos": {
                        "x": 0,
                        "y": 18,
                        "w": 24,
                        "h": 12
                    },
                    "options": {
                        "basemap": {
                            "name": "OpenStreetMap",
                            "type": "osm-standard"
                        },
                        "controls": {
                            "mouseWheelZoom": True,
                            "showAttribution": True,
                            "showZoom": True
                        },
                        "layers": [
                            {
                                "config": {
                                    "style": {
                                        "color": {
                                            "fixed": "dark-green"
                                        },
                                        "opacity": 0.6,
                                        "size": {
                                            "fixed": 5
                                        }
                                    }
                                },
                                "name": "Gazetted Forests",
                                "type": "markers"
                            }
                        ]
                    }
                }
            ]
        }
    }
    
    # Save the layer configuration
    with open("kenya_forest_layer.json", "w") as f:
        json.dump(forest_layer, f, indent=2)
    
    print("Grafana forest layer saved to kenya_forest_layer.json")
    return forest_layer

def create_deforestation_risk_model():
    """
    Create a sample deforestation risk model based on historical data
    This would be used to identify high-risk areas for sensor deployment
    """
    print("Creating deforestation risk model...")
    
    # Sample risk factors for different forest areas
    risk_factors = [
        {"forest": "Karura Forest", "urban_proximity": 0.9, "accessibility": 0.8, "historical_loss": 0.3, "risk_score": 0.67},
        {"forest": "Uhuru Park", "urban_proximity": 1.0, "accessibility": 1.0, "historical_loss": 0.8, "risk_score": 0.93},
        {"forest": "Ngong Forest", "urban_proximity": 0.7, "accessibility": 0.7, "historical_loss": 0.5, "risk_score": 0.63},
        {"forest": "Aberdare Forest", "urban_proximity": 0.2, "accessibility": 0.4, "historical_loss": 0.2, "risk_score": 0.27},
        {"forest": "Mt. Kenya Forest", "urban_proximity": 0.3, "accessibility": 0.5, "historical_loss": 0.1, "risk_score": 0.30},
        {"forest": "Kakamega Forest", "urban_proximity": 0.4, "accessibility": 0.6, "historical_loss": 0.6, "risk_score": 0.53}
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(risk_factors)
    
    # Save as CSV
    df.to_csv("deforestation_risk_model.csv", index=False)
    print("Deforestation risk model saved to deforestation_risk_model.csv")
    
    return df

def update_grafana_dashboard_with_layers():
    """
    Update the existing Grafana dashboard with new layers for Kenyan forests
    """
    print("Updating Grafana dashboard with Kenya forest layers...")
    
    # Read the existing dashboard
    try:
        with open("grafana_dashboard.json", "r") as f:
            dashboard = json.load(f)
    except FileNotFoundError:
        print("Error: grafana_dashboard.json not found")
        return
    
    # Add forest boundary layer
    forest_boundary_panel = {
        "id": 6,
        "type": "geomap",
        "title": "Kenya Gazetted Forest Boundaries",
        "gridPos": {
            "x": 0,
            "y": 18,
            "w": 12,
            "h": 9
        },
        "options": {
            "basemap": {
                "name": "OpenStreetMap",
                "type": "osm-standard"
            },
            "controls": {
                "mouseWheelZoom": True,
                "showAttribution": True,
                "showZoom": True
            },
            "layers": [
                {
                    "config": {
                        "style": {
                            "color": {
                                "fixed": "dark-green"
                            },
                            "opacity": 0.6,
                            "size": {
                                "fixed": 5
                            }
                        }
                    },
                    "name": "Gazetted Forests",
                    "type": "markers"
                }
            ]
        }
    }
    
    # Add deforestation risk layer
    risk_layer_panel = {
        "id": 7,
        "type": "geomap",
        "title": "Deforestation Risk Zones",
        "gridPos": {
            "x": 12,
            "y": 18,
            "w": 12,
            "h": 9
        },
        "options": {
            "basemap": {
                "name": "OpenStreetMap",
                "type": "osm-standard"
            },
            "controls": {
                "mouseWheelZoom": True,
                "showAttribution": True,
                "showZoom": True
            },
            "layers": [
                {
                    "config": {
                        "style": {
                            "color": {
                                "fixed": "dark-orange"
                            },
                            "opacity": 0.4,
                            "size": {
                                "fixed": 5
                            }
                        }
                    },
                    "name": "High-Risk Areas",
                    "type": "markers"
                }
            ]
        }
    }
    
    # Add the new panels to the dashboard
    dashboard["dashboard"]["panels"].extend([forest_boundary_panel, risk_layer_panel])
    
    # Save the updated dashboard
    with open("grafana_dashboard_enhanced.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    print("Enhanced Grafana dashboard saved to grafana_dashboard_enhanced.json")

def generate_influxdb_line_protocol_examples():
    """
    Generate example InfluxDB Line Protocol entries for the new Kenya forest data
    """
    print("Generating InfluxDB Line Protocol examples...")
    
    examples = [
        # Example 1: Forest boundary data
        'forest_boundaries,forest_name="Karura Forest",forest_type="Urban Forest" area_km2=17.5,lat=-1.2723,lng=36.8080 1634567890',
        
        # Example 2: Deforestation risk data
        'deforestation_risk,forest_name="Karura Forest" risk_score=0.67,urban_proximity=0.9,accessibility=0.8,historical_loss=0.3 1634567890',
        
        # Example 3: Biodiversity data
        'biodiversity,forest_name="Kakamega Forest",species_type="Bird" species_count=200,conservation_status="High" 1634567890',
        
        # Example 4: Sensor deployment recommendation
        'sensor_deployment,forest_name="Uhuru Park" priority=9,reason="High risk urban area",recommended_sensors=3 1634567890'
    ]
    
    # Save examples to file
    with open("influxdb_line_protocol_examples.txt", "w") as f:
        f.write("# InfluxDB Line Protocol Examples for Kenya Forest Data\n\n")
        for example in examples:
            f.write(f"{example}\n")
    
    print("InfluxDB Line Protocol examples saved to influxdb_line_protocol_examples.txt")
    return examples

def create_sample_nursery_inventory():
    """
    Create a sample nursery inventory JSON file for reforestation tracking
    """
    print("Creating sample nursery inventory...")
    
    nursery_inventory = {
        "metadata": {
            "created_date": datetime.now().isoformat(),
            "location": "Kenya Forest Service Nursery Network",
            "total_nurseries": 5
        },
        "nurseries": [
            {
                "id": "NUR-001",
                "name": "Karura Forest Nursery",
                "location": "Karura Forest, Nairobi",
                "coordinates": {"lat": -1.2723, "lng": 36.8080},
                "species": [
                    {
                        "name": "Markhamia lutea",
                        "count": 500,
                        "stage": "Ready for planting",
                        "last_updated": "2024-01-15"
                    },
                    {
                        "name": "Croton megalocarpus",
                        "count": 300,
                        "stage": "Growing",
                        "last_updated": "2024-01-15"
                    }
                ],
                "total_capacity": 1000,
                "current_stock": 800
            },
            {
                "id": "NUR-002",
                "name": "Ngong Forest Nursery",
                "location": "Ngong Forest, Nairobi",
                "coordinates": {"lat": -1.3500, "lng": 36.7000},
                "species": [
                    {
                        "name": "Juniperus procera",
                        "count": 800,
                        "stage": "Ready for planting",
                        "last_updated": "2024-01-15"
                    }
                ],
                "total_capacity": 1500,
                "current_stock": 800
            }
        ]
    }
    
    # Save to JSON file
    with open("sample_nursery_inventory.json", "w") as f:
        json.dump(nursery_inventory, f, indent=2)
    
    print("Sample nursery inventory saved to sample_nursery_inventory.json")
    return nursery_inventory

def main():
    """
    Main function to integrate Kenya forest data into the Acoustic Guardian system
    """
    print("Acoustic Guardian - Kenya Forest Data Integration")
    print("=" * 50)
    print()
    
    # 1. Download sample data
    forest_data = download_sample_data()
    print()
    
    # 2. Create Grafana forest layer
    forest_layer = create_grafana_forest_layer()
    print()
    
    # 3. Create deforestation risk model
    risk_model = create_deforestation_risk_model()
    print()
    
    # 4. Update Grafana dashboard with new layers
    update_grafana_dashboard_with_layers()
    print()
    
    # 5. Generate InfluxDB Line Protocol examples
    line_protocol_examples = generate_influxdb_line_protocol_examples()
    print()
    
    # 6. Create sample nursery inventory
    nursery_inventory = create_sample_nursery_inventory()
    print()
    
    # Summary
    print("Integration Summary:")
    print("-" * 20)
    print(f"✓ Downloaded {len(forest_data)} Kenya forest locations")
    print("✓ Created Grafana forest boundary layer")
    print(f"✓ Created deforestation risk model with {len(risk_model)} forests")
    print("✓ Updated Grafana dashboard with new layers")
    print(f"✓ Generated {len(line_protocol_examples)} InfluxDB Line Protocol examples")
    print("✓ Created sample nursery inventory")
    print()
    print("Next steps:")
    print("1. Download actual GIS data from the provided sources")
    print("2. Convert Shapefiles to GeoJSON for Grafana integration")
    print("3. Update the Grafana dashboard with real forest boundary data")
    print("4. Train AI models with the deforestation risk data")
    print("5. Import nursery inventory data into InfluxDB")

if __name__ == "__main__":
    main()