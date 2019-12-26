import numpy as np
from scipy.optimize import fsolve
import sys
from flask import Flask, jsonify, request

app = Flask(__name__)


def f(x, constants):
    solid, totalWater, conMoist2, oustu, uustu = constants
    return ((solid-x[0])*((100-((100*(solid-x[0])))/(totalWater-conMoist2*x[0]))/(((100*(solid-x[0]))/(totalWater-conMoist2*x[0])))))-oustu*x[1]-((solid-x[0]-x[1])*(uustu))


def vf(x, *constants):
    return [f(x, constants), f(x, constants)]


@app.route('/03c91e2d0e8b5f4ad25c3f254eb37135/', methods=['GET'])
def calculate():
    
    solid = request.args.get('solid', None)
    moist = request.args.get('moist', None)
    water = request.args.get('water', None)
    moist2 = request.args.get('moist2', None)
    oustu = request.args.get('oustu', None)
    uustu = request.args.get('uustu', None)

    if not solid or not moist or not water or not moist2 or not oustu or not uustu:
        return jsonify({'status': 'error'})

    solid = float(solid)
    moist = float(moist)
    water = float(water)
    moist2 = float(moist2)
    oustu = float(oustu)
    uustu = float(uustu)

    totalWater = solid + moist + water
    conMoist2 = (moist2 / 100) + 1

    xx = fsolve(vf, args=(solid, totalWater, conMoist2, oustu, uustu), x0=[0, 0])
    emptyArray = []
    emptyArray.append(xx[0])
    emptyArray.append(xx[1])
    resp = jsonify({'result': emptyArray})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(host='localhost', port='6001')
