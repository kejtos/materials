import polars as pl
import numpy as np
from datetime import datetime


PLAYER_PATH = r'C:\Users\rejth\OneDrive - kejtos\Connection\Plocha\Doktorát\Choking under pressure\final_dataset.csv' # final dataset has correct elimination_match and groups dummy
ON_OFF_PATH = r'C:\Users\rejth\OneDrive - kejtos\Connection\Plocha\Doktorát\Choking under pressure\events_on_off.csv'


TEAMS_PATH = r'C:\Users\rejth\OneDrive - kejtos\Connection\Plocha\Doktorát\Choking under pressure\final_data.csv'
BRACKET_PATH = r'C:\Users\rejth\OneDrive - kejtos\Connection\Plocha\Doktorát\Choking under pressure\event_results_processed.csv'
RANKINGS = r'C:\Users\rejth\OneDrive - kejtos\Connection\Plocha\Doktorát\Choking under pressure\all_team_rankings.csv'


events_lan = (
    pl.read_csv(ON_OFF_PATH, encoding='utf8')
    .drop('Event', 'Number_of_teams', 'Prizepool')
    .rename({'Team_url':'Event_id', 'Online_offline':'Offline'})
    .with_columns(
        pl.col('Event_id').str.split('/').list.get(-2).cast(pl.Int64),
        pl.col('Offline').cast(pl.Categorical).name.keep()
    )
    .filter(pl.col('Offline') != 'Other')
    .with_columns(
        Offline=(
            pl.when(pl.col('Offline') == 'Online')
            .then(pl.lit(0))
            .otherwise(pl.lit(1))
        )
    )
)

experience = (
    pl.read_csv(PLAYER_PATH)
    .with_columns(
        pl.col('Date').cast(pl.Date).name.keep()
    )
    .filter(
        (pl.col('Side') == 'Both') &
        (pl.col('Rating') > 0) &
        (pl.col('Map') == 'All maps')
    )
    .unique(['Event_id', 'Player_id'])
    .sort('Player_id', 'Date', 'Event_id', descending=False)
    .with_columns(
        Number_of_events=pl.col('Event_id').cum_count().over('Player_id')
    )
    .select('Event_id', 'Player_id', 'Number_of_events')
)

players = (
    pl.read_csv(PLAYER_PATH)
    .sort('Player_id', 'Date')
    .with_columns(pl.col('Date').cast(pl.Date).name.keep())
    .filter(
        (pl.col('Side') == 'Both') &
        (pl.col('Rating') > 0) &
        (pl.col('Map') == 'All maps') &
        (pl.col('2.0') == 1) &
        (pl.col('Groups_dummy') == 0) &
        ~(
            (pl.col('Team_id') == 7801) &
            (pl.col('Match_id') == 2329064) &
            (pl.col('Player_id') == 7382) &
            (pl.col('Date') == datetime(2018, 11, 18)) &
            (pl.col('Rating') == 0.92)
        )
    )
    .select('Date', 'Points', 'Event_id', 'Team_id', 'Player_id', 'Match_id', 'Year', 'Rating', 'Enemy_id', 'Enemy_points', 'Elimination_match', 'Rounds_to_end', 'Team_rank', 'Enemy_rank')
    .unique(['Match_id', 'Player_id'])
    .join(
        events_lan,
        'Event_id',
        'inner'
    )
    .join(
        experience,
        ['Event_id', 'Player_id'],
        'inner'
    )
    .join(
        pl.read_csv(TEAMS_PATH, encoding='utf8').select('Event_id', 'Prizepool').unique('Event_id'),
        on='Event_id',
        how='inner'
    )
    .drop_nulls()
    .filter(
        (pl.col('Prizepool') > 10000) &
        (pl.col('Rounds_to_end') > 7)
    )
    .rename({
        'Rounds_to_end': 'Stage'
    })
    .with_columns(Stage = (pl.col('Stage') - 7))
    .filter(pl.col('Player_id').is_in([17145, 15940, 9798, 6904, 13466, 11343]))
)

players.group_by('Stage').count()
players.write_csv('players_analysis.csv')
