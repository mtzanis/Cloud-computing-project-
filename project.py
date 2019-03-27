from flask import Flask, render_template, request, jsonify
import json
import requests
from pprint import pprint
from functools import wraps
from flask import Response
from cassandra.cluster import Cluster


def check_auth(username, password):
    return username == 'mtzanis' and password == 'Upur2eh7er'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


cluster = Cluster(['35.234.140.169'],port=9042)
session = cluster.connect('database')

app = Flask(__name__)

@app.route("/")
@requires_auth
def index():
    return render_template("project.html")

response = 'https://api.airvisual.com/v2/city?city={CITY}&state={STATE}&country={COUNTRY}&key=Mip7589CqMSA8xFcL'


@app.route('/words', methods=['GET' , 'POST'])
def city():

    city = request.form.get("CITY")
    country = request.form.get("COUNTRY")
    state = request.args.get("STATE")

    rows = session.execute("""select state from stats where city= '{}' ALLOW FILTERING""".format(city))

    for database in rows:
        data = database.state

    city_url= response.format(CITY = city,STATE=data,COUNTRY= country)

    resp =requests.get(city_url)
    if resp.ok:
            showinfo = resp.json()
    else:
            print(resp.reason)

    return jsonify(showinfo)

if __name__ == "__main__":
    app.run(debug = True,port=8080)

