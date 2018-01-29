import numpy as np
import random
from flask import Flask
from flask import jsonify, request

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']


# Load
#results = np.load('RecommendingResult.npy').item()
results = np.load(app.config['ENGINE_DATABASE']).item()
#results = sorted(results)

NBRECOMMEND = 3
NOTFOUND = "not_found"

# On fait un dico avec des id numériques
i0 = 100001
i = i0
iddict = {}
for k, v in results.items():
    iddict[i] = v
    i += 1

dic_name_id = {}
i = i0
for k, v in results.items():
    dic_name_id[k] = i
    i += 1
       

imax = i-1

def getid(name):
    name = name.lower()
    return dic_name_id[name]
    
def getname(id):
    for k, v in dic_name_id.items():
        if v == id:
            return k
    return NOTFOUND
   
@app.route('/')
def index():
    accueil = '<h1 align="center">Moteur de recommandation de films</h1>'
    accueil += "<h2 style=""margin-top:50"">Ajoutez /recommend/nom_du_film ou /recommend/id à l'adresse actuelle pour une recommandation de film</h2>"
    accueil += "<h3>Les id des films vont de " + str(i0) + " à " + str(imax) + "</h3>"
    return accueil

@app.route('/recommend/<id>', methods=['GET'])
def recommend(id):
    id = id.lower()
    if id in results:
        #return jsonify({"_results":results[id][:NBRECOMMEND]})
        return jsonify(formatresult(results, id))

    try:
        if int(id) in iddict:
            name = getname(int(id))
            if name == NOTFOUND:
                return not_found()
            #return jsonify({"_results":iddict[int(id)][:NBRECOMMEND]})
            return jsonify(formatresult(results, name))
    except:
        return not_found()
    return not_found()

def formatresult(tbl, name):
    # On prends 5 au hasard parmi les 10 plus proches
    rnd = random.sample(tbl[name], 5)
    t = []
    for row in rnd:
        d = {}
        d["id"] = str(getid(row[1]))
        d["name"] = row[1]
        #d["score"] = row[0]
        t.append(d)

    ret = {"_results":t}
    return ret


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
