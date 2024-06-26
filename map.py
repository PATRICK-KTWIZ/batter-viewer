import pandas as pd
import streamlit as st
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go

def factor_year_count_map(dataframe, y_factor):

    col_index = len(dataframe['game_year'].unique())

    factor_year_count_map_fig = px.density_contour(dataframe, x='plate_x', y='plate_z', z=y_factor, histfunc="count", facet_col='game_year',
                        height = 460, width = col_index*400)

    factor_year_count_map_fig.update_yaxes(domain=[0.1, 0.97])

    factor_year_count_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    
    factor_year_count_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[0.27,1.25], bargap = 0,
                                    xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False}, showlegend = False)

    factor_year_count_map_fig.update_layout({'plot_bgcolor': 'rgba(13,8,135,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

    factor_year_count_map_fig.update_yaxes(gridcolor='rgba(13,8,135,1)')
    factor_year_count_map_fig.update_xaxes(gridcolor='rgba(13,8,135,1)')

    factor_year_count_map_fig.update_traces(contours_coloring="fill", contours_showlabels = True, colorscale="Viridis")

    homex = [-0.23, 0.23, 0.23, -0.23, -0.23]
    homey = [0.45, 0.45, 1.05, 1.05, 0.45]

    factor_year_count_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='white', width=4) ), row = 'all' , col = 'all')
    factor_year_count_map_fig.add_trace(go.Scatter(x=[0], y=[0.42], text=["<b>Strike Zone<b>"], mode="text", textfont_size=18, textfont_color='white',), row = 'all' , col = 'all')

    homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
    homey = [0.59, 0.59, 0.91, 0.91, 0.59]

    factor_year_count_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='red', width=3) ), row = 'all' , col = 'all')
    factor_year_count_map_fig.add_trace(go.Scatter(x=[0], y=[0.56], text=["<b>Core Zone<b>"], mode="text", textfont_size=20, textfont_color='red',), row = 'all' , col = 'all')

    factor_year_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.915, x1=-0.125, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_count_map_fig.add_shape(type="rect", x0=-0.115, y0=0.915, x1=0.115, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.915, x1=0.34, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    factor_year_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.595, x1=-0.125, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.595, x1=0.34, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    factor_year_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.35, x1=-0.125, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_count_map_fig.add_shape(type="rect", x0=-0.115, y0=0.35, x1=0.115, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.35, x1=0.34, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    return factor_year_count_map_fig

def factor_period_coount_map(dataframe, y_factor):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    dataframe = dataframe[(dataframe['game_date'] >= date1) & (dataframe['game_date'] <= date2)]

    col_index = len(dataframe['p_kind'].unique())

    if len(dataframe) > 0:

        factor_period_coount_map_fig = px.density_contour(dataframe, x='plate_x', y='plate_z', z=y_factor, histfunc="count", facet_col='p_kind',
                                                          category_orders={"p_kind": ["Fastball", "Breaking", 'Off_Speed']},
                                                        height = 445, width = col_index * 400)
        
        factor_period_coount_map_fig.update_yaxes(domain=[0.1, 0.97])

        factor_period_coount_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        
        factor_period_coount_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[0.27,1.25], bargap = 0,
                                        xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False}, showlegend = False)

        factor_period_coount_map_fig.update_layout({'plot_bgcolor': 'rgba(13,8,135,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

        factor_period_coount_map_fig.update_yaxes(gridcolor='rgba(13,8,135,1)')
        factor_period_coount_map_fig.update_xaxes(gridcolor='rgba(13,8,135,1)')

        factor_period_coount_map_fig.update_traces(contours_coloring="fill", contours_showlabels = True, colorscale="Viridis")

        homex = [-0.23, 0.23, 0.23, -0.23, -0.23]
        homey = [0.45, 0.45, 1.05, 1.05, 0.45]

        factor_period_coount_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='white', width=4) ), row = 'all' , col = 'all')
        factor_period_coount_map_fig.add_trace(go.Scatter(x=[0], y=[0.42], text=["<b>Strike Zone<b>"], mode="text", textfont_size=18, textfont_color='white',), row = 'all' , col = 'all')

        homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
        homey = [0.59, 0.59, 0.91, 0.91, 0.59]

        factor_period_coount_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='red', width=3) ), row = 'all' , col = 'all')
        factor_period_coount_map_fig.add_trace(go.Scatter(x=[0], y=[0.56], text=["<b>Core Zone<b>"], mode="text", textfont_size=20, textfont_color='red',), row = 'all' , col = 'all')

        factor_period_coount_map_fig.add_shape(type="rect", x0=-0.34, y0=0.915, x1=-0.125, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_coount_map_fig.add_shape(type="rect", x0=-0.115, y0=0.915, x1=0.115, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_coount_map_fig.add_shape(type="rect", x0=0.125, y0=0.915, x1=0.34, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        factor_period_coount_map_fig.add_shape(type="rect", x0=-0.34, y0=0.595, x1=-0.125, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_coount_map_fig.add_shape(type="rect", x0=0.125, y0=0.595, x1=0.34, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        factor_period_coount_map_fig.add_shape(type="rect", x0=-0.34, y0=0.35, x1=-0.125, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_coount_map_fig.add_shape(type="rect", x0=-0.115, y0=0.35, x1=0.115, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_coount_map_fig.add_shape(type="rect", x0=0.125, y0=0.35, x1=0.34, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        return factor_period_coount_map_fig
    
    else:
        factor_period_coount_map_fig = go.Figure()
        factor_period_coount_map_fig.add_shape(type="rect", x0=0, y0=0, x1=1, y1=1, line=dict(color="gray", width=1), fillcolor="white", opacity=0.3)
        factor_period_coount_map_fig.update_layout(width=450, height=100, title="데이터가 존재하지 않습니다.")
        factor_period_coount_map_fig.update_xaxes(visible=False, range=[0, 1])
        factor_period_coount_map_fig.update_yaxes(visible=False, range=[0, 1])

        return factor_period_coount_map_fig

def swingmap_count_map(dataframe, y_factor):

    col_index = len(dataframe['swingmap'].unique())

    swingmap_count_map_fig = px.density_contour(dataframe, x='plate_x', y='plate_z', z=y_factor, histfunc="count", facet_col='swingmap',
                                                category_orders={"swingmap": ["Called_Strike", "Ball", 'Foul','Whiff','HIT','Out']},
                                                height = 365, width = col_index*300)
    swingmap_count_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    swingmap_count_map_fig.update_yaxes(domain=[0.1, 0.97])
    
    swingmap_count_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[0.27,1.25], bargap = 0,
                                    xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False}, showlegend = False)

    swingmap_count_map_fig.update_layout({'plot_bgcolor': 'rgba(13,8,135,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

    swingmap_count_map_fig.update_yaxes(gridcolor='rgba(13,8,135,1)')
    swingmap_count_map_fig.update_xaxes(gridcolor='rgba(13,8,135,1)')

    swingmap_count_map_fig.update_traces(contours_coloring="fill", contours_showlabels = False, colorscale="Viridis")

    homex = [-0.23, 0.23, 0.23, -0.23, -0.23]
    homey = [0.45, 0.45, 1.05, 1.05, 0.45]

    swingmap_count_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='white', width=4) ), row = 'all' , col = 'all')
    swingmap_count_map_fig.add_trace(go.Scatter(x=[0], y=[0.42], text=["<b>Strike Zone<b>"], mode="text", textfont_size=18, textfont_color='white',), row = 'all' , col = 'all')

    homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
    homey = [0.59, 0.59, 0.91, 0.91, 0.59]

    swingmap_count_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='red', width=3) ), row = 'all' , col = 'all')
    swingmap_count_map_fig.add_trace(go.Scatter(x=[0], y=[0.56], text=["<b>Core Zone<b>"], mode="text", textfont_size=20, textfont_color='red',), row = 'all' , col = 'all')

    swingmap_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.915, x1=-0.125, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    swingmap_count_map_fig.add_shape(type="rect", x0=-0.115, y0=0.915, x1=0.115, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    swingmap_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.915, x1=0.34, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    swingmap_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.595, x1=-0.125, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    swingmap_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.595, x1=0.34, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    swingmap_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.35, x1=-0.125, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    swingmap_count_map_fig.add_shape(type="rect", x0=-0.115, y0=0.35, x1=0.115, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    swingmap_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.35, x1=0.34, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    return swingmap_count_map_fig

def swingmap_period_count_map(dataframe, y_factor):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    col_index = len(dataframe['swingmap'].unique())

    dataframe = dataframe[(dataframe['game_date'] >= date1) & (dataframe['game_date'] <= date2)]

    if len(dataframe) > 0:

        swingmap_period_count_map_fig = px.density_contour(dataframe, x='plate_x', y='plate_z', z=y_factor, histfunc="count", facet_col='swingmap',
                                                            category_orders={"swingmap": ["Called_Strike", "Ball", 'Foul','Whiff','HIT','Out']},
                                                            height = 365, width = col_index*300)
        swingmap_period_count_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        swingmap_period_count_map_fig.update_yaxes(domain=[0.1, 0.97])
        
        swingmap_period_count_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[0.27,1.25], bargap = 0,
                                        xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False}, showlegend = False)

        swingmap_period_count_map_fig.update_layout({'plot_bgcolor': 'rgba(13,8,135,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

        swingmap_period_count_map_fig.update_yaxes(gridcolor='rgba(13,8,135,1)')
        swingmap_period_count_map_fig.update_xaxes(gridcolor='rgba(13,8,135,1)')

        swingmap_period_count_map_fig.update_traces(contours_coloring="fill", contours_showlabels = False, colorscale="Viridis")

        homex = [-0.23, 0.23, 0.23, -0.23, -0.23]
        homey = [0.45, 0.45, 1.05, 1.05, 0.45]

        swingmap_period_count_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='white', width=4) ), row = 'all' , col = 'all')
        swingmap_period_count_map_fig.add_trace(go.Scatter(x=[0], y=[0.42], text=["<b>Strike Zone<b>"], mode="text", textfont_size=18, textfont_color='white',), row = 'all' , col = 'all')

        homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
        homey = [0.59, 0.59, 0.91, 0.91, 0.59]

        swingmap_period_count_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='red', width=3) ), row = 'all' , col = 'all')
        swingmap_period_count_map_fig.add_trace(go.Scatter(x=[0], y=[0.56], text=["<b>Core Zone<b>"], mode="text", textfont_size=20, textfont_color='red',), row = 'all' , col = 'all')

        swingmap_period_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.915, x1=-0.125, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        swingmap_period_count_map_fig.add_shape(type="rect", x0=-0.115, y0=0.915, x1=0.115, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        swingmap_period_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.915, x1=0.34, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        swingmap_period_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.595, x1=-0.125, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        swingmap_period_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.595, x1=0.34, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        swingmap_period_count_map_fig.add_shape(type="rect", x0=-0.34, y0=0.35, x1=-0.125, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        swingmap_period_count_map_fig.add_shape(type="rect", x0=-0.115, y0=0.35, x1=0.115, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        swingmap_period_count_map_fig.add_shape(type="rect", x0=0.125, y0=0.35, x1=0.34, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        return swingmap_period_count_map_fig
    else:
        swingmap_period_count_map_fig = go.Figure()
        swingmap_period_count_map_fig.add_shape(type="rect", x0=0, y0=0, x1=1, y1=1, line=dict(color="gray", width=1), fillcolor="white", opacity=0.3)
        swingmap_period_count_map_fig.update_layout(width=450, height=100, title="데이터가 존재하지 않습니다.")
        swingmap_period_count_map_fig.update_xaxes(visible=False, range=[0, 1])
        swingmap_period_count_map_fig.update_yaxes(visible=False, range=[0, 1])

        return swingmap_period_count_map_fig

def swingmap_period_symbol_map(dataframe):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    col_index = len(dataframe['swingmap'].unique())

    dataframe = dataframe[(dataframe['game_date'] >= date1) & (dataframe['game_date'] <= date2)]

    if len(dataframe) > 0:

        colors = {'called_strike':'rgba(24,85,144,0.6)', 'whiff':'rgba(244,247,143,0.9)', 'ball': 'rgba(108,122,137,0.7)', 'foul': 'rgba(241,106,227,0.5)', 'hit': 'rgba(255,105,97,1)', 'out': 'rgba(140,86,75,0.6)'}
        symbols = {'4-Seam Fastball':'circle', '2-Seam Fastball':'triangle-down', 'Cutter': 'triangle-se', 'Slider': 'triangle-right', 'Curveball': 'triangle-up', 'Sweeper':'cross', 'Changeup': 'diamond', 'Split-Finger':'square'}

        swingmap_period_symbol_map_fig = px.scatter(dataframe, x='plate_x', y='plate_z', color='swingmap', symbol='pitch_name', facet_col = 'swingmap',
                                                    color_discrete_map=colors,
                                                    hover_name="player_name", hover_data=["rel_speed(km)","pitch_name","events","exit_velocity","description","launch_speed_angle","launch_angle"],
                                                    template="simple_white",
                                                    category_orders={"swingmap": ["Called_Strike", "Ball", 'Foul','Whiff','HIT','Out']},
                                                    height = 385, width = col_index*290)

        swingmap_period_symbol_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        swingmap_period_symbol_map_fig.update_yaxes(domain=[0.1, 0.97])
        
        swingmap_period_symbol_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[0.27,1.25], bargap = 0,
                                        xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False}, showlegend = False)

        for i, d in enumerate(swingmap_period_symbol_map_fig.data):
            swingmap_period_symbol_map_fig.data[i].marker.symbol = symbols[swingmap_period_symbol_map_fig.data[i].name.split(', ')[1]]

        swingmap_period_symbol_map_fig.update_layout(showlegend=False)

        swingmap_period_symbol_map_fig.update_layout({'plot_bgcolor': 'rgba(255,255,255,0.1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

        swingmap_period_symbol_map_fig.update_traces(marker=dict(size=25))
        swingmap_period_symbol_map_fig.update_traces(textfont_size=24)

        swingmap_period_symbol_map_fig.add_hline(y=0.59, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
        swingmap_period_symbol_map_fig.add_hline(y=0.91, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')

        swingmap_period_symbol_map_fig.add_vline(x=-0.12, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')
        swingmap_period_symbol_map_fig.add_vline(x=0.12, line_width=2, line_dash='dash', line_color='rgba(30,30,30,0.8)')


        homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
        homey = [0.59, 0.59, 0.91, 0.91, 0.59]

        swingmap_period_symbol_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='red', width=4) ), row = 'all' , col = 'all')
        swingmap_period_symbol_map_fig.add_trace(go.Scatter(x=[0], y=[0.57], text=["<b>Core Zone<b>"], mode="text", textfont_size=20, textfont_color='red',), row = 'all' , col = 'all')

        homex = [-0.26, 0.26, 0.26, -0.26, -0.26]
        homey = [0.45, 0.45, 1.05, 1.05, 0.45]

        # period_swingmap_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='rgba(108,122,137,0.8)', width=4) ), row = 1 , col = 1)
        swingmap_period_symbol_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='rgba(108,122,137,0.9)', width=4) ), row = 'all' , col = 'all')
        swingmap_period_symbol_map_fig.add_trace(go.Scatter(x=[0], y=[0.43], text=["<b>Strike Zone<b>"], mode="text", textfont_size=20, textfont_color='rgba(108,122,137,0.9)',), row = 'all' , col = 'all')

        swingmap_period_symbol_map_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
        swingmap_period_symbol_map_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)

        return swingmap_period_symbol_map_fig
    
    else:
        swingmap_period_symbol_map_fig = go.Figure()
        swingmap_period_symbol_map_fig.add_shape(type="rect", x0=0, y0=0, x1=1, y1=1, line=dict(color="gray", width=1), fillcolor="white", opacity=0.3)
        swingmap_period_symbol_map_fig.update_layout(width=450, height=100, title="데이터가 존재하지 않습니다.")
        swingmap_period_symbol_map_fig.update_xaxes(visible=False, range=[0, 1])
        swingmap_period_symbol_map_fig.update_yaxes(visible=False, range=[0, 1])

        return swingmap_period_symbol_map_fig


def factor_year_sum_map(dataframe, y_factor):

    year = dataframe['game_year'] >= 2021
    dataframe = dataframe[year]

    col_index = len(dataframe['game_year'].unique())

    factor_year_sum_map_fig = px.density_contour(dataframe, x='plate_x', y='plate_z', z=y_factor, histfunc="sum", facet_col='game_year',
                         height = 460, width = col_index*400)
    factor_year_sum_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    factor_year_sum_map_fig.update_yaxes(domain=[0.1, 0.97])
    
    factor_year_sum_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[0.27,1.25], bargap = 0,
                                       xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False}, showlegend = False)

    factor_year_sum_map_fig.update_layout({'plot_bgcolor': 'rgba(13,8,135,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

    factor_year_sum_map_fig.update_yaxes(gridcolor='rgba(13,8,135,1)')
    factor_year_sum_map_fig.update_xaxes(gridcolor='rgba(13,8,135,1)')

    factor_year_sum_map_fig.update_traces(contours_coloring="fill", contours_showlabels = True, colorscale="Viridis")

    homex = [-0.23, 0.23, 0.23, -0.23, -0.23]
    homey = [0.45, 0.45, 1.05, 1.05, 0.45]

    factor_year_sum_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='white', width=4) ), row = 'all' , col = 'all')
    factor_year_sum_map_fig.add_trace(go.Scatter(x=[0], y=[0.42], text=["<b>Strike Zone<b>"], mode="text", textfont_size=18, textfont_color='white',), row = 'all' , col = 'all')

    homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
    homey = [0.59, 0.59, 0.91, 0.91, 0.59]

    factor_year_sum_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='red', width=3) ), row = 'all' , col = 'all')
    factor_year_sum_map_fig.add_trace(go.Scatter(x=[0], y=[0.56], text=["<b>Core Zone<b>"], mode="text", textfont_size=20, textfont_color='red',), row = 'all' , col = 'all')

    factor_year_sum_map_fig.add_shape(type="rect", x0=-0.34, y0=0.915, x1=-0.125, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_sum_map_fig.add_shape(type="rect", x0=-0.115, y0=0.915, x1=0.115, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_sum_map_fig.add_shape(type="rect", x0=0.125, y0=0.915, x1=0.34, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    factor_year_sum_map_fig.add_shape(type="rect", x0=-0.34, y0=0.595, x1=-0.125, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_sum_map_fig.add_shape(type="rect", x0=0.125, y0=0.595, x1=0.34, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    factor_year_sum_map_fig.add_shape(type="rect", x0=-0.34, y0=0.35, x1=-0.125, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_sum_map_fig.add_shape(type="rect", x0=-0.115, y0=0.35, x1=0.115, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
    factor_year_sum_map_fig.add_shape(type="rect", x0=0.125, y0=0.35, x1=0.34, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

    return factor_year_sum_map_fig

def factor_period_sum_map(dataframe, y_factor):
    
    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    dataframe = dataframe[(dataframe['game_date'] >= date1) & (dataframe['game_date'] <= date2)]

    col_index = len(dataframe['p_kind'].unique())

    if len(dataframe) > 0 :

        factor_period_sum_map_fig = px.density_contour(dataframe, x='plate_x', y='plate_z', z=y_factor, facet_col='p_kind', 
                                                       category_orders={"p_kind": ["Fastball", "Breaking", 'Off_Speed']},
                                                       histfunc="sum", height = 445, width = col_index * 400)
        factor_period_sum_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        factor_period_sum_map_fig.update_yaxes(domain=[0.1, 0.97])
        
        factor_period_sum_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[0.27,1.25], bargap = 0,
                                        xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False}, showlegend = False)

        factor_period_sum_map_fig.update_layout({'plot_bgcolor': 'rgba(13,8,135,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

        factor_period_sum_map_fig.update_yaxes(gridcolor='rgba(13,8,135,1)')
        factor_period_sum_map_fig.update_xaxes(gridcolor='rgba(13,8,135,1)')

        factor_period_sum_map_fig.update_traces(contours_coloring="fill", contours_showlabels = False, colorscale="Viridis")

        homex = [-0.23, 0.23, 0.23, -0.23, -0.23]
        homey = [0.45, 0.45, 1.05, 1.05, 0.45]

        factor_period_sum_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='white', width=4) ), row = 'all' , col = 'all')
        factor_period_sum_map_fig.add_trace(go.Scatter(x=[0], y=[0.42], text=["<b>Strike Zone<b>"], mode="text", textfont_size=18, textfont_color='white',), row = 'all' , col = 'all')

        homex = [-0.12, 0.12, 0.12, -0.12, -0.12]
        homey = [0.59, 0.59, 0.91, 0.91, 0.59]

        factor_period_sum_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='red', width=3) ), row = 'all' , col = 'all')
        factor_period_sum_map_fig.add_trace(go.Scatter(x=[0], y=[0.56], text=["<b>Core Zone<b>"], mode="text", textfont_size=20, textfont_color='red',), row = 'all' , col = 'all')

        factor_period_sum_map_fig.add_shape(type="rect", x0=-0.34, y0=0.915, x1=-0.125, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_sum_map_fig.add_shape(type="rect", x0=-0.115, y0=0.915, x1=0.115, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_sum_map_fig.add_shape(type="rect", x0=0.125, y0=0.915, x1=0.34, y1=1.15, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        factor_period_sum_map_fig.add_shape(type="rect", x0=-0.34, y0=0.595, x1=-0.125, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_sum_map_fig.add_shape(type="rect", x0=0.125, y0=0.595, x1=0.34, y1=0.905, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        factor_period_sum_map_fig.add_shape(type="rect", x0=-0.34, y0=0.35, x1=-0.125, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_sum_map_fig.add_shape(type="rect", x0=-0.115, y0=0.35, x1=0.115, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')
        factor_period_sum_map_fig.add_shape(type="rect", x0=0.125, y0=0.35, x1=0.34, y1=0.585, line=dict(color="white", width=1, dash='dash'), row = 'all' , col = 'all')

        return factor_period_sum_map_fig
    
    else:
        factor_period_sum_map_fig = go.Figure()
        factor_period_sum_map_fig.add_shape(type="rect", x0=0, y0=0, x1=1, y1=1, line=dict(color="gray", width=1), fillcolor="white", opacity=0.3)
        factor_period_sum_map_fig.update_layout(width=450, height=100, title="데이터가 존재하지 않습니다.")
        factor_period_sum_map_fig.update_xaxes(visible=False, range=[0, 1])
        factor_period_sum_map_fig.update_yaxes(visible=False, range=[0, 1])

        return factor_period_sum_map_fig


def factor_year_sum_plate_map(dataframe, y_factor):

    year = dataframe['game_year'] >= 2021
    dataframe = dataframe[year]

    col_index = len(dataframe['game_year'].unique())

    factor_year_sum_plate_map_fig = px.density_contour(dataframe, x='contactZ', y='contactX', z=y_factor, histfunc="sum", facet_col='game_year',
                         height = 460, width = col_index*400)
    factor_year_sum_plate_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    factor_year_sum_plate_map_fig.update_yaxes(domain=[0.1, 0.97])

    factor_year_sum_plate_map_fig.update_layout({'plot_bgcolor': 'rgba(13,8,135,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

    factor_year_sum_plate_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[-0.1,1.05],
                                                bargap = 0, xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False})

    factor_year_sum_plate_map_fig.update_traces(contours_coloring="fill", contours_showlabels = True, colorscale="Viridis")


    homex = [-0.26, 0, 0.26, 0.26, -0.26, -0.26]
    homey = [0.215, 0, 0.215, 0.43, 0.43, 0.215]

    factor_year_sum_plate_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='white', width=4) ), row = 'all' , col = 'all')

    factor_year_sum_plate_map_fig.add_hline(y=1, line_dash='dash' ,line_width=1, line_color='white')
    factor_year_sum_plate_map_fig.add_hline(y=0.43,  line_dash='dash' ,line_width=1, line_color='white')
    factor_year_sum_plate_map_fig.add_hline(y=0,  line_dash='dash' ,line_width=1, line_color='white')
    factor_year_sum_plate_map_fig.add_vline(x=-0.37,line_width=1, line_color='white')
    factor_year_sum_plate_map_fig.add_vline(x=0.37, line_width=1, line_color='white')
    factor_year_sum_plate_map_fig.add_vline(x=-0.26, line_dash='dash' ,line_width=1, line_color='white')
    factor_year_sum_plate_map_fig.add_vline(x=0.26, line_dash='dash', line_width=1, line_color='white')

    factor_year_sum_plate_map_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
    factor_year_sum_plate_map_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)


    return factor_year_sum_plate_map_fig

def factor_period_sum_plate_map(dataframe, y_factor):
    
    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    dataframe = dataframe[(dataframe['game_date'] >= date1) & (dataframe['game_date'] <= date2)]

    if len(dataframe) > 0:

        factor_period_sum_plate_map_fig = px.density_contour(dataframe, x='contactZ', y='contactX', z=y_factor, histfunc="sum", facet_col='game_year',
                            height = 460, width = 450)
        factor_period_sum_plate_map_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        factor_period_sum_plate_map_fig.update_yaxes(domain=[0.1, 0.97])

        factor_period_sum_plate_map_fig.update_layout({'plot_bgcolor': 'rgba(13,8,135,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

        factor_period_sum_plate_map_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-0.45,0.45], yaxis_range=[-0.1,1.05], bargap = 0,
                                                    xaxis = {'showgrid': False, 'zeroline': False}, yaxis = {'showgrid': False, 'zeroline': False})

        factor_period_sum_plate_map_fig.update_traces(contours_coloring="fill", contours_showlabels = True,  colorscale="Viridis")

        homex = [-0.26, 0, 0.26, 0.26, -0.26, -0.26]
        homey = [0.215, 0, 0.215, 0.43, 0.43, 0.215]

        factor_period_sum_plate_map_fig.append_trace(go.Scatter(x=homex,y=homey, mode = 'lines', line=dict(color='white', width=4) ), row = 'all' , col = 'all')

        factor_period_sum_plate_map_fig.add_hline(y=1, line_dash='dash' ,line_width=1, line_color='white')
        factor_period_sum_plate_map_fig.add_hline(y=0.43,  line_dash='dash' ,line_width=1, line_color='white')
        factor_period_sum_plate_map_fig.add_hline(y=0,  line_dash='dash' ,line_width=1, line_color='white')
        factor_period_sum_plate_map_fig.add_vline(x=-0.37,line_width=1, line_color='white')
        factor_period_sum_plate_map_fig.add_vline(x=0.37, line_width=1, line_color='white')
        factor_period_sum_plate_map_fig.add_vline(x=-0.26, line_dash='dash' ,line_width=1, line_color='white')
        factor_period_sum_plate_map_fig.add_vline(x=0.26, line_dash='dash', line_width=1, line_color='white')

        factor_period_sum_plate_map_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
        factor_period_sum_plate_map_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)

        return factor_period_sum_plate_map_fig
    
    else:
        factor_period_sum_plate_map_fig = go.Figure()
        factor_period_sum_plate_map_fig.add_shape(type="rect", x0=0, y0=0, x1=1, y1=1, line=dict(color="gray", width=1), fillcolor="white", opacity=0.3)
        factor_period_sum_plate_map_fig.update_layout(width=450, height=100, title="데이터가 존재하지 않습니다.")
        factor_period_sum_plate_map_fig.update_xaxes(visible=False, range=[0, 1])
        factor_period_sum_plate_map_fig.update_yaxes(visible=False, range=[0, 1])

        return factor_period_sum_plate_map_fig

def season_spraychart(dataframe):

    colors = {'field_out':'rgba(140,86,75,0.3)','fielders_choice_out':'rgba(140,86,75,0.3)', 'field_error':'rgba(140,86,75,0.3)', 'sac_fly':'rgba(140,86,75,0.3)', 
          'force_out':'rgba(140,86,75,0.3)', 'double_play':'rgba(140,86,75,0.3)', 'grounded_into_double_play':'rgba(140,86,75,0.3)',
          'home_run':'rgba(255,72,120,1)', 'triple':'rgba(255,72,120,1)', 'double':'rgba(255,72,120,1)', 'single':'rgba(67,89,119,0.7)' }
    symbols = {'4-Seam Fastball':'circle', '2-Seam Fastball':'triangle-down', 'Cutter': 'triangle-se', 'Slider': 'triangle-right', 'Curveball': 'triangle-up', 'Sweeper':'cross', 'Changeup': 'diamond', 'Split-Finger':'square'}

    col_index = len(dataframe['game_year'].unique())

    season_spraychart_fig = px.scatter(dataframe, x='groundX', y='groundY', color='events',  facet_col='game_year', symbol="pitch_name",
                         color_discrete_map=colors,
                         hover_name="player_name", hover_data=["rel_speed(km)","pitch_name","events","exit_velocity","description","launch_speed_angle","launch_angle",'hit_spin_rate'],
                        #  category_orders={"game_year": [2021,2022, 2023]},
                         height = 580, width = col_index*500)
    
    for i, d in enumerate(season_spraychart_fig.data):
        season_spraychart_fig.data[i].marker.symbol = symbols[season_spraychart_fig.data[i].name.split(', ')[1]]

    season_spraychart_fig.update_yaxes(domain=[0.1, 0.97])

    season_spraychart_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-10,130], yaxis_range=[-10,130])

    season_spraychart_fig.update_layout({'plot_bgcolor': 'rgba(255,255,255,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

    season_spraychart_fig.update_yaxes(gridcolor='rgba(255,255,255,1)')
    season_spraychart_fig.update_xaxes(gridcolor='rgba(255,255,255,1)')

    season_spraychart_fig.update_traces(marker=dict(size=20))

    season_spraychart_fig.update_layout(showlegend=False)

    season_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=28, y1=28, line=dict(color="rgba(108,122,137,0.7)"), line_width=5, row="all", col="all")

    season_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=135, y1=135, line=dict(color="rgba(108,122,137,0.7)"), line_width=5, row="all", col="all")

    season_spraychart_fig.add_shape(type="path", path="M 0,100 Q 120,120 100,0", line_color="rgba(108,122,137,0.7)", line_width = 5, row="all", col="all")

    season_spraychart_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
    season_spraychart_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)

    return  st.plotly_chart(season_spraychart_fig, layout="wide")

def season_hangtime_spraychart(dataframe):

    colors = {'shrot':'rgba(67,89,119,0.7)','long':'rgba(140,86,75,0.3)', 'challenge':'rgba(255,72,120,1)' }
    symbols = {'4-Seam Fastball':'circle', '2-Seam Fastball':'triangle-down', 'Cutter': 'triangle-se', 'Slider': 'triangle-right', 'Curveball': 'triangle-up', 'Sweeper': 'cross', 'Changeup': 'diamond', 'Split-Finger':'square'}

    col_index = len(dataframe['game_year'].unique())

    season_spraychart_fig = px.scatter(dataframe, x='groundX', y='groundY', color='hangtime_type', color_discrete_map=colors, facet_col='game_year', symbol="pitch_name",
                         hover_name="player_name", hover_data=["rel_speed(km)","pitch_name","events","exit_velocity","description","launch_speed_angle","launch_angle",'hit_spin_rate','hangtime'],
                        #  category_orders={"game_year": [2021,2022, 2023]},
                         height = 580, width = col_index*500)
    
    for i, d in enumerate(season_spraychart_fig.data):
        season_spraychart_fig.data[i].marker.symbol = symbols[season_spraychart_fig.data[i].name.split(', ')[1]]

    season_spraychart_fig.update_yaxes(domain=[0.1, 0.97])

    season_spraychart_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-10,130], yaxis_range=[-10,130])

    season_spraychart_fig.update_layout({'plot_bgcolor': 'rgba(255,255,255,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

    season_spraychart_fig.update_yaxes(gridcolor='rgba(255,255,255,1)')
    season_spraychart_fig.update_xaxes(gridcolor='rgba(255,255,255,1)')

    season_spraychart_fig.update_traces(marker=dict(size=20))

    season_spraychart_fig.update_layout(showlegend=False)

    season_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=28, y1=28, line=dict(color="rgba(108,122,137,0.7)"), line_width=5, row="all", col="all")

    season_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=135, y1=135, line=dict(color="rgba(108,122,137,0.7)"), line_width=5, row="all", col="all")

    season_spraychart_fig.add_shape(type="path", path="M 0,100 Q 120,120 100,0", line_color="rgba(108,122,137,0.7)", line_width = 5, row="all", col="all")

    season_spraychart_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
    season_spraychart_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)

    return  season_spraychart_fig
    
def season_period_spraychart(dataframe):

    date2 = pd.to_datetime('today')
    date1 = date2 - timedelta(weeks=2)

    dataframe = dataframe[(dataframe['game_date'] >= date1) & (dataframe['game_date'] <= date2)]

    if len(dataframe) > 0:

        colors = {'field_out':'rgba(140,86,75,0.3)','fielders_choice_out':'rgba(140,86,75,0.3)', 'field_error':'rgba(140,86,75,0.3)', 'sac_fly':'rgba(140,86,75,0.3)', 
            'force_out':'rgba(140,86,75,0.3)', 'double_play':'rgba(140,86,75,0.3)', 'grounded_into_double_play':'rgba(140,86,75,0.3)',
            'home_run':'rgba(255,72,120,1)', 'triple':'rgba(255,72,120,1)', 'double':'rgba(255,72,120,1)', 'single':'rgba(67,89,119,0.7)' }
        symbols = {'4-Seam Fastball':'circle', '2-Seam Fastball':'triangle-down', 'Cutter': 'triangle-se', 'Slider': 'triangle-right', 'Curveball': 'triangle-up','Sweeper': 'cross', 'Changeup': 'diamond', 'Split-Finger':'square'}

        season_spraychart_fig = px.scatter(dataframe, x='groundX', y='groundY', color='events',  facet_col='game_year', symbol="pitch_name",
                            color_discrete_map=colors,
                            hover_name="player_name", hover_data=["rel_speed(km)","pitch_name","events","exit_velocity","description","launch_speed_angle","launch_angle",'hit_spin_rate'],
                            #  category_orders={"game_year": [2021,2022, 2023]},
                            height = 580, width = 550)
        
        for i, d in enumerate(season_spraychart_fig.data):
            season_spraychart_fig.data[i].marker.symbol = symbols[season_spraychart_fig.data[i].name.split(', ')[1]]

        season_spraychart_fig.update_yaxes(domain=[0.1, 0.97])

        season_spraychart_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-10,130], yaxis_range=[-10,130])

        season_spraychart_fig.update_layout({'plot_bgcolor': 'rgba(255,255,255,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

        season_spraychart_fig.update_yaxes(gridcolor='rgba(255,255,255,1)')
        season_spraychart_fig.update_xaxes(gridcolor='rgba(255,255,255,1)')

        season_spraychart_fig.update_traces(marker=dict(size=20))

        season_spraychart_fig.update_layout(showlegend=False)

        season_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=28, y1=28, line=dict(color="rgba(108,122,137,0.7)"), line_width=5, row="all", col="all")

        season_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=135, y1=135, line=dict(color="rgba(108,122,137,0.7)"), line_width=5, row="all", col="all")

        season_spraychart_fig.add_shape(type="path", path="M 0,100 Q 120,120 100,0", line_color="rgba(108,122,137,0.7)", line_width = 5, row="all", col="all")

        season_spraychart_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
        season_spraychart_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)

        return  season_spraychart_fig
    
    else:
        season_spraychart_fig = go.Figure()
        season_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=1, y1=1, line=dict(color="gray", width=1), fillcolor="white", opacity=0.3)
        season_spraychart_fig.update_layout(width=450, height=100, title="데이터가 존재하지 않습니다.")
        season_spraychart_fig.update_xaxes(visible=False, range=[0, 1])
        season_spraychart_fig.update_yaxes(visible=False, range=[0, 1])

        return season_spraychart_fig

def season_zone_spraychart(dataframe, zone):

    game_year = dataframe['game_year'].max()
    dataframe = dataframe[(dataframe['game_year'] == game_year) & (dataframe['new_zone'] == zone)]
    
    colors = {'field_out':'rgba(140,86,75,0.3)','fielders_choice_out':'rgba(140,86,75,0.3)', 'field_error':'rgba(140,86,75,0.3)', 'sac_fly':'rgba(140,86,75,0.3)', 
          'force_out':'rgba(140,86,75,0.3)', 'double_play':'rgba(140,86,75,0.3)', 'grounded_into_double_play':'rgba(140,86,75,0.3)',
          'home_run':'rgba(255,72,120,1)', 'triple':'rgba(255,72,120,1)', 'double':'rgba(255,72,120,1)', 'single':'rgba(67,89,119,0.7)' }
    symbols = {'4-Seam Fastball':'circle', '2-Seam Fastball':'triangle-down', 'Cutter': 'triangle-se', 'Slider': 'triangle-right', 'Curveball': 'triangle-up', 'Sweeper': 'cross','Changeup': 'diamond', 'Split-Finger':'square'}

    season_zone_spraychart_fig = px.scatter(dataframe, x='groundX', y='groundY', color='events',  facet_col='new_zone', facet_row='new_zone', symbol="pitch_name",
                         color_discrete_map=colors,
                         hover_name="player_name", hover_data=["rel_speed(km)","pitch_name","events","exit_velocity","description","launch_speed_angle","launch_angle",'hit_spin_rate'],
                        #  category_orders={"game_year": [2021,2022, 2023]},
                         height = 300, width = 300)
    
    for i, d in enumerate(season_zone_spraychart_fig.data):
        season_zone_spraychart_fig.data[i].marker.symbol = symbols[season_zone_spraychart_fig.data[i].name.split(', ')[1]]

    season_zone_spraychart_fig.update_yaxes(domain=[0.1, 0.97])

    season_zone_spraychart_fig.update_layout(autosize=False, margin=dict(l=50, r=50, t=50, b=50), xaxis_range=[-10,130], yaxis_range=[-10,130])

    season_zone_spraychart_fig.update_layout({'plot_bgcolor': 'rgba(255,255,255,1)', 'paper_bgcolor': 'rgba(255,255,255,1)',})

    season_zone_spraychart_fig.update_yaxes(gridcolor='rgba(255,255,255,1)')
    season_zone_spraychart_fig.update_xaxes(gridcolor='rgba(255,255,255,1)')

    season_zone_spraychart_fig.update_traces(marker=dict(size=20))

    season_zone_spraychart_fig.update_layout(showlegend=False)

    season_zone_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=28, y1=28, line=dict(color="rgba(108,122,137,0.7)"), line_width=5, row="all", col="all")

    season_zone_spraychart_fig.add_shape(type="rect", x0=0, y0=0, x1=135, y1=135, line=dict(color="rgba(108,122,137,0.7)"), line_width=5, row="all", col="all")

    season_zone_spraychart_fig.add_shape(type="path", path="M 0,100 Q 120,120 100,0", line_color="rgba(108,122,137,0.7)", line_width = 5, row="all", col="all")

    season_zone_spraychart_fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)
    season_zone_spraychart_fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(108,122,137,0.9)', mirror=True)

    return  season_zone_spraychart_fig


def zone_spraychart_fig(spraychart_dataframe):

    col1, col2, col3 = st.columns(3)

    with col1:
        zone = 'nz1'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")

    with col2:
        zone = 'nz2'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")

    with col3:
        zone = 'nz3'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")


    col4, col5, col6 = st.columns(3)

    with col4:
        zone = 'nz4'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")

    with col5:
        zone = 'core'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")

    with col6:
        zone = 'nz6'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")

    col7, col8, col9 = st.columns(3)

    with col7:
        zone = 'nz7'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")

    with col8:
        zone = 'nz8'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")

    with col9:
        zone = 'nz9'
        season_zone_spraychart_fig = season_zone_spraychart(spraychart_dataframe, zone)
        season_zone_spraychart_fig.update_layout(height=500, width=500)
        season_zone_spraychart_fig.update_coloraxes(showscale=False)
        st.plotly_chart(season_zone_spraychart_fig, layout="wide")





def select_count_option(dataframe, factor):

    season_pitched_fig = factor_year_count_map(dataframe, factor)
    st.plotly_chart(season_pitched_fig, layout="wide")

    with st.expander("Recent 2 Weeks"):
        week2_pitched_fig = factor_period_coount_map(dataframe, factor)
        st.plotly_chart(week2_pitched_fig, layout="wide") 

    with st.expander("Fastball"):
        selected_df = dataframe[dataframe['p_kind'] == "Fastball"]
        season_pitched_fig = factor_year_count_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")
    
    with st.expander("Breaking"):
        selected_df = dataframe[dataframe['p_kind'] == "Breaking"]
        season_pitched_fig = factor_year_count_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")

    with st.expander("Off-Speed"):
        selected_df = dataframe[dataframe['p_kind'] == "Off_Speed"]
        season_pitched_fig = factor_year_count_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")

def select_sum_option(dataframe, factor):

    season_pitched_fig = factor_year_sum_map(dataframe, factor)
    st.plotly_chart(season_pitched_fig, layout="wide")

    with st.expander("Recent 2 Weeks"):
        week2_pitched_fig = factor_period_sum_map(dataframe, factor)
        st.plotly_chart(week2_pitched_fig, layout="wide")

    with st.expander("Fastball"):
        selected_df = dataframe[dataframe['p_kind'] == "Fastball"]
        season_pitched_fig = factor_year_sum_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")
    
    with st.expander("Breaking"):
        selected_df = dataframe[dataframe['p_kind'] == "Breaking"]
        season_pitched_fig = factor_year_sum_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")
    
    with st.expander("Off-Speed"):
        selected_df = dataframe[dataframe['p_kind'] == "Off_Speed"]
        season_pitched_fig = factor_year_sum_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")


def select_sum_plate_option(dataframe, factor):

    season_pitched_plate_fig = factor_year_sum_plate_map(dataframe, factor)
    st.plotly_chart(season_pitched_plate_fig, layout="wide")

    with st.expander("Recent 2 Weeks"):
        week2_pitched_plate_fig = factor_period_sum_plate_map(dataframe, factor)
        st.plotly_chart(week2_pitched_plate_fig, layout="wide")   

    with st.expander("Fastball"):
        selected_df = dataframe[dataframe['p_kind'] == "Fastball"]
        season_pitched_plate_fig = factor_year_sum_plate_map(selected_df, factor)
        st.plotly_chart(season_pitched_plate_fig, layout="wide")
    
    with st.expander("Breaking"):
        selected_df = dataframe[dataframe['p_kind'] == "Breaking"]
        season_pitched_plate_fig = factor_year_sum_plate_map(selected_df, factor)
        st.plotly_chart(season_pitched_plate_fig, layout="wide")

    with st.expander("Off-Speed"):
        selected_df = dataframe[dataframe['p_kind'] == "Off_Speed"]
        season_pitched_plate_fig = factor_year_sum_plate_map(selected_df, factor)
        st.plotly_chart(season_pitched_plate_fig, layout="wide")


def swingmap_count_option(dataframe, factor):

    season_pitched_fig = swingmap_count_map(dataframe, factor)
    st.plotly_chart(season_pitched_fig, layout="wide")

    with st.expander("Recent 2 Weeks"):
        week2_pitched_fig = swingmap_period_count_map(dataframe, factor)
        week2_symbol_fig = swingmap_period_symbol_map(dataframe)

        st.plotly_chart(week2_pitched_fig, layout="wide")
        st.plotly_chart(week2_symbol_fig, layout="wide")    

    with st.expander("Fastball"):
        selected_df = dataframe[dataframe['p_kind'] == "Fastball"]
        season_pitched_fig = swingmap_count_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")

    with st.expander("Breaking"):
        selected_df = dataframe[dataframe['p_kind'] == "Breaking"]
        season_pitched_fig = swingmap_count_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")

    with st.expander("Off-Speed"):
        selected_df = dataframe[dataframe['p_kind'] == "Off_Speed"]
        season_pitched_fig = swingmap_count_map(selected_df, factor)
        st.plotly_chart(season_pitched_fig, layout="wide")


