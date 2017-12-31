from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507, host='0.0.0.0')

@app.route('/graph', methods=['GET','POST'])
def bokeh():
    if request.method == 'POST':
        ticker = request.form['ticker']
        
        return render_template('graph.html', ticker = ticker)
    
    
    fig = figure(plot_width=600, plot_height=600)
    fig.line(
        x=[1, 2, 3, 4],
        y=[1.7, 2.2, 4.6, 3.9],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'graph.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)