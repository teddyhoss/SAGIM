import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Number of records to generate
num_records = 50000

# Function to generate random dates
def random_dates(start, end, n):
    start_u = int(start.timestamp())
    end_u = int(end.timestamp())
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

# 1. 🔮 Market Predictive Analysis
def generate_market_predictive_analysis(num_records):
    dates = random_dates(datetime(2022, 1, 1), datetime(2023, 12, 31), num_records)
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia']
    historical_sales = np.random.randint(1000, 50000, num_records)
    predicted_sales = historical_sales * np.random.uniform(0.9, 1.2, num_records)
    market_trends = np.random.choice(['Growing', 'Stable', 'Declining'], num_records)
    df = pd.DataFrame({
        'Date': dates,
        'Region': np.random.choice(regions, num_records),
        'Historical_Sales': historical_sales,
        'Predicted_Sales': predicted_sales.astype(int),
        'Market_Trend': market_trends
    })
    df.to_csv('market_predictive_analysis.csv', index=False)

# 2. 📊 Social Media Analysis and Sentiment Analysis
def generate_social_media_analysis(num_records):
    dates = random_dates(datetime(2022, 1, 1), datetime(2023, 12, 31), num_records)
    platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'TikTok']
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia']
    sentiment_scores = np.random.uniform(-1, 1, num_records)
    mentions = np.random.randint(100, 10000, num_records)
    engagement_rate = np.random.uniform(0.01, 0.2, num_records)
    df = pd.DataFrame({
        'Date': dates,
        'Platform': np.random.choice(platforms, num_records),
        'Region': np.random.choice(regions, num_records),
        'Sentiment_Score': sentiment_scores,
        'Mentions': mentions,
        'Engagement_Rate': engagement_rate
    })
    df.to_csv('social_media_analysis.csv', index=False)

# 3. 🌐 Global Supply Chain Optimization
def generate_supply_chain_optimization(num_records):
    suppliers = ['Supplier ' + str(i) for i in range(1, 51)]
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia']
    component_ids = ['Component_{:03d}'.format(i) for i in range(1, 21)]  # 20 components
    lead_times = np.random.randint(5, 60, num_records)  # in days
    costs = np.random.uniform(1000, 50000, num_records)
    reliability_scores = np.random.uniform(0.7, 1.0, num_records)
    df = pd.DataFrame({
        'Supplier': np.random.choice(suppliers, num_records),
        'Region': np.random.choice(regions, num_records),
        'Component_ID': np.random.choice(component_ids, num_records),
        'Lead_Time_Days': lead_times,
        'Cost_USD': costs,
        'Reliability_Score': reliability_scores
    })
    df.to_csv('supply_chain_optimization.csv', index=False)

# 4. 🎨 Product Customization Based on Local Preferences
def generate_product_customization(num_records):
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia']
    customization_options = ['Color', 'Size', 'Packaging', 'Features', 'Design']
    popularity_scores = np.random.uniform(0, 1, num_records)
    df = pd.DataFrame({
        'Region': np.random.choice(regions, num_records),
        'Customization_Option': np.random.choice(customization_options, num_records),
        'Popularity_Index': popularity_scores
    })
    df.to_csv('product_customization.csv', index=False)

# 5. 💹 Dynamic Pricing and Optimization
def generate_dynamic_pricing(num_records):
    dates = random_dates(datetime(2022, 1, 1), datetime(2023, 12, 31), num_records)
    product_ids = ['Product_{:03d}'.format(i) for i in range(1, 21)]  # 20 products
    base_prices = np.random.uniform(10, 100, num_records)
    demand_levels = np.random.choice(['Low', 'Medium', 'High'], num_records)
    competitor_prices = base_prices * np.random.uniform(0.9, 1.1, num_records)
    optimized_prices = base_prices * np.random.uniform(0.8, 1.2, num_records)
    df = pd.DataFrame({
        'Date': dates,
        'Product_ID': np.random.choice(product_ids, num_records),
        'Base_Price_USD': base_prices,
        'Competitor_Price_USD': competitor_prices,
        'Demand_Level': demand_levels,
        'Optimized_Price_USD': optimized_prices
    })
    df.to_csv('dynamic_pricing.csv', index=False)

# 6. 🛡️ Geopolitical and Economic Risk Management
def generate_risk_management(num_records):
    countries = ['Country ' + str(i) for i in range(1, 51)]
    risk_types = ['Political', 'Economic', 'Environmental', 'Regulatory', 'Social']
    risk_levels = np.random.choice(['Low', 'Medium', 'High'], num_records)
    impact_scores = np.random.uniform(1, 5, num_records)
    df = pd.DataFrame({
        'Country': np.random.choice(countries, num_records),
        'Risk_Type': np.random.choice(risk_types, num_records),
        'Risk_Level': risk_levels,
        'Impact_Score': impact_scores
    })
    df.to_csv('risk_management.csv', index=False)

# 7. 🌍 Cultural Data Analysis and Business Adaptation
def generate_cultural_data_analysis(num_records):
    countries = ['Country ' + str(i) for i in range(1, 51)]
    cultural_factors = ['Language', 'Religion', 'Values', 'Customs', 'Etiquette']
    adaptation_needed = np.random.choice(['Yes', 'No'], num_records)
    adaptation_level = np.random.uniform(0, 1, num_records)
    df = pd.DataFrame({
        'Country': np.random.choice(countries, num_records),
        'Cultural_Factor': np.random.choice(cultural_factors, num_records),
        'Adaptation_Needed': adaptation_needed,
        'Adaptation_Level': adaptation_level
    })
    df.to_csv('cultural_data_analysis.csv', index=False)

# 8. 🎯 Personalized Recommendation Systems
def generate_recommendation_system(num_records):
    customer_ids = ['Customer_' + str(i) for i in range(1, num_records + 1)]
    product_ids = ['Product_{:03d}'.format(i) for i in range(1, 21)]  # 20 products
    purchase_history = [';'.join(random.sample(product_ids, k=random.randint(1, 3))) for _ in range(num_records)]
    recommended_products = np.random.choice(product_ids, num_records)
    recommendation_scores = np.random.uniform(0.7, 1.0, num_records)
    df = pd.DataFrame({
        'Customer_ID': customer_ids,
        'Purchase_History': purchase_history,
        'Recommended_Product_ID': recommended_products,
        'Recommendation_Score': recommendation_scores
    })
    df.to_csv('recommendation_system.csv', index=False)

# 9. 🧩 Market Entry Scenario Simulations
def generate_market_entry_simulations(num_records):
    scenarios = ['Scenario ' + str(i) for i in range(1, num_records + 1)]
    countries = ['Country ' + str(i) for i in range(1, 51)]
    investment_required = np.random.uniform(100000, 5000000, num_records)
    projected_roi = np.random.uniform(5, 25, num_records)
    risk_levels = np.random.choice(['Low', 'Medium', 'High'], num_records)
    df = pd.DataFrame({
        'Scenario': scenarios,
        'Country': np.random.choice(countries, num_records),
        'Investment_Required_USD': investment_required,
        'Projected_ROI_Percent': projected_roi,
        'Risk_Level': risk_levels
    })
    df.to_csv('market_entry_simulations.csv', index=False)

# Generate all datasets
generate_market_predictive_analysis(num_records)
generate_social_media_analysis(num_records)
generate_supply_chain_optimization(num_records)
generate_product_customization(num_records)
generate_dynamic_pricing(num_records)
generate_risk_management(num_records)
generate_cultural_data_analysis(num_records)
generate_recommendation_system(num_records)
generate_market_entry_simulations(num_records)

print("Synthetic datasets generated successfully!")
