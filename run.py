# -*- coding: utf-8 -*-
import numpy as np

from flask import Flask
from flask import jsonify, request

app = Flask(__name__)

# Load
results = np.load('RecommendingResult.npy').item()

# On fait un dico avec des id numériques
iddict = {}
i=10001
for k, v in results.items():
    iddict[i] = v
    i += 1
    
@app.route('/')
def index():
    return "Hello world !"


@app.route('/recommend/<id>', methods=['GET'])
def recommend(id):
    id = id.lower()
    if id in results:
        return jsonify({"_results":results[id][:10]})

    if int(id) in iddict:
        return jsonify({"_results":iddict[int(id)][:10]})

    return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
     app.run()
