from flask import Flask
from flask import jsonify
from flask import render_template
import stats


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/loadavg')
def loadavg():
    return jsonify(stats.loadavg())


@app.route('/cpu')
def cpustats():
    return jsonify(stats.cpustats())


@app.route('/mem')
def memstats():
    return jsonify(stats.meminfo())


@app.route('/mounts')
def mounts():
    return jsonify(stats.mounts())


@app.route('/net')
def netstats():
    return jsonify({})


@app.route('/uptime')
def uptime():
    return jsonify(stats.uptime())


@app.route('/blocks')
def blocks():
    return jsonify(stats.listblocks())


@app.route('/blocks/<block>')
def blockinfo(block):
    return jsonify(stats.blockinfo(block))


@app.route('/devices')
def devices():
    return jsonify(stats.devices())
