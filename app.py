from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import HoverTool
import requests
import simplejson as json
import pandas as pd
import numpy as np
import datetime as dt



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test/')
def test():
    return render_template('index.html')

@app.route('/graph', methods=['GET','POST'])
def bokeh():
    if request.method == 'POST':
        ticker = request.form['ticker']
        testvar = 'print this message'
        
        prev_month = str(dt.date.today() - dt.timedelta(days=30))
        r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=fYn3C1q9An-WQVvoQzQH&date.gt=%s&ticker=%s&qopts.columns=ticker,date,close' %(prev_month, ticker))
        data_json = r.json()
        df = pd.DataFrame([x for x in data_json['datatable']['data']],
                  columns=[x['name'] for x in data_json['datatable']['columns']])
        
        if df.shape[0] == 0:
            return render_template('index.html',hidden = '*Ticker symbol not found in database')
        test = df.iloc[0][0]
        
        y=df['close']
        x=pd.to_datetime(df['date'])
        x_date=[str(z) for z in df['date']]
                
        hover = HoverTool(tooltips=[("price","@y{$0,0.00}")],
                          mode = "vline")
        
        fig = figure(plot_width=720, plot_height=540, 
                     x_axis_type="datetime", tools=[hover])
        fig.border_fill_color = "whitesmoke"
        fig.min_border_left = 80
        
        fig.xaxis.axis_label = "Date"
        fig.xaxis.axis_label_text_font_style = "bold"
        fig.xaxis.minor_tick_line_color = "orange"

        fig.yaxis.axis_label = "Price (USD)"
        fig.yaxis.axis_label_text_font_style = "bold"
        
        fig.line(y=y, x=x,
            legend = ticker,
            line_width = 2,
        )
        
        fig.legend.location = "top_left"
        fig.legend.label_text_font_style = "bold"
        
        # grab the static resources
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()

        # render template
        script, div = components(fig)

       
        return render_template('graph.html',
            plot_script=script,
            plot_div=div,
            js_resources=js_resources,
            css_resources=css_resources,
            ticker = ticker, test = test)
    return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507, host='0.0.0.0', debug = True)

