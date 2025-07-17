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
    initial_sidebar_state="expanded",
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

    st.sidebar.markdown("")
    
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
        
        option = st.sidebar.selectbox('리그 선택', ("-", "KBO(1군)", "KBO(2군)", "AAA(마이너)","KBA(아마)"))


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

            st.title('[시즌 :red[Spray Chart]] - 타구 비행시간 기준')
            
            for batter, batter_df in batter_dataframes.items():
                batter_raw_df = globals()[f"df_{batter}"] = batter_df
            
                batter_str = str(batter)
                batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
                batter_name = batter_finder.iloc[0]['NAME']
            
                st.subheader(f"{batter_name}")
            
                # 'game_year' 컬럼을 명시적으로 사용
                year_col = 'game_year'
                
                # 고유 연도 추출 및 내림차순 정렬
                years = sorted(batter_raw_df[year_col].unique(), reverse=True)
                
                # 최대 3개 시즌만 표시
                display_years = years[:3]
                
                # 3개 컬럼 생성
                cols = st.columns(3)
                
                # 각 연도별 데이터 표시 (타구 비행시간 기준)
                for i in range(min(3, len(display_years))):
                    with cols[i]:
                        current_year = display_years[i]
                        st.write(f"#### {current_year} 시즌")
                        
                        # 해당 연도 데이터 필터링
                        year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                        
                        # Spray Chart 데이터 생성
                        year_spraychart_dataframe = spraychart_df(year_data)
                        
                        # 타구 비행시간 기준 Spray Chart 표시 (올바른 함수명 사용)
                        spraychart_hangtime_fig = season_hangtime_spraychart(
                            year_spraychart_dataframe, 
                            batter_name=f"{batter_name} ({current_year})"
                        )
                        st.plotly_chart(spraychart_hangtime_fig, key=f"season_hangtime_{batter}_{current_year}", use_container_width=True)
                
                # 남은 컬럼에 빈 내용 표시
                for i in range(len(display_years), 3):
                    with cols[i]:
                        st.write("#### 시즌 정보 없음")
                        st.info("해당 시즌의 데이터가 없습니다.")
                
                # 타구 비행시간 색상 범례 표시
                st.markdown(""" <div style="text-align: left; font-size: 0.9em;">
                            <span style="font-weight: bold;">색상 범례:</span> 
                            붉은색: 2~4초 비행 / 옅은 파란색: 1초 미만 / 옅은 갈색: 4초 이상
                            </div>
                            """, 
                            unsafe_allow_html=True)
                
                # 구종 컬럼 확인 후 처리
                pitch_type_col = None
                possible_pitch_cols = ['pkind', 'pitch_type', 'pitch_name', 'pitch_code', 'ptype']
                
                for col in possible_pitch_cols:
                    if col in batter_raw_df.columns:
                        pitch_type_col = col
                        break
                
                # 스트라이크 컬럼 확인
                strikes_col = None
                possible_strikes_cols = ['strikes', 'strike_count', 's_count']
                
                for col in possible_strikes_cols:
                    if col in batter_raw_df.columns:
                        strikes_col = col
                        break
                
                # 구종 분류가 가능한 경우에만 expander 표시
                if pitch_type_col is not None:
                    with st.expander(f"by 구종 분류: {batter_name} (타구 비행시간)"):
                        st.write("구종별 스프레이 차트 - 타구 비행시간 기준")
                        
                        # 구종 데이터 확인
                        unique_pitches = batter_raw_df[pitch_type_col].unique()
                        st.write(f"사용 가능한 구종: {unique_pitches}")
                        
                        # Fastball 판별 로직 (여러 가능성 고려)
                        fastball_types = ['Fastball', 'FF', '4-Seam Fastball', 'Fourseam', 'Four-Seam Fastball', 
                                        'Sinker', 'SI', 'Two-Seam Fastball', 'Twoseam', 'FT']
                        
                        # 탭 생성 - 2S 탭 추가
                        if strikes_col is not None:
                            tab_all, tab_2s = st.tabs(["전체 카운트", "2스트라이크 상황"])
                        else:
                            tab_all = st.container()
                        
                        # 전체 카운트 탭
                        with tab_all if strikes_col is not None else tab_all:
                            st.write("### 전체 카운트 (타구 비행시간)")
                            all_cols = st.columns(3)
                            
                            for i in range(min(3, len(display_years))):
                                with all_cols[i]:
                                    current_year = display_years[i]
                                    st.write(f"#### {current_year} 시즌")
                                    
                                    # 해당 연도 데이터 필터링
                                    year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                                    
                                    if len(year_data) > 0:
                                        # Spray Chart 데이터 생성 (Fastball과 Non-Fastball 구분)
                                        fastball_data = year_data[year_data[pitch_type_col].isin(fastball_types)]
                                        non_fastball_data = year_data[~year_data[pitch_type_col].isin(fastball_types)]
                                        
                                        # 통합 차트 생성 (모양으로 구분)
                                        combined_fig = season_hangtime_spraychart_combined(
                                            fastball_data, non_fastball_data,
                                            batter_name=f"{batter_name} 구종별 ({current_year})"
                                        )
                                        st.plotly_chart(combined_fig, key=f"combined_pitch_{batter}_{current_year}", use_container_width=True)
                                        
                                        # 범례 표시
                                        st.markdown("""
                                        <div style="font-size: 0.8em;">
                                        <span style="font-weight: bold;">모양 구분:</span> ● Fastball / ▲ Non-Fastball
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.info(f"{current_year} 시즌 데이터가 없습니다.")
                            
                            # 남은 컬럼에 빈 내용 표시
                            for i in range(len(display_years), 3):
                                with all_cols[i]:
                                    st.write("#### 시즌 정보 없음")
                                    st.info("해당 시즌의 데이터가 없습니다.")
                        
                        # 2스트라이크 상황 탭
                        if strikes_col is not None:
                            with tab_2s:
                                st.write("### 2스트라이크 상황 (타구 비행시간)")
                                s2_cols = st.columns(3)
                                
                                for i in range(min(3, len(display_years))):
                                    with s2_cols[i]:
                                        current_year = display_years[i]
                                        st.write(f"#### {current_year} 시즌")
                                        
                                        # 해당 연도 및 2스트라이크 데이터 필터링
                                        year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                                        two_strike_data = year_data[year_data[strikes_col] == 2]
                                        
                                        if len(two_strike_data) > 0:
                                            # Fastball과 Non-Fastball 구분
                                            fastball_2s_data = two_strike_data[two_strike_data[pitch_type_col].isin(fastball_types)]
                                            non_fastball_2s_data = two_strike_data[~two_strike_data[pitch_type_col].isin(fastball_types)]
                                            
                                            # 통합 차트 생성
                                            combined_2s_fig = season_hangtime_spraychart_combined(
                                                fastball_2s_data, non_fastball_2s_data,
                                                batter_name=f"{batter_name} 2S 구종별 ({current_year})"
                                            )
                                            st.plotly_chart(combined_2s_fig, key=f"combined_2s_pitch_{batter}_{current_year}", use_container_width=True)
                                            
                                            # 범례 표시
                                            st.markdown("""
                                            <div style="font-size: 0.8em;">
                                            <span style="font-weight: bold;">모양 구분:</span> ● Fastball / ▲ Non-Fastball
                                            </div>
                                            """, unsafe_allow_html=True)
                                        else:
                                            st.info(f"{current_year} 시즌 2스트라이크 데이터가 없습니다.")
                                
                                # 남은 컬럼에 빈 내용 표시
                                for i in range(len(display_years), 3):
                                    with s2_cols[i]:
                                        st.write("#### 시즌 정보 없음")
                                        st.info("해당 시즌의 데이터가 없습니다.")
                        
                        # 구종별 범례 (타구 비행시간)
                        st.markdown(""" <div style="text-align: left; font-size: 0.9em;">
                                <span style="font-weight: bold;">색상 범례:</span> 
                                붉은색: 2~4초 비행 / 옅은 파란색: 1초 미만 / 옅은 갈색: 4초 이상
                                </div>
                                """, 
                                unsafe_allow_html=True)
                else:
                    st.info("구종 정보가 없어 구종별 분석을 건너뜁니다.")
            
                # 투수 유형별 타구 비행시간 expander
                pitcher_hand_col = None
                possible_pitcher_cols = ['p_throws', 'pitcher_hand', 'pitcher_throws', 'p_hand']
                
                for col in possible_pitcher_cols:
                    if col in batter_raw_df.columns:
                        pitcher_hand_col = col
                        break
                
                if pitcher_hand_col is not None:
                    with st.expander(f"by 투수 유형별: {batter_name} (타구 비행시간)"):
                        st.write("투수 유형별 타구 비행시간")
                        
                        # 탭 생성 - 2S 탭 추가
                        if strikes_col is not None:
                            tab_righty, tab_lefty, tab_righty_2s, tab_lefty_2s = st.tabs(["우투수", "좌투수", "우투수 2S", "좌투수 2S"])
                        else:
                            tab_righty, tab_lefty = st.tabs(["우투수", "좌투수"])
                        
                        # 우투수 탭
                        with tab_righty:
                            st.write("### 우투수 상대 (타구 비행시간)")
                            righty_cols = st.columns(3)
                            
                            for i in range(min(3, len(display_years))):
                                with righty_cols[i]:
                                    current_year = display_years[i]
                                    st.write(f"#### {current_year} 시즌")
                                    
                                    # 해당 연도 및 우투수 데이터 필터링
                                    year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                                    righty_data = year_data[year_data[pitcher_hand_col] == 'R']
                                    
                                    if len(righty_data) > 0:
                                        # Spray Chart 데이터 생성
                                        righty_spraychart_dataframe = spraychart_df(righty_data)
                                        
                                        # 올바른 함수명 사용
                                        spraychart_hangtime_fig = season_hangtime_spraychart(
                                            righty_spraychart_dataframe, 
                                            batter_name=f"{batter_name} vs 우투수 ({current_year})"
                                        )
                                        st.plotly_chart(spraychart_hangtime_fig, key=f"hangtime_righty_{batter}_{current_year}", use_container_width=True)
                                    else:
                                        st.info(f"{current_year} 시즌 우투수 상대 데이터가 없습니다.")
                            
                            # 남은 컬럼에 빈 내용 표시
                            for i in range(len(display_years), 3):
                                with righty_cols[i]:
                                    st.write("#### 시즌 정보 없음")
                                    st.info("해당 시즌의 데이터가 없습니다.")
                        
                        # 좌투수 탭
                        with tab_lefty:
                            st.write("### 좌투수 상대 (타구 비행시간)")
                            lefty_cols = st.columns(3)
                            
                            for i in range(min(3, len(display_years))):
                                with lefty_cols[i]:
                                    current_year = display_years[i]
                                    st.write(f"#### {current_year} 시즌")
                                    
                                    # 해당 연도 및 좌투수 데이터 필터링
                                    year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                                    lefty_data = year_data[year_data[pitcher_hand_col] == 'L']
                                    
                                    if len(lefty_data) > 0:
                                        # Spray Chart 데이터 생성
                                        lefty_spraychart_dataframe = spraychart_df(lefty_data)
                                        
                                        # 올바른 함수명 사용
                                        spraychart_hangtime_fig = season_hangtime_spraychart(
                                            lefty_spraychart_dataframe, 
                                            batter_name=f"{batter_name} vs 좌투수 ({current_year})"
                                        )
                                        st.plotly_chart(spraychart_hangtime_fig, key=f"hangtime_lefty_{batter}_{current_year}", use_container_width=True)
                                    else:
                                        st.info(f"{current_year} 시즌 좌투수 상대 데이터가 없습니다.")
                            
                            # 남은 컬럼에 빈 내용 표시
                            for i in range(len(display_years), 3):
                                with lefty_cols[i]:
                                    st.write("#### 시즌 정보 없음")
                                    st.info("해당 시즌의 데이터가 없습니다.")
                        
                        # 우투수 2S 탭
                        if strikes_col is not None:
                            with tab_righty_2s:
                                st.write("### 우투수 상대 2스트라이크 (타구 비행시간)")
                                righty_2s_cols = st.columns(3)
                                
                                for i in range(min(3, len(display_years))):
                                    with righty_2s_cols[i]:
                                        current_year = display_years[i]
                                        st.write(f"#### {current_year} 시즌")
                                        
                                        # 해당 연도, 우투수, 2스트라이크 데이터 필터링
                                        year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                                        righty_2s_data = year_data[(year_data[pitcher_hand_col] == 'R') & (year_data[strikes_col] == 2)]
                                        
                                        if len(righty_2s_data) > 0:
                                            # Spray Chart 데이터 생성
                                            righty_2s_spraychart_dataframe = spraychart_df(righty_2s_data)
                                            
                                            spraychart_hangtime_fig = season_hangtime_spraychart(
                                                righty_2s_spraychart_dataframe, 
                                                batter_name=f"{batter_name} vs 우투수 2S ({current_year})"
                                            )
                                            st.plotly_chart(spraychart_hangtime_fig, key=f"hangtime_righty_2s_{batter}_{current_year}", use_container_width=True)
                                        else:
                                            st.info(f"{current_year} 시즌 우투수 2S 데이터가 없습니다.")
                                
                                # 남은 컬럼에 빈 내용 표시
                                for i in range(len(display_years), 3):
                                    with righty_2s_cols[i]:
                                        st.write("#### 시즌 정보 없음")
                                        st.info("해당 시즌의 데이터가 없습니다.")
                            
                            # 좌투수 2S 탭
                            with tab_lefty_2s:
                                st.write("### 좌투수 상대 2스트라이크 (타구 비행시간)")
                                lefty_2s_cols = st.columns(3)
                                
                                for i in range(min(3, len(display_years))):
                                    with lefty_2s_cols[i]:
                                        current_year = display_years[i]
                                        st.write(f"#### {current_year} 시즌")
                                        
                                        # 해당 연도, 좌투수, 2스트라이크 데이터 필터링
                                        year_data = batter_raw_df[batter_raw_df[year_col] == current_year]
                                        lefty_2s_data = year_data[(year_data[pitcher_hand_col] == 'L') & (year_data[strikes_col] == 2)]
                                        
                                        if len(lefty_2s_data) > 0:
                                            # Spray Chart 데이터 생성
                                            lefty_2s_spraychart_dataframe = spraychart_df(lefty_2s_data)
                                            
                                            spraychart_hangtime_fig = season_hangtime_spraychart(
                                                lefty_2s_spraychart_dataframe, 
                                                batter_name=f"{batter_name} vs 좌투수 2S ({current_year})"
                                            )
                                            st.plotly_chart(spraychart_hangtime_fig, key=f"hangtime_lefty_2s_{batter}_{current_year}", use_container_width=True)
                                        else:
                                            st.info(f"{current_year} 시즌 좌투수 2S 데이터가 없습니다.")
                                
                                # 남은 컬럼에 빈 내용 표시
                                for i in range(len(display_years), 3):
                                    with lefty_2s_cols[i]:
                                        st.write("#### 시즌 정보 없음")
                                        st.info("해당 시즌의 데이터가 없습니다.")
                        
                        # 투수 유형별 범례
                        st.markdown(""" <div style="text-align: left; font-size: 0.9em;">
                                <span style="font-weight: bold;">색상 범례:</span> 
                                붉은색: 2~4초 비행 / 옅은 파란색: 1초 미만 / 옅은 갈색: 4초 이상
                                </div>
                                """, 
                                unsafe_allow_html=True)
                else:
                    st.info("투수 정보가 없어 투수 유형별 분석을 건너뜁니다.")
            
                # KT_WIZ 투수별 분석 expander (타구 비행시간)
                pitcher_team_col = None
                pitcher_name_col = None
                
                possible_team_cols = ['pitcherteam', 'pitcher_team', 'p_team', 'team']
                possible_name_cols = ['player_name', 'pitcher_name', 'p_name', 'name']
                
                for col in possible_team_cols:
                    if col in batter_raw_df.columns:
                        pitcher_team_col = col
                        break
                
                for col in possible_name_cols:
                    if col in batter_raw_df.columns:
                        pitcher_name_col = col
                        break
                
                if pitcher_team_col is not None and pitcher_name_col is not None:
                    with st.expander(f"vs KT_WIZ 투수별: {batter_name} (타구 비행시간)"):
                        st.write("KT_WIZ 투수별 스프레이 차트 - 타구 비행시간 기준")
                        
                        # KT_WIZ 투수 데이터 필터링
                        kt_wiz_data = batter_raw_df[batter_raw_df[pitcher_team_col] == 'KT_WIZ']
                        
                        if len(kt_wiz_data) > 0:
                            # KT_WIZ 투수 목록 추출
                            kt_pitchers = kt_wiz_data[pitcher_name_col].unique()
                            
                            if len(kt_pitchers) > 0:
                                # 투수별 탭 생성 (최대 10명까지)
                                if strikes_col is not None:
                                    # 각 투수별로 전체와 2S 탭 생성
                                    for pitcher in kt_pitchers[:5]:  # 최대 5명으로 제한 (탭이 너무 많아지지 않도록)
                                        with st.expander(f"vs {pitcher}"):
                                            tab_pitcher_all, tab_pitcher_2s = st.tabs(["전체 카운트", "2스트라이크"])
                                            
                                            # 해당 투수 데이터 필터링
                                            pitcher_data = kt_wiz_data[kt_wiz_data[pitcher_name_col] == pitcher]
                                            
                                            # 전체 카운트 탭
                                            with tab_pitcher_all:
                                                st.write(f"### vs {pitcher} 전체 (타구 비행시간)")
                                                
                                                # 연도별 컬럼 생성
                                                pitcher_cols = st.columns(3)
                                                
                                                # 해당 투수와의 연도별 데이터 표시
                                                pitcher_years = sorted(pitcher_data[year_col].unique(), reverse=True)
                                                display_pitcher_years = pitcher_years[:3]
                                                
                                                for i in range(min(3, len(display_pitcher_years))):
                                                    with pitcher_cols[i]:
                                                        current_year = display_pitcher_years[i]
                                                        st.write(f"#### {current_year} 시즌")
                                                        
                                                        # 해당 연도 및 투수 데이터 필터링
                                                        year_pitcher_data = pitcher_data[pitcher_data[year_col] == current_year]
                                                        
                                                        if len(year_pitcher_data) > 0:
                                                            # Spray Chart 데이터 생성
                                                            pitcher_spraychart_dataframe = spraychart_df(year_pitcher_data)
                                                            
                                                            # 올바른 함수명 사용
                                                            pitcher_hangtime_fig = season_hangtime_spraychart(
                                                                pitcher_spraychart_dataframe, 
                                                                batter_name=f"{batter_name} vs {pitcher} ({current_year})"
                                                            )
                                                            st.plotly_chart(pitcher_hangtime_fig, key=f"kt_pitcher_hangtime_{batter}_{pitcher}_{current_year}", use_container_width=True)
                                                            
                                                            # 간단한 통계 표시
                                                            total_pitches = len(year_pitcher_data)
                                                            hits = len(year_pitcher_data[year_pitcher_data['events'].notna()])
                                                            st.write(f"총 대결: {total_pitches}구")
                                                            if hits > 0:
                                                                st.write(f"안타: {hits}개")
                                                        else:
                                                            st.info(f"{current_year} 시즌 데이터 없음")
                                                
                                                # 남은 컬럼에 빈 내용 표시
                                                for i in range(len(display_pitcher_years), 3):
                                                    with pitcher_cols[i]:
                                                        st.write("#### 시즌 정보 없음")
                                                        st.info("해당 시즌의 데이터가 없습니다.")
                                            
                                            # 2스트라이크 탭
                                            with tab_pitcher_2s:
                                                st.write(f"### vs {pitcher} 2스트라이크 (타구 비행시간)")
                                                
                                                # 연도별 컬럼 생성
                                                pitcher_2s_cols = st.columns(3)
                                                
                                                for i in range(min(3, len(display_pitcher_years))):
                                                    with pitcher_2s_cols[i]:
                                                        current_year = display_pitcher_years[i]
                                                        st.write(f"#### {current_year} 시즌")
                                                        
                                                        # 해당 연도, 투수, 2스트라이크 데이터 필터링
                                                        year_pitcher_2s_data = pitcher_data[
                                                            (pitcher_data[year_col] == current_year) & 
                                                            (pitcher_data[strikes_col] == 2)
                                                        ]
                                                        
                                                        if len(year_pitcher_2s_data) > 0:
                                                            # Spray Chart 데이터 생성
                                                            pitcher_2s_spraychart_dataframe = spraychart_df(year_pitcher_2s_data)
                                                            
                                                            pitcher_2s_hangtime_fig = season_hangtime_spraychart(
                                                                pitcher_2s_spraychart_dataframe, 
                                                                batter_name=f"{batter_name} vs {pitcher} 2S ({current_year})"
                                                            )
                                                            st.plotly_chart(pitcher_2s_hangtime_fig, key=f"kt_pitcher_2s_hangtime_{batter}_{pitcher}_{current_year}", use_container_width=True)
                                                            
                                                            # 간단한 통계 표시
                                                            total_2s_pitches = len(year_pitcher_2s_data)
                                                            hits_2s = len(year_pitcher_2s_data[year_pitcher_2s_data['events'].notna()])
                                                            st.write(f"2S 상황 대결: {total_2s_pitches}구")
                                                            if hits_2s > 0:
                                                                st.write(f"2S 상황 안타: {hits_2s}개")
                                                        else:
                                                            st.info(f"{current_year} 시즌 2S 데이터 없음")
                                                
                                                # 남은 컬럼에 빈 내용 표시
                                                for i in range(len(display_pitcher_years), 3):
                                                    with pitcher_2s_cols[i]:
                                                        st.write("#### 시즌 정보 없음")
                                                        st.info("해당 시즌의 데이터가 없습니다.")
                                else:
                                    # strikes_col이 없는 경우 기존 방식 유지
                                    pitcher_tabs = st.tabs([f"{pitcher}" for pitcher in kt_pitchers[:10]])
                                    
                                    for idx, pitcher in enumerate(kt_pitchers[:10]):
                                        with pitcher_tabs[idx]:
                                            st.write(f"### vs {pitcher} (타구 비행시간)")
                                            
                                            # 해당 투수 데이터 필터링
                                            pitcher_data = kt_wiz_data[kt_wiz_data[pitcher_name_col] == pitcher]
                                            
                                            # 연도별 컬럼 생성
                                            pitcher_cols = st.columns(3)
                                            
                                            # 해당 투수와의 연도별 데이터 표시
                                            pitcher_years = sorted(pitcher_data[year_col].unique(), reverse=True)
                                            display_pitcher_years = pitcher_years[:3]
                                            
                                            for i in range(min(3, len(display_pitcher_years))):
                                                with pitcher_cols[i]:
                                                    current_year = display_pitcher_years[i]
                                                    st.write(f"#### {current_year} 시즌")
                                                    
                                                    # 해당 연도 및 투수 데이터 필터링
                                                    year_pitcher_data = pitcher_data[pitcher_data[year_col] == current_year]
                                                    
                                                    if len(year_pitcher_data) > 0:
                                                        # Spray Chart 데이터 생성
                                                        pitcher_spraychart_dataframe = spraychart_df(year_pitcher_data)
                                                        
                                                        # 올바른 함수명 사용
                                                        pitcher_hangtime_fig = season_hangtime_spraychart(
                                                            pitcher_spraychart_dataframe, 
                                                            batter_name=f"{batter_name} vs {pitcher} ({current_year})"
                                                        )
                                                        st.plotly_chart(pitcher_hangtime_fig, key=f"kt_pitcher_hangtime_{batter}_{pitcher}_{current_year}", use_container_width=True)
                                                        
                                                        # 간단한 통계 표시
                                                        total_pitches = len(year_pitcher_data)
                                                        hits = len(year_pitcher_data[year_pitcher_data['events'].notna()])
                                                        st.write(f"총 대결: {total_pitches}구")
                                                        if hits > 0:
                                                            st.write(f"안타: {hits}개")
                                                    else:
                                                        st.info(f"{current_year} 시즌 데이터 없음")
                                            
                                            # 남은 컬럼에 빈 내용 표시
                                            for i in range(len(display_pitcher_years), 3):
                                                with pitcher_cols[i]:
                                                    st.write("#### 시즌 정보 없음")
                                                    st.info("해당 시즌의 데이터가 없습니다.")
                            else:
                                st.info("KT_WIZ 투수 데이터가 없습니다.")
                        else:
                            st.info(f"{batter_name}의 KT_WIZ 상대 데이터가 없습니다.")
                        
                        # KT_WIZ 투수별 범례 (타구 비행시간)
                        st.markdown(""" <div style="text-align: left; font-size: 0.9em;">
                                <span style="font-weight: bold;">색상 범례:</span> 
                                붉은색: 2~4초 비행 / 옅은 파란색: 1초 미만 / 옅은 갈색: 4초 이상
                                </div>
                                """, 
                                unsafe_allow_html=True)
                else:
                    st.info("투수 정보가 없어 KT_WIZ 투수별 분석을 건너뜁니다.")



                


            

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
