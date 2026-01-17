# Youth Academy Player Comparison: Hale End vs. La Masia

A comprehensive data analysis project comparing two elite football youth academies - **Arsenal's Hale End** and **Barcelona's La Masia** using large-scale web scraping and interactive visual analytics.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)

---

## TL;DR
- Scraped and integrated data from **FBref, Transfermarkt, and Sofascore**
- Analyzed **player performance, market value progression, and match ratings**
- Built **interactive dashboards** for player-level temporal comparison
- Compared development trajectories across two elite youth academies

---

## Project Overview

This project evaluates player development pathways from two of the world's most prestigious football academies, **Hale End** (Arsenal) and **La Masia** (Barcelona).

By integrating match performance metrics, market valuation trends, and match ratings, the analysis provides a **multi-dimensional comparison of academy outputs and player growth over time.

### Data Sources
- **FBref:** Match logs and per-90 performance statistics
- **Transfermarkt:** Market value progression
- **Sofascore:** Match-by-match performance ratings

---

## From Coursework to Applied Sports Analytics
This project was developed for STA 141B, emphasizing:
- Real-world web scraping at scale
- Data integration from heterogeneous sources
- Time-aligned longitudinal analysis
- Interactive data visualization for exploratory analysis

### Key Extensions
- Multi-source data fusion (performance + valuation + ratings)
- Temporal aggregation of player statistics
- Interactive dashboards with synchronized time axes
- Academy-level comparative framework

---

## Players Analyzed

### Arsenal (Hale End)
- Bukayo Saka
- Ethan Nwaneri
- Myles Lewis-Skelly

### Barcelona (La Masia)
- Lamine Yamal
- Gavi
- Pau Cubarsí
- Dani Olmo
- Alejandro Balde
- Fermín López
- Marc Casadó
- Eric García
- Iñaki Peña
- Ansu Fati
- Héctor Fort
- Marc Bernal

---

## Key Findings

### Player Development Trends
- Performance metrics (goals, assists, shots, passes) show **distinct growth patterns** across academies
- Breakout periods often coincide with **rapid increases in market value**
- Players with consistent Sofascore ratings demonstrate **more stable valuation trajectories**

### Market Value Dynamics
- Transfermarkt valuations tend to lag short-term performance spikes
- Sustained performance is more predictive of long-term valuation growth
- Early senior-team integration correlates with higher valuation volatility

### Academy Comparison
- La Masia players show **earlier senior exposure**
- Hale End players demonstrate **steadier incremental development**
- Differences reflect academy philosophy rather than raw performance quality

---

## Dataset

### Sources
- **FBref:** Match logs, per-90 statistics
- **Transfermarkt:** Market value history
- **Sofascore:** Match ratings (0–10 scale)

### Scope
- Club-level matches only (league, domestic cups, European competitions)
- Excludes friendlies and international fixtures
- UTF-8 encoding preserves accented player names

---

## Technical Implementation

### Data Collection Pipeline
#### 1. FBref Scraping
  - Match-level data collection
  - Per-90 statistic computation
  - Competition filtering
  - Rate limiting with randomized user agents
#### 2. Transfermarkt Scraping
  - Academy graduate identification
  - Market value time series extraction
  - Player position metadata
#### 3. Sofascore Scraping
  - Match-by-match ratings
  - Tournament filtering
  - Time-aligned aggregation with market value dates

### Interactive Visualization
#### Dashboard Features
- Player selection dropdown
- Metric selector (goals, assists, shots, SCA, passes)
- Synchronized time axes across all plots

#### Visual Components
- **Market Value Progression** (line plot)
- **Per-90 Performance Metrics** (line plot)
- **Sofascore Ratings** (color-coded bar chart)

This allows intuitive comparison of **performance vs. valuation vs. consistency**.

---

## Methodology

### 1. Data Ingestion & Cleaning
- Scraped raw HTML and API responses
- Standardized team and player naming
- Filtered invalid competitions and matches

### 2. Feature Engineering
- Computed per-90 performance metrics
- Aggregated match ratings over valuation periods
- Aligned datasets temporally

### 3. Comparative Analysis
- Player-level longitudinal analysis
- Cross-academy comparison
- Metric correlation exploration

### 4. Visualization & Interpretation
- Interactive dashboards for exploratory analysis
- Visual alignment of performance and valuation
- Qualitative interpretation of academy philosophies

---

## Reproducibility

### Environment
- Python 3.8+
- Jupyter Notebooks
- BeautifulSoup
- Pandas
- Plotly

### Run
```
pip install requests beautifulsoup4 pandas fake-useragent plotly
python fbref.py
```
- Run all cells in `TransferMarkt.ipynb`
- Run all cells in `Sofascore_work.ipynb`
- Run all cells in `Interactive visual.ipynb`

---

## Project Structure

comparing-academy-graduates/
│
├── fbref.py                          # FBref scraping & per-90 stats
├── TransferMarkt.ipynb               # Market value scraping
├── Sofascore_work.ipynb              # Match rating scraping
├── Interactive visual.ipynb          # Interactive dashboard
├── STA 141B Report.pdf
├── all_players_matches.csv
├── all_players_per90_stats.csv
└── README.md

--- 

## Ethical & Practical Considerations
- Analysis does **not** evaluate player potential or future success
- Market values are influenced by external factors (media, contracts)
- Scraping respects rate limits and public data policies
- Results intended for **educational and analytical purposes only**

---

## Technologies Used

### Programming & Tools
- Python
- Pandas
- BeautifulSoup
- Requests
- Plotly

### Analytical Techniques
- Web scraping with rate limiting
- Time-series aggregation
- Feature engineering
- Interactive visualization

---

## Author
Developed by a 3-person team for STA 141B.

**Angelina Cottone, Taarunya Sekaran, Kieran Sullivan** 
UC Davis, 2025

---
*Last Updated: March 2025*
