import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time
from fake_useragent import UserAgent
import re
from datetime import datetime, timedelta

# Dictionary mapping FBref column names to desired column names
FBREF_COLUMN_MAP = {
    'date': 'date', 'dayofweek': 'day', 'comp': 'comp', 'round': 'round', 'venue': 'venue', 'result': 'result', 'squad': 'team', 
    'opponent': 'opponent', 'game_started': 'starter', 'position': 'position', 'minutes': 'minutes', 'goals': 'goals', 
    'assists': 'assists', 'pens_made': 'penalties_scored', 'pens_att': 'penalties_attempted', 'shots': 'shots'
}

# Stats for per-90 calculations
STATS_FOR_PER90 = [
    'goals', 'assists', 'shots', 'shots_on_goal', 'touches', 'tackles', 'interceptions', 'blocks', 'sca', 'sca_gca', 'passes_comp', 
    'passes', 'prog_passes', 'carries', 'progressive_carries', 'take_ons_attempted', 'successful_take_ons'
]

# Valid competitions to include
VALID_COMPETITIONS = [
    'La Liga', 'Premier League', 'Champions Lg', 'UEFA Super Cup', 'Copa del Rey', 'FA Cup', 'EFL Cup', 'Community Shield'
]

def request(url):
    """
    HTTP requests with random user agents and delays to avoid rate limiting.
    """
    time.sleep(6) # Time delay btwn requests
    headers = {
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code} error")
    return response

def get_column_names(table):
    """
    Extract column names from the table.
    """
    header_rows = table.find_all('tr')[:2]
    column_names = []
    
    for th in header_rows[1].find_all('th'):
        stat_name = th.get('data-stat', '')
        if stat_name:
            column_names.append(FBREF_COLUMN_MAP.get(stat_name, stat_name))
    
    return column_names

def clean_team_names(df):
    """
    Clean team names by removing unnecessary characters.
    """
    if 'team' in df.columns:
        df['team'] = df['team'].str.extract(r'([^a-z].*)', flags=re.IGNORECASE).fillna(df['team'])
        df['team'] = df['team'].str.strip()
    if 'opponent' in df.columns:
        df['opponent'] = df['opponent'].str.extract(r'([^a-z].*)', flags=re.IGNORECASE).fillna(df['opponent'])
        df['opponent'] = df['opponent'].str.strip()
    return df

def scrape_player_matches(player_id, name):
    """
    Scrape match logs for a given player.
    """
    print(f"\nScraping data for {name}...")
    base_url = f"https://fbref.com/en/players/{player_id}/{name}-Match-Logs"
    
    # Get main page and find season links
    response = request(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Filter season links to get summary links and exclude national team links
    season_links = [link for link in soup.find_all('a', href=lambda x: x and f'/players/{player_id}/matchlogs/' in x 
                    and '/summary/' in x and x.endswith('Match-Logs') and 'nat_tm' not in x)]
    
    all_seasons_df = pd.DataFrame()
    
    # Process each season
    for i, link in enumerate(season_links, 1):
        season_url = "https://fbref.com" + link['href']
        season = link['href'].split('/')[-3]
        
        # Get and parse season page
        response = request(season_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        table = soup.find('div', id='all_matchlogs_all')
        if not table:
            continue
        
        # Convert table to pandas DataFrame and clean
        df = pd.read_html(StringIO(str(table.find('table'))))[0]
        df.columns = get_column_names(table.find('table'))
        
        # Add player and season info
        df['player_id'] = player_id
        df['player_name'] = name
        df['season'] = season
        
        # Filter and clean data
        df = (df[pd.to_datetime(df['date'], errors='coerce').notna()] 
              .assign(minutes=lambda x: pd.to_numeric(x['minutes'], errors='coerce').fillna(0)).query('minutes > 0'))
        
        df = clean_team_names(df)
        df = df[df['comp'].isin(VALID_COMPETITIONS)]
        
        # Add valid matches to main DataFrame
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            all_seasons_df = pd.concat([all_seasons_df, df])
    
    # Process complete DataFrame
    if not all_seasons_df.empty:
        all_seasons_df = all_seasons_df.drop_duplicates(subset=['date', 'opponent', 'comp', 'minutes'], keep='first')
        all_seasons_df = all_seasons_df.sort_values('date').reset_index(drop=True)
        
        print(f"✓ {name}: {len(all_seasons_df)} matches | {all_seasons_df['minutes'].sum():.0f} mins")
        print(f"  Range: {all_seasons_df['date'].min().strftime('%Y-%m-%d')} to {all_seasons_df['date'].max().strftime('%Y-%m-%d')}")
    
    return all_seasons_df

def calculate_stats(df):
    """
    Calculate overall stats for each player from their match logs.
    """
    if df.empty:
        return None
    
    # Basic metrics
    total_minutes = df['minutes'].sum()
    total_90s = total_minutes / 90 # Convert minutes to 90 minutes periods
    
    # Stats dictionary with metrics
    stats = {
        'player_name': df['player_name'].iloc[0],
        'total_minutes': total_minutes,
        'total_matches': len(df),
        'total_90s': round(total_90s, 2),
        'seasons_played': df['season'].nunique()
    }
    
    # Calculate per-90 stats for each metric
    for stat in STATS_FOR_PER90:
        if stat in df.columns:
            total = df[stat].astype(float).sum()

            # Calculate per-90 and total stats
            stats[f'{stat}_per90'] = round(total / total_90s, 2) if total_90s > 0 else 0
            stats[f'total_{stat}'] = round(total, 2)
    
    return stats

def calculate_period_stats(df, start_date=None, end_date=None, last_n_matches=None, min_minutes=None):
    """
    Calculate stats for a specific period or number of matches.
    """
    if df.empty:
        return None
        
    period_df = df.copy()
    
    # Filter data for specified date range
    if start_date:
        period_df = period_df[period_df['date'] >= pd.to_datetime(start_date)]
    if end_date:
        period_df = period_df[period_df['date'] <= pd.to_datetime(end_date)]
    
    if period_df.empty:
        return None
    
    # Calculate metrics for the period
    total_minutes = period_df['minutes'].sum()
    total_90s = total_minutes / 90
    
    stats = {
        'player_name': period_df['player_name'].iloc[0],
        'date': pd.to_datetime(end_date).strftime('%Y-%m-%d')
    }
    
    # Calculate per-90 stats
    for stat in STATS_FOR_PER90:
        if stat in period_df.columns:
            total = period_df[stat].astype(float).sum()
            stats[f'{stat}_per90'] = round(total / total_90s, 2) if total_90s > 0 else 0
    
    if all(x in period_df.columns for x in ['goals', 'assists']):
        total_gc = period_df['goals'].astype(float).sum() + period_df['assists'].astype(float).sum()
        stats['goal_contributions_per90'] = round(total_gc / total_90s, 2) if total_90s > 0 else 0
    
    if all(x in period_df.columns for x in ['passes_comp', 'passes']):
        total_passes = period_df['passes'].astype(float).sum()
        if total_passes > 0:
            completion = (period_df['passes_comp'].astype(float).sum() / total_passes) * 100
            stats['pass_completion_pct'] = round(completion, 1)
    
    return stats

# Analyze player statistics across time periods
def analyze_player_periods(player_df, periods):
    period_stats = []
    
    for period in periods:
        stats = calculate_period_stats(
            player_df,
            start_date=period.get('start_date'),
            end_date=period.get('end_date'),
            last_n_matches=period.get('last_n_matches'),
            min_minutes=period.get('min_minutes')
        )
        
        if stats:
            period_stats.append(stats)
    
    return period_stats

def create_analysis_periods(dates, first_match_date):
    periods = []
    sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, '%b %d, %Y'))
    
    first_date = datetime.strptime(sorted_dates[0], '%b %d, %Y')
    periods.append({
        'name': first_date.strftime('%Y-%m-%d'),
        'start_date': first_match_date.strftime('%Y-%m-%d'),
        'end_date': first_date.strftime('%Y-%m-%d')
    })
    
    for i in range(1, len(sorted_dates)):
        start_date = datetime.strptime(sorted_dates[i-1], '%b %d, %Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(sorted_dates[i], '%b %d, %Y').strftime('%Y-%m-%d')
        periods.append({
            'name': end_date,
            'start_date': start_date,
            'end_date': end_date
        })
    
    return periods

PLAYERS = [
    {"id": "82ec26c1", "name": "Lamine-Yamal"},
    {"id": "19cae58d", "name": "Gavi"},
    {"id": "cc7888f3", "name": "Pau-Cubarsi"},
    {"id": "ae44e8e2", "name": "Dani-Olmo"},
    {"id": "5ccc9672", "name": "Alejandro-Balde"},
    {"id": "c1fe5f0b", "name": "Fermin-Lopez"},
    {"id": "2ef08833", "name": "Marc-Casado"},
    {"id": "2bed3eab", "name": "Eric-Garcia"},
    {"id": "cc1c5035", "name": "Inaki-Pena"},
    {"id": "0ba976e4", "name": "Ansu-Fati"},
    {"id": "2e31f3a6", "name": "Hector-Fort"},
    {"id": "29117812", "name": "Marc-Bernal"},
    {"id": "bc7dc64d", "name": "Bukayo-Saka"},
    {"id": "7f94982c", "name": "Ethan-Nwaneri"},
    {"id": "5dff6c28", "name": "Myles-Lewis-Skelly"}
]

PLAYER_ANALYSIS_DATES = {
    "Lamine-Yamal": [
        "Aug 21, 2023", "Oct 13, 2023", "Dec 22, 2023", "Mar 21, 2024", "Jun 7, 2024", "Jul 18, 2024", "Oct 11, 2024", "Dec 27, 2024"
    ],
    "Gavi": [
        "Oct 13, 2021", "Dec 30, 2021", "Mar 21, 2022", "Jun 3, 2022", "Sep 23, 2022", "Nov 7, 2022", "Jun 13, 2023", "Dec 22, 2023", 
        "Jun 7, 2024", "Dec 27, 2024"
    ],
    "Pau-Cubarsi": [
        "Oct 13, 2023", "Dec 20, 2023", "Mar 21, 2024", "Jun 7, 2024", "Oct 11, 2024", "Dec 27, 2024"
    ],
    "Dani-Olmo": [ 
        "Mar 17, 2015", "Sep 14, 2015", "Mar 14, 2016", "Sep 14, 2016", "Mar 13, 2017", "Oct 23, 2017", "Mar 18, 2018", "Sep 25, 2018", 
        "Mar 11, 2019", "Sep 16, 2019", "Dec 27, 2019", "Apr 8, 2020", "Nov 26, 2020", "Feb 10, 2021", "May 31, 2021", "Jul 15, 2021", 
        "Dec 22, 2021", "Mar 24, 2022", "Jun 9, 2022", "Nov 9, 2022", "Jun 22, 2023", "Oct 18, 2023", "Dec 14, 2023", "May 29, 2024", 
        "Jul 18, 2024", "Dec 27, 2024"
    ],
    "Alejandro-Balde": [
        "Oct 8, 2020",  "Jan 8, 2021", "Jun 30, 2021", "Oct 13, 2021", "Dec 30, 2021", "Jun 3, 2022", "Jun 29, 2023", "Sep 23, 2022", 
        "Nov 7, 2022", "Mar 23, 2023", "Jun 13, 2023", "Dec 22, 2023", "Mar 21, 2024", "Jun 7, 2024", "Dec 27, 2024"
    ],
    "Fermin-Lopez": [
        "Sep 26, 2022", "Dec 29, 2022", "Jun 30, 2023", "Oct 13, 2023", "Dec 22, 2023", "Jun 7, 2024", "Oct 11, 2024", "Dec 27, 2024"
    ],
    "Marc-Casado": [
        "Sep 26, 2022", "Dec 29, 2022", "Jun 30, 2023", "Dec 20, 2023", "Mar 26, 2024", "Jun 24, 2024", "Oct 11, 2024", "Dec 27, 2024"
    ],
    "Eric-Garcia": [
        "Sep 25, 2019", "Apr 8, 2020", "Jul 30, 2020", "Oct 13, 2020", "Mar 18, 2021", "May 31, 2021", "Dec 30, 2021", "Jun 3, 2022", 
        "Nov 7, 2022", "Mar 23, 2023", "Jun 13, 2023", "Oct 13, 2023", "Dec 22, 2023", "Jun 7, 2024", "Dec 27, 2024"
    ],
    "Inaki-Pena": [
        "Sep 3, 2018", "Feb 19, 2019", "Jun 29, 2019", "Sep 10, 2019", "Feb 11, 2020", "Apr 8, 2020", "Oct 8, 2020", "Jan 8, 2021", 
        "Jun 10, 2021", "Dec 30, 2021", "Mar 31, 2022", "Jun 1, 2022", "Nov 7, 2022", "Jun 13, 2023", "Dec 22, 2023", "Jun 7, 2024", 
        "Dec 27, 2024"
    ],
    "Ansu-Fati": [
        "Sep 10, 2019", "Dec 20, 2019", "Apr 8, 2020", "Jul 23, 2020", "Oct 8, 2020", "Jan 5, 2021", "Jun 10, 2021", "Dec 30, 2021", 
        "Jun 3, 2022", "Nov 7, 2022", "Mar 23, 2023", "Jun 13, 2023", "Dec 19, 2023", "May 27, 2024", "Oct 11, 2024", "Dec 27, 2024"
    ],
    "Hector-Fort": [
        "Sep 11, 2023", "Oct 13, 2023", "Dec 20, 2023", "Mar 21, 2024", "Jun 7, 2024", "Dec 27, 2024"
    ],
    "Marc-Bernal": [
        "Sep 12, 2023", "Dec 20, 2023", "Jun 24, 2024", "Oct 11, 2024", "Dec 27, 2024"
    ],
    "Bukayo-Saka": [
        "Sep 23, 2019", "Dec 10, 2019", "Mar 9, 2020", "Apr 8, 2020", "Jul 30, 2020", "Oct 13, 2020", "Mar 18, 2021", "May 28, 2021", 
        "Dec 23, 2021", "Jun 15, 2022", "Sep 15, 2022", "Nov 3, 2022", "Dec 23, 2022", "Mar 16, 2023", "Jun 20, 2023", "Dec 19, 2023", 
        "Mar 14, 2024", "May 27, 2024", "Dec 16, 2024"
    ],
    "Ethan-Nwaneri": [
        "Dec 19, 2023", "Mar 14, 2024", "Oct 1, 2024", "Dec 16, 2024"
    ],
    "Myles-Lewis-Skelly": [
        "Dec 19, 2023", "Oct 1, 2024", "Dec 16, 2024"
    ]
}

def process_player_periods(player_data, dates):
    print(f"\nProcessing {player_data['name']}'s performance periods...")
    
    try:
        matches_df = scrape_player_matches(player_data['id'], player_data['name'])
        
        if not matches_df.empty:
            cols = ['player_name'] + [col for col in matches_df.columns 
                                    if col not in ['player_name', 'match_report', 'player_id']]
            matches_df = matches_df[cols]
            
            first_match_date = pd.to_datetime(matches_df['date'].min())
            
            stats_df = pd.DataFrame(
                analyze_player_periods(
                    matches_df, 
                    create_analysis_periods(dates, first_match_date)
                )
            )
            
            print(f"Analyzed {len(stats_df)} periods for {player_data['name']}")
            return matches_df, stats_df
            
    except Exception as e:
        print(f"Error processing {player_data['name']}'s data: {e}")
    return None, None

if __name__ == "__main__":
        results = {
        'matches': [],
        'stats': []
    }
    
    for player in [p for p in PLAYERS if p['name'] in PLAYER_ANALYSIS_DATES]:
        matches_df, stats_df = process_player_periods(
            player, 
            PLAYER_ANALYSIS_DATES[player['name']]
        )
        
        if matches_df is not None:
            results['matches'].append(matches_df)
        if stats_df is not None:
            results['stats'].append(stats_df)
    
    if results['matches']:
        all_matches = pd.concat(results['matches'], ignore_index=True)
        all_matches.to_csv("all_players_matches.csv", index=False)
        print(f"\nSaved {len(all_matches)} matches to all_players_matches.csv")
    
    if results['stats']:
        all_stats = pd.concat(results['stats'], ignore_index=True)
        all_stats.to_csv("all_players_per90_stats.csv", index=False)
        print(f"Saved {len(all_stats)} analysis periods to all_players_per90_stats.csv")
    
    print("\nProcessing complete!")
    print(f"Total players processed: {len([p for p in PLAYERS if p['name'] in PLAYER_ANALYSIS_DATES])}")