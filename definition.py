import pandas as pd
from datetime import timedelta
from dataframe import dataframe, base_df, stats_df, pivot_base_df

def select_league(option):

    if option == "KBO(1군)":
        league = "'KoreaBaseballOrganization'"
        return league
    elif option == "KBO(2군)":
        league = "'KBO Minors'"
        return league
    elif option == "AAA(마이너)":
        league =  "'aaa'"
        return league
    elif option == "KBA(아마)":
        league =  "'TeamExclusive'"
        return league
    else:
        league == "'KoreaBaseballOrganization'"
        return league

def stats(player_df):

    merged_base_df = base_df(player_df)
    stats_output_df = stats_df(merged_base_df)
    
    season_stats_df = stats_output_df.reindex([2024, 2023, 2022])

    return season_stats_df


def period_stats(player_df):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    sdf = player_df[(player_df['game_date'] >= date1) & (player_df['game_date'] <= date2)]

    if len(sdf) > 0:
        merged_base_df = base_df(sdf)
        period_stats_df = stats_df(merged_base_df)

        period_stats_df = period_stats_df.reset_index()
        period_stats_df.at[0, 'game_year'] = '2 Weeks'
        period_stats_df = period_stats_df.set_index('game_year')
        return period_stats_df

    else:
        period_stats_df = base_df(player_df)
        period_stats_df = period_stats_df.head(1)
        period_stats_df = stats_df(period_stats_df)
        period_stats_df = period_stats_df.reset_index()
        period_stats_df.iloc[0] = '-'
        period_stats_df.at[0, 'game_year'] = '2 Weeks'
        period_stats_df = period_stats_df.set_index('game_year')
        return period_stats_df


def seoson_inplay_events(player_df):

    year = player_df['game_year'] >= 2022
    inplay_df = player_df[year]

    pitched = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='pitch_name', aggfunc='count', margins=True))
    rel_speed = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='rel_speed(km)', aggfunc='mean', margins=True))
    inplay = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='inplay', aggfunc='count', margins=True))
    exit_velocity = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='exit_velocity', aggfunc='mean', margins=True))
    launch_angleX = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='launch_angleX', aggfunc='mean', margins=True))
    hit_spin_rate = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='hit_spin_rate', aggfunc='mean', margins=True))
    hit_distance = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='hit_distance', aggfunc='mean', margins=True))

    season_events = pd.concat([pitched, rel_speed, inplay,exit_velocity,launch_angleX,hit_spin_rate, hit_distance], axis=1)

    season_events = season_events[['pitch_name', 'exit_velocity','launch_angleX','hit_spin_rate','hit_distance']]
    season_events = season_events.round({'rel_speed(km)':1, 'exit_velocity':1, 'launch_angleX':1, 'hit_spin_rate':0, 'hit_distance':1 })

    season_events = season_events.reindex([2024, 2023, 2022, 2021, 2020, 2018], level='game_year')
    season_events = season_events.reindex(['single','double','triple','home_run','field_out'], level='events')

    season_events = season_events.reset_index()
    season_events = season_events.astype({'game_year':'str'})

    return season_events


def period_inplay_events(player_df):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    inplay_df = player_df[(player_df['game_date'] >= date1) & (player_df['game_date'] <= date2)]

    if len(inplay_df) > 0:

        pitched = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='pitch_name', aggfunc='count', margins=True))
        rel_speed = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='rel_speed(km)', aggfunc='mean', margins=True))
        inplay = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='inplay', aggfunc='count', margins=True))
        exit_velocity = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='exit_velocity', aggfunc='mean', margins=True))
        launch_angleX = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='launch_angleX', aggfunc='mean', margins=True))
        hit_spin_rate = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='hit_spin_rate', aggfunc='mean', margins=True))
        hit_distance = inplay_df.groupby(['game_year']).apply(lambda x: x.pivot_table(index='events', values='hit_distance', aggfunc='mean', margins=True))

        period_events = pd.concat([pitched, rel_speed, inplay,exit_velocity,launch_angleX,hit_spin_rate, hit_distance], axis=1)

        period_events = period_events[['pitch_name', 'exit_velocity','launch_angleX','hit_spin_rate','hit_distance']]
        period_events = period_events.round({'rel_speed(km)':1, 'exit_velocity':1, 'launch_angleX':1, 'hit_spin_rate':0, 'hit_distance':1 })
        period_events = period_events.reindex(['single','double','triple','home_run','field_out'], level='events')

        period_events=period_events.rename(index={2024:'2 Weeks'})
        period_events = period_events.reset_index()

        return period_events
    
    else:

        period_events = pd.DataFrame({'game_year':['2 Weeks'],'pitch_name':['-'], 'exit_velocity':['-'],'launch_angleX':['-'],'hit_spin_rate':['-'],'hit_distance':['-']})
        
        return period_events



def season_pthrows(player_df):

    season = player_df['game_year'] >= 2022
    sdf = player_df[season]

    pivot_index = 'p_throws'

    merged_base_df = pivot_base_df(sdf,pivot_index)
    season_pthrows_df = stats_df(merged_base_df)

    season_pthrows_df = season_pthrows_df.reindex([2024, 2023, 2022], level='game_year')
    season_pthrows_df = season_pthrows_df.reindex(['R','L','S'], level='p_throws')

    season_pthrows_df = season_pthrows_df.reset_index()
    season_pthrows_df = season_pthrows_df.astype({'game_year':'str'})

    return season_pthrows_df


def period_pthrows(player_df):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    pivot_index = 'p_throws'
    sdf = player_df[(player_df['game_date'] >= date1) & (player_df['game_date'] <= date2)]

    if len(sdf) > 0:

        merged_base_df = pivot_base_df(sdf,pivot_index)
        period_pthrows_df = stats_df(merged_base_df)

        period_pthrows_df = period_pthrows_df.reindex(['R','L','S'], level='p_throws')

        period_pthrows_df=period_pthrows_df.rename(index={2024:'2 Weeks'})
        period_pthrows_df = period_pthrows_df.reset_index()

        return period_pthrows_df
    else:

        period_pthrows_df = pivot_base_df(player_df,pivot_index)
        period_pthrows_df = period_pthrows_df.head(1)
        period_pthrows_df = stats_df(period_pthrows_df)
        period_pthrows_df = period_pthrows_df.reset_index()
        period_pthrows_df.iloc[0] = '-'
        period_pthrows_df.at[0, 'game_year'] = '2 Weeks'
        # period_pthrows_df = period_pthrows_df.set_index('game_year')
        return period_pthrows_df


def season_pkind(player_df):

    season = player_df['game_year'] >= 2022
    sdf = player_df[season]

    pivot_index = 'p_kind'

    merged_base_df = pivot_base_df(sdf,pivot_index)
    season_pkind_df = stats_df(merged_base_df)

    season_pkind_df = season_pkind_df.reindex([2024, 2023, 2022], level='game_year')
    season_pkind_df = season_pkind_df.reindex(['Fastball','Breaking','Off_Speed'], level='p_kind')

    season_pkind_df = season_pkind_df.reset_index()
    season_pkind_df = season_pkind_df.astype({'game_year':'str'})

    return season_pkind_df


def period_pkind(player_df):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    pivot_index = 'p_kind'
    sdf = player_df[(player_df['game_date'] >= date1) & (player_df['game_date'] <= date2)]


    if len(sdf) > 0:

        merged_base_df = pivot_base_df(sdf,pivot_index)
        period_pkind_df = stats_df(merged_base_df)

        period_pkind_df = period_pkind_df.reindex(['Fastball','Breaking','Off_Speed'], level='p_kind')

        period_pkind_df=period_pkind_df.rename(index={2024:'2 Weeks'})
        period_pkind_df = period_pkind_df.reset_index()

        return period_pkind_df
    
    else:
        
        period_pkind_df = pivot_base_df(player_df,pivot_index)
        period_pkind_df = period_pkind_df.head(1)
        period_pkind_df = stats_df(period_pkind_df)
        period_pkind_df = period_pkind_df.reset_index()
        period_pkind_df.iloc[0] = '-'
        period_pkind_df.at[0, 'game_year'] = '2 Weeks'

        return period_pkind_df


def season_pitchname(player_df):

    season = player_df['game_year'] >= 2022
    sdf = player_df[season]

    pivot_index = 'pitch_name'

    merged_base_df = pivot_base_df(sdf,pivot_index)
    season_pitchname_df = stats_df(merged_base_df)

    season_pitchname_df = season_pitchname_df.reindex([2024, 2023, 2022], level='game_year')
    season_pitchname_df = season_pitchname_df.reindex(['4-Seam Fastball','2-Seam Fastball','Cutter','Slider','Curveball','Sweeper','Changeup','Split-Finger'], level='pitch_name')

    season_pitchname_df = season_pitchname_df.reset_index()
    season_pitchname_df = season_pitchname_df.astype({'game_year':'str'})

    return season_pitchname_df


def period_pitchname(player_df):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    pivot_index = 'pitch_name'
    sdf = player_df[(player_df['game_date'] >= date1) & (player_df['game_date'] <= date2)]

    if len(sdf) > 0:

        merged_base_df = pivot_base_df(sdf,pivot_index)
        period_pitchname_df = stats_df(merged_base_df)

        period_pitchname_df = period_pitchname_df.reindex(['4-Seam Fastball','2-Seam Fastball','Cutter','Slider','Curveball','Sweeper','Changeup','Split-Finger'], level='pitch_name')
        
        period_pitchname_df=period_pitchname_df.rename(index={2024:'2 Weeks'})
        period_pitchname_df = period_pitchname_df.reset_index()

        return period_pitchname_df
    
    else:
       
        period_pitchname_df = pivot_base_df(player_df,pivot_index)
        period_pitchname_df = period_pitchname_df.head(1)
        period_pitchname_df = stats_df(period_pitchname_df)
        period_pitchname_df = period_pitchname_df.reset_index()
        period_pitchname_df.iloc[0] = '-'
        period_pitchname_df.at[0, 'game_year'] = '2 Weeks'

        return period_pitchname_df

def stats_viewer(dataframe):

    stats_viewer_df = dataframe[['game_date','pa','ab','hit','walk','avg','obp','slg','ops','exit_velocity','launch_angleX','hit_spin_rate']]
    stats_viewer_df = stats_viewer_df.rename(columns={'game_year':'구분','game_date':'경기수','pa':'타석','ab':'타수','hit':'안타','walk':'볼넷','avg':'타율','obp':'출루율','slg':'장타율','ops':'OPS',
                                                        'exit_velocity':'타구속도','launch_angleX':'발사각도','hit_spin_rate':'타구스핀량'})

    return stats_viewer_df

def swing_viewer(dataframe):

    swing_viewer_df = dataframe[['z%','z_swing%','z_con%', 'z_inplay%', 'o%','o_swing%', 'o_con%', 'o_inplay%', 'f_swing%', 'swing%', 'whiff%','inplay_sw',
                                'plus_lsa4', 'approach']]
    swing_viewer_df = swing_viewer_df.rename(columns={'game_year':'구분',
                                                        'z%':'존투구%','z_swing%':'존스윙%','z_con%':'존컨택%', 'z_inplay%':'존인플레이%', 
                                                        'o%':'존외부%','o_swing%':'존외스윙%', 'o_con%':'존외컨택%', 'o_inplay%':'존외인플레이%', 
                                                        'f_swing%':'초구스윙%', 'swing%':'스윙%', 'whiff%':'헛스윙%','inplay_sw':'스윙당인플레이%',
                                                        'plus_lsa4':'LSA 4+', 'approach':'타격 어프로치'})

    return swing_viewer_df


def event_viewer(dataframe):

    event_viewer_df = dataframe[['events','pitch_name', 'exit_velocity','launch_angleX','hit_spin_rate','hit_distance']]
    event_viewer_df = event_viewer_df.rename(columns={'events':'타격결과','pitch_name':'투구수', 'exit_velocity':'타구속도','launch_angleX':'발사각도','hit_spin_rate':'타구스핀량','hit_distance':'비거리'})

    event_viewer_df.loc[event_viewer_df['타격결과'] == 'single', '타격결과'] = '1루타'
    event_viewer_df.loc[event_viewer_df['타격결과'] == 'double', '타격결과'] = '2루타'
    event_viewer_df.loc[event_viewer_df['타격결과'] == 'triple', '타격결과'] = '3루타'
    event_viewer_df.loc[event_viewer_df['타격결과'] == 'home_run', '타격결과'] = '홈런'
    event_viewer_df.loc[event_viewer_df['타격결과'] == 'field_out', '타격결과'] = '필드아웃'

    return event_viewer_df

def stats_viewer_pthrows(dataframe):

    stats_viewer_pthrows_df = dataframe[['p_throws','game_date','pa','ab','hit','walk','avg','obp','slg','ops','exit_velocity','launch_angleX','hit_spin_rate']]
    stats_viewer_pthrows_df = stats_viewer_pthrows_df.rename(columns={'game_year':'구분','p_throws':'투수유형','game_date':'경기수','pa':'타석','ab':'타수','hit':'안타','walk':'볼넷','avg':'타율','obp':'출루율','slg':'장타율','ops':'OPS',
                                                        'exit_velocity':'타구속도','launch_angleX':'발사각도','hit_spin_rate':'타구스핀량'})

    return stats_viewer_pthrows_df

def swing_viewer_pthrows(dataframe):

    swing_viewer_pthrows_df = dataframe[['p_throws','z%','z_swing%','z_con%', 'z_inplay%', 'o%','o_swing%', 'o_con%', 'o_inplay%', 'f_swing%', 'swing%', 'whiff%','inplay_sw',
                                'plus_lsa4', 'approach']]
    swing_viewer_pthrows_df = swing_viewer_pthrows_df.rename(columns={'game_year':'구분','p_throws':'투수유형',
                                                        'z%':'존투구%','z_swing%':'존스윙%','z_con%':'존컨택%', 'z_inplay%':'존인플레이%', 
                                                        'o%':'존외부%','o_swing%':'존외스윙%', 'o_con%':'존외컨택%', 'o_inplay%':'존외인플레이%', 
                                                        'f_swing%':'초구스윙%', 'swing%':'스윙%', 'whiff%':'헛스윙%','inplay_sw':'스윙당인플레이%',
                                                        'plus_lsa4':'LSA 4+', 'approach':'타격 어프로치'})

    return swing_viewer_pthrows_df

# def event_viewer(dataframe):

#     event_viewer_df = dataframe[['events','pitch_name', 'exit_velocity','launch_angleX','hit_spin_rate','hit_distance']]
#     event_viewer_df = event_viewer_df.rename(columns={'events':'타격결과','pitch_name':'투구수', 'exit_velocity':'타구속도','launch_angleX':'발사각도','hit_spin_rate':'타구스핀량','hit_distance':'비거리'})

    return event_viewer_df

def stats_viewer_pkind(dataframe):

    stats_viewer_pkind_df = dataframe[['p_kind','game_date','pa','ab','hit','walk','avg','obp','slg','ops','exit_velocity','launch_angleX','hit_spin_rate']]
    stats_viewer_pkind_df = stats_viewer_pkind_df.rename(columns={'game_year':'구분','p_kind':'구종유형','game_date':'경기수','pa':'타석','ab':'타수','hit':'안타','walk':'볼넷','avg':'타율','obp':'출루율','slg':'장타율','ops':'OPS',
                                                        'exit_velocity':'타구속도','launch_angleX':'발사각도','hit_spin_rate':'타구스핀량'})

    return stats_viewer_pkind_df

def swing_viewer_pkind(dataframe):

    swing_viewer_pkind_df = dataframe[['p_kind','z%','z_swing%','z_con%', 'z_inplay%', 'o%','o_swing%', 'o_con%', 'o_inplay%', 'f_swing%', 'swing%', 'whiff%','inplay_sw',
                                'plus_lsa4', 'approach']]
    swing_viewer_pkind_df = swing_viewer_pkind_df.rename(columns={'game_year':'구분','p_kind':'구종유형',
                                                        'z%':'존투구%','z_swing%':'존스윙%','z_con%':'존컨택%', 'z_inplay%':'존인플레이%', 
                                                        'o%':'존외부%','o_swing%':'존외스윙%', 'o_con%':'존외컨택%', 'o_inplay%':'존외인플레이%', 
                                                        'f_swing%':'초구스윙%', 'swing%':'스윙%', 'whiff%':'헛스윙%','inplay_sw':'스윙당인플레이%',
                                                        'plus_lsa4':'LSA 4+', 'approach':'타격 어프로치'})

    return swing_viewer_pkind_df

def stats_viewer_pitchname(dataframe):

    stats_viewer_pitchname_df = dataframe[['pitch_name','game_date','pa','ab','hit','walk','avg','obp','slg','ops','exit_velocity','launch_angleX','hit_spin_rate']]
    stats_viewer_pitchname_df = stats_viewer_pitchname_df.rename(columns={'game_year':'구분','pitch_name':'세부구종','game_date':'경기수','pa':'타석','ab':'타수','hit':'안타','walk':'볼넷','avg':'타율','obp':'출루율','slg':'장타율','ops':'OPS',
                                                        'exit_velocity':'타구속도','launch_angleX':'발사각도','hit_spin_rate':'타구스핀량'})

    return stats_viewer_pitchname_df

def swing_viewer_pitchname(dataframe):

    swing_viewer_pitchname_df = dataframe[['pitch_name','z%','z_swing%','z_con%', 'z_inplay%', 'o%','o_swing%', 'o_con%', 'o_inplay%', 'f_swing%', 'swing%', 'whiff%','inplay_sw',
                                'plus_lsa4', 'approach']]
    swing_viewer_pitchname_df = swing_viewer_pitchname_df.rename(columns={'game_year':'구분','pitch_name':'세부구종',
                                                        'z%':'존투구%','z_swing%':'존스윙%','z_con%':'존컨택%', 'z_inplay%':'존인플레이%', 
                                                        'o%':'존외부%','o_swing%':'존외스윙%', 'o_con%':'존외컨택%', 'o_inplay%':'존외인플레이%', 
                                                        'f_swing%':'초구스윙%', 'swing%':'스윙%', 'whiff%':'헛스윙%','inplay_sw':'스윙당인플레이%',
                                                        'plus_lsa4':'LSA 4+', 'approach':'타격 어프로치'})

    return swing_viewer_pitchname_df


def swingmap_df(dataframe):

    called_strike_df = dataframe[(dataframe['game_year'] >= 2022)  & (dataframe['description'] == "called_strike")]
    called_strike_df['swingmap'] = 'Called_Strike'
    whiff_df = dataframe[(dataframe['game_year'] >= 2022)  & (dataframe['whiff'] == 1)]
    whiff_df['swingmap'] = 'Whiff'
    ball_df = dataframe[(dataframe['game_year'] >= 2022)  & (dataframe['type'] == "B")]
    ball_df['swingmap'] = 'Ball'
    foul_df = dataframe[(dataframe['game_year'] >= 2022)  & (dataframe['foul'] == 1)]
    foul_df['swingmap'] = 'Foul'
    hit_df = dataframe[(dataframe['game_year'] >= 2022)  & (dataframe['hit'] == 1)]
    hit_df['swingmap'] = 'HIT'
    out_df = dataframe[(dataframe['game_year'] >= 2022)  & (dataframe['field_out'] == 1)]
    out_df['swingmap'] = 'Out'

    swingmap_dataframe = pd.concat([called_strike_df, whiff_df, ball_df, foul_df, hit_df, out_df])

    return swingmap_dataframe

def spraychart_df(dataframe):

    year = dataframe['game_year'] >= 2022
    xtype = dataframe['type'] == 'X'

    spraychart_dataframe = dataframe[year & xtype]

    walk = spraychart_dataframe['events'].isin(['walk'])
    strikeout = spraychart_dataframe['events'].isin(['strikeout'])
    hit_by_pitch = spraychart_dataframe['events'].isin(['hit_by_pitch'])

    spraychart_dataframe = spraychart_dataframe[~walk]
    spraychart_dataframe = spraychart_dataframe[~strikeout]
    spraychart_dataframe = spraychart_dataframe[~hit_by_pitch]

    spraychart_dataframe = spraychart_dataframe[spraychart_dataframe['events'].notnull()]
    spraychart_dataframe = spraychart_dataframe[spraychart_dataframe['groundX'].notnull()]
    spraychart_dataframe = spraychart_dataframe[spraychart_dataframe['groundY'].notnull()]

    return spraychart_dataframe
