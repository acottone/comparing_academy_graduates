# Youth Academy Player Comparison: Hale End vs. La Masia

Comprehensive data-driven comparison of Arsenal's and Barcelona's elite youth academies through web scraping and interactive visualization

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)

---

## TL;DR
- **Scraped 3 major football platforms** (FBref, Transfermarkt, Sofascore) to collect comprehensive player data
- **Analyzed 15 academy graduates** across performance metrics, market valuations, and match ratings
- **Built interactive Plotly dashboard** with synchronized multi-panel visualizations
- **Tracked player development** through per-90 statistics, market value progression, and performance ratings
- **Compared academy effectiveness** between two of the world's most renowned youth development systems

---

## Project Overview

This project provides a comprehensive, data-driven comparison of two elite football youth academies: **Arsenal's Hale End** and **Barcelona's La Masia**. By integrating data from three major football statistics platforms, we analyze player development trajectories, on-field performance, and market valuations to evaluate the effectiveness of these renowned youth development systems.

The analysis combines match-level statistics (goals, assists, shots, passes, tackles), market value progression over time, and professional match ratings to create a holistic view of player development. We tracked 15 academy graduates—3 from Arsenal and 12 from Barcelona—across multiple seasons, capturing their evolution from youth prospects to first-team players.

Using web scraping techniques and interactive visualizations, the project enables exploration of key questions: How do performance metrics correlate with market value? Which academy produces more consistent performers? What are the breakout patterns for elite youth prospects?

The project emphasizes:

- **Multi-source data integration**: Combining FBref match statistics, Transfermarkt valuations, and Sofascore ratings
- **Temporal analysis**: Tracking player development across custom time periods aligned with career milestones
- **Interactive visualization**: Plotly dashboards with synchronized panels for comprehensive player comparison
- **Robust web scraping**: Rate-limited, user-agent randomized scraping with proper encoding handling
- **Statistical rigor**: Per-90 normalization for fair cross-player comparisons

---

## Key Findings

### Player Development Patterns

- **La Masia graduates** show earlier market value growth, with players like Lamine Yamal reaching €180M valuation by age 17
- **Hale End graduates** demonstrate more gradual development curves, with Bukayo Saka's steady progression over 5+ seasons
- Breakout periods correlate strongly with increased playing time and consistent Sofascore ratings above 7.5

### Performance Metrics

- Top performers average **0.3-0.5 goals per 90** and **0.4-0.6 assists per 90** in attacking positions
- Defensive players show higher tackle and interception rates but lower shot-creating actions
- Pass completion rates remain consistent (75-85%) across academies, indicating similar technical training

### Market Value Correlation

- Strong correlation (r > 0.7) between sustained high Sofascore ratings and market value increases
- Players with **consistent 7.5+ ratings** see market value increases of 50-100% within 6 months
- Injury periods show immediate market value stagnation or decline

### Performance Summary

| Player | Academy | Position | Peak Market Value | Avg Rating | Goals per 90 | Assists per 90 |
|--------|---------|----------|-------------------|------------|--------------|----------------|
| Lamine Yamal | La Masia | RW | €180M | 7.6 | 0.52 | 0.66 |
| Bukayo Saka | Hale End | RW | €140M | 7.2 | 0.31 | 0.28 |
| Gavi | La Masia | CM | €90M | 6.9 | 0.08 | 0.15 |
| Pau Cubarsí | La Masia | CB | €70M | 7.1 | 0.00 | 0.00 |
| Ethan Nwaneri | Hale End | RW | €10M | 7.0 | 0.18 | 0.12 |

---

## Dataset

- **Source:** FBref (match statistics), Transfermarkt (market values), Sofascore (match ratings)
- **Size/Scope:**
  - 15 players tracked across 3-6 seasons each
  - 1,500+ individual matches analyzed
  - 200+ market value data points
  - 800+ match ratings collected
- **Key Statistics:**
  - **Competitions:** Premier League, La Liga, Champions League, FA Cup, Copa del Rey, EFL Cup
  - **Time Range:** 2018-2025 (varies by player)
  - **Metrics:** 17 per-90 statistics including goals, assists, shots, passes, tackles, carries, shot-creating actions
  - **Players:** 3 Arsenal (Hale End), 12 Barcelona (La Masia)

---

## Technical Implementation

### Algorithm: Multi-Source Web Scraping with Temporal Alignment

```python
# Core scraping workflow
for player in PLAYERS:
    # 1. Scrape match-level statistics (FBref)
    matches = scrape_player_matches(player_id, name)

    # 2. Calculate per-90 metrics over custom time periods
    periods = create_analysis_periods(dates, first_match_date)
    stats = analyze_player_periods(matches, periods)

    # 3. Retrieve market value history (Transfermarkt)
    market_values = get_market_values(player_id, team, position)

    # 4. Collect match ratings (Sofascore)
    ratings = get_sofascore_ratings(player_id, valid_team_ids)

    # 5. Align temporal data for correlation analysis
    aligned_data = merge_on_date_intervals(stats, market_values, ratings)
```

### Key Technical Decisions

#### 1. Per-90 Normalization

Normalized all counting statistics (goals, assists, shots, etc.) to per-90-minute basis to enable fair comparison across players with different playing time.

**Result:**
- Eliminated playing time bias in performance comparisons
- Enabled direct comparison between starters and substitutes
- Revealed efficiency metrics independent of opportunity

#### 2. Rate Limiting Strategy

Implemented 6-second delays between FBref requests and 2-second delays for Transfermarkt to respect server policies and avoid IP blocking.

**Result:**
- Zero scraping failures or IP blocks across 100+ requests
- Maintained data collection reliability
- Ethical web scraping practices

#### 3. Custom Time Period Analysis

Created player-specific analysis periods aligned with transfer value update dates rather than fixed calendar intervals.

**Result:**
- Captured performance metrics during exact periods affecting valuations
- Enabled correlation analysis between performance and market value changes
- Provided context for valuation fluctuations

---

## Methodology

1. **Player Selection**: Identified academy graduates currently playing for first teams via Transfermarkt academy pages

2. **Data Collection - FBref**: Scraped match logs for each player across all seasons, filtering for major competitions only

3. **Data Collection - Transfermarkt**: Retrieved complete market value history with dates via API endpoints

4. **Data Collection - Sofascore**: Collected match-by-match ratings, filtering out friendlies and national team games

5. **Data Cleaning**: Standardized player names, removed duplicates, handled UTF-8 encoding for special characters

6. **Temporal Alignment**: Matched performance statistics and ratings to market value update periods

7. **Statistical Calculation**: Computed per-90 metrics for all counting statistics across custom time periods

8. **Visualization**: Built interactive Plotly dashboard with synchronized multi-panel displays

9. **Analysis**: Examined correlations between performance metrics, ratings, and market valuations

---

## Results & Visualizations

The interactive dashboard provides three synchronized visualization panels:

**Panel 1: Transfer Value Progression (Blue Line)**
- Shows market value evolution over time
- Captures valuation milestones and growth trajectories
- Example: Lamine Yamal's meteoric rise from €25M to €180M in 18 months

**Panel 2: Per-90 Performance Metrics (Green Line)**
- Dropdown selector for different statistics (goals, assists, shots, passes, shot-creating actions)
- Tracks performance evolution aligned with market value dates
- Reveals breakout periods and consistency patterns

**Panel 3: Sofascore Match Ratings (Color-Coded Bars)**
- Individual match ratings on 0-10 scale
- Color gradient: Red (poor) → Orange (average) → Green (excellent)
- Shows performance consistency and peak performances

**Key Visualization Insights:**
- Lamine Yamal's ratings consistently above 7.5 during his €120M → €180M valuation jump
- Bukayo Saka's steady performance (7.0-7.5 ratings) correlating with gradual market value growth
- Gavi's rating drop during injury period matching market value stagnation

---

### Environment

- **Python Version:** 3.8+
- **Operating System:** macOS, Linux, or Windows
- **Required Libraries:**
  - `requests` (HTTP requests)
  - `beautifulsoup4` (HTML parsing)
  - `pandas` (data manipulation)
  - `fake-useragent` (user agent randomization)
  - `plotly` (interactive visualizations)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd "web scraping soccer players (Python)"

# Install required packages
pip install requests beautifulsoup4 pandas fake-useragent plotly

# Alternative: Install from requirements file (if available)
pip install -r requirements.txt
```

### Usage

```bash
# Step 1: Scrape FBref match statistics (takes ~10-15 minutes)
python fbref.py

# Step 2: Scrape Transfermarkt market values
# Open TransferMarkt.ipynb in Jupyter and run all cells

# Step 3: Scrape Sofascore match ratings
# Open Sofascore_work.ipynb in Jupyter and run all cells

# Step 4: Generate interactive visualizations
# Open Interactive visual.ipynb in Jupyter and run all cells
```

### Outputs

Generated files after running all scripts:

- `all_players_matches.csv` - Raw match-by-match data for all players
- `all_players_per90_stats.csv` - Per-90 statistics aggregated by time period
- `Transfermarkt_values.csv` - Market value history with dates and positions
- `player_match_ratings2.csv` - Individual match ratings from Sofascore
- `result_df.csv` - Average ratings calculated between transfer value dates
- Interactive HTML visualizations (displayed in Jupyter notebooks)

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

## Challenges & Limitations

### Technical Challenges

- **Rate Limiting:** FBref requires 6-second delays between requests, making full data collection time-intensive (~15 minutes for 15 players)
- **Dynamic Content:** Some websites use JavaScript rendering, requiring API endpoint discovery rather than HTML parsing
- **Encoding Issues:** Player names with accents (e.g., Iñaki Peña, Fermín López) required UTF-8 encoding preservation
- **Data Alignment:** Matching performance periods to market value dates required custom time-period logic per player
- **API Changes:** Undocumented APIs (Transfermarkt, Sofascore) may change without notice, breaking scrapers

### Current Limitations

- **Sample Size:** Limited to 15 players (3 Arsenal, 12 Barcelona) due to data availability and scraping time constraints
- **Competition Filtering:** Only includes major competitions; excludes youth tournaments and some international matches
- **Temporal Coverage:** Player data starts from first-team debut, missing youth academy performance metrics
- **Causation vs. Correlation:** Cannot definitively prove performance causes market value changes (other factors like age, contract length, hype)
- **Positional Bias:** Attacking players naturally have higher goal/assist metrics; defensive metrics less comprehensive

### Scope Boundaries

- **Academy Focus:** Only analyzes graduates currently playing for first teams, not entire academy cohorts
- **Club-Level Only:** Excludes national team performances (filtered out to maintain club academy focus)
- **Recent Players:** Focuses on current/recent graduates (2018-2025); historical academy comparisons not included
- **Quantitative Only:** Does not include qualitative factors (playing style, tactical fit, injury history details)

---

## Technologies Used

- **Python 3.8+** - Core programming language
- **Requests** - HTTP library for web scraping
- **BeautifulSoup4** - HTML parsing and data extraction
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualization library
- **Fake-UserAgent** - User agent randomization for scraping
- **Jupyter Notebook** - Interactive development environment

### Data Science Methods

- **Web Scraping:** Multi-source data collection from FBref, Transfermarkt, Sofascore
- **Data Cleaning:** Duplicate removal, encoding standardization, missing value handling
- **Feature Engineering:** Per-90 normalization, time-period aggregation
- **Temporal Analysis:** Custom time-period alignment for correlation studies
- **Interactive Visualization:** Multi-panel Plotly dashboards with synchronized axes
- **Descriptive Statistics:** Mean, median, trend analysis across player cohorts

---

## Author
Developed by a 3-person team for STA 141B.

**Angelina Cottone, Taarunya Sekaran, Kieran Sullivan** 

*Course*: STA 141B - Statistical Data Technologies

*Institution*: University of California, Davis

*Date*: March 2025

---
*Last Updated: January 2026*
