import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=1, cols=2, subplot_titles=('Title1', 'Title2'),
    horizontal_spacing=0.051
)

fig.add_trace(go.Bar(x=['A', 'B', 'C', 'D'], y=[4, 2, 1, 5]), row=1, col=1)  # this is the trace of index 0
fig.add_trace(go.Scatter(x=['A', 'B', 'C', 'D'], y=[2, 1.45, 0.25, 2.1],
                         line_width=3), row=1, col=1)  # trace of index 1

fig.add_trace(go.Scatter(x=np.arange(10),
                         y=1 + 3 * np.random.rand(10),
                         marker_size=6), row=1, col=2)  # trace of index 2

# traces=[0, 1, 2]` in the frame definition makes the difference: it tells that
# the traces of index 0, 1 from the subplot(1,1), are unchanged, and we only ensure their visibility in each #frame (because neither x nor y are modified)
# while the trace 2 from the subplot(1,2) is animated, because the y-values are changed.

frames = [go.Frame(data=[go.Bar(visible=True),
                         go.Scatter(visible=True),
                         go.Scatter(y=2 + 3 * np.random.rand(10))],
                   traces=[0, 1, 2]) for k in range(20)]  # define 20 frames

fig.frames = frames
button = dict(
    label='Play',
    method='animate',
    args=[None, dict(frame=dict(duration=50, redraw=False),
                     transition=dict(duration=0),
                     fromcurrent=True,
                     mode='immediate')])
fig.update_layout(updatemenus=[dict(type='buttons',
                                    showactive=False,
                                    y=0,
                                    x=1.05,
                                    xanchor='left',
                                    yanchor='bottom',
                                    buttons=[button])
                               ],
                  width=800, height=500)

fig.update_layout(yaxis2_range=[0, 5.5], yaxis2_autorange=False)
fig.show()