# 📈 FutureFit: AI-Driven Labor Market Forecasting (2025)
**Author:** Dinesh Kumaralingam

## 📌 Executive Summary
In a rapidly shifting labor market, static job descriptions are obsolete. This project leverages **Big Data (1.29 Million Job Postings)** and **Unsupervised Learning** to forecast skill demand across the US. By analyzing skill co-occurrence and geographic clusters, we provide actionable intelligence for workforce planning.

**Business Impact:**
* **Scale:** Scraped and processed **1.29M+ unique job postings** from LinkedIn to capture a real-time snapshot of the US labor market.
* **Skill Strategy:** Quantified the "Hard vs. Soft Skill" equilibrium, revealing that top roles (Data Scientist, Consultant) require a 60/40 split, contradicting the "tech-only" hiring bias.
* **Geo-Clustering:** Identified distinct "Skill Micro-Climates"—showing that a Data Analyst in NYC requires a fundamentally different tech stack (Finance/Excel-heavy) compared to one in SF (Python/ML-heavy).

## 🛠️ Technical Architecture
This project utilizes a Python-based data science stack for high-volume text analysis and clustering.

### 1. Data Pipeline (ETL)
* **Source:** LinkedIn Job Postings (Scraped via Selenium/Python).
* **Volume:** 1,290,000+ records across 5 strategic roles (Data Analyst, Data Scientist, Supply Chain, Marketing, Consultant).
* **Engineering:** Built robust parsers to extract structured "Skills" arrays from unstructured JD text.

### 2. Analytical Engine (Machine Learning)
* **Clustering:** Applied **K-Means Clustering** on skill vectors to identify 3 distinct market segments:
    * *Cluster 0:* Generalist/Core Analytics
    * *Cluster 1:* Specialized Tech/ML
    * *Cluster 2:* Domain-Specific (Supply Chain/Finance)
* **Geospatial Analysis:** Mapped skill demand hotspots, revealing that **Florida & Texas** are emerging as dominant hubs for Supply Chain roles, while **California** retains the monopoly on ML research.

## 📊 Key Insights
*(See `notebooks/` for full analysis)*

* **The "Hybrid" Worker:** 2025 demand forecasts show a massive spike in "Hybrid" roles where soft skills (Communication, Strategy) co-occur with hard skills (SQL, Python) in **85%** of high-salary listings.
* **Location Matters:** Training programs cannot be one-size-fits-all. A "Marketing Analyst" in New York (AdTech focus) shares only **40%** of the skill requirements of a Marketing Analyst in Seattle (Product focus).

## 📂 Repository Structure
```text
├── notebooks/
│   └── analysis_main.ipynb   # Complete data pipeline and clustering analysis
├── src/
│   └── scraper.py            # Selenium script for LinkedIn data collection
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation


