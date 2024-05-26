from flask import Flask, request, jsonify
import sqlite3 as sq
from marshmallow import ValidationError
import datetime

from Models.AddPoints import AddPoints
from Models.Card import Card
from Utils.validate import validate

app = Flask(__name__)

def get_db():
    conn = sq.connect('CarteFedelta.sqlite3')
    conn.row_factory = sq.Row
    return conn

@app.route("/")
def hello():
    return 'Hello world!'

@app.route("/card", methods = ['POST'])
def add_card():
    try:
        result = validate(request.json, Card())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    conn = get_db()
    cur = conn.cursor()

    try:
        saldoPunti = result["SaldoPunti"]   
    except:
        saldoPunti = '0'
    
    cur.execute("INSERT INTO TCarteFedelta (Titolare, SaldoPunti) VALUES (?, ?)", (result["Titolare"], saldoPunti))
    conn.commit()
    return jsonify(result)

@app.route("/add_points", methods = ['POST'])
def add_points():
    try:
        result = validate(request.json, AddPoints())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM TCarteFedelta WHERE CartaFedeltaID = ?", [str(result["CartaFedeltaID"])])
    cartaFedelta = cur.fetchone()

    if not cartaFedelta:
        return jsonify({'message': "Card not found"}), 404

    dataNow = datetime.datetime.now()
    cur.execute("INSERT INTO TMovimenti (CartaFedeltaID, DataMovimento, TipoMovimento, Punti) VALUES (?, ?, ?, ?)", [str(result["CartaFedeltaID"]), dataNow, '1', str(result["SaldoPunti"])])
    conn.commit()

    cur.execute("UPDATE TCarteFedelta SET SaldoPunti = ? WHERE CartaFedeltaID = ?", [str(cartaFedelta['SaldoPunti'] + result["SaldoPunti"]), str(result["CartaFedeltaID"])])
    conn.commit()
    
    return 'success', 200