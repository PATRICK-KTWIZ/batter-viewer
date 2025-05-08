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
    # 데이터가 비어있는지 확인
    if player_df.empty:
        return pd.DataFrame()  # 빈 데이터프레임 반환
    
    # 기본 통계 계산
    merged_base_df = base_df(player_df)
    
    # 통계 데이터프레임이 비어있는지 확인
    if merged_base_df.empty:
        return pd.DataFrame()  # 빈 데이터프레임 반환
    
    # 통계 계산
    stats_output_df = stats_df(merged_base_df)
    
    # 연도 정보 확인 및 추출
    try:
        # game_date에서 연도 추출
        if 'game_date' in stats_output_df.columns:
            # 데이터 타입에 따라 연도 추출 방식 결정
            if stats_output_df['game_date'].dtype == 'object':
                stats_output_df['year'] = stats_output_df['game_date'].str[:4].astype(int)
            else:
                stats_output_df['year'] = stats_output_df['game_date'].dt.year
            
            # 2023년 이상 데이터만 필터링
            year_filter = stats_output_df['year'] >= 2023
            filtered_df = stats_output_df[year_filter]
            
            # 필터링 후 데이터가 없는 경우 빈 데이터프레임 반환
            if filtered_df.empty:
                return pd.DataFrame()
            
            # 존재하는 연도 확인 (내림차순 정렬)
            existing_years = sorted(filtered_df['year'].unique())
            
            # 연도별로 그룹화하고 첫 번째 행 선택
            result_dfs = []
            for year in existing_years:
                year_data = filtered_df[filtered_df['year'] == year].iloc[0:1]
                if not year_data.empty:
                    result_dfs.append(year_data)
            
            # 결과 데이터프레임 병합
            if result_dfs:
                result_df = pd.concat(result_dfs)
                # 연도를 인덱스로 설정
                result_df = result_df.set_index('year')
                return result_df
            else:
                return pd.DataFrame()
        else:
            # game_date 컬럼이 없는 경우
            return stats_output_df
    except Exception as e:
        print(f"연도별 데이터 처리 중 오류 발생: {e}")
        return stats_output_df  # 오류 발생 시 원본 데이터 반환


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
    # 데이터가 비어있는지 확인
    if player_df.empty:
        return pd.DataFrame()  # 빈 데이터프레임 반환
    
    # 2023년 이상 데이터만 필터링 (데이터가 있는 경우에만)
    if 'game_year' in player_df.columns:
        year = player_df['game_year'] >= 2023
        inplay_df = player_df[year]
        
        # 필터링 후 데이터가 없는 경우 빈 데이터프레임 반환
        if inplay_df.empty:
            return pd.DataFrame()
    else:
        return pd.DataFrame()  # game_year 컬럼이 없으면 빈 데이터프레임 반환
    
    # 필요한 컬럼이 모두 있는지 확인하고 안전하게 피벗 테이블 생성
    dfs = {}
    
    # 각 피벗 테이블을 안전하게 생성
    try:
        if 'events' in inplay_df.columns and 'pitch_name' in inplay_df.columns:
            dfs['pitched'] = inplay_df.groupby(['game_year']).apply(
                lambda x: x.pivot_table(index='events', values='pitch_name', aggfunc='count', margins=True)
            )
    except:
        dfs['pitched'] = pd.DataFrame()
        
    try:
        if 'events' in inplay_df.columns and 'rel_speed(km)' in inplay_df.columns:
            dfs['rel_speed'] = inplay_df.groupby(['game_year']).apply(
                lambda x: x.pivot_table(index='events', values='rel_speed(km)', aggfunc='mean', margins=True)
            )
    except:
        dfs['rel_speed'] = pd.DataFrame()
        
    try:
        if 'events' in inplay_df.columns and 'inplay' in inplay_df.columns:
            dfs['inplay'] = inplay_df.groupby(['game_year']).apply(
                lambda x: x.pivot_table(index='events', values='inplay', aggfunc='count', margins=True)
            )
    except:
        dfs['inplay'] = pd.DataFrame()
        
    try:
        if 'events' in inplay_df.columns and 'exit_velocity' in inplay_df.columns:
            dfs['exit_velocity'] = inplay_df.groupby(['game_year']).apply(
                lambda x: x.pivot_table(index='events', values='exit_velocity', aggfunc='mean', margins=True)
            )
    except:
        dfs['exit_velocity'] = pd.DataFrame()
        
    try:
        if 'events' in inplay_df.columns and 'launch_angleX' in inplay_df.columns:
            dfs['launch_angleX'] = inplay_df.groupby(['game_year']).apply(
                lambda x: x.pivot_table(index='events', values='launch_angleX', aggfunc='mean', margins=True)
            )
    except:
        dfs['launch_angleX'] = pd.DataFrame()
        
    try:
        if 'events' in inplay_df.columns and 'hit_spin_rate' in inplay_df.columns:
            dfs['hit_spin_rate'] = inplay_df.groupby(['game_year']).apply(
                lambda x: x.pivot_table(index='events', values='hit_spin_rate', aggfunc='mean', margins=True)
            )
    except:
        dfs['hit_spin_rate'] = pd.DataFrame()
        
    try:
        if 'events' in inplay_df.columns and 'hit_distance' in inplay_df.columns:
            dfs['hit_distance'] = inplay_df.groupby(['game_year']).apply(
                lambda x: x.pivot_table(index='events', values='hit_distance', aggfunc='mean', margins=True)
            )
    except:
        dfs['hit_distance'] = pd.DataFrame()
    
    # 모든 데이터프레임이 비어있는지 확인
    if all(df.empty for df in dfs.values()):
        return pd.DataFrame()
    
    # 비어있지 않은 데이터프레임만 concat
    non_empty_dfs = [df for df in dfs.values() if not df.empty]
    if not non_empty_dfs:
        return pd.DataFrame()
    
    season_events = pd.concat(non_empty_dfs, axis=1)
    
    # 필요한 컬럼만 선택 (존재하는 경우에만)
    columns_to_select = []
    for col in ['pitch_name', 'exit_velocity', 'launch_angleX', 'hit_spin_rate', 'hit_distance']:
        if col in season_events.columns:
            columns_to_select.append(col)
    
    if not columns_to_select:
        return pd.DataFrame()
    
    season_events = season_events[columns_to_select]
    
    # 반올림 (존재하는 컬럼에만 적용)
    round_cols = {
        'rel_speed(km)': 1, 
        'exit_velocity': 1, 
        'launch_angleX': 1, 
        'hit_spin_rate': 0, 
        'hit_distance': 1
    }
    
    for col, decimal in round_cols.items():
        if col in season_events.columns:
            season_events[col] = season_events[col].round(decimal)
    
    # 인덱스 재정렬 (존재하는 연도와 이벤트만)
    try:
        # 존재하는 연도만 필터링
        existing_years = sorted(inplay_df['game_year'].unique(), reverse=True)
        if existing_years:
            season_events = season_events.reindex(existing_years, level='game_year')
        
        # 존재하는 이벤트만 필터링
        event_types = ['single', 'double', 'triple', 'home_run', 'field_out']
        existing_events = [event for event in event_types if event in inplay_df['events'].unique()]
        if existing_events:
            season_events = season_events.reindex(existing_events, level='events')
    except:
        # 인덱스 재정렬에 실패한 경우 처리하지 않고 계속 진행
        pass
    
    # 인덱스 리셋 및 컬럼명 변경
    try:
        season_events = season_events.reset_index()
        if 'game_year' in season_events.columns:
            season_events = season_events.astype({'game_year': 'str'})
            season_events = season_events.rename(columns={'game_year': '연도'})
    except:
        # 오류 발생 시 현재 상태 그대로 반환
        pass
    
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

        period_events=period_events.rename(index={2025:'2 Weeks'})
        period_events = period_events.reset_index()

        return period_events
    
    else:

        period_events = pd.DataFrame({'game_year':['2 Weeks'],'pitch_name':['-'], 'exit_velocity':['-'],'launch_angleX':['-'],'hit_spin_rate':['-'],'hit_distance':['-']})
        
        return period_events



def season_pthrows(player_df):

    season = player_df['game_year'] >= 2023
    sdf = player_df[season]

    pivot_index = 'p_throws'

    merged_base_df = pivot_base_df(sdf,pivot_index)
    season_pthrows_df = stats_df(merged_base_df)

    season_pthrows_df = season_pthrows_df.reindex([2025, 2024, 2023], level='game_year')
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

        period_pthrows_df=period_pthrows_df.rename(index={2025:'2 Weeks'})
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

    season = player_df['game_year'] >= 2023
    sdf = player_df[season]

    pivot_index = 'p_kind'

    merged_base_df = pivot_base_df(sdf,pivot_index)
    season_pkind_df = stats_df(merged_base_df)

    season_pkind_df = season_pkind_df.reindex([2025, 2024, 2023], level='game_year')
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

        period_pkind_df=period_pkind_df.rename(index={2025:'2 Weeks'})
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

    season = player_df['game_year'] >= 2023
    sdf = player_df[season]

    pivot_index = 'pitch_name'

    merged_base_df = pivot_base_df(sdf,pivot_index)
    season_pitchname_df = stats_df(merged_base_df)

    season_pitchname_df = season_pitchname_df.reindex([2025, 2024, 2023], level='game_year')
    season_pitchname_df = season_pitchname_df.reindex(['4-Seam Fastball','2-Seam Fastball','Cutter','Slider','Curveball','Changeup','Split-Finger'], level='pitch_name')

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

        period_pitchname_df = period_pitchname_df.reindex(['4-Seam Fastball','2-Seam Fastball','Cutter','Slider','Curveball','Changeup','Split-Finger'], level='pitch_name')
        
        period_pitchname_df=period_pitchname_df.rename(index={2025:'2 Weeks'})
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

    called_strike_df = dataframe[(dataframe['game_year'] >= 2023)  & (dataframe['description'] == "called_strike")]
    called_strike_df['swingmap'] = 'Called_Strike'
    whiff_df = dataframe[(dataframe['game_year'] >= 2023)  & (dataframe['whiff'] == 1)]
    whiff_df['swingmap'] = 'Whiff'
    ball_df = dataframe[(dataframe['game_year'] >= 2023)  & (dataframe['type'] == "B")]
    ball_df['swingmap'] = 'Ball'
    foul_df = dataframe[(dataframe['game_year'] >= 2023)  & (dataframe['foul'] == 1)]
    foul_df['swingmap'] = 'Foul'
    hit_df = dataframe[(dataframe['game_year'] >= 2023)  & (dataframe['hit'] == 1)]
    hit_df['swingmap'] = 'HIT'
    out_df = dataframe[(dataframe['game_year'] >= 2023)  & (dataframe['field_out'] == 1)]
    out_df['swingmap'] = 'Out'

    swingmap_dataframe = pd.concat([called_strike_df, whiff_df, ball_df, foul_df, hit_df, out_df])

    return swingmap_dataframe



def spraychart_df(dataframe):

    year = dataframe['game_year'] >= 2023
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

