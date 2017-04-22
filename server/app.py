from flask import Flask
from flask import jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return 'here is something for you!'


@app.route('/cpu')
def cpustats():
    return jsonify({})


memunits = {
    'kB': 1024,
}


@app.route('/mem')
def memstats():
    stats = {}

    for line in open('/proc/meminfo'):
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
