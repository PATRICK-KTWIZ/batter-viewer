import streamlit as st
import pandas as pd
from definition import select_league, stats, seoson_inplay_events, season_pthrows, stats_viewer_pkind, swing_viewer_pkind, swing_viewer_pitchname
from definition import season_pkind, stats_viewer, swing_viewer, stats_viewer_pthrows, swing_viewer_pthrows, spraychart_df
from dataframe import dataframe
from map import season_spraychart, factor_year_count_map, factor_year_sum_map, swingmap_count_map, season_hangtime_spraychart, zone_spraychart_fig, factor_year_sum_map_scatter, factor_year_sum_plate_map_scatter, swingmap_count_map_scatter
import time
from PIL import Image
from user import login
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from streamlit.components.v1 import html

# Set a unique token for the cookie
COOKIE_TOKEN = "my_unique_cookie_token"

# 페이지 설정
st.set_page_config(
    layout="wide",
    # initial_sidebar_state="collapsed",
    page_title="KT WIZ BATTING ANALYTICS"
)

if 'loggedIn' not in st.session_state:
    st.session_state.loggedIn = False

# 로그인 페이지와 메인 페이지를 위한 CSS 스타일 분리
st.markdown("""
<style>
    
    /* 전체 페이지 스타일 */
    .stApp {
        background: linear-gradient(135deg, #2d2d2d 50%, #f0f0f0 50%);
        background-attachment: fixed;
        height: 95vh; /* 뷰포트 높이의 80%로 설정 - 원하는 대로 조정 가능 */
        max-height: 1000px; /* 최대 높이 설정 */
        overflow: auto;
    }

    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background-color: #cccccc !important;
        color: black !important;
        width: 100%;
        border-radius: 7px;  /* 모서리 둥글기 */
        padding: 0.5rem 1rem;  /* 상하 패딩 증가 (0.5rem → 0.8rem) */
        height: 2rem;  /* 버튼 높이 지정 */
        font-size: 16px;  /* 글자 크기 */
        margin-bottom: 0px;  /* 버튼 사이 간격 */
        font-weight: 500;  /* 글자 두께 */
    }

    /* 사이드바 selectbox 라벨 색상 변경 (옅은 회색) */
    [data-testid="stSidebar"] .css-81oif8,
    [data-testid="stSidebar"] .css-1inwz65,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox > div > label {
        color: #ababab !important;
    }

    /* 사이드바 selectbox 내부 텍스트 색상 변경 */
    [data-testid="stSidebar"] .stSelectbox > div > div > div {
        color: black !important;
    }
    
    /* 사이드바 markdowncontainer 내부 텍스트 색상 변경 */
    [data-testid="stSidebar"] button:has([data-testid="stMarkdownContainer"]) {
        color: black !important; 
        font-weight: bold !important;
        font-size: 15px;
    }

    /* 드롭다운 메뉴 텍스트 색상 */
    .stSelectbox option {
        color: black;
    }
  
    /* 헤더 스타일 */
    .header-container {
        padding: 1rem;
        margin: 0;
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -47vw;
        margin-right: -50vw;
        margin-top: -2vw;
    }
    
    /* 로그인 컨테이너 스타일 */
    .login-container {
        max-width: 100px;
        margin: 20px auto;
        padding: 20px;
        background-color: #f0f0f0;
    }
    
    /* 로고 컨테이너 */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* 로그인 폼 스타일 */
    .stTextInput > div > div > input {
        border: 0px solid #ddd;
        padding: 10px;
        border-radius: 0px;
        margin-bottom: 0px;
    }

    /* 메인 버튼 스타일 */
    .stButton > button {
        background-color: #333333;
        color: #c0c0c0;
        width: 100%;
        padding: 10px;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }


    /* 푸터 스타일 */
    .footer {
        text-align: center;
        position: fixed;
        bottom: 60px;
        width: 100%;
        color: #333;
        font-size: 15px;
    }
    /* 로그인 페이지 배경 */
    .login-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #f0f0f0;
        background-size: cover;
        z-index: -1;
    }
    /* 헤더 텍스트 스타일 */
    .header-text {
        font-size: 35px;
        font-weight: bold;
        color: red;
        margin-bottom: 0px;
    }
    /* 서브헤더 텍스트 스타일 */
    .subheader-text {
        color: #c0c0c0;
        font-size: 18px;
        margin-bottom: 10px;
    }
    
    /* 안내 텍스트 스타일 */
    .info-text {
        font-size: 15px;
        color: #666;
    }
        
    /* 경고 텍스트 스타일 */
    .warning-text {
        color: red;
        font-weight: bold;
        margin-bottom: 12px;
        font-size: 16px;
        text-align: right;
    }

</style>
""", unsafe_allow_html=True)


headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()

# Define a function to get the user's ID from the session cookie
def get_user_id():
    return st.session_state.get(COOKIE_TOKEN)

# Define a function to set the user's ID in the session cookie
def set_user_id(user_id):
    st.session_state[COOKIE_TOKEN] = user_id

# Define a function to check if the user is logged in
def is_user_logged_in():
    return st.session_state.get('loggedIn', False)

def find_id(player_dataset, select_player):
    find_player = player_dataset[player_dataset['NAME'] == select_player]
    id = find_player.iloc[0]['TM_ID']
    return id

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
  
def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.sidebar.button("Log Out", key="logout", on_click=LoggedOut_Clicked)

def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        set_user_id(userName)  # Set the user ID in the session cookie
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("유효하지 않은 ID 또는 패스워드 입니다.")

def reset_selections():
    st.session_state.selected_players = []

def show_login_page():

   
    # st.markdown("<h1 style='text-align: left'><span style='color: #c0c0c0;'>KT WIZ</span> <span style='color: red;'>BATTING ANALYTICS</span> <span style='color: #c0c0c0;'>PAGE[Multiple Choice]</span></h1>"
    #             , unsafe_allow_html=True)

    st.markdown("""
    <style>
        /* 특정 컨테이너에 스타일 적용 */
        [data-testid="stVerticalBlock"] > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        /* 컨테이너 내부 제목 스타일 */
        .header-container h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
            line-height: 1.5;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
                <div class="header-container">
                    <h1 class="header-text">
                        <span style='color: #c0c0c0;'>KT WIZ</span> 
                        <span style='color: red;'>BATTING ANALYTICS</span> 
                        <span style='color: #c0c0c0;'>PAGE[Multiple Choice]</span>
                    </h1>
                </div>
                """, unsafe_allow_html=True)

    # Main layout with two columns
    left_col, middle1_col, middle2_col, right_col = st.columns([0.7, 4, 5, 0.7])

    with middle1_col:
        # Logo area
        st.markdown("""
        <div class="logo-container" style="padding-top: 100px;">
        """, unsafe_allow_html=True)
        st.image("ktwiz_emblem.png", width=280)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with middle2_col:
        # Login form container
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="warning-text">※허가된 사용자 외 사용을 금함</div>', unsafe_allow_html=True)

        # Header text
        st.markdown('<div class="header-text">케이티 위즈</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader-text">타자 분석페이지에 오신것을 환영합니다.</div>', unsafe_allow_html=True)
        
        # Horizontal line
        st.markdown('<hr style="margin: 0px 0;">', unsafe_allow_html=True)

        form_col = st.container()
        with form_col:
            userName = st.text_input("", placeholder="아이디", label_visibility="collapsed")
            password = st.text_input("", placeholder="비밀번호", type="password", label_visibility="collapsed")
            st.session_state['password'] = password

            st.markdown("""
            <style>
                [data-testid="element-container"] [data-testid="stButton"][key="login_btn"] button {
                    background-color: #333333 !important;
                    color: #c0c0c0 !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            login_button = st.button("로그인", on_click=LoggedIn_Clicked, args=(userName, password))
        
        st.markdown('</div>', unsafe_allow_html=True)

        # 체크박스와 안내 텍스트를 같은 행에 배치
        checkbox_col1, checkbox_col2 = st.columns([1, 3])
        with checkbox_col1:
            remember_id = st.checkbox("아이디 저장", key="remember_id")
        with checkbox_col2:
            st.markdown('<div class="info-text-custom">아이디와 비밀번호를 입력하여 로그인 후 사용해 주세요.</div>', unsafe_allow_html=True)
    
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Close the login container div
        st.markdown('</div>', unsafe_allow_html=True)

        
   # Footer
    st.markdown("""
    <div class="footer">
        Copyright © 2025 kt wiz baseball club. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

    # 로그인 페이지 클래스 닫기
    st.markdown('</div>', unsafe_allow_html=True)

def show_main_page():
    # Check if the user is logged in
    
    if not is_user_logged_in():
        show_login_page()
        return

    # 메인 페이지 클래스 추가
    st.markdown('<div class="main-page">', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        .stApp {
        background: #ffffff;
        height: 100vh; /* 뷰포트 높이의 80%로 설정 - 원하는 대로 조정 가능 */
        overflow: auto;
    }

    </style>
    """, unsafe_allow_html=True)

    with mainSection:
        
        st.title("KT WIZ :red[BATTING ANALYTICS] PAGE[Multiple Choice]")

        with st.sidebar:
    
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.image("ktwiz_emblem.png", width=300)
    
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

        id_dataset = pd.read_csv('./player_id_info_2025.csv')
        id_dataset = id_dataset[['team','NAME','POS','TM_ID']]
        id_dataset = id_dataset[id_dataset['POS'] != 'P']

        #------------------------------------------------------------------------------

        sidebar_text = '<p style="text-align: center; font-family:sans-serif; color:red; font-size: 22px;font-weight:bold">[타자분석 페이지]</p>'
        st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

        sidebar_text = '<p style="text-align: center; font-family:sans-serif; color: #c0c0c0; font-size: 16px;">본 웹페이지는 kt wiz 전략데이터팀이<br> 개발 및 발행하였으며 허용되는 사용자 외 <br>배포 및 사용을 엄금함</p>'
        st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

        #-------------------------------------------------------------------------

        teams = id_dataset['team'].tolist() 
        teams_list = id_dataset['team'].unique().tolist()
        select_team = st.sidebar.selectbox('팀명 선택', teams_list)
        player_dataset = id_dataset[id_dataset['team'] == select_team]

        player_list = player_dataset['NAME'].unique().tolist()
        select_player = st.sidebar.selectbox('선수 선택', player_list)

        player_id = find_id(player_dataset, select_player)
        
        option = st.sidebar.selectbox('리그 선택', ("-", "KBO(1군)", "KBO(2군)", "AAA","KBA(아마)"))


        # Create a session_state variable to store selected player information
        if 'selected_players' not in st.session_state:
            st.session_state.selected_players = []

        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button('선수추가', key="add_player_btn"):
                st.session_state.selected_players.append({'Team': select_team, 'Player Name': select_player, 'League': option, 'ID': player_id})
     
        with col2:
            if st.button('새로고침', key="refresh_btn"):
                st.session_state.selected_players = []

        selected_player_df = pd.DataFrame()
            # Display the selected player names
        if st.session_state.selected_players:
            st.subheader('Selected Players:')
            for player_info in st.session_state.selected_players:
                st.write(f"Team: {player_info['Team']}, Player Name: {player_info['Player Name']}, League: {player_info['League']}, ID: {player_info['ID']}")

                select_player_df = id_dataset[ (id_dataset['team'] == player_info['Team']) & (id_dataset['TM_ID'] == player_info['ID']) ]
                selected_player_df = pd.concat([selected_player_df, select_player_df])
        

        # if st.sidebar.button('선수추가'):
        #     st.session_state.selected_players.append({'Team': select_team, 'Player Name': select_player, 'League': option, 'ID' : player_id})

        # selected_player_df = pd.DataFrame()
        # # Display the selected player names
        # if st.session_state.selected_players:
        #     st.subheader('Selected Players:')
        #     for player_info in st.session_state.selected_players:
        #         st.write(f"Team: {player_info['Team']}, Player Name: {player_info['Player Name']}, League: {player_info['League']}, ID: {player_info['ID']}")

        #         select_player_df = id_dataset[ (id_dataset['team'] == player_info['Team']) & (id_dataset['TM_ID'] == player_info['ID']) ]
        #         selected_player_df = pd.concat([selected_player_df, select_player_df])

        # if st.sidebar.button('새로고침', key="refresh_btn"):
        #      st.session_state.selected_players = []

        if st.sidebar.button('실행'):
            
            concatenated_df = pd.DataFrame()
            # final_results = pd.DataFrame()

            for player_info in st.session_state.selected_players:

                league = select_league(player_info['League'])
                id = player_info['ID']
                # player_name = player_info['Player Name']

                player_df = dataframe(league, id, st.session_state['password'])

                concatenated_df = pd.concat([concatenated_df, player_df])
            
            batter_dataframes = {}
            
            for batter, group in concatenated_df.groupby('batter'):
                batter_dataframes[batter] = group.copy()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------
            
            st.title('[시즌별 :red[주요현황]]')
            st.subheader(':gray[기록 & 타구]')

            season_stats_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_stats_df = stats(batter_raw_df)
                stats_viewer_df = stats_viewer(season_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                stats_f_row_df = stats_viewer_df.iloc[:1]
                game_year = stats_f_row_df.index.values[0]

                stats_f_row_df['선수명'] = batter_name
                stats_f_row_df.set_index('선수명', inplace=True)

                stats_f_row_df.insert(0,'연도',game_year)
                
                season_stats_concat_df = pd.concat([season_stats_concat_df, stats_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            s1 = dict(selector='th', props=[('text-align', 'center')])
            s2 = dict(selector='td', props=[('text-align', 'center')])  

            styled_df = season_stats_concat_df.style.set_table_styles([s1, s2])

            st.dataframe(styled_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_stats_df = stats(batter_raw_df)
                stats_viewer_df = stats_viewer(season_stats_df)

                stats_viewer_df = stats_viewer_df.reset_index()
                stats_viewer_df = stats_viewer_df.astype({'game_year':'str'})
                stats_viewer_df = stats_viewer_df.rename(columns={'game_year':'연도'})
                stats_viewer_df = stats_viewer_df.set_index('연도')

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(stats_viewer_df, width=1300)

#-------------------------------------------------------------------------------------------------------

            st.subheader(':gray[스윙경향성]')

            season_swing_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_stats_df = stats(batter_raw_df)
                swing_viewer_df = swing_viewer(season_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                swing_f_row_df = swing_viewer_df.iloc[:1]
                game_year = swing_f_row_df.index.values[0]

                swing_f_row_df['선수명'] = batter_name
                swing_f_row_df.set_index('선수명', inplace=True)

                swing_f_row_df.insert(0,'연도',game_year)
                
                season_swing_concat_df = pd.concat([season_swing_concat_df, swing_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(season_swing_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_stats_df = stats(batter_raw_df)
                swing_viewer_df = swing_viewer(season_stats_df)

                swing_viewer_df = swing_viewer_df.reset_index()
                swing_viewer_df = swing_viewer_df.astype({'game_year':'str'})
                swing_viewer_df = swing_viewer_df.rename(columns={'game_year':'연도'})
                swing_viewer_df = swing_viewer_df.set_index('연도')

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(swing_viewer_df, width=1300)

            
            with st.expander("LSA(Launch Speed Angle) 이란?"):
                st.write("LSA(Launch Speed Angle)은 Baseball Savant의 타구표에서 활용되는 지표로 6단계로 타구의 질을 구분하고 있음 (*괄호의 %는 안타확률)")
                st.write("LSA 1: Weak(10.4%) / LSA 2: Topped(22.3%) / LSA 3: Under(7.7%) / LSA 4: Flare & Burner(70.8%) / LSA 5: Solid Contact(46.3%) / LSA 6: Barrel(70.5%)")
                st.markdown("""<style>[data-testid=stExpander] [data-testid=stImage]{text-align: left;display: block;margin-left: 10; margin-right: auto; width: 50%;}</style>""", unsafe_allow_html=True)
                st.image("approach.jpg")

            with st.expander("타격 어프로치 구분"):
                st.write("타격 어프로치는 타자들의 타격성향을 나타내기 위해 작성된 내용으로 리그의 평균적인 존에 대한 스윙시도, 존 외부에 대한 스윙시도를 기준으로 4가지의 성향을 구분하고 있음")
                st.markdown("""<style>[data-testid=stExpander] [data-testid=stImage]{text-align: left;display: block;margin-left: 10; margin-right: auto; width: 80%;}</style>""", unsafe_allow_html=True)
                st.image("plate_discipline.png")


            st.divider()


# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌별 :red[인플레이 현황]]')

            season_inplay_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_events_df = seoson_inplay_events(batter_raw_df)
                season_events_df = season_events_df.rename(columns={'game_year':'연도', 'events':'구분','pitch_name':'인플레이수','exit_velocity':'타구속도','launch_angleX':'발사각도', 'hit_spin_rate':'타구스핀량','hit_distance':'비거리'})

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                events_f_row_df = season_events_df.iloc[:1]
                game_year = events_f_row_df.iloc[0]['연도']
                events_f_row_df = season_events_df[season_events_df['연도'] == game_year]
                
                events_f_row_df['선수명'] = batter_name
                events_f_row_df.set_index('선수명', inplace=True)
                
                season_inplay_concat_df = pd.concat([season_inplay_concat_df, events_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(season_inplay_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                season_events_df = seoson_inplay_events(batter_raw_df)
                season_events_df = season_events_df.rename(columns={'game_year':'연도', 'events':'구분','pitch_name':'인플레이수','exit_velocity':'타구속도','launch_angleX':'발사각도', 'hit_spin_rate':'타구스핀량','hit_distance':'비거리'})

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(season_events_df, width=1300)
            
            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[투수유형별] 현황]')
            st.subheader(':gray[기록 & 타구]')

            throws_stats_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                throws_stats_df = season_pthrows(batter_raw_df)
                throws_stats_df = throws_stats_df.set_index('game_year')
                stats_viewer_df = stats_viewer_pthrows(throws_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                stats_viewer_df = stats_viewer_df.reset_index()
                stats_viewer_df = stats_viewer_df.astype({'game_year':'str'})
                stats_viewer_df = stats_viewer_df.rename(columns={'game_year':'연도'})

                stats_f_row_df = stats_viewer_df.iloc[:1]
                game_year = stats_f_row_df.iloc[0]['연도']
                stats_f_row_df = stats_viewer_df[stats_viewer_df['연도'] == game_year]

                stats_f_row_df['선수명'] = batter_name
                stats_f_row_df.set_index('선수명', inplace=True)

                # stats_f_row_df.insert(0,'연도',game_year)
                
                throws_stats_concat_df = pd.concat([throws_stats_concat_df, stats_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(throws_stats_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                throws_stats_df = season_pthrows(batter_raw_df)
                throws_stats_df = throws_stats_df.rename(columns={'game_year':'연도'})
                throws_stats_df = throws_stats_df.set_index('연도')
                stats_viewer_df = stats_viewer_pthrows(throws_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(stats_viewer_df, width=1300)

# -------------------------------------------------------------------------------------------------------

            st.subheader(':gray[스윙경향성]')

            throws_swing_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                throws_stats_df = season_pthrows(batter_raw_df)
                throws_stats_df = throws_stats_df.set_index('game_year')
                swing_viewer_df = swing_viewer_pthrows(throws_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                swing_viewer_df = swing_viewer_df.reset_index()
                swing_viewer_df = swing_viewer_df.astype({'game_year':'str'})
                swing_viewer_df = swing_viewer_df.rename(columns={'game_year':'연도'})

                swing_f_row_df = swing_viewer_df.iloc[:1]
                game_year = swing_f_row_df.iloc[0]['연도']
                swing_f_row_df = swing_viewer_df[swing_viewer_df['연도'] == game_year]

                swing_f_row_df['선수명'] = batter_name
                swing_f_row_df.set_index('선수명', inplace=True)

                # swing_f_row_df.insert(0,'연도',game_year)
                
                throws_swing_concat_df = pd.concat([throws_swing_concat_df, swing_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(throws_swing_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                throws_stats_df = season_pthrows(batter_raw_df)
                throws_stats_df = throws_stats_df.rename(columns={'game_year':'연도'})
                throws_stats_df = throws_stats_df.set_index('연도')
                swing_viewer_df = swing_viewer_pthrows(throws_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(swing_viewer_df, width=1300)

            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[구종유형별] 현황]')
            st.subheader(':gray[기록 & 타구]')

            pkind_stats_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                pkind_stats_df = season_pkind(batter_raw_df)
                pkind_stats_df = pkind_stats_df.set_index('game_year')
                stats_viewer_df = stats_viewer_pkind(pkind_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                stats_viewer_df = stats_viewer_df.reset_index()
                stats_viewer_df = stats_viewer_df.astype({'game_year':'str'})
                stats_viewer_df = stats_viewer_df.rename(columns={'game_year':'연도'})

                stats_f_row_df = stats_viewer_df.iloc[:1]
                game_year = stats_f_row_df.iloc[0]['연도']
                stats_f_row_df = stats_viewer_df[stats_viewer_df['연도'] == game_year]

                stats_f_row_df['선수명'] = batter_name
                stats_f_row_df.set_index('선수명', inplace=True)

                # stats_f_row_df.insert(0,'연도',game_year)
                
                pkind_stats_concat_df = pd.concat([pkind_stats_concat_df, stats_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(pkind_stats_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                pkind_stats_df = season_pkind(batter_raw_df)
                pkind_stats_df = pkind_stats_df.rename(columns={'game_year':'연도'})
                pkind_stats_df = pkind_stats_df.set_index('연도')                
                pkind_stats_df = stats_viewer_pkind(pkind_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(stats_viewer_df, width=1300)

# -------------------------------------------------------------------------------------------------------

            st.subheader(':gray[스윙경향성]')

            pkind_swing_concat_df = pd.DataFrame()

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                pkind_stats_df = season_pkind(batter_raw_df)
                pkind_stats_df = pkind_stats_df.set_index('game_year')
                swing_viewer_df = swing_viewer_pkind(pkind_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                swing_viewer_df = swing_viewer_df.reset_index()
                swing_viewer_df = swing_viewer_df.astype({'game_year':'str'})
                swing_viewer_df = swing_viewer_df.rename(columns={'game_year':'연도'})

                swing_f_row_df = swing_viewer_df.iloc[:1]
                game_year = swing_f_row_df.iloc[0]['연도']
                swing_f_row_df = swing_viewer_df[swing_viewer_df['연도'] == game_year]

                swing_f_row_df['선수명'] = batter_name
                swing_f_row_df.set_index('선수명', inplace=True)

                # swing_f_row_df.insert(0,'연도',game_year)
                
                pkind_swing_concat_df = pd.concat([pkind_swing_concat_df, swing_f_row_df])

            pd.set_option('display.max_colwidth', 100)

            st.dataframe(pkind_swing_concat_df, width=1400)
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                pkind_stats_df = season_pkind(batter_raw_df)
                pkind_stats_df = pkind_stats_df.rename(columns={'game_year':'연도'})
                pkind_stats_df = pkind_stats_df.set_index('연도')
                pkind_stats_df = swing_viewer_pkind(pkind_stats_df)

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']                

                with st.expander(f"상세기록:  {batter_name}"):
                    st.dataframe(swing_viewer_df, width=1300)

            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[스윙지점]]')
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df
            
                game_year = batter_raw_df['game_year'].max()
                batter_recent_df = batter_raw_df[batter_raw_df['game_year'] == game_year]
            
                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']
            
                st.subheader(f"{batter_name}, {game_year}")
            
                col1, col2, col3, col4 = st.columns(4)
            
                pitched_factor = 'player_name'
                swing_factor = 'swing'
                lsa_factor = 'launch_speed_angle'
            
                with col1:
                    original_title = '<p style="text-align: center; color:gray; font-size: 25px;">투구지점</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    season_pitched_fig = factor_year_count_map(batter_recent_df, pitched_factor)
                    season_pitched_fig.update_layout(height=400, width=450)
                    season_pitched_fig.update_coloraxes(showscale=False)
                    st.plotly_chart(season_pitched_fig, layout="wide", key=f"season_pitched_{batter}")
            
                with col2:
                    original_title = '<p style="text-align: center; color:gray; font-size: 25px;">스윙지점</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    season_swing_fig = factor_year_sum_map(batter_recent_df, swing_factor)
                    season_swing_fig.update_layout(height=400, width=450)
                    season_swing_fig.update_coloraxes(showscale=False)
                    st.plotly_chart(season_swing_fig, layout="wide", key=f"season_swing_{batter}")
            
                batter_recent_las4 = batter_recent_df[batter_recent_df['plus_lsa4'] == 1]
            
                with col3:
                    original_title = '<p style="text-align: center; color:gray; font-size: 25px;">LSA 4+ Zone</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    season_lsa_fig = factor_year_sum_map_scatter(batter_recent_las4)
                    season_lsa_fig.update_layout(height=400, width=450)
                    season_lsa_fig.update_coloraxes(showscale=False)
                    st.plotly_chart(season_lsa_fig, layout="wide", key=f"season_lsa_{batter}")
            
                with col4:
                    original_title = '<p style="text-align: center; color:gray; font-size: 25px;">LSA 4+ Plate</p>'
                    st.markdown(original_title, unsafe_allow_html=True)
                    season_lsa_fig = factor_year_sum_plate_map_scatter(batter_recent_las4)
                    season_lsa_fig.update_layout(height=400, width=430)
                    season_lsa_fig.update_coloraxes(showscale=False)
                    st.plotly_chart(season_lsa_fig, layout="wide", key=f"season_lsa_plate_{batter}")
                
                st.markdown(""" <div style="text-align: right; font-size: 0.9em;">
                                <span style="font-weight: bold;">색상 범례:</span> 
                                붉은색: 2루타 이상 / 파란색: 단타 / 옅은 갈색: 아웃
                            </div>
                            """, 
                            unsafe_allow_html=True)
            
                # 선수별 연도별 그림을 볼 수 있는 expander 추가
                with st.expander(f"연도별: {batter_name}"):
                    # 해당 선수의 모든 연도 데이터 가져오기
                    years = sorted(batter_raw_df['game_year'].unique(), reverse=True)
                    
                    # 각 연도별로 그래프 표시
                    for year_idx, year in enumerate(years):
                        st.subheader(f"{year}년")
                        
                        # 해당 연도의 데이터 필터링
                        year_df = batter_raw_df[batter_raw_df['game_year'] == year]
                        year_swing_df = year_df[year_df['swing'] == 1]
                        year_lsa4_df = year_df[year_df['plus_lsa4'] == 1]
                        
                        # 연도별 그래프 표시
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            original_title = '<p style="text-align: center; color:gray; font-size: 25px;">투구지점 (히트맵)</p>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            year_pitched_heatmap = factor_year_count_map(year_df, pitched_factor)
                            year_pitched_heatmap.update_layout(height=400, width=450)
                            year_pitched_heatmap.update_coloraxes(showscale=False)
                            st.plotly_chart(year_pitched_heatmap, layout="wide", key=f"year_pitched_heatmap_{batter}_{year}")
                        
                        with col2:
                            original_title = '<p style="text-align: center; color:gray; font-size: 25px;">스윙지점 (히트맵)</p>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            year_swing_heatmap = factor_year_sum_map(year_df, swing_factor)
                            year_swing_heatmap.update_layout(height=400, width=450)
                            year_swing_heatmap.update_coloraxes(showscale=False)
                            st.plotly_chart(year_swing_heatmap, layout="wide", key=f"year_swing_heatmap_{batter}_{year}")
                        
                        with col3:
                            original_title = '<p style="text-align: center; color:gray; font-size: 25px;">LSA 4+ Zone</p>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            year_lsa_fig = factor_year_sum_map_scatter(year_lsa4_df)
                            year_lsa_fig.update_layout(height=400, width=450)
                            year_lsa_fig.update_coloraxes(showscale=False)
                            st.plotly_chart(year_lsa_fig, layout="wide", key=f"year_lsa_fig_{batter}_{year}")
                        
                        with col4:
                            original_title = '<p style="text-align: center; color:gray; font-size: 25px;">LSA 4+ Plate</p>'
                            st.markdown(original_title, unsafe_allow_html=True)
                            year_lsa_plate_fig = factor_year_sum_plate_map_scatter(year_lsa4_df)
                            year_lsa_plate_fig.update_layout(height=400, width=430)
                            year_lsa_plate_fig.update_coloraxes(showscale=False)
                            st.plotly_chart(year_lsa_plate_fig, layout="wide", key=f"year_lsa_plate_fig_{batter}_{year}")
                        
                        # 연도별 구분선 추가
                        st.markdown("---")
            
                st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[Swing Map]]')

            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df

                game_year = batter_raw_df['game_year'].max()
                batter_recent_df = batter_raw_df[batter_raw_df['game_year'] == game_year]

                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']

                called_strike_df = batter_recent_df[batter_recent_df['description'] == "called_strike"]
                called_strike_df['swingmap'] = 'Called_Strike'
                whiff_df = batter_recent_df[batter_recent_df['whiff'] == 1]
                whiff_df['swingmap'] = 'Whiff'
                ball_df = batter_recent_df[batter_recent_df['type'] == "B"]
                ball_df['swingmap'] = 'Ball'
                foul_df = batter_recent_df[batter_recent_df['foul'] == 1]
                foul_df['swingmap'] = 'Foul'
                hit_df = batter_recent_df[batter_recent_df['hit'] == 1]
                hit_df['swingmap'] = 'HIT'
                out_df = batter_recent_df[batter_recent_df['field_out'] == 1]
                out_df['swingmap'] = 'Out'

                swingmap_dataframe = pd.concat([called_strike_df, whiff_df, ball_df, foul_df, hit_df, out_df])
                swingmap_factor = 'player_name'

                st.subheader(f"{batter_name}, {game_year}")

                season_pitched_fig = swingmap_count_map(swingmap_dataframe, swingmap_factor)
                season_pitched_fig_scatter = swingmap_count_map_scatter(swingmap_dataframe)

                st.plotly_chart(season_pitched_fig, key=f"main_swingmap_{batter}", layout="wide")
                st.plotly_chart(season_pitched_fig_scatter, key=f"main_swingmap_scatter_{batter}", layout="wide")

                                # 선수별 연도별 스윙맵을 볼 수 있는 expander 추가
                with st.expander(f"연도별: {batter_name}"):
                    # 해당 선수의 모든 연도 데이터 가져오기
                    years = sorted(batter_raw_df['game_year'].unique(), reverse=True)
                    
                    # 각 연도별로 그래프 표시
                    for year in years:
                        st.subheader(f"{year}년")
                        
                        # 해당 연도의 데이터 필터링
                        year_df = batter_raw_df[batter_raw_df['game_year'] == year]
                        
                        # 연도별 스윙맵 데이터 준비
                        year_called_strike_df = year_df[year_df['description'] == "called_strike"]
                        year_called_strike_df['swingmap'] = 'Called_Strike'
                        year_whiff_df = year_df[year_df['whiff'] == 1]
                        year_whiff_df['swingmap'] = 'Whiff'
                        year_ball_df = year_df[year_df['type'] == "B"]
                        year_ball_df['swingmap'] = 'Ball'
                        year_foul_df = year_df[year_df['foul'] == 1]
                        year_foul_df['swingmap'] = 'Foul'
                        year_hit_df = year_df[year_df['hit'] == 1]
                        year_hit_df['swingmap'] = 'HIT'
                        year_out_df = year_df[year_df['field_out'] == 1]
                        year_out_df['swingmap'] = 'Out'
                        
                        year_swingmap_df = pd.concat([year_called_strike_df, year_whiff_df, year_ball_df, 
                                                    year_foul_df, year_hit_df, year_out_df])
                        
                        # 연도별 스윙맵 그래프 표시
                        year_swing_fig = swingmap_count_map(year_swingmap_df, swingmap_factor)
                        year_swing_scatter = swingmap_count_map_scatter(year_swingmap_df)
                        
                        st.plotly_chart(year_swing_fig, key=f"year_{batter}_{year}_swingmap", layout="wide")
                        st.plotly_chart(year_swing_scatter, key=f"year_{batter}_{year}_swingmap_scatter", layout="wide")
                        
                        # 연도별 구분선 추가
                        st.markdown("---")
            

            st.divider()

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[Spray Chart]]')


            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df
            
                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']
            
                st.subheader(f"{batter_name}")

                # st.markdown("""
                #         <style>
                #             .element-container {
                #                 padding: 0 !important;
                #             }
                #             .stPlotlyChart {
                #                 margin: 0 !important;
                #                 padding: 0 !important;
                #             }
                #             .block-container {
                #                 padding-top: 1rem;
                #                 padding-bottom: 1rem;
                #                 padding-left: 1rem;
                #                 padding-right: 1rem;
                #             }
                #             div[data-testid="column"] {
                #                 padding: 0 0.3rem;
                #             }
                #         </style>
                #     """, unsafe_allow_html=True)
                
                # 'game_year' 컬럼을 명시적으로 사용
                year_col = 'game_year'
                
                # 고유 연도 추출 및 내림차순 정렬
                years = sorted(batter_raw_df[year_col].unique(), reverse=True)
                
                # 최대 3개 시즌만 표시
                display_years = years[:3]
                
                # 3개 컬럼 생성
                cols = st.columns(3)
                
                # 각 연도별 데이터 표시
                for i in range(min(3, len(display_years))):  # 실제 연도 수와 3 중 작은 값만큼 반복
                    with cols[i]:
                        current_year = display_years[i]
                        st.write(f"#### {current_year} 시즌")
                        
                        # 해당 연도 데이터 필터링
                        year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                        
                        # Spray Chart 데이터 생성
                        year_spraychart_dataframe = spraychart_df(year_data)
                        
                        # Spray Chart 표시
                        season_spraychart(year_spraychart_dataframe, key=f"season_spray_{batter}_{current_year}")
                
                # 남은 컬럼에 빈 내용 표시
                for i in range(len(display_years), 3):
                    with cols[i]:
                        st.write("#### 시즌 정보 없음")
                        st.info("해당 시즌의 데이터가 없습니다.")
                
                # 색상 범례 표시
                st.markdown(""" <div style="text-align: left; font-size: 0.9em;">
                            <span style="font-weight: bold;">색상 범례:</span> 
                            붉은색: 2루타 이상 / 파란색: 단타 / 옅은 갈색: 아웃
                            </div>
                            """, 
                            unsafe_allow_html=True)
                
                # 스트라이크 존 기준 차트 (최근 연도만)
                with st.expander(f" by 스트라이크 존:  {batter_name}(최근연도)"):
                    if len(years) > 0:
                        st.write(f"S존 기준차트 ({years[0]} 시즌)")
                        
                        # 최근 연도 데이터 필터링
                        recent_year_data = batter_raw_df[batter_raw_df[year_col] == years[0]]
                        recent_spraychart_dataframe = spraychart_df(recent_year_data)

                        zone_spraychart_fig(recent_spraychart_dataframe, batter_name=f"{batter_name} ({years[0]})")
                        
                        st.markdown(""" <div style="text-align: left; font-size: 0.9em;">
                                <span style="font-weight: bold;">색상 범례:</span> 
                                붉은색: 2루타 이상 / 파란색: 단타 / 옅은 갈색: 아웃
                                </div>
                                """, 
                                unsafe_allow_html=True)
                    else:
                        st.info("스트라이크 존 분석을 위한 데이터가 없습니다.")
            
                # 타구 비행시간 차트 (최근 3개 연도)
                with st.expander(f" by 타구비행시간:  {batter_name}"):
                    st.write("타구 비행시간")
                    
                    # 3개 컬럼 생성
                    hangtime_cols = st.columns(3)
                    
                    # 각 연도별 타구 비행시간 차트 표시
                    for i in range(min(3, len(display_years))):  # 실제 연도 수와 3 중 작은 값만큼 반복
                        with hangtime_cols[i]:
                            current_year = display_years[i]
                            st.write(f"#### {current_year} 시즌")
                            
                            # 해당 연도 데이터 필터링
                            year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                            
                            # Spray Chart 데이터 생성
                            year_spraychart_dataframe = spraychart_df(year_data)
                            
                            # 타구 비행시간 차트 표시
                            spraychart_hangtime_fig = season_hangtime_spraychart(year_spraychart_dataframe, batter_name=f"{batter_name} ({current_year})")
                            st.plotly_chart(spraychart_hangtime_fig, key=f"hangtime_{batter}_{current_year}", use_container_width=True)
                    
                    # 남은 컬럼에 빈 내용 표시
                    for i in range(len(display_years), 3):
                        with hangtime_cols[i]:
                            st.write("#### 시즌 정보 없음")
                            st.info("해당 시즌의 데이터가 없습니다.")
                    
                    st.markdown(""" <div style="text-align: left; font-size: 0.9em;">
                            <span style="font-weight: bold;">색상 범례:</span> 
                            붉은색: 1~4초 비행 / 옅은 파란색: 1초 미만 / 옅은 갈색: 4초 이상
                            </div>
                            """, 
                            unsafe_allow_html=True)
            
                st.divider()


# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

            st.title('[시즌 :red[Plate Discipline]]')

            # 최근 경기의 타석 결과를 타석별로 scatter chart로 표시
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df
            
                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']
                
                # 최근 경기 데이터 필터링
                recent_game_date = batter_raw_df['game_date'].max()
                recent_game_df = batter_raw_df[batter_raw_df['game_date'] == recent_game_date]
            
                st.subheader(f"{batter_name} ({recent_game_date})")
                
                # 타석별 결과 시각화
                colors = {
                    'called_strike': 'rgba(24,85,144,0.6)', 
                    'swinging_strike': 'rgba(247,222,52,1)', 
                    'ball': 'rgba(108,122,137,0.7)', 
                    'foul': 'rgba(241,106,227,0.5)', 
                    'hit_into_play_no_out': 'rgba(255,105,97,1)', 
                    'hit_into_play_score': 'rgba(255,105,97,1)',
                    'hit_into_play': 'rgba(140,86,75,0.6)'
                }
                
                symbols = {
                    '4-Seam Fastball': 'circle', 
                    '2-Seam Fastball': 'triangle-down', 
                    'Cutter': 'triangle-se', 
                    'Slider': 'triangle-right', 
                    'Curveball': 'triangle-up', 
                    'Changeup': 'diamond', 
                    'Split-Finger': 'square', 
                    'Sweeper': 'cross'
                }
                
                # 이닝 목록 가져오기 (최대 5개)
                innings = sorted(recent_game_df['inning'].unique())[:5]
                
                # 5개 컬럼 생성
                cols = st.columns(5)
                
                # 각 이닝별 데이터 표시
                for i in range(5):  # 항상 5개 컬럼 생성
                    with cols[i]:
                        if i < len(innings):  # 이닝 데이터가 있는 경우
                            current_inning = innings[i]
                            
                            # 해당 이닝 데이터 필터링
                            inning_data = recent_game_df[recent_game_df['inning'] == current_inning]
                            
                            # 투수 이름 가져오기
                            if not inning_data.empty:
                                pitcher_name = inning_data['player_name'].iloc[0]
                                st.write(f"#### {current_inning}회 - {pitcher_name}")
                            else:
                                st.write(f"#### {current_inning}회")
                            
                            # 이닝별 차트 생성
                            inning_fig = px.scatter(
                                inning_data, 
                                x='plate_x', 
                                y='plate_z', 
                                color='description', 
                                symbol='pitch_name',
                                text='pitch_number',
                                color_discrete_map=colors,
                                hover_name="player_name", 
                                hover_data=["rel_speed(km)", "pitch_name", "events", "exit_velocity", "description", "launch_speed_angle", "launch_angle"],
                                template="simple_white",
                                height=300, 
                                width=250
                            )
                            
                            # 텍스트 크기와 색상 설정
                            inning_fig.update_traces(
                                textfont=dict(
                                    size=18,
                                    color='rgba(0,0,0,1)'  # 검은색으로 설정 (완전 불투명)
                                )
                            )
                            
                            # 심볼 설정
                            for a, b in enumerate(inning_fig.data):
                                pitch_name = inning_fig.data[a].name.split(', ')[1] if ',' in inning_fig.data[a].name else inning_fig.data[a].name
                                if pitch_name in symbols:
                                    inning_fig.data[a].marker.symbol = symbols[pitch_name]
                            
                            # 차트 레이아웃 설정
                            inning_fig.update_layout(
                                showlegend=False,
                                autosize=False,
                                margin=dict(l=10, r=10, t=10, b=10),
                                plot_bgcolor='rgba(255,255,255,0.1)', 
                                paper_bgcolor='rgba(255,255,255,1)',
                            )
                            
                            # x, y 범위 설정
                            inning_fig.update_xaxes(range=[-0.6, 0.6], showgrid=False, zeroline=False, showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True, showticklabels=False, title_text='')
                            inning_fig.update_yaxes(range=[0.0, 1.5], showgrid=False, zeroline=False, showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True, showticklabels=False, title_text='')
                            
                            inning_fig.update_traces(marker=dict(size=30, opacity=1))  # 마커 크기 조정 및 불투명도 설정
                            inning_fig.update_traces(textfont_size=18)      # 텍스트 크기 조정
                            
                            # 스트라이크 존과 코어 존 추가
                            # 스트라이크 존 라인 추가
                            inning_fig.add_hline(y=0.59, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
                            inning_fig.add_hline(y=0.91, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
                            inning_fig.add_vline(x=-0.12, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
                            inning_fig.add_vline(x=0.12, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
                            
                            # Core Zone 추가
                            homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
                            homey = [0.59, 0.59, 0.91, 0.91, 0.59]
                            inning_fig.add_trace(go.Scatter(
                                x=homex, 
                                y=homey, 
                                mode='lines', 
                                line=dict(color='red', width=2),
                                showlegend=False
                            ))
                            
                            # Strike Zone 추가
                            homex = [-0.26, 0.26, 0.26, -0.26, -0.26]
                            homey = [0.45, 0.45, 1.05, 1.05, 0.45]
                            inning_fig.add_trace(go.Scatter(
                                x=homex, 
                                y=homey, 
                                mode='lines', 
                                line=dict(color='rgba(108,122,137,0.9)', width=2),
                                showlegend=False
                            ))
                            
                            # 차트 표시 - 고유한 키 추가
                            st.plotly_chart(inning_fig, use_container_width=True, key=f"recent_{batter}_{current_inning}_{i}_{recent_game_date}")
                        
                        else:  # 이닝 데이터가 없는 경우
                            st.write("#### -")
                            st.info("-")
                
                st.markdown("""
                <div style="text-align: left; font-size: 0.9em;">
                <span style="font-weight: bold;">색상 범례:</span> 
                파란색: 콜드 스트라이크 / 노란색: 스윙 스트라이크 / 회색: 볼 / 분홍색: 파울 / 빨간색: 안타 / 갈색: 아웃
                </div>
                """, unsafe_allow_html=True)
                
                # 선수별 expander로 시즌 경기별 타석 결과 차트 표시
                with st.expander(f"시즌 경기별 타석 결과(최근 5경기): {batter_name}"):
                    # 시즌 데이터에서 게임 날짜 목록 가져오기
                    game_dates = sorted(batter_raw_df['game_date'].unique(), reverse=True)
                    
                    for date_idx, game_date in enumerate(game_dates[:5]):  # 최근 5경기만 표시
                        st.write(f"### 경기 날짜: {game_date}")
                        
                        # 해당 날짜의 데이터 필터링
                        game_df = batter_raw_df[batter_raw_df['game_date'] == game_date]
                        
                        # 이닝 목록 가져오기 (최대 5개)
                        game_innings = sorted(game_df['inning'].unique())[:5]
                        
                        # 5개 컬럼 생성
                        game_cols = st.columns(5)
                        
                        # 각 이닝별 데이터 표시
                        for i in range(5):  # 항상 5개 컬럼 생성
                            with game_cols[i]:
                                if i < len(game_innings):  # 이닝 데이터가 있는 경우
                                    current_inning = game_innings[i]
                                    
                                    # 해당 이닝 데이터 필터링
                                    inning_data = game_df[game_df['inning'] == current_inning]
                                    
                                    # 투수 이름 가져오기
                                    if not inning_data.empty:
                                        pitcher_name = inning_data['player_name'].iloc[0]
                                        st.write(f"#### {current_inning}회 - {pitcher_name}")
                                    else:
                                        st.write(f"#### {current_inning}회")
                                    
                                    # 이닝별 차트 생성
                                    inning_fig = px.scatter(
                                        inning_data, 
                                        x='plate_x', 
                                        y='plate_z', 
                                        color='description', 
                                        symbol='pitch_name',
                                        text='pitch_number',
                                        color_discrete_map=colors,
                                        hover_name="player_name", 
                                        hover_data=["rel_speed(km)", "pitch_name", "events", "exit_velocity", "description", "launch_speed_angle", "launch_angle"],
                                        template="simple_white",
                                        height=300, 
                                        width=250
                                    )
                                    
                                    # 텍스트 크기와 색상 설정
                                    inning_fig.update_traces(
                                        textfont=dict(
                                            size=18,
                                            color='rgba(0,0,0,1)'  # 검은색으로 설정 (완전 불투명)
                                        )
                                    )
                                    
                                    # 심볼 설정
                                    for a, b in enumerate(inning_fig.data):
                                        pitch_name = inning_fig.data[a].name.split(', ')[1] if ',' in inning_fig.data[a].name else inning_fig.data[a].name
                                        if pitch_name in symbols:
                                            inning_fig.data[a].marker.symbol = symbols[pitch_name]
                                    
                                    # 차트 레이아웃 설정
                                    inning_fig.update_layout(
                                        showlegend=False,
                                        autosize=False,
                                        margin=dict(l=10, r=10, t=10, b=10),
                                        plot_bgcolor='rgba(255,255,255,0.1)', 
                                        paper_bgcolor='rgba(255,255,255,1)',
                                    )
                                    
                                    # x, y 범위 설정
                                    inning_fig.update_xaxes(range=[-0.6, 0.6], showgrid=False, zeroline=False, showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True, showticklabels=False, title_text='')
                                    inning_fig.update_yaxes(range=[0.0, 1.5], showgrid=False, zeroline=False, showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True, showticklabels=False, title_text='')
                                    
                                    inning_fig.update_traces(marker=dict(size=30, opacity=1))  # 마커 크기 조정 및 불투명도 설정
                                    inning_fig.update_traces(textfont_size=18)      # 텍스트 크기 조정
                                    
                                    # 스트라이크 존과 코어 존 추가
                                    # 스트라이크 존 라인 추가
                                    inning_fig.add_hline(y=0.59, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
                                    inning_fig.add_hline(y=0.91, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
                                    inning_fig.add_vline(x=-0.12, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
                                    inning_fig.add_vline(x=0.12, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
                                    
                                    # Core Zone 추가
                                    homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
                                    homey = [0.59, 0.59, 0.91, 0.91, 0.59]
                                    inning_fig.add_trace(go.Scatter(
                                        x=homex, 
                                        y=homey, 
                                        mode='lines', 
                                        line=dict(color='red', width=2),
                                        showlegend=False
                                    ))
                                    
                                    # Strike Zone 추가
                                    homex = [-0.26, 0.26, 0.26, -0.26, -0.26]
                                    homey = [0.45, 0.45, 1.05, 1.05, 0.45]
                                    inning_fig.add_trace(go.Scatter(
                                        x=homex, 
                                        y=homey, 
                                        mode='lines', 
                                        line=dict(color='rgba(108,122,137,0.9)', width=2),
                                        showlegend=False
                                    ))
                                    
                                    # 차트 표시 - 고유한 키 추가 (날짜와 이닝을 조합)
                                    st.plotly_chart(inning_fig, use_container_width=True, key=f"history_{batter}_{game_date}_{current_inning}_{i}")
                                
                                else:  # 이닝 데이터가 없는 경우
                                    st.write("#### -")
                                    st.info("-")
                        
                        # 날짜별 구분선 추가
                        st.markdown("---")
            
            

            st.divider()
# -------------------------------------------------------------------------------------------------------


with headerSection:
    # Get the user's ID from the session cookie
    user_id = get_user_id()

    if user_id is None:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        st.session_state['loggedIn'] = True
        show_main_page()
