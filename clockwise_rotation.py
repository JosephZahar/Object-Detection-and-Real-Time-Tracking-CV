from plotly.subplots import make_subplots
import math
import plotly.graph_objects as go
import numpy as np

tetas = np.arange(0, 10 * math.pi, 0.01)
z1 = [16 * (1 - math.cos(teta - (math.pi / 2))) for teta in tetas]
z2 = [16 * (1 - math.cos(teta)) for teta in tetas]
fig3 = make_subplots(
    rows=1, cols=2,
    horizontal_spacing=0.2)

fig3.add_trace(go.Scatter(x=[0], y=[z1[0]], line=dict(width=2, color="blue")), row=1, col=1)
fig3.add_trace(go.Scatter(x=[0], y=[z2[0]], line=dict(width=2, color="red")), row=1, col=2)
frames = [go.Frame(data=[go.Scatter(x=[0], y=[z1[i]]),
                         go.Scatter(x=[0], y=[z2[i]])],
                         traces=[0,1]) for i in range(len(z1))]
fig3.frames=frames

button = dict(
             label='Play',
             method='animate',
            args=[None, {"frame": {"duration": 50,
                           "redraw": False},
                 "fromcurrent": True,
                 "transition": {"duration": 0}}])
fig3.update_layout(updatemenus=[dict(type='buttons',
                              showactive=False,
                              y=-0.5,
                              x=-0.05,
                              xanchor='left',
                              yanchor='bottom',
                              buttons=[button] )], template="simple_white", width=700, height=800)
fig3.update(layout_showlegend=False)
fig3['layout']['yaxis']['title']='z2'
fig3['layout']['yaxis2']['title']='z1'
fig3['layout']['title']='Counter-Clockwise Rotation'
fig3.update_layout(yaxis=dict(tickvals=np.arange(-4,33,4)),
                   yaxis2=dict(tickvals=np.arange(-4,33,4)))
fig3.show()


