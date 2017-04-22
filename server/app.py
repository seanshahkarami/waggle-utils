from flask import Flask
from flask import jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return 'here is something for you!'


@app.route('/cpu')
def cpustats():
    stats = {}

    with open('/proc/stat') as f:
        for line in f:
            if line.startswith('cpu'):
                fields = line.split()
                stats[fields[0]] = {
                    'user': int(fields[1]),
                    'nice': int(fields[2]),
                    'system': int(fields[3]),
                    'idle': int(fields[4]),
                    'iowait': int(fields[5]),
                    'softirq': int(fields[6]),
                }

    return jsonify(stats)


memunits = {
    'kB': 1024,
}


@app.route('/mem')
def memstats():
    stats = {}

    with open('/proc/meminfo') as f:
        for line in f:
            fields = line.split(':')
            key = fields[0].strip()
            rhs = fields[1].split()

            if len(rhs) == 1:
                value = int(rhs[0])
            elif len(rhs) == 2:
                try:
                    value = int(rhs[0]) * memunits[rhs[1]]
                except KeyError:
                    value = -1

            stats[key] = value

    return jsonify(stats)


@app.route('/net')
def netstats():
    return jsonify({})


@app.route('/uptime')
def uptime():
    with open('/proc/uptime') as f:
        fields = f.readline().split()
        return jsonify({
            'uptime': float(fields[0]),
            'idle': float(fields[1]),
        })
