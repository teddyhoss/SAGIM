-- Creazione delle tabelle e inserimento dei dati mockup

-- 🔮 Analisi predittiva di mercato
CREATE TABLE IF NOT EXISTS market_predictions (
    id SERIAL PRIMARY KEY,
    product_id INT,
    date DATE,
    predicted_sales DECIMAL(10,2),
    actual_sales DECIMAL(10,2)
);

INSERT INTO market_predictions (product_id, date, predicted_sales, actual_sales) VALUES
(1, '2024-01-01', 1000.00, 1050.00),
(1, '2024-01-02', 1100.00, 1080.00),
(2, '2024-01-01', 500.00, 520.00),
(2, '2024-01-02', 550.00, 540.00);

-- 📊 Analisi dei social media e sentiment analysis
CREATE TABLE IF NOT EXISTS social_media_sentiment (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50),
    date DATE,
    sentiment DECIMAL(3,2),
    mentions INT
);

INSERT INTO social_media_sentiment (platform, date, sentiment, mentions) VALUES
('Twitter', '2024-01-01', 0.75, 1000),
('Facebook', '2024-01-01', 0.65, 800),
('Instagram', '2024-01-01', 0.80, 1200);

-- 🌐 Ottimizzazione della catena di approvvigionamento globale
CREATE TABLE IF NOT EXISTS supply_chain_performance (
    id SERIAL PRIMARY KEY,
    supplier_id INT,
    product_id INT,
    lead_time INT,
    cost DECIMAL(10,2),
    quality_score DECIMAL(3,2)
);

INSERT INTO supply_chain_performance (supplier_id, product_id, lead_time, cost, quality_score) VALUES
(1, 1, 5, 100.00, 0.95),
(2, 1, 7, 90.00, 0.90),
(3, 2, 6, 110.00, 0.98);

-- 🎨 Personalizzazione del prodotto basata su preferenze locali
CREATE TABLE IF NOT EXISTS product_preferences (
    id SERIAL PRIMARY KEY,
    region VARCHAR(50),
    product_id INT,
    feature VARCHAR(50),
    preference_score DECIMAL(3,2)
);

INSERT INTO product_preferences (region, product_id, feature, preference_score) VALUES
('North America', 1, 'Color', 0.8),
('Europe', 1, 'Size', 0.7),
('Asia', 2, 'Material', 0.9);

-- 🕵️ Analisi competitiva avanzata
CREATE TABLE IF NOT EXISTS competitive_analysis (
    id SERIAL PRIMARY KEY,
    competitor_id INT,
    product_category VARCHAR(50),
    market_share DECIMAL(5,2),
    price_point DECIMAL(10,2),
    customer_satisfaction DECIMAL(3,2)
);

INSERT INTO competitive_analysis (competitor_id, product_category, market_share, price_point, customer_satisfaction) VALUES
(1, 'Electronics', 25.5, 599.99, 4.2),
(2, 'Electronics', 30.0, 649.99, 4.0),
(3, 'Clothing', 15.3, 79.99, 4.5);

-- 💹 Pricing dinamico e ottimizzazione
CREATE TABLE IF NOT EXISTS dynamic_pricing (
    id SERIAL PRIMARY KEY,
    product_id INT,
    date DATE,
    base_price DECIMAL(10,2),
    optimal_price DECIMAL(10,2),
    demand_forecast INT
);

INSERT INTO dynamic_pricing (product_id, date, base_price, optimal_price, demand_forecast) VALUES
(1, '2024-01-01', 100.00, 110.00, 1000),
(1, '2024-01-02', 100.00, 105.00, 950),
(2, '2024-01-01', 200.00, 190.00, 500);

-- 🛡️ Gestione del rischio geopolitico ed economico
CREATE TABLE IF NOT EXISTS geopolitical_risk (
    id SERIAL PRIMARY KEY,
    country VARCHAR(50),
    risk_factor VARCHAR(50),
    risk_score DECIMAL(3,2),
    impact_on_business DECIMAL(3,2)
);

INSERT INTO geopolitical_risk (country, risk_factor, risk_score, impact_on_business) VALUES
('USA', 'Political Stability', 0.2, 0.1),
('China', 'Trade Relations', 0.6, 0.5),
('Germany', 'Economic Growth', 0.3, 0.2);

-- 🌍 Analisi dei dati culturali e adattamento del business
CREATE TABLE IF NOT EXISTS cultural_analysis (
    id SERIAL PRIMARY KEY,
    country VARCHAR(50),
    cultural_dimension VARCHAR(50),
    score DECIMAL(3,2),
    business_impact VARCHAR(255)
);

INSERT INTO cultural_analysis (country, cultural_dimension, score, business_impact) VALUES
('Japan', 'Power Distance', 54, 'Hierarchical communication important'),
('USA', 'Individualism', 91, 'Focus on personal achievement in marketing'),
('Brazil', 'Uncertainty Avoidance', 76, 'Clear rules and structures needed');

-- 🎯 Sistemi di raccomandazione personalizzati
CREATE TABLE IF NOT EXISTS product_recommendations (
    id SERIAL PRIMARY KEY,
    user_id INT,
    recommended_product_id INT,
    relevance_score DECIMAL(3,2)
);

INSERT INTO product_recommendations (user_id, recommended_product_id, relevance_score) VALUES
(1, 101, 0.95),
(1, 102, 0.85),
(2, 103, 0.90);

-- 🧩 Simulazioni di scenario per strategie di ingresso nel mercato
CREATE TABLE IF NOT EXISTS market_entry_scenarios (
    id SERIAL PRIMARY KEY,
    scenario_name VARCHAR(100),
    market VARCHAR(50),
    investment_required DECIMAL(12,2),
    expected_roi DECIMAL(5,2),
    risk_level VARCHAR(20)
);

INSERT INTO market_entry_scenarios (scenario_name, market, investment_required, expected_roi, risk_level) VALUES
('Direct Export', 'Europe', 500000.00, 15.5, 'Medium'),
('Joint Venture', 'Asia', 1000000.00, 22.0, 'High'),
('Licensing', 'South America', 250000.00, 10.0, 'Low');