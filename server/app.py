from flask import Flask
from flask import jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return 'here is something for you!'


@app.route('/cpu')
def cpustats():
    return jsonify({})


@app.route('/mem')
def memstats():
    stats = {}

    for line in open('/proc/meminfo'):
        fields = line.split(':')
        stats[fields[0].strip()] = fields[1].strip()

    return jsonify(stats)
