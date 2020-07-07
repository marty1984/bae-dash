import plotly.offline as pyo
import plotly.graph_objects as go
import pandas as pd; import numpy as np; import os

import dash
import dash_core_components as dcc
import dash_html_components as html

data_dir = r'C:\Users\marti\Google Drive\Projects\Dash-Playing\New folder\Data'
df = pd.read_csv(data_dir + r'\example.csv')

df.sort_values(by = ['forecast'], inplace=True)
df['cdrl_tots'] = np.arange(1,df.shape[0]+1,1)
df.reset_index()

### quick line chart
x_values = df['forecast'][::-1]
y_values = df['cdrl_tots'] 

trace = go.Scatter(x=x_values, 
                   y=y_values, 
                   mode='markers+lines+text', 
                   name='markers' , 
                   hovertext= df['pp'],
                   hoverinfo='x+y+text')

data = [trace]
layout = go.Layout(title='burn down chart')

fig=go.Figure(data=data, layout=layout)


### quick bar chart
temp = df.loc[: , ['domain' ,'state' , 'shock' ]]

for i in df['state'].drop_duplicates():
    print (i)
    filt = temp['state']==i
    temp.loc[filt , i] = 1

ipt  = temp.groupby('domain').sum()
ipt = ipt.T
ipt['cdrl_tots'] = ipt.agg(sum,axis=1)
ipt=ipt.T
ipt['domain_tots'] = ipt.agg(sum,axis=1)

traces=[]; colour = []
for i,j in enumerate(ipt.keys()):
    print (j)
    trace = go.Bar(x=ipt.index.to_list(), y=ipt[j],name=j)
    traces.append(trace)
layout = go.Layout(title='cdrls')
fig2 = go.Figure(data=traces,layout=layout)


traces=[]; colour = []
for i,j in enumerate(ipt.keys()[:-1]):
    print (j)
    trace = go.Bar(x=ipt.index.to_list(), y=ipt[j],name=j)
    traces.append(trace)
layout1 = go.Layout(title='cdrls_stacked',barmode='stack')
layout2 = go.Layout(title='cdrls_unstacked')
fig3 = go.Figure(data=traces,layout=layout1)
fig4 = go.Figure(data=traces,layout=layout2)


### application

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('example dashboard'),
    html.H2('all of the data here is randomly generated'),
    html.Div(
            dcc.Graph(id='burn down example',
              figure= fig
            )       
        ),

    dcc.Graph(id='stacked',
              figure= fig3
            ),
    dcc.Graph(id='unstacked',
              figure= fig4)

    ]    
    )

# app.css.append_css({
#     'external_url':'https://codepen.io/chriddyp/pen/pen/bWLwgP.css'})

# app.layout = html.Div(children=[
#     html.H1('page title: cdrl dashboard'),
#     dcc.Graph(id='burn down example',
#               figure= dict(data=[go.Scatter(
#                   x=df['forecast'][::-1] ,
#                   y=df['cdrl_tots'] ,
#                   hovertext= df['pp'],
#                   hoverinfo='x+y+text'   ,               
#                   mode='markers',
#                   )])

#             )

#     ]    
#     )

if __name__=='__main__':
    app.run_server()
    
    
#http://127.0.0.1:8050/