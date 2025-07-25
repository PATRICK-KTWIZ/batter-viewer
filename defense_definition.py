import os
import pandas as pd
from pandas import DataFrame
from pandas import Series
import numpy as np
# import sidetable
import math
from PIL import Image
from io import BytesIO
import streamlit as st

# from google.colab import data_table
# from vega_datasets import data

import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from collections import defaultdict
import requests

import plotly.offline as pyo
# import plotly.plotly as py


def select_level(option):
    """리그 옵션을 실제 데이터의 level 값으로 변환"""
    if option == "KBO(1군)":
        return "KoreaBaseballOrganization"
    elif option == "KBO(2군)":
        return "KBO Minors"  
    elif option == "-":
        return None
    else:
        return None
    
def filter_player_data(full_data, player_id, player_league=None):
    """전체 데이터에서 특정 선수의 데이터만 필터링하는 함수"""
    if full_data.empty:
        st.warning("전체 데이터가 비어있습니다.")
        return pd.DataFrame()
    
    
    # 선수 ID로 필터링 (batter 컬럼 사용)
    try:
        player_data = full_data[full_data['batter'] == int(player_id)].copy()
    except Exception as e:
        st.error(f"선수 ID 필터링 오류: {str(e)}")
        return pd.DataFrame()
    
    # 선수 데이터가 없는 경우
    if len(player_data) == 0:
        st.warning(f"⚠️ 선수 ID {player_id}에 해당하는 데이터가 없습니다!")
        # 실제 존재하는 batter ID들 일부 표시
        available_batters = full_data['batter'].unique()[:10]
        st.write(f"사용 가능한 batter ID 예시: {available_batters}")
        return pd.DataFrame()
    
    # 리그 필터링 (player_league가 None이 아닐 때만)
    if player_league is not None and 'level' in player_data.columns:
        before_count = len(player_data)
        
        # 실제 level 값들 먼저 확인
        actual_levels = player_data['level'].unique()
        
        # 리그 필터링 적용
        player_data = player_data[player_data['level'] == player_league]
        after_count = len(player_data)
        
        if after_count == 0:
            st.warning(f"⚠️ '{player_league}' 리그에 해당하는 데이터가 없습니다!")
            st.write(f"💡 select_level() 함수의 변환이 올바른지 확인하세요.")
    elif player_league is None:
        st.write("🌐 전체 리그 데이터 사용")
    else:
        st.warning("⚠️ 'level' 컬럼이 데이터에 없습니다!")
        # 실제 컬럼명들 확인
        st.write(f"사용 가능한 컬럼들: {list(player_data.columns)}")
    
    return player_data

# GitHub 설정
OWNER = "Henryjeon1"
REPO = "Trackman"
TOKEN = "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"
TAG_NAME = "KoreaBaseballOrganization"

# 필요한 컬럼만 선택 (메모리 최적화)
required_columns = [
    'game_year', 'game_date', 'hometeam', 'awayteam', 'zone', 'new_zone', 
    'strikes', 'p_throw', 'type', 'events', 'description', 'pitcherteam', 
    'pitname', 'pitcher', 'batter', 'NAME_batter', 'NAME_pitcher', 
    'rel_speed(km)', 'release_spin_rate', 'exit_velocity', 'launch_angleX', 
    'hit_spin_rate', 'hit_distance', 'pitch_name', 'p_kind', 'level', 
    'groundX', 'groundY', 'hang_time'
]

@st.cache_data(ttl=3600, show_spinner=False)
def get_kbo_data():
    """KBO 1군 데이터만 가져오는 함수"""
    try:
        print("🔄 KBO 1군 데이터 다운로드 시작...")
        
        # 릴리스 정보 가져오기
        release_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG_NAME}"
        headers = {"Authorization": f"token {TOKEN}"}
        response = requests.get(release_url, headers=headers, timeout=60)

        if response.status_code != 200:
            print(f"❌ GitHub API 오류: {response.status_code}")
            return None

        release_data = response.json()
        
        # KoreaBaseballOrganization.parquet 파일 찾기
        target_asset = None
        for asset in release_data.get("assets", []):
            if asset["name"] == "KoreaBaseballOrganization.parquet":
                target_asset = asset
                break
        
        if target_asset is None:
            print("❌ KoreaBaseballOrganization.parquet 파일을 찾을 수 없습니다.")
            return None
        
        # 파일 다운로드
        asset_url = target_asset["url"]
        download_headers = {
            "Authorization": f"token {TOKEN}",
            "Accept": "application/octet-stream"
        }

        asset_response = requests.get(asset_url, headers=download_headers, 
                                    allow_redirects=True, timeout=180, stream=True)

        if asset_response.status_code == 200:
            # 메모리 효율적인 방식으로 데이터 로드
            content = BytesIO()
            for chunk in asset_response.iter_content(chunk_size=8192):
                content.write(chunk)
            content.seek(0)
            
            df = pd.read_parquet(content, engine="pyarrow")
            
            # 필요한 컬럼만 선택 (메모리 최적화)
            available_columns = [col for col in required_columns if col in df.columns]
            df = df[available_columns]
            
            # 2023년 이후 데이터만 필터링
            if 'game_year' in df.columns:
                df = df[df['game_year'] >= 2023]
            
            # level 컬럼 설정
            df['level'] = 'KoreaBaseballOrganization'
            
            print(f"✅ KBO 1군 데이터 로드 완료: {len(df):,}개")
            return df
        else:
            print(f"❌ KBO 1군 데이터 다운로드 실패: {asset_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ KBO 1군 데이터 처리 중 오류: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_minors_data():
    """KBO 2군 데이터만 가져오는 함수"""
    try:
        print("🔄 KBO 2군 데이터 다운로드 시작...")
        
        # 릴리스 정보 가져오기
        release_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG_NAME}"
        headers = {"Authorization": f"token {TOKEN}"}
        response = requests.get(release_url, headers=headers, timeout=30)

        if response.status_code != 200:
            print(f"❌ GitHub API 오류: {response.status_code}")
            return None

        release_data = response.json()
        
        # Minor.parquet 파일 찾기
        target_asset = None
        for asset in release_data.get("assets", []):
            if asset["name"] == "Minor.parquet":
                target_asset = asset
                break
        
        if target_asset is None:
            print("❌ Minor.parquet 파일을 찾을 수 없습니다.")
            return None
        
        # 파일 다운로드
        asset_url = target_asset["url"]
        download_headers = {
            "Authorization": f"token {TOKEN}",
            "Accept": "application/octet-stream"
        }

        asset_response = requests.get(asset_url, headers=download_headers, 
                                    allow_redirects=True, timeout=120)

        if asset_response.status_code == 200:
            df = pd.read_parquet(BytesIO(asset_response.content), engine="pyarrow")
            
            # 필요한 컬럼만 선택 (메모리 최적화)
            available_columns = [col for col in required_columns if col in df.columns]
            df = df[available_columns]
            
            # 2023년 이후 데이터만 필터링
            if 'game_year' in df.columns:
                df = df[df['game_year'] >= 2023]
            
            # level 컬럼 설정
            df['level'] = 'KBO Minors'
            
            print(f"✅ KBO 2군 데이터 로드 완료: {len(df):,}개")
            return df
        else:
            print(f"❌ KBO 2군 데이터 다운로드 실패: {asset_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ KBO 2군 데이터 처리 중 오류: {str(e)}")
        return None

def get_data_by_level(selected_levels):
    """선택된 레벨에 따라 적절한 데이터를 가져오는 함수"""
    dfs_to_concat = []
    
    if 'KoreaBaseballOrganization' in selected_levels:
        print("📊 KBO 1군 데이터 로딩...")
        kbo_df = get_kbo_data()
        if kbo_df is not None and len(kbo_df) > 0:
            dfs_to_concat.append(kbo_df)
            print(f"✅ KBO 1군: {len(kbo_df):,}개")
    
    if 'KBO Minors' in selected_levels:
        print("📊 KBO 2군 데이터 로딩...")
        minors_df = get_minors_data()
        if minors_df is not None and len(minors_df) > 0:
            dfs_to_concat.append(minors_df)
            print(f"✅ KBO 2군: {len(minors_df):,}개")
    
    if not dfs_to_concat:
        print("❌ 로드된 데이터가 없습니다.")
        return pd.DataFrame()
    
    # 데이터 결합
    final_df = pd.concat(dfs_to_concat, ignore_index=True)

    # strikes 컬럼을 숫자로 변환 (추가된 부분)
    if 'strikes' in final_df.columns:
        final_df['strikes'] = pd.to_numeric(final_df['strikes'], errors='coerce')
    
    # hangtime_type 컬럼 추가
    if 'hang_time' in final_df.columns:
        def hangtime_category(x):
            if pd.isna(x):
                return 'unknown'
            elif x <= 2:
                return 'short'
            elif x >= 4:
                return 'long'
            else:
                return 'challenge'
        
        final_df['hangtime_type'] = final_df['hang_time'].apply(hangtime_category)
    
    print(f"🎉 최종 데이터: {len(final_df):,}개")
    return final_df





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

def season_hangtime_spraychart(dataframe, batter_name=None):
  
  # 타구 비행시간에 따른 색상 맵 정의
  colors = {
      'short': 'rgba(67,89,119,0.5)',  
      'challenge': 'rgba(255,72,120,0.5)',     
      'long': 'rgba(140,86,75,0.3)'      
  }
  
  symbols = {'4-Seam Fastball':'circle', '2-Seam Fastball':'triangle-down', 'Cutter': 'triangle-se', 'Slider': 'triangle-right', 'Curveball': 'triangle-up', 'Changeup': 'diamond', 'Split-Finger':'square','Sweeper' : 'cross'}

  # hover_data에 포함할 컬럼 확인
  hover_data = []
  for col in ["hang_time", "events", "exit_velocity", "launch_angle", "pitch_name", "rel_speed(km)", "description", "launch_speed_angle", "hit_spin_rate","hit_distance"]:
      if col in dataframe.columns:
          hover_data.append(col)
  
  col_index = len(dataframe['game_year'].unique())
  
  # 산점도 생성
  hangtime_fig = px.scatter(dataframe, x='groundX', y='groundY', color='hangtime_type',
                      color_discrete_map=colors,
                      hover_name="player_name" if "player_name" in dataframe.columns else None, 
                      hover_data=hover_data,
                      height=450, width=550)
  
  # 투구 타입에 따른 심볼 적용
  if "pitch_name" in dataframe.columns:
      for i, d in enumerate(hangtime_fig.data):
          if len(hangtime_fig.data[i].name.split(', ')) > 1:
              pitch_name = hangtime_fig.data[i].name.split(', ')[1]
              if pitch_name in symbols:
                  hangtime_fig.data[i].marker.symbol = symbols[pitch_name]
  
  # 타이틀 설정
  if batter_name:
      hangtime_fig.update_layout(title=f"{batter_name} - 타구 비행시간")
  
  # 레이아웃 설정
  hangtime_fig.update_layout(
        autosize=False,  # 🎯 자동 크기 조정 완전 비활성화
        width=450,       # 🎯 고정 너비
        height=450,      # 🎯 고정 높이
        margin=dict(l=0, r=10, t=30, b=0), 
        xaxis_range=[-10, 130], 
        yaxis_range=[-10, 130],
        plot_bgcolor='rgba(255,255,255,1)', 
        paper_bgcolor='rgba(255,255,255,1)'
    )

  # 모든 subplot에 대한 y축 제목 제거
  hangtime_fig.update_xaxes(title_text='',showticklabels=False)
  hangtime_fig.update_yaxes(title_text='',showticklabels=False)
  
  # 그리드 및 축 설정
  hangtime_fig.update_yaxes(gridcolor='rgba(255,255,255,1)')
  hangtime_fig.update_xaxes(gridcolor='rgba(255,255,255,1)')
  hangtime_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
  hangtime_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
  
  # 마커 크기 설정
  hangtime_fig.update_traces(marker=dict(size=22, opacity=1))
  
  # 범례 숨기기
  hangtime_fig.update_layout(showlegend=False)
  
  # 야구장 요소 추가
  # 홈플레이트
  hangtime_fig.add_shape(type="rect", x0=0, y0=0, x1=28, y1=28, line=dict(color="rgba(108,122,137,0.7)"), line_width=5)
  
  # 외야 경계
  hangtime_fig.add_shape(type="rect", x0=0, y0=0, x1=135, y1=135, line=dict(color="rgba(108,122,137,0.7)"), line_width=5)
  
  # 내야-외야 경계선
  hangtime_fig.add_shape(type="path", path="M 0,100 Q 120,120 100,0", line_color="rgba(108,122,137,0.7)", line_width=5)
  
  return hangtime_fig

def season_hangtime_spraychart_combined(fastball_data, non_fastball_data, batter_name=None):
  """
  Fastball과 Non-Fastball 데이터를 하나의 차트에 다른 모양으로 표시
  """
  import plotly.graph_objects as go
  
  # 타구 비행시간에 따른 색상 맵 정의
  colors = {
      'short': 'rgba(67,89,119,0.5)',  
      'challenge': 'rgba(255,72,120,0.5)',     
      'long': 'rgba(140,86,75,0.3)'      
  }
  
  fig = go.Figure()
  
  # Fastball 데이터 처리 (동그라미)
  if len(fastball_data) > 0:
      fastball_spraychart_df = spraychart_df(fastball_data)
      
      # hangtime_type에 따른 색상 적용
      fastball_colors = []
      for hangtime_type in fastball_spraychart_df['hangtime_type']:
          fastball_colors.append(colors.get(hangtime_type, 'rgba(128,128,128,0.5)'))
      
      # hover_data 준비
      hover_text = []
      for idx, row in fastball_spraychart_df.iterrows():
          hover_info = f"<b>Fastball</b><br>"
          if 'hang_time' in row:
              hover_info += f"Hang Time: {row['hang_time']:.2f}s<br>"
          if 'exit_velocity' in row:
              hover_info += f"Exit Velocity: {row['exit_velocity']}<br>"
          if 'launch_angle' in row:
              hover_info += f"Launch Angle: {row['launch_angle']}°<br>"
          if 'events' in row:
              hover_info += f"Result: {row['events']}<br>"
          hover_text.append(hover_info)
      
      fig.add_trace(go.Scatter(
          x=fastball_spraychart_df['groundX'],
          y=fastball_spraychart_df['groundY'],
          mode='markers',
          marker=dict(
              symbol='circle',
              size=22,
              color=fastball_colors,
              opacity=1,
              line=dict(width=0)  # 경계선 제거
          ),
          name='Fastball',
          text=hover_text,
          hovertemplate='%{text}<extra></extra>'
      ))
  
  # Non-Fastball 데이터 처리 (세모)
  if len(non_fastball_data) > 0:
      non_fastball_spraychart_df = spraychart_df(non_fastball_data)
      
      # hangtime_type에 따른 색상 적용
      non_fastball_colors = []
      for hangtime_type in non_fastball_spraychart_df['hangtime_type']:
          non_fastball_colors.append(colors.get(hangtime_type, 'rgba(128,128,128,0.5)'))
      
      # hover_data 준비
      hover_text = []
      for idx, row in non_fastball_spraychart_df.iterrows():
          hover_info = f"<b>Non-Fastball</b><br>"
          if 'hang_time' in row:
              hover_info += f"Hang Time: {row['hang_time']:.2f}s<br>"
          if 'exit_velocity' in row:
              hover_info += f"Exit Velocity: {row['exit_velocity']}<br>"
          if 'launch_angle' in row:
              hover_info += f"Launch Angle: {row['launch_angle']}°<br>"
          if 'events' in row:
              hover_info += f"Result: {row['events']}<br>"
          if 'pitch_name' in row:
              hover_info += f"Pitch: {row['pitch_name']}<br>"
          hover_text.append(hover_info)
      
      fig.add_trace(go.Scatter(
          x=non_fastball_spraychart_df['groundX'],
          y=non_fastball_spraychart_df['groundY'],
          mode='markers',
          marker=dict(
              symbol='triangle-up',
              size=22,
              color=non_fastball_colors,
              opacity=1,
              line=dict(width=0)  # 경계선 제거
          ),
          name='Non-Fastball',
          text=hover_text,
          hovertemplate='%{text}<extra></extra>'
      ))
  
  # 타이틀 설정
  if batter_name:
      fig.update_layout(title=f"{batter_name} - 타구 비행시간")
  
  # 레이아웃 설정 (기존 함수와 동일)
  fig.update_layout(
      autosize=False, 
      margin=dict(l=0, r=10, t=30, b=0), 
      xaxis_range=[-10, 130], 
      yaxis_range=[-10, 130],
      plot_bgcolor='rgba(255,255,255,1)', 
      paper_bgcolor='rgba(255,255,255,1)',
      height=450, 
      width=600
  )

  # 모든 subplot에 대한 y축 제목 제거
  fig.update_xaxes(title_text='', showticklabels=False)
  fig.update_yaxes(title_text='', showticklabels=False)
  
  # 그리드 및 축 설정
  fig.update_yaxes(gridcolor='rgba(255,255,255,1)')
  fig.update_xaxes(gridcolor='rgba(255,255,255,1)')
  fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
  fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
  
  # 범례 숨기기
  fig.update_layout(showlegend=False)

 
  # 야구장 요소 추가
  # 내야 각루 (홈플레이트를 중심으로 한 다이아몬드)
  fig.add_shape(type="rect", x0=0, y0=0, x1=28, y1=28, line=dict(color="rgba(108,122,137,0.7)"), line_width=5)

 
  # 외야 경계
  fig.add_shape(type="rect", x0=0, y0=0, x1=135, y1=135, line=dict(color="rgba(108,122,137,0.7)"), line_width=5)

  # 연장선
  fig.add_shape(type="line", x0=120, y0=120, x1=0, y1=0, line=dict(color="rgba(108,122,137,0.7)", width=3, dash="dash"))
  fig.add_shape(type="line", x0=130, y0=28, x1=28, y1=28, line=dict(color="rgba(108,122,137,0.7)", width=3, dash="dash"))
  fig.add_shape(type="line", x0=28, y0=130, x1=28, y1=28, line=dict(color="rgba(108,122,137,0.7)", width=3, dash="dash"))
  
  
  # 외야 경계선 (호 모양)
  fig.add_shape(type="path", path="M 0,100 Q 120,120 100,0", line_color="rgba(108,122,137,0.7)", line_width=5)

  # 수비위치 경계선 (내야와 외야 사이)
  fig.add_shape(type="path", path="M 0,75 Q 90,90 75,0", line=dict(color="rgba(108,122,137,0.5)", width=3, dash="dash"))

      # 수비위치 경계선에 "75" 텍스트 추가
  fig.add_annotation(
      x=0, y=75,  # 좌측 y축 기준선
      text="75",
      showarrow=False,
      font=dict(size=12, color="rgba(108,122,137,0.8)"),
      xanchor="right",
      yanchor="middle",
      xshift=-5  # 축에서 약간 왼쪽으로 이동
  )
  
  fig.add_annotation(
      x=75, y=0,  # 하단 x축 기준선
      text="75",
      showarrow=False,
      font=dict(size=12, color="rgba(108,122,137,0.8)"),
      xanchor="center",
      yanchor="top",
      yshift=-5  # 축에서 약간 아래로 이동
  )
  
  return fig

def generate_hangtime_print_page(batter_dataframes, selected_player_df):
    """타구비행시간 프린트용 HTML 페이지 생성 - 이미지 기반"""
    
    # 차트 이미지가 없으면 경고
    if 'chart_images' not in st.session_state:
        return "<html><body><h1>차트 이미지가 없습니다. 먼저 분석을 실행해주세요.</h1></body></html>"
    
    chart_images = st.session_state.chart_images
    
    # 🆕 프린트용 투수 선택 정보 가져오기
    print_selected_pitchers = st.session_state.get('print_selected_pitchers', {})
    
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <style>
            @media print {
                body { margin: 0; }
                .page-break { page-break-before: always; }
                .no-print { display: none; }
            }
            
            body { font-family: 'Malgun Gothic', sans-serif; margin: 0; padding: 10px; font-size: 12px; }
            .page { width: 210mm; min-height: 297mm; margin: 0 auto; padding: 15mm; box-sizing: border-box; background: white; margin-bottom: 20px; }
            .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
            .player-name { font-size: 24px; font-weight: bold; margin: 5px 0; }
            .section-title { font-size: 18px; font-weight: bold; background: #f0f0f0; padding: 10px; margin-bottom: 15px; border-left: 4px solid #007acc; }
            .chart-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 20px; }
            .chart-container { border: 1px solid #ddd; padding: 15px; text-align: center; min-height: 320px; }
            .chart-image { max-width: 100%; height: auto; }
            .legend { background: #f8f9fa; border: 1px solid #dee2e6; padding: 12px; margin-top: 20px; font-size: 12px; }
            .kt-pitcher-section { margin-top: 30px; }
            .kt-pitcher-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
            .kt-pitcher-container { border: 1px solid #ddd; padding: 10px; text-align: center; min-height: 250px; }
        </style>
    </head>
    <body>
    """
    
    # 각 선수별로 페이지 생성
    for i, (batter, batter_df) in enumerate(batter_dataframes.items()):
        batter_str = str(batter)
        batter_finder = selected_player_df[selected_player_df['TM_ID'] == batter_str]
        batter_name = batter_finder.iloc[0]['NAME'] if len(batter_finder) > 0 else f"선수_{batter}"
        
        page_break = "page-break" if i > 0 else ""
        
        # 이미지 가져오기 함수
        def get_chart_image(chart_key):
            if chart_key in chart_images:
                return f'<img src="data:image/png;base64,{chart_images[chart_key]}" class="chart-image" alt="차트">'
            else:
                return '<div style="text-align: center; padding: 50px; color: #666;">차트 이미지 없음</div>'
        
        html_content += f"""
        <div class="page {page_break}">
            <div class="header">
                <div class="player-name">{batter_name} 타구비행시간 분석</div>
                <div>Baseball Intelligence Transformation Report</div>
                <div>생성일: 2025년 7월 22일 | 분석기간: 2023-2025시즌</div>
            </div>
            
            <div class="section-title">투수유형별</div>
            <div class="chart-grid-2">
                <div class="chart-container">
                    <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px;">vs 우투수</div>
                    {get_chart_image(f"{batter}_rhp")}
                </div>
                <div class="chart-container">
                    <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px;">vs 좌투수</div>
                    {get_chart_image(f"{batter}_lhp")}
                </div>
            </div>
            
            <div class="section-title">투수유형별 2S 이후</div>
            <div class="chart-grid-2">
                <div class="chart-container">
                    <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px;">vs 우투수 2S</div>
                    {get_chart_image(f"{batter}_rhp_2s")}
                </div>
                <div class="chart-container">
                    <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px;">vs 좌투수 2S</div>
                    {get_chart_image(f"{batter}_lhp_2s")}
                </div>
            </div>
        """
        
        # 🆕 KT 투수별 차트 추가 (프린트용으로 선택된 투수만)
        player_id = batter_str
        if player_id in print_selected_pitchers and print_selected_pitchers[player_id]:
            selected_pitcher_ids = print_selected_pitchers[player_id]
            
            html_content += """
            <div class="kt-pitcher-section">
                <div class="section-title">KT 투수별 분석</div>
                <div class="kt-pitcher-grid">
            """
            
            for pitcher_id in selected_pitcher_ids:
                # 투수 이름 가져오기
                pitcher_data = batter_df[batter_df['pitcher'] == pitcher_id]
                if not pitcher_data.empty:
                    pitcher_name = pitcher_data.iloc[0]['NAME_pitcher']
                    
                    html_content += f"""
                    <div class="kt-pitcher-container">
                        <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px;">vs {pitcher_name}</div>
                        {get_chart_image(f"{batter}_pitcher_{pitcher_id}")}
                    </div>
                    """
            
            html_content += """
                </div>
            </div>
            """
        
        html_content += """
            <div class="legend">
                <div style="font-weight: bold;">범례:</div>
                <div>● Fastball / ▲ Non-Fastball</div>
                <div>붉은색: 2~4초 비행 / 옅은 파란색: 2초 미만 / 옅은 갈색: 4초 이상</div>
            </div>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    return html_content
