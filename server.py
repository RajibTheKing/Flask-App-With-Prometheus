import random
import os
from flask import Flask, request, Response
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import prometheus_client

app = Flask(__name__)
CORS(app)
resources = {r"/api/*": {"origins": "*"}}
app.config["CORS_HEADERS"] = "Content-Type"
app.config['JSON_SORT_KEYS'] = False

#metrics = PrometheusMetrics(app)
head_counter = prometheus_client.Counter("head_count", "This is used to count flip coins for heads")
tail_counter = prometheus_client.Counter("tail_count", "This is used to count flip coins for tails")
build_info = prometheus_client.Gauge('build_info', 'Build information', ['branch', 'goversion', 'revision', 'version'])
build_info.labels('HEAD', 'go1.6.2', '16d70a8b6bd90f0ff793813405e84d5724a9ba65', '1.0.1').set(1)

file_creation_date = prometheus_client.Gauge('file_creation_date', 'File creation date', ['snapshot', 'FOREX_file_Forex_1', 'FOREX_file_Forex_2', 'FOREX_file_Forex_3'])
file_creation_date.labels("2023-10-17:12.14.17", "2023-10-17:12.14.17", "2023-10-16:18.17.20", "2023-10-15:18.17.15").set(1)

file_creation_date2 = prometheus_client.Gauge('file_creation_date2', 'File creation date 2', ['value'])
file_creation_date2.labels("{snapshot.dat,2023-10-17.12.14.17 FOREX-file-Forex-1,2023-10-17.12.14.17 FOREX-file-Forex-2,2023-10-16.18.17.20 FOREX-file-Forex-3,2023-10-15.18.17.15}").set(1)

file_creation_date3 = prometheus_client.Gauge('file_creation_date3', 'File creation date 3', ['value'])
file_creation_date3.labels("{snapshot(2023-10-17.12.14.17), Forex-1(2023-10-17.12.14.17), Forex-2(2023-10-16.18.17.20), Forex-3(2023-10-15.18.17.15)}").set(1)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/flip_coins/')
def flip_coins():
    print('Inside flip_coins: args = ', request.args)
    times = request.args.get('times', default = 100, type = int)
    heads = 0
    tails = 0
    for i in range(0, times):
        if random.randint(0,1):
            heads += 1
            head_counter.inc()
        else:
            tails += 1
            tail_counter.inc()
    
    tails = times - heads

    return {
        "heads": heads,
        "tails": tails
    }

@app.route('/metrics')
def metrics():
    res = prometheus_client.generate_latest()
    return Response(res, mimetype="text/plain")
    # return "{key = \"file_creation_date\", value=\"snapshot.dat(2023-10-17:12.14.17), FOREX-file-Forex-1(2023-10-17:12.14.17), FOREX-file-Forex-2(2023-10-16:18.17.20), FOREX-file-Forex-3(2023-10-15:18.17.15)\"}"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
