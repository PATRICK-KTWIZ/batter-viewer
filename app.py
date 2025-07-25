import os
import pandas as pd
import numpy as np
from PIL import Image
from io import BytesIO
import streamlit as st
from datetime import datetime
import streamlit.components.v1

# defense_definition에서 필요한 함수들만 import
from defense_definition import (
    select_level,filter_player_data, 
    generate_hangtime_print_page, season_hangtime_spraychart_combined, 
    season_hangtime_spraychart, spraychart_df, get_data_by_level
)

# Set a unique token for the cookie
COOKIE_TOKEN = "my_unique_cookie_token"

# 페이지 설정
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="KT WIZ BATTING ANALYTICS"
)

# 세션 상태 초기화
if 'loggedIn' not in st.session_state:
    st.session_state.loggedIn = False

if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"

if 'selected_players' not in st.session_state:
    st.session_state.selected_players = []

# CSS 스타일
st.markdown("""
<style>
    /* 전체 페이지 스타일 */
    .stApp {
        background: linear-gradient(135deg, #6c9176 50%, #f0f0f0 50%);
        background-attachment: fixed;
        height: 95vh;
        max-height: 1000px;
        overflow: auto;
    }

    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #6c9176 !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background-color: #cccccc !important;
        color: black !important;
        width: 100%;
        border-radius: 7px;
        padding: 0.5rem 1rem;
        height: 2rem;
        font-size: 16px;
        margin-bottom: 0px;
        font-weight: 500;
    }

    /* 사이드바 selectbox 라벨 색상 변경 */
    [data-testid="stSidebar"] .css-81oif8,
    [data-testid="stSidebar"] .css-1inwz65,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox > div > label {
        color: black !important;
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
        background-color: #6c9176;
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
        color: #2d2d2d;
        font-size: 18px;
        margin-bottom: 10px;
    }
    
    /* 안내 텍스트 스타일 */
    .info-text {
        font-size: 15px;
        color: #2d2d2d;
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

# 컨테이너 생성
headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()

# 🚀 데이터 캐싱 최적화
@st.cache_data(ttl=3600)
def get_cached_full_data():
    """캐시된 전체 데이터 가져오기"""
    return get_data_by_level(['KoreaBaseballOrganization', 'KBO Minors'])

# 유틸리티 함수들
def get_user_id():
    return st.session_state.get(COOKIE_TOKEN)

def set_user_id(user_id):
    st.session_state[COOKIE_TOKEN] = user_id

def is_user_logged_in():
    return st.session_state.get('loggedIn', False)

def find_id(player_dataset, select_player):
    find_player = player_dataset[player_dataset['NAME'] == select_player]
    return find_player.iloc[0]['TM_ID']

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False

def login(userName, password):
    user_df = pd.read_csv('./user_info_2025.csv')
    user_id = user_df['ID'].tolist()
    user_password = user_df['Password'].tolist()
    
    if userName in user_id:
        index = user_id.index(userName)
        return password == user_password[index]
    return False

def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        set_user_id(userName)
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("유효하지 않은 ID 또는 패스워드 입니다.")

def show_print_page():
    """프린트 전용 페이지 - A4 용지 규격 2x2 레이아웃"""

    from datetime import datetime
    today_date = datetime.now().strftime('%Y년 %m월 %d일')
    
    st.markdown("""
    <style>
        /* A4 용지 규격 설정 */
        .stApp { 
            background: #ffffff !important; 
            max-width: 300mm !important;
            margin: 0 auto !important;
            padding-top: 0 !important;
        }
        
        /* 사이드바 숨기기 */
        [data-testid="stSidebar"] { display: none; }
        
        /* Streamlit 기본 여백 제거 */
        .main .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
        }
        
        /* 프린트 시 Streamlit 요소들 완전히 숨기기 */
        @media print {
            /* 페이지 설정 */
            @page {
                margin: 5mm !important;
                size: A4 !important;
            }
            
            /* 모든 버튼 숨기기 */
            button, .stButton, [data-testid="stButton"], .element-container button {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                width: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            
            /* no-print 클래스 완전히 제거 */
            .no-print, .no-print * {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                width: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                position: absolute !important;
                left: -9999px !important;
            }
            
            /* Streamlit 헤더/푸터 숨기기 */
            header, footer, .stApp > header, .stApp > footer {
                display: none !important;
            }
            
            /* 기타 Streamlit UI 요소들 숨기기 */
            [data-testid="stToolbar"], 
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"],
            .streamlit-container > div:first-child {
                display: none !important;
            }
            
            /* 최상단 여백 완전 제거 */
            html, body {
                margin: 0 !important;
                padding: 0 !important;
                font-size: 9px !important;
            }
            
            .stApp {
                margin: 5 !important;
                padding: 0 !important;
            }
            
            .main .block-container {
                padding: 0 !important;
                margin: 10px !important;
            }
            
            /* 프린트용 차트 컨테이너 - 크기 증가 */
            .stPlotlyChart {
                height: 400px !important;
                max-height: 400px !important;
                width: 50% !important;
                max-width: 50% !important;      
                margin: 10px !important;
                padding: 0px !important;  
            }
                
            /* 컬럼 컨테이너 */   
            div[data-testid="column"] {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;    /* 🎯 프린트용도 중앙 정렬 */
                padding-left: 10px !important;
                padding-right: 10px !important;
                margin-bottom: 1px !important;
            }
                        
            /* 페이지 브레이크 */
            .page-break {
                page-break-after: always;
            }
            
            /* 프린트 시 여백 최소화 */
            .chart-row-spacing {
                margin-bottom: 5px !important;
            }
            
            .legend-spacing {
                margin-top: 10px !important;
                margin-bottom: 10px !important;
                font-size: 13px !important;
            }
            
            /* 헤더 크기 축소 */
            .page-header {
                margin-top: 0 !important;
                margin-bottom: 8px !important;
                padding-top: 0 !important;
                padding-bottom: 3px !important;
            }
            
            .page-title {
                font-size: 22px !important;  /* 프린트용 제목 크게 */
                margin-bottom: 1px !important;
                font-weight: bold !important;
                letter-spacing: 0.3px !important;
            }
            
            .page-subtitle {
                font-size: 16px !important;
                margin-bottom: 1px !important;
            }
            
            .page-info {
                font-size: 13px !important;
                margin-bottom: 0px !important;
            }
            
            /* 빈 페이지 방지 - 높이 증가 */
            .no-data {
                height: 350px !important;
                page-break-inside: avoid;
                font-size: 12px !important;
            }
            
            /* 첫 페이지 공백 방지 */
            .page-container:first-child {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
                

            /* 컬럼 간격 완전 제거 */
            .row-widget.stHorizontal {
                gap: 0px !important;           /* 컬럼 간 간격 제거 */
                margin: 10px !important;
                padding: 0 !important;
            }
        }
        
        /* 화면용 */
        .stPlotlyChart {
            height: 400px !important;
            max-height: 400px !important;
            width: 100% !important;
            max-width: 95% !important;      /* 컨테이너의 95%까지 */
            margin: 0 auto !important;      /* 중앙 정렬 */
            padding: 0 !important;
        }
                
        /* 컬럼 간격 완전 제거 */
        .row-widget.stHorizontal {
            gap: 0px !important;           /* 컬럼 간 간격 제거 */
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Streamlit 기본 컬럼 스타일 오버라이드 */
        .element-container {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }

        /* 컬럼 컨테이너 간격 제거 */
        div[data-testid="column"] {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: flex-start !important;
            padding: 0px !important;        /* 모든 패딩 제거 */
            margin: 0px !important;         /* 모든 마진 제거 */
            border: none !important;
            min-width: 0 !important;        /* 최소 너비 제한 제거 */
            flex: 1 !important;             /* 동일한 크기로 분할 */
        }

        /* 헤더 스타일 */
        .page-header {
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 5px;
            margin-bottom: 12px;
            margin-top: 0px !important;
            padding-top: 0px !important;
            page-break-inside: avoid;
        }
        
        /* 제목 스타일일 */        
        .page-title {
            font-size: 28px;              /* 20px → 28px */
            font-weight: bold;
            margin-bottom: 2px;
            color: #333;
            letter-spacing: 0.5px;        /* 글자 간격 추가로 더 선명하게 */
        }
        
        .page-subtitle {
            font-size: 15px;
            color: #666;
            margin-bottom: 2px;
        }
        
        .page-info {
            font-size: 11px;
            color: #888;
            margin-bottom: 0px;    
        }
        
        /* 차트 행 간격 최소화 */
        .chart-row-spacing {
            margin-bottom: 2px !important;
        }
        
        /* 범례 간격 조정 */
        .legend-spacing {
            margin-top: 5px !important;
            margin-bottom: 10px !important;
        }
        
        /* 데이터 없음 표시 - 크기 증가 */
        .no-data {
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-style: italic;
            border: 2px dashed #ddd;
            border-radius: 5px;
            background-color: #f8f9fa;
            font-size: 14px;
            margin-bottom: 0px !important;
        }
                
        /* 페이지 컨테이너 */
        .page-container {
            page-break-inside: avoid;
            min-height: 0vh;
            margin-top: 0px !important;
            padding-top: 0px !important;
        }
                

    /* 전체 앱 컨테이너 - 연한 회색 */
    .stApp {
        background: #f0f0f0 !important;
        border: 3px solid #ff0000 !important; /* 빨간 테두리 */
    }
    
    /* 메인 블록 컨테이너 - 연한 파란색 */
    .main .block-container {
        background: #e6f3ff !important;
        border: 2px solid #0066cc !important; /* 파란 테두리 */
    }
    
    /* 수평 컨테이너 (컬럼들의 부모) - 연한 녹색 */
    .row-widget.stHorizontal,
    .stHorizontal,
    div[data-testid="stHorizontalBlock"] {
        background: #e6ffe6 !important;
        border: 2px solid #00cc00 !important; /* 녹색 테두리 */
        gap: 0px !important;
        margin: 0px !important;
        padding: 5px !important; /* 디버깅용 패딩 */
    }
    
    /* 개별 컬럼 - 연한 노란색과 연한 주황색 번갈아 */
    div[data-testid="column"]:nth-child(1) {
        background: #fff9e6 !important; /* 연한 노란색 */
        border: 2px solid #ff9900 !important; /* 주황 테두리 */
        padding: 3px !important;
        margin: 0px !important;
        flex: 1 1 50% !important;
    }
    
    div[data-testid="column"]:nth-child(2) {
        background: #ffe6f0 !important; /* 연한 분홍색 */
        border: 2px solid #ff0099 !important; /* 분홍 테두리 */
        padding: 3px !important;
        margin: 0px !important;
        flex: 1 1 50% !important;
    }
    
    /* element-container - 연한 보라색 */
    .element-container {
        background: #f0e6ff !important;
        border: 1px solid #9900cc !important; /* 보라 테두리 */
        margin: 2px !important;
        padding: 2px !important;
    }
    
    /* 차트 컨테이너 - 연한 청록색 */
    .stPlotlyChart,
    div[data-testid="stPlotlyChart"] {
        background: #e6ffff !important;
        border: 2px solid #00cccc !important; /* 청록 테두리 */
        margin: 1px !important;
        padding: 1px !important;
        width: 100% !important;
        height: 400px !important;
    }
    
    /* no-data 영역 - 연한 회색 */
    .no-data {
        background: #f5f5f5 !important;
        border: 2px dashed #999999 !important;
        color: #666 !important;
    }
    
    /* 🎯 프린트 시에는 색상 제거 */
    @media print {
        .stApp,
        .main .block-container,
        .row-widget.stHorizontal,
        .stHorizontal,
        div[data-testid="stHorizontalBlock"],
        div[data-testid="column"],
        .element-container,
        .stPlotlyChart,
        div[data-testid="stPlotlyChart"],
        .no-data {
            background: white !important;
            border: none !important;
        }
        
        /* 프린트용 간격 설정 */
        .row-widget.stHorizontal,
        .stHorizontal {
            gap: 0px !important;
            padding: 0px !important;
            margin: 0px !important;
        }
        
        div[data-testid="column"] {
            padding: 0px !important;
            margin: 0px !important;
            flex: 1 1 50% !important;
        }
        
        .element-container {
            margin: 0px !important;
            padding: 0px !important;
        }
        
        .stPlotlyChart {
            margin: 0px !important;
            padding: 0px !important;
            height: 500px !important;
        }
    }
    
    /* 디버깅 정보 표시 */
    .debug-info {
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 12px;
        z-index: 9999;
    }
    
    @media print {
        .debug-info {
            display: none !important;
        }
    }


    </style>
    """, unsafe_allow_html=True)
    
    # 필요한 데이터 확인
    required_keys = ['analysis_batter_dataframes', 'analysis_selected_player_df', 'print_charts']
    missing_keys = [key for key in required_keys if key not in st.session_state]
    
    if missing_keys:
        st.error(f"❌ 필요한 데이터가 없습니다: {missing_keys}")
        st.info("메인 페이지에서 분석을 먼저 실행해주세요.")
        return
    
    # 저장된 차트들 표시
    batter_dataframes = st.session_state.analysis_batter_dataframes
    selected_player_df = st.session_state.analysis_selected_player_df
    print_charts = st.session_state.print_charts
    kt_pitcher_charts = st.session_state.get('kt_pitcher_charts', {})
    
    page_number = 1
    
    # 각 타자별 프린트 페이지 생성
    for batter_idx, (batter, batter_df) in enumerate(batter_dataframes.items()):
        batter_str = str(batter)
        batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
        batter_name = batter_finder.iloc[0]['NAME'] if len(batter_finder) > 0 else f"선수_{batter}"
        
        # # 페이지 컨테이너 시작 - 첫 페이지 여백 제거
        # st.markdown(f'<div class="page-container" style="margin-top: 0px; padding-top: 0px;">', unsafe_allow_html=True)

        # 페이지 구분 (첫 번째 선수가 아닐 때)
        if batter_idx > 0:
            st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="page-header" style="margin-top: 0px !important; padding-top: 0px !important;">
            <div class="page-title">{batter_name} 타구비행시간 분석(2025)</div>
            <div class="page-subtitle">Baseball Intelligence Transformation Report</div>
            <div class="page-info">생성일: {today_date} | 분석기간: 2025시즌 | KT WIZ | Page {page_number}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 첫 번째 행: 우투수 vs 좌투수
        col1, col2 = st.columns(2)
        with col1:
            if f"{batter}_rhp" in print_charts:
                chart = print_charts[f"{batter}_rhp"]
                chart.update_layout(height=400, width=400, margin=dict(l=0, r=34, t=40, b=30))
                st.plotly_chart(chart, use_container_width=False, key=f"print_rhp_{batter}")
                
            else:
                st.markdown('<div class="no-data">우투수 데이터 없음</div>', unsafe_allow_html=True)
        
        with col2:
            if f"{batter}_lhp" in print_charts:
                chart = print_charts[f"{batter}_lhp"]
                chart.update_layout(height=400, width=400, margin=dict(l=0, r=34, t=40, b=30))
                st.plotly_chart(chart, use_container_width=False, key=f"print_lhp_{batter}")
            else:
                st.markdown('<div class="no-data">좌투수 데이터 없음</div>', unsafe_allow_html=True)
        
        # 두 번째 행: 우투수 2S vs 좌투수 2S
        col3, col4 = st.columns(2)
        with col3:
            if f"{batter}_rhp_2s" in print_charts:
                chart = print_charts[f"{batter}_rhp_2s"]
                chart.update_layout(height=400, width=400, margin=dict(l=0, r=34, t=40, b=30))
                st.plotly_chart(chart, use_container_width=False, key=f"print_rhp_2s_{batter}")
            else:
                st.markdown('<div class="no-data">우투수 2S 데이터 없음</div>', unsafe_allow_html=True)
        
        with col4:
            if f"{batter}_lhp_2s" in print_charts:
                chart = print_charts[f"{batter}_lhp_2s"]
                chart.update_layout(height=400, width=400, margin=dict(l=0, r=34, t=40, b=30))
                st.plotly_chart(chart, use_container_width=False, key=f"print_lhp_2s_{batter}")
            else:
                st.markdown('<div class="no-data">좌투수 2S 데이터 없음</div>', unsafe_allow_html=True)
        
        # 범례
        st.markdown("""
        <div class="legend-spacing" style="text-align: left; font-size: 0.8em; padding: 3px; background-color: #f8f9fa; border-radius: 3px;">
            <span style="font-weight: bold;">모양:</span> ● Fastball / ▲ Non-Fastball &nbsp;&nbsp;
            <span style="font-weight: bold;">색상:</span> 붉은색: 2~4초 / 파란색: 2초 미만 / 갈색: 4초 이상
        </div>
        """, unsafe_allow_html=True)

        page_number += 1
        

        
        # 🎯 KT 투수별 차트 추가 (hit_distance >= 40)
        kt_pitcher_keys = [key for key in kt_pitcher_charts.keys() if key.startswith(f"{batter}_pitcher_")]
        
        if kt_pitcher_keys:
            
            # KT 투수별 분석을 새 페이지에서 시작
            st.markdown('<div class="kt-pitcher-section">', unsafe_allow_html=True)

            # 페이지 브레이크 추가
            st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="page-header" style="margin-top: 0px !important; padding-top: 0px !important;">
                <div class="page-title">{batter_name} vs KT 투수별 분석</div>
                <div class="page-subtitle">Baseball Intelligence Transformation Report</div>
                <div class="page-info">생성일: {today_date} | 분석기간: 2025~2023 통합데이터터시즌 | KT WIZ | Page {page_number}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # KT 투수별 차트를 2x2 그리드로 표시
            kt_charts_list = list(kt_pitcher_keys)
            
            # 2x2 그리드로 표시 (한 번에 최대 4개)
            for i in range(0, len(kt_charts_list), 4):
                batch_charts = kt_charts_list[i:i+4]

                # 첫 번째 그룹이 아닐 때 페이지 브레이크 추가
                if i > 0:
                    st.markdown('<div class="kt-pitcher-grid-break"></div>', unsafe_allow_html=True)
                    page_number += 1
                    # 새 페이지 헤더
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 15px; padding: 5px; background-color: #f0f0f0; border-radius: 3px;">
                        <h5 style="margin: 0; color: #333;">{batter_name} vs KT 투수별 분석 (계속) | Page {page_number}</h5>
                    </div>
                    """, unsafe_allow_html=True)                
                
                # 첫 번째 행 (2개)
                if len(batch_charts) >= 1:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if len(batch_charts) >= 1:
                            chart_key = batch_charts[0]
                            if chart_key in kt_pitcher_charts:
                                chart = kt_pitcher_charts[chart_key]
                                chart.update_layout(height=400, width=400, margin=dict(l=0, r=34, t=40, b=30))
                                st.plotly_chart(chart, use_container_width=False, key=f"kt_print_{chart_key}")
                            else:
                                st.markdown('<div class="no-data">차트 없음</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="no-data">-</div>', unsafe_allow_html=True)
                    
                    with col2:
                        if len(batch_charts) >= 2:
                            chart_key = batch_charts[1]
                            if chart_key in kt_pitcher_charts:
                                chart = kt_pitcher_charts[chart_key]
                                chart.update_layout(height=400, width=400, margin=dict(l=0, r=34, t=40, b=30))
                                st.plotly_chart(chart, use_container_width=False, key=f"kt_print_{chart_key}")
                            else:
                                st.markdown('<div class="no-data">차트 없음</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="no-data">-</div>', unsafe_allow_html=True)
                
                # 두 번째 행 (2개 더)
                if len(batch_charts) >= 3:
                    col3, col4 = st.columns(2)
                    
                    with col3:
                        if len(batch_charts) >= 3:
                            chart_key = batch_charts[2]
                            if chart_key in kt_pitcher_charts:
                                chart = kt_pitcher_charts[chart_key]
                                chart.update_layout(height=400, width=400, margin=dict(l=0, r=34, t=40, b=30))
                                st.plotly_chart(chart, use_container_width=False, key=f"kt_print_{chart_key}")
                            else:
                                st.markdown('<div class="no-data">차트 없음</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="no-data">-</div>', unsafe_allow_html=True)
                    
                    with col4:
                        if len(batch_charts) >= 4:
                            chart_key = batch_charts[3]
                            if chart_key in kt_pitcher_charts:
                                chart = kt_pitcher_charts[chart_key]
                                chart.update_layout(height=400, width=400, margin=dict(l=0, r=34, t=40, b=30))
                                st.plotly_chart(chart, use_container_width=False, key=f"kt_print_{chart_key}")
                            else:
                                st.markdown('<div class="no-data">차트 없음</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="no-data">-</div>', unsafe_allow_html=True)
                
                # 8개 이상일 경우 페이지 구분
                if i + 4 < len(kt_charts_list):
                    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)
                
                
            
            # 범례
            st.markdown("""
            <div class="legend-spacing" style="text-align: left; font-size: 0.8em; padding: 3px; background-color: #f8f9fa; border-radius: 3px;">
                <span style="font-weight: bold;">모양:</span> ● Fastball / ▲ Non-Fastball &nbsp;&nbsp;
                <span style="font-weight: bold;">색상:</span> 붉은색: 2~4초 / 파란색: 2초 미만 / 갈색: 4초 이상
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)  # kt-pitcher-section 종료


        # # 페이지 구분선 (다음 선수가 있을 때만)
        # if page_number < len(batter_dataframes):
        #     st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)
        #     st.markdown("---")
        
            page_number += 1

        # 개인 투수별 차트(다음페이지)





    # 뒤로가기 버튼
    st.markdown('<div class="no-print" style="margin-top: 10px; text-align: center;">', unsafe_allow_html=True)
    if st.button("← 메인으로", key="back_to_main", help="메인 페이지로 돌아가기"):
        st.session_state.current_page = "main"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)




def show_login_page():
    """로그인 페이지"""
    
    st.markdown("""
    <style>
        [data-testid="stVerticalBlock"] > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
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
                        <span style='color: #2d2d2d;'>KT WIZ</span> 
                        <span style='color: red;'>DEFENSIVE SHIFT ANALYTICS</span> 
                        <span style='color: #2d2d2d;'>PAGE[Outfield]</span>
                    </h1>
                </div>
                """, unsafe_allow_html=True)

    left_col, middle1_col, middle2_col, right_col = st.columns([0.7, 4, 5, 0.7])

    with middle1_col:
        st.markdown('<div class="logo-container" style="padding-top: 100px;">', unsafe_allow_html=True)
        st.image("ktwiz_emblem.png", width=280)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with middle2_col:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="warning-text">※허가된 사용자 외 사용을 금함</div>', unsafe_allow_html=True)
        st.markdown('<div class="header-text">케이티 위즈</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader-text">수비시프트 분석페이지에 오신것을 환영합니다.</div>', unsafe_allow_html=True)
        st.markdown('<hr style="margin: 0px 0;">', unsafe_allow_html=True)

        userName = st.text_input("", placeholder="아이디", label_visibility="collapsed")
        password = st.text_input("", placeholder="비밀번호", type="password", label_visibility="collapsed")
        
        st.button("로그인", on_click=LoggedIn_Clicked, args=(userName, password))
        
        checkbox_col1, checkbox_col2 = st.columns([1, 3])
        with checkbox_col1:
            remember_id = st.checkbox("아이디 저장", key="remember_id")
        with checkbox_col2:
            st.markdown('<div class="info-text-custom">아이디와 비밀번호를 입력하여 로그인 후 사용해 주세요.</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Copyright © 2025 kt wiz baseball club. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

def show_analysis_page():
    """메인 분석 페이지"""
    
    st.markdown("""
    <style>
        .stApp {
            background: #ffffff;
            height: 100vh;
            overflow: auto;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("KT WIZ :red[DEFENSEIVE SHIFT] PAGE[타구비행시간]")
    
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.image("ktwiz_emblem.png", width=300)
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

    # 선수 데이터 로드
    id_dataset = pd.read_csv('./player_id_info_2025.csv')
    id_dataset = id_dataset[['team','NAME','POS','TM_ID']]
    id_dataset = id_dataset[id_dataset['POS'] != 'P']

    # 사이드바 설정
    sidebar_text = '<p style="text-align: center; font-family:sans-serif; color:red; font-size: 22px;font-weight:bold">[수비시프트 페이지]</p>'
    st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

    sidebar_text = '<p style="text-align: center; font-family:sans-serif; color: black; font-size: 16px;">본 웹페이지는 kt wiz 전략데이터팀이<br> 개발 및 발행하였으며 허용되는 사용자 외 <br>배포 및 사용을 엄금함</p>'
    st.sidebar.markdown(sidebar_text, unsafe_allow_html=True)

    # 선수 선택 UI
    teams_list = id_dataset['team'].unique().tolist()
    select_team = st.sidebar.selectbox('팀명 선택', teams_list)
    player_dataset = id_dataset[id_dataset['team'] == select_team]

    player_list = player_dataset['NAME'].unique().tolist()
    select_player = st.sidebar.selectbox('선수 선택', player_list)
    player_id = find_id(player_dataset, select_player)
    option = st.sidebar.selectbox('리그 선택', ("-", "KBO(1군)", "KBO(2군)"))

    # 선수 추가/제거 버튼
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button('선수추가', key="add_player_btn"):
            st.session_state.selected_players.append({
                'Team': select_team, 
                'Player Name': select_player, 
                'Level': option, 
                'ID': player_id
            })
    with col2:
        if st.button('새로고침', key="refresh_btn"):
            st.session_state.selected_players = []

    # 선택된 선수 표시
    selected_player_df = pd.DataFrame()
    if st.session_state.selected_players:
        st.subheader('Selected Players:')
        
        for player_info in st.session_state.selected_players:
            st.write(f"Team: {player_info['Team']}, Player Name: {player_info['Player Name']}, Level: {player_info['Level']}, ID: {player_info['ID']}")
            select_player_df = id_dataset[(id_dataset['team'] == player_info['Team']) & (id_dataset['TM_ID'] == player_info['ID'])]
            selected_player_df = pd.concat([selected_player_df, select_player_df])

    # 🚀 실행 버튼
    if st.sidebar.button('실행'):

        st.session_state.analysis_completed = False

        if not st.session_state.selected_players:
            st.warning("⚠️ 선수를 먼저 추가해주세요!")
        else:
            # 🎯 선택된 선수들의 레벨 추출 및 변환
            selected_levels = []
            for player_info in st.session_state.selected_players:
                converted_level = select_level(player_info['Level'])
                if converted_level and converted_level not in selected_levels:
                    selected_levels.append(converted_level)
             
            # 필요한 레벨의 데이터만 로드
            with st.spinner('선택된 레벨의 데이터를 로딩 중입니다...'):
                full_data = get_data_by_level(selected_levels)
            
            if full_data.empty:
                st.error("❌ 데이터를 가져올 수 없습니다.")
            else:
                concatenated_df = pd.DataFrame()
                               
                # 배치 처리로 최적화
                progress_bar = st.progress(0)
                
                for i, player_info in enumerate(st.session_state.selected_players):
                    progress_bar.progress((i + 1) / len(st.session_state.selected_players))
                    
                    player_id = player_info['ID']
                    player_name = player_info['Player Name']
                    
                    # 🎯 여기가 핵심! select_level로 변환
                    player_level = select_level(player_info['Level'])  # 변환된 값 사용
                                      
                    try:
                        # 변환된 level 값으로 필터링 (이미 로드된 full_data에서)
                        player_df = filter_player_data(full_data, player_id, player_level)
                        
                        if not player_df.empty:
                            player_df = player_df.copy()
                            player_df['player_name'] = player_name
                            player_df['team'] = player_info['Team']
                            player_df['selected_level'] = player_info['Level']  # 원본 표시용
                            
                            concatenated_df = pd.concat([concatenated_df, player_df], ignore_index=True)
                        else:
                            st.warning(f"⚠️ {player_name}: 해당 조건에 맞는 데이터가 없습니다")
                            
                    except Exception as e:
                        st.error(f"❌ {player_name} 데이터 처리 중 오류: {str(e)}")
                        continue
                
                progress_bar.empty()
                
                if not concatenated_df.empty:
                    # 🎯 분석 실행 및 저장
                    execute_analysis(concatenated_df, selected_player_df, id_dataset)

                    # 🎯 분석 완료 후 상태 업데이트
                    st.session_state.analysis_completed = True
                    
                else:
                    st.error("❌ 결합된 데이터가 없습니다.")
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📄 페이지 이동")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 메인", key="sidebar_main"):
                st.session_state.current_page = "main"
                st.rerun()
        
        with col2:
            if st.button("🖨️ 프린트", key="sidebar_print"):
                if st.session_state.get('print_charts'):
                    st.session_state.current_page = "print"
                    st.rerun()
                else:
                    st.error("프린트할 데이터가 없습니다!")    

def execute_analysis(concatenated_df, selected_player_df, id_dataset):
    """분석 실행 함수"""
    
    # 타자별로 그룹화
    batter_dataframes = {}
    for batter, group in concatenated_df.groupby('batter'):
        batter_dataframes[batter] = group.copy()
    
    # 🎯 분석 결과를 세션에 저장
    st.session_state.analysis_batter_dataframes = batter_dataframes
    st.session_state.analysis_selected_player_df = selected_player_df
    st.session_state.analysis_id_dataset = id_dataset
    st.session_state.analysis_completed = True
    
    # 차트 표시
    display_charts(batter_dataframes, selected_player_df)

def display_charts(batter_dataframes, selected_player_df):
    """차트 표시 함수 - 프린트용 차트도 함께 저장"""
    
    # 프린트용 차트 저장소 초기화
    if 'print_charts' not in st.session_state:
        st.session_state.print_charts = {}
    
    # 선택된 투수 정보 저장소 초기화
    if 'selected_pitchers_for_print' not in st.session_state:
        st.session_state.selected_pitchers_for_print = {}    
    
    for batter, batter_df in batter_dataframes.items():
        batter_str = str(batter)
        batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
        
        if len(batter_finder) > 0:
            batter_name = batter_finder.iloc[0]['NAME']
        else:
            batter_name = f"선수_{batter_str}"

        st.subheader(f"{batter_name}")

        # 투수 유형별 컬럼 확인
        pitcher_hand_col = None
        possible_hand_cols = ['p_throw', 'pitcher_throws', 'throws', 'hand']
        
        for col in possible_hand_cols:
            if col in batter_df.columns:
                pitcher_hand_col = col
                break
        
        # count_value 컬럼 확인
        count_value_col = None
        possible_count_cols = ['count_value', 'count', 'ball_strike', 'count_situation', 'strikes']

        for col in possible_count_cols:
            if col in batter_df.columns:
                count_value_col = col
                break
        
        # 투수 관련 컬럼 확인
        pitcher_team_col = None
        pitcher_name_col = None

        # 투수 팀 컬럼 찾기
        possible_team_cols = ['pitcherteam', 'pitcher_team', 'p_team', 'team_pitcher']
        for col in possible_team_cols:
            if col in batter_df.columns:
                pitcher_team_col = col
                break

        # 투수 이름 컬럼 찾기
        possible_name_cols = ['NAME_pitcher', 'pitcher_name', 'p_name', 'name_pitcher']
        for col in possible_name_cols:
            if col in batter_df.columns:
                pitcher_name_col = col
                break

        # 연도별 데이터 처리
        year_col = 'game_year'
        years = sorted(batter_df[year_col].unique(), reverse=True)
        display_years = years[:3]
        
        # 기본 차트 표시 (3개 컬럼)
        cols = st.columns(3)
        pitch_type_col = 'p_kind' if 'p_kind' in batter_df.columns else None
        
        for i in range(min(3, len(display_years))):
            with cols[i]:
                current_year = display_years[i]
                st.write(f"#### {current_year} 시즌")
                
                year_data = batter_df[batter_df[year_col] == current_year]
                
                if len(year_data) > 0 and pitch_type_col is not None:
                    fastball_data = year_data[year_data[pitch_type_col] == 'Fastball']
                    non_fastball_data = year_data[year_data[pitch_type_col] != 'Fastball']
                    
                    combined_fig = season_hangtime_spraychart_combined(
                        fastball_data, non_fastball_data,
                        batter_name=f"{batter_name} ({current_year})"
                    )
                    st.plotly_chart(combined_fig, key=f"basic_hangtime_{batter}_{current_year}", use_container_width=True)
                else:
                    year_spraychart_dataframe = spraychart_df(year_data)
                    spraychart_hangtime_fig = season_hangtime_spraychart(
                        year_spraychart_dataframe, 
                        batter_name=f"{batter_name} ({current_year})"
                    )
                    st.plotly_chart(spraychart_hangtime_fig, key=f"basic_hangtime_{batter}_{current_year}", use_container_width=True)
        
        # 남은 컬럼에 빈 내용 표시
        for i in range(len(display_years), 3):
            with cols[i]:
                st.write("#### 시즌 정보 없음")
                st.info("해당 시즌의 데이터가 없습니다.")
        
        # 기본 범례 표시
        st.markdown("""
        <div style="text-align: left; font-size: 0.9em;">
        <span style="font-weight: bold;">모양 구분:</span> ● Fastball / ▲ Non-Fastball<br>
        <span style="font-weight: bold;">색상 범례:</span> 붉은색: 2~4초 비행 / 옅은 파란색: 1초 미만 / 옅은 갈색: 4초 이상
        </div>
        """, unsafe_allow_html=True)
        
        # 투수 유형별 컬럼 확인
        pitcher_hand_col = None
        possible_hand_cols = ['p_throw', 'pitcher_throws', 'throws', 'hand']
        
        for col in possible_hand_cols:
            if col in batter_df.columns:
                pitcher_hand_col = col
                break
        
        # count_value 컬럼 확인
        count_value_col = None
        possible_count_cols = ['count_value', 'count', 'ball_strike', 'count_situation', 'strikes']

        for col in possible_count_cols:
            if col in batter_df.columns:
                count_value_col = col
                break
        
        # 🎯 2025년 데이터로 프린트용 차트 생성 및 저장
        if pitcher_hand_col is not None:
            pitcher_2025_data = batter_df[batter_df[year_col] == 2025]
            
            if len(pitcher_2025_data) > 0:
                # 우투수 데이터
                rhp_data = pitcher_2025_data[pitcher_2025_data[pitcher_hand_col] == 'R']
                if len(rhp_data) > 0 and pitch_type_col is not None:
                    fastball_data = rhp_data[rhp_data[pitch_type_col] == 'Fastball']
                    non_fastball_data = rhp_data[rhp_data[pitch_type_col] != 'Fastball']
                    rhp_fig = season_hangtime_spraychart_combined(
                        fastball_data, non_fastball_data,
                        batter_name=f"{batter_name} vs 우투수"
                    )
                    st.session_state.print_charts[f"{batter}_rhp"] = rhp_fig
                
                # 좌투수 데이터
                lhp_data = pitcher_2025_data[pitcher_2025_data[pitcher_hand_col] == 'L']
                if len(lhp_data) > 0 and pitch_type_col is not None:
                    fastball_data = lhp_data[lhp_data[pitch_type_col] == 'Fastball']
                    non_fastball_data = lhp_data[lhp_data[pitch_type_col] != 'Fastball']
                    lhp_fig = season_hangtime_spraychart_combined(
                        fastball_data, non_fastball_data,
                        batter_name=f"{batter_name} vs 좌투수"
                    )
                    st.session_state.print_charts[f"{batter}_lhp"] = lhp_fig
                
                # 2S 이후 데이터
                if count_value_col is not None:
                    # 우투수 2S
                    if count_value_col == 'strikes':
                        rhp_2s_data = rhp_data[rhp_data[count_value_col] >= 2]
                    else:
                        rhp_2s_data = rhp_data[rhp_data[count_value_col] == 'After_2S']
                    
                    if len(rhp_2s_data) > 0 and pitch_type_col is not None:
                        fastball_data = rhp_2s_data[rhp_2s_data[pitch_type_col] == 'Fastball']
                        non_fastball_data = rhp_2s_data[rhp_2s_data[pitch_type_col] != 'Fastball']
                        rhp_2s_fig = season_hangtime_spraychart_combined(
                            fastball_data, non_fastball_data,
                            batter_name=f"{batter_name} vs 우투수 2S"
                        )
                        st.session_state.print_charts[f"{batter}_rhp_2s"] = rhp_2s_fig
                    
                    # 좌투수 2S
                    if count_value_col == 'strikes':
                        lhp_2s_data = lhp_data[lhp_data[count_value_col] >= 2]
                    else:
                        lhp_2s_data = lhp_data[lhp_data[count_value_col] == 'After_2S']
                    
                    if len(lhp_2s_data) > 0 and pitch_type_col is not None:
                        fastball_data = lhp_2s_data[lhp_2s_data[pitch_type_col] == 'Fastball']
                        non_fastball_data = lhp_2s_data[lhp_2s_data[pitch_type_col] != 'Fastball']
                        lhp_2s_fig = season_hangtime_spraychart_combined(
                            fastball_data, non_fastball_data,
                            batter_name=f"{batter_name} vs 좌투수 2S"
                        )
                        st.session_state.print_charts[f"{batter}_lhp_2s"] = lhp_2s_fig


        # 🎯 KT 투수별 프린트용 차트 생성 및 저장 (hit_distance >= 40)
        if pitcher_team_col is not None and pitcher_name_col is not None:
            # KT 투수별 차트 저장소 초기화
            if 'kt_pitcher_charts' not in st.session_state:
                st.session_state.kt_pitcher_charts = {}
            
            # KT WIZ 데이터 필터링
            kt_team_names = ['KT_WIZ', 'MIN_KTW']
            kt_wiz_data = batter_df[batter_df[pitcher_team_col].isin(kt_team_names)]
            
            # 🔧 2025년 KT WIZ 소속 투수들만 먼저 식별
            kt_wiz_2025_data = kt_wiz_data[kt_wiz_data[year_col] == 2025]
            if len(kt_wiz_2025_data) > 0:
                # 2025년 KT 소속 투수 ID 목록 추출
                kt_2025_pitcher_ids = kt_wiz_2025_data['pitcher'].unique()
                
                # hit_distance 컬럼 확인
                hit_distance_col = None
                possible_distance_cols = ['hit_distance', 'distance', 'hit_dist', 'ball_distance']
                for col in possible_distance_cols:
                    if col in batter_df.columns:
                        hit_distance_col = col
                        break
                
                if hit_distance_col is not None:
                    # 🔧 먼저 2025년 KT 소속 투수 ID만 추출
                    kt_2025_data = batter_df[
                        (batter_df[pitcher_team_col].isin(kt_team_names)) &
                        (batter_df[year_col] == 2025)
                    ]
                    kt_2025_pitcher_ids = kt_2025_data['pitcher'].unique()
                    
                    # 🔧 전체 데이터에서 2025년 KT 소속 투수들의 데이터만 필터링
                    target_years = [2023, 2024, 2025]
                    kt_pitcher_all_data = batter_df[
                        (batter_df['pitcher'].isin(kt_2025_pitcher_ids)) &  # 2025년 KT 소속 투수만
                        (batter_df[year_col].isin(target_years))  # 지정된 연도만
                    ]
                    
                    if len(kt_pitcher_all_data) > 0:
                        # hit_distance >= 40인 데이터만 필터링
                        kt_filtered_data = kt_pitcher_all_data[kt_pitcher_all_data[hit_distance_col] >= 40]
                        
                        if len(kt_filtered_data) > 0:
                            # 투수별로 그룹화하여 충분한 데이터가 있는 투수들만 선택
                            pitcher_counts = kt_filtered_data['pitcher'].value_counts()
                            qualified_pitchers = pitcher_counts[pitcher_counts >= 3].index  # 최소 3개 이상
                            
                            # 상위 8명의 투수만 선택 (프린트 페이지 제한)
                            top_pitchers = qualified_pitchers[:8]
                            
                            for pitcher_id in top_pitchers:
                                pitcher_data = kt_filtered_data[kt_filtered_data['pitcher'] == pitcher_id]
                                
                                if len(pitcher_data) > 0:
                                    # 투수 이름 가져오기
                                    pitcher_name = pitcher_data[pitcher_name_col].iloc[0]
                                    
                                    # 2025년 팀 정보 (1군/2군 구분)
                                    pitcher_2025 = kt_wiz_2025_data[kt_wiz_2025_data['pitcher'] == pitcher_id]
                                    if len(pitcher_2025) > 0:
                                        current_team = pitcher_2025[pitcher_team_col].iloc[0]
                                        team_display = "1군" if current_team == "KT_WIZ" else "2군"
                                    else:
                                        team_display = "기타"  # 이론적으로는 발생하지 않아야 함
                                    
                                    # 연도 정보 추가
                                    available_years = sorted(pitcher_data[year_col].unique())
                                    year_range = f"{max(available_years)}-{min(available_years)}" if len(available_years) > 1 else str(available_years[0])
                                    
                                    # Fastball/Non-Fastball 구분하여 차트 생성
                                    if pitch_type_col is not None:
                                        fastball_data = pitcher_data[pitcher_data[pitch_type_col] == 'Fastball']
                                        non_fastball_data = pitcher_data[pitcher_data[pitch_type_col] != 'Fastball']
                                        
                                        if len(fastball_data) > 0 or len(non_fastball_data) > 0:
                                            # 통합 차트 생성
                                            pitcher_chart = season_hangtime_spraychart_combined(
                                                fastball_data, non_fastball_data,
                                                batter_name=f"{batter_name} vs {pitcher_name}({team_display}, {year_range})"
                                            )
                                            
                                            # 프린트용 차트 저장
                                            chart_key = f"{batter}_pitcher_{pitcher_id}"
                                            st.session_state.kt_pitcher_charts[chart_key] = pitcher_chart







                                
        # Expander 1: 투수유형별/연도별
        if pitcher_hand_col is not None:
            with st.expander(f"투수유형별/연도별: {batter_name}"):
                st.write("투수 유형별 타구 비행시간 (연도별)")
                
                # 우투수/좌투수 탭 생성
                tab_righty, tab_lefty = st.tabs(["우투수", "좌투수"])
                
                # 우투수 탭
                with tab_righty:
                    st.write("### 우투수 상대")
                    righty_cols = st.columns(3)
                    
                    for i in range(min(3, len(display_years))):
                        with righty_cols[i]:
                            current_year = display_years[i]
                            st.write(f"#### {current_year} 시즌")
                            
                            # 해당 연도 및 우투수 데이터 필터링
                            year_data = batter_df[batter_df[year_col] == current_year]  # 🔧 수정
                            righty_data = year_data[year_data[pitcher_hand_col] == 'R']
                            
                            if len(righty_data) > 0 and pitch_type_col is not None:
                                # Fastball과 Non-Fastball 구분
                                fastball_data = righty_data[righty_data[pitch_type_col] == 'Fastball']
                                non_fastball_data = righty_data[righty_data[pitch_type_col] != 'Fastball']
                                
                                # 통합 차트 생성
                                combined_fig = season_hangtime_spraychart_combined(
                                    fastball_data, non_fastball_data,
                                    batter_name=f"{batter_name} vs 우투수 ({current_year})"
                                )
                                st.plotly_chart(combined_fig, key=f"righty_hangtime_{batter}_{current_year}", use_container_width=True)
                            else:
                                st.info(f"{current_year} 시즌 우투수 상대 데이터가 없습니다.")
                    

                    # 남은 컬럼에 빈 내용 표시
                    for i in range(len(display_years), 3):
                        with righty_cols[i]:
                            st.write("#### 시즌 정보 없음")
                            st.info("해당 시즌의 데이터가 없습니다.")
                
                # 좌투수 탭
                with tab_lefty:
                    st.write("### 좌투수 상대")
                    lefty_cols = st.columns(3)
                    
                    for i in range(min(3, len(display_years))):
                        with lefty_cols[i]:
                            current_year = display_years[i]
                            st.write(f"#### {current_year} 시즌")
                            
                            # 해당 연도 및 좌투수 데이터 필터링
                            year_data = batter_df[batter_df[year_col] == current_year]
                            lefty_data = year_data[year_data[pitcher_hand_col] == 'L']
                            
                            if len(lefty_data) > 0 and pitch_type_col is not None:
                                # Fastball과 Non-Fastball 구분
                                fastball_data = lefty_data[lefty_data[pitch_type_col] == 'Fastball']
                                non_fastball_data = lefty_data[lefty_data[pitch_type_col] != 'Fastball']
                                
                                # 통합 차트 생성
                                combined_fig = season_hangtime_spraychart_combined(
                                    fastball_data, non_fastball_data,
                                    batter_name=f"{batter_name} vs 좌투수 ({current_year})"
                                )
                                st.plotly_chart(combined_fig, key=f"lefty_hangtime_{batter}_{current_year}", use_container_width=True)
                            else:
                                st.info(f"{current_year} 시즌 좌투수 상대 데이터가 없습니다.")
                    
                    # 남은 컬럼에 빈 내용 표시
                    for i in range(len(display_years), 3):
                        with lefty_cols[i]:
                            st.write("#### 시즌 정보 없음")
                            st.info("해당 시즌의 데이터가 없습니다.")
        
        # count_value 컬럼 확인
        count_value_col = None
        possible_count_cols = ['count_value', 'count', 'ball_strike', 'count_situation', 'strikes']

        for col in possible_count_cols:
            if col in batter_df.columns:  # 🔧 수정
                count_value_col = col
                break

        # Expander 2: 2S 이후 (투수유형별/연도별)
        if pitcher_hand_col is not None and count_value_col is not None:
            with st.expander(f"2S 이후 (투수유형별/연도별): {batter_name}"):
                st.write("2S 이후 투수 유형별 타구 비행시간 (연도별)")
                
                # 우투수/좌투수 탭 생성
                tab_righty_2s, tab_lefty_2s = st.tabs(["우투수 2S", "좌투수 2S"])
                
                # 우투수 2S 탭
                with tab_righty_2s:
                    st.write("### 우투수 상대 2S 이후")
                    righty_2s_cols = st.columns(3)
                    
                    for i in range(min(3, len(display_years))):
                        with righty_2s_cols[i]:
                            current_year = display_years[i]
                            st.write(f"#### {current_year} 시즌")
                            
                            # 해당 연도, 우투수, 2스트라이크 이후 데이터 필터링
                            year_data = batter_df[batter_df[year_col] == current_year]  # 🔧 수정
                            
                            # strikes 컬럼 사용 시 조건 수정
                            if count_value_col == 'strikes':
                                righty_2s_data = year_data[(year_data[pitcher_hand_col] == 'R') & (year_data[count_value_col] >= 2)]
                            else:
                                righty_2s_data = year_data[(year_data[pitcher_hand_col] == 'R') & (year_data[count_value_col] == 'After_2S')]
                            
                            if len(righty_2s_data) > 0 and pitch_type_col is not None:
                                # Fastball과 Non-Fastball 구분
                                fastball_data = righty_2s_data[righty_2s_data[pitch_type_col] == 'Fastball']
                                non_fastball_data = righty_2s_data[righty_2s_data[pitch_type_col] != 'Fastball']
                                
                                # 통합 차트 생성
                                combined_fig = season_hangtime_spraychart_combined(
                                    fastball_data, non_fastball_data,
                                    batter_name=f"{batter_name} vs 우투수 2S ({current_year})"
                                )
                                st.plotly_chart(combined_fig, key=f"righty_2s_hangtime_{batter}_{current_year}", use_container_width=True)
                            else:
                                st.info(f"{current_year} 시즌 우투수 2S 데이터가 없습니다.")
                    
                    # 남은 컬럼에 빈 내용 표시
                    for i in range(len(display_years), 3):
                        with righty_2s_cols[i]:
                            st.write("#### 시즌 정보 없음")
                            st.info("해당 시즌의 데이터가 없습니다.")
                
                # 좌투수 2S 탭
                with tab_lefty_2s:
                    st.write("### 좌투수 상대 2S 이후")
                    lefty_2s_cols = st.columns(3)
                    
                    for i in range(min(3, len(display_years))):
                        with lefty_2s_cols[i]:
                            current_year = display_years[i]
                            st.write(f"#### {current_year} 시즌")
                            
                            # 해당 연도, 좌투수, 2스트라이크 이후 데이터 필터링
                            year_data = batter_df[batter_df[year_col] == current_year]  # 🔧 수정
                            
                            # strikes 컬럼 사용 시 조건 수정
                            if count_value_col == 'strikes':
                                lefty_2s_data = year_data[(year_data[pitcher_hand_col] == 'L') & (year_data[count_value_col] >= 2)]
                            else:
                                lefty_2s_data = year_data[(year_data[pitcher_hand_col] == 'L') & (year_data[count_value_col] == 'After_2S')]
                            
                            if len(lefty_2s_data) > 0 and pitch_type_col is not None:
                                # Fastball과 Non-Fastball 구분
                                fastball_data = lefty_2s_data[lefty_2s_data[pitch_type_col] == 'Fastball']
                                non_fastball_data = lefty_2s_data[lefty_2s_data[pitch_type_col] != 'Fastball']
                                
                                # 통합 차트 생성
                                combined_fig = season_hangtime_spraychart_combined(
                                    fastball_data, non_fastball_data,
                                    batter_name=f"{batter_name} vs 좌투수 2S ({current_year})"
                                )
                                st.plotly_chart(combined_fig, key=f"lefty_2s_hangtime_{batter}_{current_year}", use_container_width=True)
                            else:
                                st.info(f"{current_year} 시즌 좌투수 2S 데이터가 없습니다.")
                    
                    # 남은 컬럼에 빈 내용 표시
                    for i in range(len(display_years), 3):
                        with lefty_2s_cols[i]:
                            st.write("#### 시즌 정보 없음")
                            st.info("해당 시즌의 데이터가 없습니다.")
        
        # 투수 관련 컬럼 확인
        pitcher_team_col = None
        pitcher_name_col = None

        # 투수 팀 컬럼 찾기
        possible_team_cols = ['pitcherteam', 'pitcher_team', 'p_team', 'team_pitcher']
        for col in possible_team_cols:
            if col in batter_df.columns:  # 🔧 수정
                pitcher_team_col = col
                break

        # 투수 이름 컬럼 찾기
        possible_name_cols = ['NAME_pitcher', 'pitcher_name', 'p_name', 'name_pitcher']
        for col in possible_name_cols:
            if col in batter_df.columns:  # 🔧 수정
                pitcher_name_col = col
                break

        # Expander 3: KT WIZ 투수별 (순수 분석만)
        if pitcher_team_col is not None and pitcher_name_col is not None:
            with st.expander(f"KT WIZ 투수별 타구비행시간: {batter_name}"):
                
            # 🎯 프린트용 KT 투수별 차트 저장소 초기화
                if 'kt_pitcher_charts' not in st.session_state:
                    st.session_state.kt_pitcher_charts = {}
                
                # 🔥 기본 데이터 필터링
                kt_team_names = ['KT_WIZ', 'MIN_KTW']
                kt_wiz_data = batter_df[batter_df[pitcher_team_col].isin(kt_team_names)]
                kt_wiz_2025_data = kt_wiz_data[kt_wiz_data[year_col] == 2025]
                
                if len(kt_wiz_2025_data) == 0:
                    st.info(f"{batter_name}의 2025년 KT 상대 데이터가 없습니다.")
                else:
                    # 🔥 투수 기본 정보 수집
                    kt_pitcher_ids = kt_wiz_2025_data['pitcher'].unique()[:20]
                    all_pitcher_data = batter_df[batter_df['pitcher'].isin(kt_pitcher_ids)]
                    
                    pitcher_info_dict = {}
                    for pitcher_id in kt_pitcher_ids:
                        pitcher_rows = all_pitcher_data[all_pitcher_data['pitcher'] == pitcher_id]
                        if len(pitcher_rows) > 0:
                            pitcher_name = pitcher_rows[pitcher_name_col].iloc[0]
                            
                            # 2025년 팀 정보
                            team_2025 = kt_wiz_2025_data[kt_wiz_2025_data['pitcher'] == pitcher_id]
                            if len(team_2025) > 0:
                                current_team = team_2025[pitcher_team_col].iloc[0]
                                team_display = "1군" if current_team == "KT_WIZ" else "2군"
                            else:
                                team_display = "Unknown"
                            
                            total_pitches = len(pitcher_rows)
                            pitcher_info_dict[pitcher_id] = {
                                'pitcher_name': pitcher_name,
                                'team_display': team_display,
                                'total_pitches': total_pitches
                            }
                    
                    # 🔥 투수별 상세 분석 (프린트 관련 코드 제거)
                    st.subheader("📊 투수별 상세 분석")
                    
                    # 탭으로 투수별 구분
                    if len(pitcher_info_dict) > 0:
                        pitcher_names = [info['pitcher_name'] for info in pitcher_info_dict.values()]
                        pitcher_tabs = st.tabs(pitcher_names[:20])  # 최대 6개 탭
                        
                        for tab_idx, (pitcher_id, pitcher_info) in enumerate(list(pitcher_info_dict.items())[:20]):
                            with pitcher_tabs[tab_idx]:
                                pitcher_name = pitcher_info['pitcher_name']
                                team_display = pitcher_info['team_display']
                                total_pitches = pitcher_info['total_pitches']
                                
                                st.write(f"### {pitcher_name} ({team_display})")
                                st.write(f"**총 대결:** {total_pitches}구")
                                
                                # 🔥 연도별 데이터 확인 및 표시
                                pitcher_data = all_pitcher_data[all_pitcher_data['pitcher'] == pitcher_id]
                                available_years = sorted(pitcher_data[year_col].unique(), reverse=True)
                                target_years = [2025, 2024, 2023]
                                
                                # 🔥 3개 컬럼 생성
                                col1, col2, col3 = st.columns(3)
                                columns = [col1, col2, col3]
                                year_labels = ["2025년", "2024년", "2023년"]
                                
                                for i, (year, col, label) in enumerate(zip(target_years, columns, year_labels)):
                                    with col:
                                        st.write(f"#### {label}")
                                        
                                        if year in available_years:
                                            year_data = pitcher_data[pitcher_data[year_col] == year]
                                            
                                            if len(year_data) > 0 and pitch_type_col is not None:
                                                try:
                                                    fastball_data = year_data[year_data[pitch_type_col] == 'Fastball']
                                                    non_fastball_data = year_data[year_data[pitch_type_col] != 'Fastball']
                                                    
                                                    if len(fastball_data) > 0 or len(non_fastball_data) > 0:
                                                        # 차트 생성
                                                        year_chart = season_hangtime_spraychart_combined(
                                                            fastball_data, non_fastball_data,
                                                            batter_name=f"{batter_name} vs {pitcher_name} ({year})"
                                                        )
                                                        
                                                        st.plotly_chart(
                                                            year_chart, 
                                                            key=f"kt_detail_{batter}_{pitcher_id}_{year}",
                                                            use_container_width=True,
                                                            height=400
                                                        )
                                                        
                                                        st.metric("총 투구", f"{len(year_data)}구")
                                                        st.caption(f"FB: {len(fastball_data)}, NF: {len(non_fastball_data)}")
                                                        
                                                        if year == 2025:
                                                            team_2025 = kt_wiz_2025_data[kt_wiz_2025_data['pitcher'] == pitcher_id]
                                                            if len(team_2025) > 0:
                                                                current_team = team_2025[pitcher_team_col].iloc[0]
                                                                team_status = "1군" if current_team == "KT_WIZ" else "2군"
                                                                st.caption(f"현재 소속: {team_status}")
                                                    else:
                                                        st.info(f"📊 {len(year_data)}구")
                                                        st.caption("차트 생성용 데이터 부족")
                                                
                                                except Exception as e:
                                                    st.error(f"❌ 차트 생성 실패")
                                                    st.caption(f"데이터: {len(year_data)}구")
                                            else:
                                                st.info(f"📊 {len(year_data)}구")
                                                st.caption("구종 정보 없음")
                                        else:
                                            st.info(f"📭 {year}년 데이터 없음")
                    else:
                        st.info("표시할 투수 데이터가 없습니다.")

        
        # 전체 범례 표시
        st.markdown("""
        <div style="text-align: left; font-size: 0.9em; margin-top: 20px;">
        <span style="font-weight: bold;">모양 구분:</span> ● Fastball / ▲ Non-Fastball<br>
        <span style="font-weight: bold;">색상 범례:</span> 붉은색: 2~4초 비행 / 옅은 파란색: 1초 미만 / 옅은 갈색: 4초 이상<br>
        </div>
                    
        """, unsafe_allow_html=True)




def safe_session_init():
    """안전한 세션 상태 초기화"""
    default_session_state = {
        'loggedIn': False,
        'current_page': "main",
        'selected_players': [],
        'print_charts': {},
        'selected_pitchers_for_print': {},
        'analysis_completed': False
    }
    
    for key, default_value in default_session_state.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def show_main_page():
    """메인 페이지 라우터"""
    if not is_user_logged_in():
        show_login_page()
        return

    # 페이지 라우팅
    if st.session_state.current_page == "print":
        show_print_page()
        return  # 프린트 페이지면 여기서 종료
    elif st.session_state.current_page == "main":
        show_analysis_page()
        
        # 🎯 프린트 버튼 (분석 완료 후에만 표시)
        if st.session_state.get('analysis_completed', False):
            st.markdown("---")
            
            col1, col2, col3 = st.columns([2, 2, 2])
            with col2:
                if st.button("📄 프린트 페이지로 이동", use_container_width=True):
                    # 🎯 분석 완료 조건 추가
                    if st.session_state.get('analysis_completed', False) and st.session_state.get('print_charts'):                    
                        st.session_state.current_page = "print"
                        st.rerun()
    else:
        st.error(f"❌ 알 수 없는 페이지: {st.session_state.current_page}")
        st.session_state.current_page = "main"
        st.rerun()


# 메인 실행부 - 세션 안전 버전
with headerSection:
    safe_session_init()  # 안전한 초기화
    
    user_id = get_user_id()
    
    if user_id is None:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        st.session_state['loggedIn'] = True
        show_main_page()

