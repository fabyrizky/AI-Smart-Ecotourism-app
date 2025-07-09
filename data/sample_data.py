import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sample_locations():
    """Generate sample tourism location data"""
    locations = [
        {
            'name': 'Borobudur Heritage Complex',
            'type': 'Cultural Heritage',
            'province': 'Central Java',
            'sustainability_score': 9.2,
            'monthly_visitors': 28500,
            'satisfaction_rating': 8.9,
            'carbon_footprint': 1.2,
            'education_programs': 15
        },
        {
            'name': 'Komodo National Park',
            'type': 'Wildlife Conservation',
            'province': 'East Nusa Tenggara',
            'sustainability_score': 9.5,
            'monthly_visitors': 8200,
            'satisfaction_rating': 9.3,
            'carbon_footprint': 0.8,
            'education_programs': 12
        },
        {
            'name': 'Ubud Rice Terraces',
            'type': 'Agricultural Heritage',
            'province': 'Bali',
            'sustainability_score': 9.1,
            'monthly_visitors': 15600,
            'satisfaction_rating': 9.0,
            'carbon_footprint': 0.4,
            'education_programs': 18
        },
        {
            'name': 'Raja Ampat Marine Reserve',
            'type': 'Marine Conservation',
            'province': 'West Papua',
            'sustainability_score': 9.4,
            'monthly_visitors': 3200,
            'satisfaction_rating': 9.7,
            'carbon_footprint': 0.6,
            'education_programs': 8
        },
        {
            'name': 'Mount Bromo Volcanic Park',
            'type': 'Geological Heritage',
            'province': 'East Java',
            'sustainability_score': 8.8,
            'monthly_visitors': 22000,
            'satisfaction_rating': 8.7,
            'carbon_footprint': 1.5,
            'education_programs': 10
        },
        {
            'name': 'Lake Toba Caldera',
            'type': 'Natural Heritage',
            'province': 'North Sumatra',
            'sustainability_score': 8.6,
            'monthly_visitors': 18500,
            'satisfaction_rating': 8.5,
            'carbon_footprint': 1.1,
            'education_programs': 14
        }
    ]
    
    return pd.DataFrame(locations)

def generate_sustainability_metrics():
    """Generate sustainability tracking data"""
    metrics = {
        'renewable_energy_percent': random.uniform(75, 95),
        'waste_diversion_rate': random.uniform(85, 98),
        'water_conservation_percent': random.uniform(80, 95),
        'local_employment_percent': random.uniform(85, 96),
        'carbon_offset_tons': random.uniform(150, 300),
        'community_investment_usd': random.uniform(50000, 150000)
    }
    return metrics

def generate_visitor_trends(days=30):
    """Generate visitor trend data"""
    base_date = datetime.now() - timedelta(days=days)
    dates = [base_date + timedelta(days=i) for i in range(days)]
    
    # Simulate seasonal patterns
    visitor_data = []
    for i, date in enumerate(dates):
        base_visitors = 1000
        seasonal_factor = 1 + 0.3 * np.sin(i * 2 * np.pi / 30)  # Monthly cycle
        weekly_factor = 1 + 0.2 * np.sin(i * 2 * np.pi / 7)    # Weekly cycle
        random_factor = random.uniform(0.8, 1.2)
        
        visitors = int(base_visitors * seasonal_factor * weekly_factor * random_factor)
        
        visitor_data.append({
            'date': date,
            'visitors': visitors,
            'satisfaction': random.uniform(8.0, 9.5),
            'carbon_offset_kg': visitors * random.uniform(0.5, 1.2)
        })
    
    return pd.DataFrame(visitor_data)
