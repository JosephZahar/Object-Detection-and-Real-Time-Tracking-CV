import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = 'simple_white'

experiment3 = pd.read_csv("/Users/macbookpro/PycharmProjects/Object_Tracker/data/Exp3/Exp3_1.csv")
mmperpixel_rect = 20/1090

def phi(x0, y0, x1, y1, teta):
    if y1 - y0 > 0 and x1 - x0 > 0:
        return teta
    elif y1 - y0 > 0 and x1 - x0 < 0:
        return teta + 180
    elif y1 - y0 < 0 and x1 - x0 > 0:
        return teta + 360
    elif y1 - y0 < 0 and x1 - x0 < 0:
        return teta + 180

def angle_sign(xc, x0, xm, theta):
    if x0 > xc:
        if x0 < xm:
            return theta
        else:
            return -theta
    else:
       if x0 > xm:
            return theta
       else:
            return -theta

def tracker_analysis(data):
    df = data.copy()
    df['centery'] = df['centery'].mean()
    df['centerx'] = df['centerx'].mean()

    df['circle_x1-1'] = df['circle_x1'].shift(1, fill_value=0)
    df['circle_x2-1'] = df['circle_x2'].shift(1, fill_value=0)
    df['circle_x3-1'] = df['circle_x3'].shift(1, fill_value=0)

    df['angle_x1'] = np.arctan2(df['circle_y1'] - df['centery'], df['circle_x1'] - df['centerx']) * (180.0 / math.pi)
    df['angle_x2'] = np.arctan2(df['circle_y2'] - df['centery'], df['circle_x2'] - df['centerx']) * (180.0 / math.pi)
    df['angle_x3'] = np.arctan2(df['circle_y3'] - df['centery'], df['circle_x3'] - df['centerx']) * (180.0 / math.pi)

    df['angle_x1_2'] = df.apply(lambda row: angle_sign(row['centerx'], row['circle_x1'], row['circle_x1-1'], row['angle_x1']), axis=1)
    df['angle_x2_2'] = df.apply(lambda row: angle_sign(row['centerx'], row['circle_x2'], row['circle_x2-1'], row['angle_x2']), axis=1)
    df['angle_x3_2'] = df.apply(lambda row: angle_sign(row['centerx'], row['circle_x3'], row['circle_x3-1'], row['angle_x3']), axis=1)

    df['angle_x1-1'] = df['angle_x1_2'].shift(1, fill_value=0)
    df['angle_x2-1'] = df['angle_x2_2'].shift(1, fill_value=0)
    df['angle_x3-1'] = df['angle_x3_2'].shift(1, fill_value=0)

    df['m21'] = np.tan(df['angle_x1'])
    df['m22'] = np.tan(df['angle_x2'])
    df['m23'] = np.tan(df['angle_x3'])
    df['m11'] = np.tan(df['angle_x1-1'])
    df['m12'] = np.tan(df['angle_x2-1'])
    df['m13'] = np.tan(df['angle_x3-1'])

    df['angle_x1_f'] = np.arctan(abs((df['m11'] - df['m21'])/(1 + df['m11']*df['m21']))).cumsum()
    df['angle_x2_f'] = np.arctan(abs((df['m12'] - df['m22'])/(1 + df['m12']*df['m22']))).cumsum()
    df['angle_x3_f'] = np.arctan(abs((df['m13'] - df['m23'])/(1 + df['m13']*df['m23']))).cumsum()

    df['avg_angle_cumsum'] = (df['angle_x1_f'] + df['angle_x2_f'] + df['angle_x3_f'])/3

    df['x6'] = abs(df['rect_x5'] - df['rect_x5'][1])
    # df['x6_translation_cumsum_mm'] = df['x6_translation_change_mm'].cumsum()
    df['x6_angle_change'] = np.arccos((1 - (df['x6'] / 142)))
    df['x6_angle_cumsum'] = df['x6_angle_change'].cumsum()


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['x6_angle_change'],
                    mode='lines',
                    name='Master Angle <br> (Input)',
                    line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=df.index, y=df['avg_angle_cumsum'],
                    mode='lines',
                    name='Slave Angle <br> (Output)',
                    line=dict(color='red', width=1)))

    fig.update_layout(showlegend=True, yaxis_title='Shaft Angle', xaxis_title='t',
                  font=dict(family="Computer Modern",size=14))
    fig.update_yaxes(ticksuffix="°")
    fig.show()

tracker_analysis(experiment3)

def piston_length(df):
    df['x1_change'] = (df['circle_y3'] - df['rect_y4']) * mmperpixel_piston
    df['x2_change'] = (df['circle_y2'] - df['circle_y1']) * mmperpixel_piston

    diff = df['x2_change'][0] - df['x1_change'][0]
    df['x1_change'] = df['x1_change'] + diff

    plt.plot(df.index/6, df['x1_change'], label='circle_x1', color='royalblue')
    plt.plot(df.index/6, df['x2_change'], label='circle_x2', color='crimson')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xlabel('Seconds')
    plt.ylabel('')
    plt.show()
