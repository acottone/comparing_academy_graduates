# Youth Academy Player Comparison: Hale End vs. La Masia

A comprehensive data analysis project comparing two elite football youth academies - **Arsenal's Hale End** and **Barcelona's La Masia** - through web scraping and interactive visualizations.

**Course:** STA141B
**Contributors:** Angelina Cottone, Taarunya Sekaran, Kieran Sullivan

---

## Project Overview

This project analyzes player performance and development from two of the world's most renowned youth academies by collecting and visualizing data from three major football statistics platforms:

- **FBref**: Match logs and per-90 statistics (goals, assists, shots, passes, etc.)
- **Transfermarkt**: Market value progression over time
- **Sofascore**: Match ratings and performance scores

The analysis provides insights into player development trajectories, performance metrics, and market valuations to evaluate the effectiveness of these youth development systems.

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

## Project Structure

### 1. `fbref.py`
**Purpose:** Scrapes detailed match statistics from FBref and calculates per-90 metrics.

**Key Features:**
- Scrapes match logs for each player across multiple seasons
- Filters for valid competitions (La Liga, Premier League, Champions League, domestic cups)
- Calculates per-90 statistics for goals, assists, shots, touches, tackles, passes, and more
- Implements rate limiting and random user agents to avoid blocking
- Exports data to `all_players_matches.csv` and `all_players_per90_stats.csv`

**Important Functions:**
- `scrape_player_matches()`: Retrieves all match data for a player
- `calculate_stats()`: Computes overall per-90 statistics
- `calculate_period_stats()`: Analyzes performance over specific time periods
- `clean_team_names()`: Standardizes team name formatting

**Usage:**
```bash
python fbref.py
```

**Output Files:**
- `all_players_matches.csv`: Raw match-by-match data
- `all_players_per90_stats.csv`: Aggregated per-90 statistics by time period

---

### 2. `TransferMarkt.ipynb`
**Purpose:** Scrapes market value history from Transfermarkt for all academy graduates.

**Key Features:**
- Automatically identifies academy graduates currently playing for the first team
- Retrieves complete market value history with dates
- Preserves player names with proper encoding (accents, special characters)
- Includes player positions for additional context

**Important Steps:**
1. Fetches academy squad pages for Barcelona and Arsenal
2. Extracts player IDs and positions from squad tables
3. Calls Transfermarkt API to get market value progression
4. Exports to `Transfermarkt_values.csv` with UTF-8 encoding

**Output:**
- `Transfermarkt_values.csv`: Market value history with dates, clubs, and positions

---

### 3. `Sofascore_work.ipynb`
**Purpose:** Scrapes match ratings from Sofascore and calculates average ratings over time.

**Key Features:**
- Retrieves match-by-match Sofascore ratings (0-10 scale)
- Filters out friendly matches and non-club games
- Matches ratings to transfer value dates for correlation analysis
- Removes accents from player names for data merging

**Important Steps:**
1. Defines player names and Sofascore IDs
2. Fetches match events and ratings via Sofascore API
3. Filters for Arsenal/Barcelona matches only
4. Calculates average ratings between transfer value update dates
5. Exports to `player_match_ratings2.csv` and `result_df.csv`

**Output:**
- `player_match_ratings2.csv`: Individual match ratings
- `result_df.csv`: Average ratings by time period

---

### 4. `Interactive visual.ipynb`
**Purpose:** Creates interactive visualizations combining all three data sources.

**Key Features:**
- Multi-panel interactive dashboard using Plotly
- Three synchronized visualizations:
  - **Transfer Value**: Market value progression over time (blue line)
  - **Per-90 Stats**: Performance metrics with dropdown selector (green line)
  - **Sofascore Ratings**: Color-coded bar chart (red=poor, orange=average, green=excellent)
- Player selector dropdown to switch between all analyzed players
- Stat selector dropdown (goals, assists, shots, shot-creating actions, passes)
- Synchronized time axes for easy comparison

**Available Metrics:**
- `goals_per90`: Goals scored per 90 minutes
- `assists_per90`: Assists per 90 minutes
- `shots_per90`: Shots taken per 90 minutes
- `sca_per90`: Shot-creating actions per 90 minutes
- `passes_per90`: Completed passes per 90 minutes

---

## Installation & Setup

### Prerequisites
```bash
pip install requests beautifulsoup4 pandas fake-useragent plotly
```

### Required Libraries
- `requests`: HTTP requests for web scraping
- `beautifulsoup4`: HTML parsing
- `pandas`: Data manipulation and analysis
- `fake-useragent`: Random user agent generation
- `plotly`: Interactive visualizations

---

## How to Run

### Step 1: Scrape FBref Data
```bash
python fbref.py
```
**Note:** This will take several minutes due to rate limiting (6-second delays between requests).

### Step 2: Scrape Transfermarkt Data
Open and run all cells in `TransferMarkt.ipynb`

### Step 3: Scrape Sofascore Data
Open and run all cells in `Sofascore_work.ipynb`

### Step 4: Generate Interactive Visualizations
Open and run all cells in `Interactive visual.ipynb`

---

## Data Sources

### FBref
- **URL Pattern:** `https://fbref.com/en/players/{player_id}/{name}-Match-Logs`
- **Data Collected:** Match logs, per-90 statistics, competition details
- **Rate Limiting:** 6-second delay between requests

### Transfermarkt
- **Academy Pages:**
  - Barcelona: `https://www.transfermarkt.us/fc-barcelona/jugendarbeit/verein/131`
  - Arsenal: `https://www.transfermarkt.us/arsenal-fc/jugendarbeit/verein/11`
- **API Endpoint:** `https://www.transfermarkt.us/ceapi/marketValueDevelopment/graph/{player_id}`
- **Data Collected:** Market value history, dates, clubs, positions

### Sofascore
- **API Endpoint:** `https://www.sofascore.com/api/v1/player/{player_id}/events/last/{page}`
- **Data Collected:** Match ratings (0-10 scale), match dates, tournaments
- **Filtering:** Excludes friendlies and national team matches

---

## Key Insights

The project enables analysis of:
- **Player Development:** How performance metrics evolve over time
- **Market Value Correlation:** Relationship between on-field performance and market valuation
- **Academy Comparison:** Relative success of Hale End vs. La Masia in developing talent
- **Performance Trends:** Identifying breakout periods and consistency

---

## Important Notes

1. **Rate Limiting:** All scraping scripts include delays to respect website policies
2. **Data Freshness:** Run scripts periodically to update with latest matches
3. **Encoding:** Player names with accents are preserved using UTF-8 encoding
4. **Valid Competitions:** Only major competitions are included (excludes friendlies)
5. **Time Periods:** Analysis dates are customized per player based on significant career milestones

---

## Output Files

| File | Description | Source |
|------|-------------|--------|
| `all_players_matches.csv` | Match-by-match data | FBref |
| `all_players_per90_stats.csv` | Per-90 statistics by period | FBref |
| `Transfermarkt_values.csv` | Market value history | Transfermarkt |
| `player_match_ratings2.csv` | Individual match ratings | Sofascore |
| `result_df.csv` | Average ratings by period | Sofascore |

---

## Additional Resources

- **Full Report:** See `STA 141B Report.pdf` for detailed analysis and findings
- **Interactive Visualizations:** Run `Interactive visual.ipynb` to explore the data

---

## Acknowledgments

Data sources:
- [FBref](https://fbref.com/) - Football statistics
- [Transfermarkt](https://www.transfermarkt.us/) - Market valuations
- [Sofascore](https://www.sofascore.com/) - Match ratings

---

## License

This project is for educational purposes as part of STA141B coursework.
