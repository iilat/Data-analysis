# !/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime


import pandas as pd

data=pd.read_excel('/Users/vk/py/costs.xlsm')

data=round(data.groupby('obj',as_index=False)['value','income'].sum(),1)

tax_value = 0.97

data['income']=round(data['income']*tax_value,1)

data['total']=round(data['income']-data['value'],1)

data.style \
.format(precision=0, thousands=" ", decimal=",") \
.format_index(str.upper, axis=1) 
a=datetime.now().date()

bar = [go.Bar(x = data['obj'], 
                                y = data['total'], 
                                name = 'Остаток'),
          go.Bar(x = data['obj'], 
                                y = data['income'], 
                                name = 'Поступления'),
          go.Bar(x = data['obj'], 
                                y = data['value'], 
                                name = 'Расходы')
       ]

fig = px.bar(data.sort_values(by='total',ascending=True), 
             x='obj', # указываем столбец с данными для оси X
             y='total', # указываем столбец с данными для оси Y
             text='total', # добавляем аргумент, который отобразит текст с информацией                    
             labels='obj',
             color='obj',
             barmode='overlay'
                )
# оформляем график
fig.update_layout(title='Остаток средств',
                   xaxis_title='Объект',
                   yaxis_title='Остаток,руб')
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')


# задаём лейаут (макет)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[  

    # формируем заголовок
    html.H1(children = 'Управление проектами'), 
    html.Label(children = a),
    html.H3(children = 'Остаток средств:'),
    html.Label(children = data['total'].sum()),


    # график 
    dcc.Graph(
        figure = {
            'data': [go.Table(header = {'values': ['<b>Объект</b>',                            
                                                   '<b>Оплатили,руб.</b>', 
                                                   '<b>Пришло,руб.</b>',
                                                   '<b>Сумма,руб.</b>'],
                                        'fill_color': 'lightgrey',
                                        'align': 'center'
                                        },
                              cells = {'values': data.T.values})],
            'layout': go.Layout(xaxis = {'title': 'Страна'},
                                yaxis = {'title': 'Макс. % городского населения'})
         },
        id = 'data'
    ), 
    html.Label('График средств'),
    
    dcc.Graph(
        figure = {
                'data': bar,
                'layout': go.Layout(xaxis = {'title': 'Объект'},
                                    yaxis = {'title': 'Остаток средств,руб.'},
                                    barmode  = 'group',

                                    height= 500)
             },
        id = 'data'
    ),
    dcc.Graph(figure=fig), 
    ])
# описываем логику дашборда
if __name__ == '__main__':
    app.run_server(debug=True)