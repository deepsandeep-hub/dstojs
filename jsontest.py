from openpyxl import load_workbook
from flask import Flask,jsonify,request,render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots




df = pd.DataFrame()
file = "D:/excel data/residential.xlsx"

def recieve_data(cty = input('Enter the City name:-')):
    sheet = ['India','ahemdabad','bangalore','chennai','hyderabad','kolkata','mumbai','delhi','pune']
    if cty in sheet:
        df= (pd.read_excel(file,sheet_name = cty,engine = 'openpyxl')).copy()
        df.drop(['Unsold','Average sqft','Price per sqft'],axis = 1,inplace = True)
        df.drop(7,axis = 0,inplace = True)
    elif cty == 'india':
        print('Enter Capital I in india')
    else:
        print('enter the name in small letters')
    
    return df #print(df)

def plotin(data = recieve_data()):
    global graphJSON
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Scatter(x=data["Years"], y=data["Launched (units)"], name="Launches"))
    fig.add_trace(go.Scatter(x=data['Years'], y=data['Sold (units)'],name="Sold"))
    fig.update_layout(title_text=' Launch vs Sold ') 
    fig.update_xaxes(title_text="Years")
    fig.update_yaxes(title_text="Launched & Sold Units ")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return  print(graphJSON)
    # return print(fig.show())
plotin()
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('jsony.html')
@app.route('/returnjson')
def ReturnJSON():
    return graphJSON

if __name__=='__main__':
	app.run(debug = False)
