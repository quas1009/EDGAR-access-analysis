from flask import Flask, render_template, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
import pandas as pd
import json
import numpy as np


def fetch_data(query):
    conn = psycopg2.connect(app.conn_str)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)    

scatterGeo = {'Afghanistan':[67.709953,33.93911],
    'Angola':[17.873887,-11.202692],
    'Albania':[20.168331,41.153332],
    'United Arab Emirates':[53.847818,23.424076],
    'Argentina':[-63.61667199999999,-38.416097],
    'Armenia':[45.038189,40.069099],
    'French Southern and AntarcticLands':[69.348557,-49.280366],
    'Australia':[133.775136,-25.274398],
    'Austria':[14.550072,47.516231],
    'Azerbaijan':[47.576927,40.143105],
    'Burundi':[29.918886,-3.373056],
    'Belgium':[4.469936,50.503887],
    'Benin':[2.315834,9.30769],
    'BurkinaFaso':[-1.561593,12.238333],
    'Bangladesh':[90.356331,23.684994],
    'Bulgaria':[25.48583,42.733883],
    'TheBahamas':[-77.39627999999999,25.03428],
    'Bosnia andHerzegovina':[17.679076,43.915886],
    'Belarus':[27.953389,53.709807],
    'Belize':[-88.49765,17.189877],
    'Bermuda':[-64.7505,32.3078],
    'Bolivia':[-63.58865299999999,-16.290154],
    'Brazil':[-51.92528,-14.235004],
    'Brunei':[114.727669,4.535277],
    'Bhutan':[90.433601,27.514162],
    'Botswana':[24.684866,-22.328474],
    'Central African Republic':[20.939444,6.611110999999999],
    'Canada':[-106.346771,56.130366],
    'Switzerland':[8.227511999999999,46.818188],
    'Chile':[-71.542969,-35.675147],
    'China':[104.195397,35.86166],
    'Hong Kong':[104.195397,35.86166],
    'IvoryCoast':[-5.547079999999999,7.539988999999999],
    'Cameroon':[12.354722,7.369721999999999],
    'Democratic Republic of the Congo':[21.758664,-4.038333],
    'Republic of the Congo':[15.827659,-0.228021],
    'Colombia':[-74.297333,4.570868],
    'CostaRica':[-83.753428,9.748916999999999],
    'Cuba':[-77.781167,21.521757],
    'Northern Cyprus':[33.429859,35.126413],
    'Cyprus':[33.429859,35.126413],
    'CzechRepublic':[15.472962,49.81749199999999],
    'Germany':[10.451526,51.165691],
    'Djibouti':[42.590275,11.825138],
    'Denmark':[9.501785,56.26392],
    'Dominican Republic':[-70.162651,18.735693],
    'Algeria':[1.659626,28.033886],
    'Ecuador':[-78.18340599999999,-1.831239],
    'Egypt':[30.802498,26.820553],
    'Eritrea':[39.782334,15.179384],
    'Spain':[-3.74922,40.46366700000001],
    'Estonia':[25.013607,58.595272],
    'Ethiopia':[40.489673,9.145000000000001],
    'Finland':[25.748151,61.92410999999999],
    'Fiji':[178.065032,-17.713371],
    'Falkland Islands':[-59.523613,-51.796253],
    'France':[2.213749,46.227638],
    'Gabon':[11.609444,-0.803689],
    'United Kingdom of Great Britain and Northern Ireland':[-3.435973,55.378051],
    'Georgia':[-82.9000751,32.1656221],
    'Ghana':[-1.023194,7.946527],
    'Guinea':[-9.696645,9.945587],
    'Gambia':[-15.310139,13.443182],
    'Guinea Bissau':[-15.180413,11.803749],
    'Equatorial Guinea':[10.267895,1.650801],
    'Greece':[21.824312,39.074208],
    'Greenland':[-42.604303,71.706936],
    'Guatemala':[-90.23075899999999,15.783471],
    'French Guiana':[-53.125782,3.933889],
    'Guyana':[-58.93018,4.860416],
    'Honduras':[-86.241905,15.199999],
    'Croatia':[15.2,45.1],
    'Haiti':[-72.285215,18.971187],
    'Hungary':[19.503304,47.162494],
    'Indonesia':[113.921327,-0.789275],
    'India':[78.96288,20.593684],
    'Ireland':[-8.24389,53.41291],
    'Iran':[53.688046,32.427908],
    'Iraq':[43.679291,33.223191],
    'Iceland':[-19.020835,64.963051],
    'Israel':[34.851612,31.046051],
    'Italy':[12.56738,41.87194],
    'Jamaica':[-77.297508,18.109581],
    'Jordan':[36.238414,30.585164],
    'Japan':[138.252924,36.204824],
    'Kazakhstan':[66.923684,48.019573],
    'Kenya':[37.906193,-0.023559],
    'Kyrgyzstan':[74.766098,41.20438],
    'Cambodia':[104.990963,12.565679],
    'Korea (Republic of)':[127.5101,40.3399],
    'South Korea':[127.766922,35.907757],
    'Kosovo':[20.902977,42.6026359],
    'Kuwait':[47.481766,29.31166],
    'Laos':[102.495496,19.85627],
    'Lebanon':[35.862285,33.854721],
    'Liberia':[-9.429499000000002,6.428055],
    'Libya':[17.228331,26.3351],
    'SriLanka':[80.77179699999999,7.873053999999999],
    'Lesotho':[28.233608,-29.609988],
    'Lithuania':[23.881275,55.169438],
    'Luxembourg':[6.129582999999999,49.815273],
    'Latvia':[24.603189,56.879635],
    'Morocco':[-7.092619999999999,31.791702],
    'Moldova':[28.369885,47.411631],
    'Madagascar':[46.869107,-18.766947],
    'Mexico':[-102.552784,23.634501],
    'Macedonia':[21.745275,41.608635],
    'Mali':[-3.996166,17.570692],
    'Myanmar':[95.956223,21.913965],
    'Montenegro':[19.37439,42.708678],
    'Mongolia':[103.846656,46.862496],
    'Mozambique':[35.529562,-18.665695],
    'Mauritania':[-10.940835,21.00789],
    'Malawi':[34.301525,-13.254308],
    'Malaysia':[101.975766,4.210484],
    'Namibia':[18.49041,-22.95764],
    'New Caledonia':[165.618042,-20.904305],
    'Niger':[8.081666,17.607789],
    'Nigeria':[8.675277,9.081999],
    'Nicaragua':[-85.207229,12.865416],
    'Netherlands':[5.291265999999999,52.132633],
    'Norway':[8.468945999999999,60.47202399999999],
    'Nepal':[84.12400799999999,28.394857],
    'New Zealand':[174.885971,-40.900557],
    'Oman':[55.923255,21.512583],
    'Pakistan':[69.34511599999999,30.375321],
    'Panama':[-80.782127,8.537981],
    'Peru':[-75.015152,-9.189967],
    'Philippines':[121.774017,12.879721],
    'Papua New Guinea':[143.95555,-6.314992999999999],
    'Poland':[19.145136,51.919438],
    'PuertoRico':[-66.590149,18.220833],
    'Korea (Republic of)':[127.510093,40.339852],
    'Portugal':[-8.224454,39.39987199999999],
    'Paraguay':[-58.443832,-23.442503],
    'Qatar':[51.183884,25.354826],
    'Romania':[24.96676,45.943161],
    'Russian Federation':[105.318756,61.52401],
    'Rwanda':[29.873888,-1.940278],
    'Western Sahara':[-12.885834,24.215527],
    'Saudi Arabia':[45.079162,23.885942],
    'Sudan':[30.217636,12.862807],
    'South Sudan':[31.3069788,6.876991899999999],
    'Senegal':[-14.452362,14.497401],
    'Solomon Islands':[160.156194,-9.64571],
    'Sierra Leone':[-11.779889,8.460555],
    'El Salvador':[-88.89653,13.794185],
    'Somaliland':[46.8252838,9.411743399999999],
    'Somalia':[46.199616,5.152149],
    'Republic of Serbia':[21.005859,44.016521],
    'Suriname':[-56.027783,3.919305],
    'Slovakia':[19.699024,48.669026],
    'Slovenia':[14.995463,46.151241],
    'Sweden':[18.643501,60.12816100000001],
    'Swaziland':[31.465866,-26.522503],
    'Syria':[38.996815,34.80207499999999],
    'Chad':[18.732207,15.454166],
    'Togo':[0.824782,8.619543],
    'Thailand':[100.992541,15.870032],
    'Tajikistan':[71.276093,38.861034],
    'Turkmenistan':[59.556278,38.969719],
    'EastTimor':[125.727539,-8.874217],
    'Trinidad andTobago':[-61.222503,10.691803],
    'Tunisia':[9.537499,33.886917],
    'Turkey':[35.243322,38.963745],
    'United Republic of Tanzania':[34.888822,-6.369028],
    'Uganda':[32.290275,1.373333],
    'Ukraine':[31.16558,48.379433],
    'Uruguay':[-55.765835,-32.522779],
    'United States of America':[-95.712891,37.09024],
    'Uzbekistan':[64.585262,41.377491],
    'Venezuela':[-66.58973,6.42375],
    'Vietnam':[108.277199,14.058324],
    'Vanuatu':[166.959158,-15.376706],
    'WestBank':[35.3027226,31.9465703],
    'Yemen':[48.516388,15.552727],
    'SouthAfrica':[22.937506,-30.559482],
    'Zambia':[27.849332,-13.133897],
    'Zimbabwe':[29.154857,-19.015438],

    "Alabama":[-87.359296,35.00118],
	"Alaska":[-131.602021,55.117982],
	"Arizona":[-109.042503,37.000263],
	"Arkansas":[-94.473842,36.501861],
	"California":[-123.233256,42.006186],
	"Colorado":[-107.919731,41.003906],
	"Connecticut":[-73.053528,42.039048],
	"Delaware":[-75.414089,39.804456],
	"District of Columbia":[-77.035264,38.993869],
	"Florida":[-85.497137,30.997536],
	"Georgia":[-83.109191,35.00118],
	"Hawaii":[-155.634835,18.948267],
	"Idaho":[-116.04751,49.000239],
	"Illinois":[-90.639984,42.510065],
	"Indiana":[-85.990061,41.759724],
	"Iowa":[-91.368417,43.501391],
	"Kansas":[-101.90605,40.001626],
	"Kentucky":[-83.903347,38.769315],
	"Louisiana":[-93.608485,33.018527],
	"Maine":[-70.703921,43.057759],
	"Maryland":[-75.994645,37.95325],
	"Massachusetts":[-70.917521,42.887974],
	"Michigan":[-83.454238,41.73233],
	"Minnesota":[-92.014696,46.705401],
	"Mississippi":[-88.471115,34.995703],
	"Missouri":[-91.833957,40.609566],
	"Montana":[-104.047534,49.000239],
	"Nebraska":[-103.324578,43.002989],
	"Nevada":[-117.027882,42.000709],
	"New Hampshire":[-71.08183,45.303304],
	"New Jersey":[-74.236547,41.14083],
	"New Mexico":[-107.421329,37.000263],
	"New York":[-73.343806,45.013027],
	"North Carolina":[-80.978661,36.56210],
	"North Dakota":[-97.228743,49.000239],
	"Ohio":[-80.518598,41.978802],
	"Oklahoma":[-100.087706,37.000263],
	"Oregon":[-123.211348,46.174138],
	"Pennsylvania":[-79.76278,42.252649],
	"Rhode Island":[-71.196845,41.6],
	"South Carolina":[-82.764143,35.06690],
	"South Dakota":[-104.047534,45.944106],
	"Tennessee":[-88.054868,36.496384],
	"Texas":[-101.812942,36.501861],
	"Utah":[-112.164359,41.995232],
	"Vermont":[-71.503554,45.013027],
	"Virginia":[-75.397659,38.01349],
	"Washington":[-117.033359,49.00],
	"West Virginia":[-80.518598,40.636951],
	"Wisconsin":[-90.415429,46.568478],
	"Wyoming":[-109.080842,45.002073],
	"Puerto Rico":[-66.448338,17.984326]
    }

########## Send data to main map ##########
batch = 0
@app.route('/query',methods=['GET'])
def query_data():
    ldict = {'name': 'Australia','type': 'lines',
       'effect': {'show': 'true', 'trailLength': 0.1,'symbol': 'arrow','symbolSize': 6},
       'lineStyle': {'normal': {'color': '#FFFFCC','width': 1,'opacity': 0.35,'curveness': 0.2}}}
    fdict = {'name': 'Australia','type': 'effectScatter','coordinateSystem': 'geo','zlevel': 2,
        'rippleEffect': {'period': 6,'scale': 6, 'brushType': 'stroke'},
        'symbolSize': 10,'itemStyle': {'normal': {'color': '#FFFFCC','opacity':0.7}}}
    tdict = {'name': 'New York','type': 'scatter','coordinateSystem': 'geo','zlevel': 3,'symbolSize': 5,
        'data': [{'name': 'New York','value': [-73.343806, 45.013027]}]}    

    global batch
    df_raw = pd.read_csv("d.csv")[["country","state","req_count"]]
    llist = []
    flist = []
    size = []
    df = pd.DataFrame(fetchdata("replace your query here"))
    for i in range(len(df)):
        try:
            if df["country"][i]=='United States of America':
                name = df["state"][i]
            else:
                name = df["country"][i]
            geoCoord = scatterGeo[name]
            llist.append({'fromName': name,'toName':'New York','coords':[geoCoord,[-73.343806, 45.013027]]})
            flist.append({'name': name,'value':geoCoord})
            size.append(df.iloc[i,2])
        except:
            llist.append({'fromName': 'United States of America','toName':'New York','coords':[[-95.712891,37.09024],[-73.343806, 45.013027]]})
    ldict.update({'data':llist})
    fdict.update({'data':flist})
    fdict.update({'symbolSize':np.median(size)*2})
    batch = batch + 10
    if batch >= len(df_raw)-10:
        batch = 0
    return jsonify({'data':[ldict,fdict,tdict]})

########## Send data to ip scroll bar ##########
patch = 0
@app.route('/ip',methods=['GET'])
def show_ip():
    global patch
    df_raw = pd.DataFrame(fetchdata("replace your queries here"))
    df = df_raw.iloc[patch:patch+10,:]
    name1 = []
    name2 = []
    value1 = []
    value2 = []
    for i in range(5):
        name1.append(df.iloc[i,0])
        value1.append(float(df.iloc[i,1]))
    for i in range(5,10):
        name2.append(df.iloc[i,0])
        value2.append(float(df.iloc[i,1]))
    patch = patch + 10
    return jsonify({'name1':name1,'name2':name2,'value1':value1,'value2':value2})


####### Send data to history map ##########
# @app.route('/acc',methods=['GET'])
# def query_acc_data():
#     data = [{"name":"Australia","value":1997},
#         {"name":"China","value":907},
#         {"name":"Korea (Republic of)","value":368},
#         {"name":"United Kingdom of Great Britain and Northern Ireland","value":314},
#         {"name":"Germany","value":266},
#         {"name":"Japan","value":222},
#         {"name":"Ireland","value":209},
#         {"name":"Canada","value":170},
#         {"name":"India","value":94},
#         {"name":"France","value":78},
#         {"name":"New Zealand","value":73},
#         {"name":"Netherlands","value":61},
#         {"name":"Poland","value":42},
#         {"name":"Bulgaria","value":40},
#         {"name":"Russian Federation","value":12},
#         {"name":"Ukraine","value":10},
#         {"name":"Slovakia","value":8},
#         {"name":"Egypt","value":4},
#         {"name":"Romania","value":4},
#         {"name":"Hong Kong","value":3},
#         {"name":"Pakistan","value":3},
#         {"name":"Singapore","value":3},
#         {"name":"Arizona","value":1933},
#         {"name":"New York","value":1240},
#         {"name":"New Jersey","value":845},
#         {"name":"Virginia","value":829},
#         {"name":"California","value":376},
#         {"name":"Connecticut","value":351},
#         {"name":"Pennsylvania","value":269},
#         {"name":"Minnesota","value":161},
#         {"name":"Kentucky","value":146},
#         {"name":"Illinois","value":120},
#         {"name":"Washington","value":95},
#         {"name":"North Carolina","value":79},
#         {"name":"Florida","value":57},
#         {"name":"Oregon","value":48},
#         {"name":"Iowa","value":29},
#         {"name":"Texas","value":22},
#         {"name":"Colorado","value":13},
#         {"name":"South Dakota","value":6},
#         {"name":"Louisiana","value":5},
#         {"name":"Missouri","value":4},
#         {"name":"Georgia","value":4},
#         {"name":"District of Columbia","value":4},
#         {"name":"Idaho","value":3},
#         {"name":"Massachusetts","value":2},
#         {"name":"Ohio","value":2},
#         {"name":"Utah","value":2},
#         {"name":"West Virginia","value":1}]
#     res = []
#     for i in data:
#         name = i['name']
#         value = i['value']
#         try:
#             geoCoord = scatterGeo[name]
#             geoCoord.append(float(value))
#             res.append({'name': name,'value':geoCoord})
#         except:
#             res.append({'name': 'United States of America','value':[-73.343806, 45.013027, value]})
#     return jsonify({'data':res})


@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    import click
    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        # Flask-login configuration
        app.secret_key = 'heartbeat'
        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=True, threaded=threaded)
    run()