import pickle
from flask import Flask, json, request, jsonify
import sqlite3 as sq
from marshmallow import ValidationError
import datetime

from Models.AddPoints import AddPoints
from Models.AwardRedemption import AwardRedemption
from Models.Card import Card
from Models.GetMovements import GetMovements
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
    
    return jsonify({"message": "Success"}), 201

@app.route("/award_redemption", methods = ['POST'])
def award_redemption():
    try:
        result = validate(request.json, AwardRedemption())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM TCarteFedelta WHERE CartaFedeltaID = ?", [str(result["CartaFedeltaID"])])
    cartaFedelta = cur.fetchone()

    cur.execute("SELECT * FROM TPremi WHERE PremioID = ?", [str(result["PremioID"])])
    premio = cur.fetchone()

    if not cartaFedelta or not premio:
        return jsonify({'message': "Card or award not found"}), 404
    
    if cartaFedelta['SaldoPunti'] - premio["PuntiMinimi"] < 0:
        return jsonify({"message": "Negative balance"}), 401

    dataNow = datetime.datetime.now()
    cur.execute("INSERT INTO TMovimenti (CartaFedeltaID, DataMovimento, TipoMovimento, PremioID, Punti) VALUES (?, ?, ?, ?, ?)", [str(result["CartaFedeltaID"]), dataNow, '2', str(result["PremioID"]), str(premio["PuntiMinimi"])])
    conn.commit()

    cur.execute("UPDATE TCarteFedelta SET SaldoPunti = ? WHERE CartaFedeltaID = ?", [str(cartaFedelta['SaldoPunti'] - premio["PuntiMinimi"]), str(result["CartaFedeltaID"])])
    conn.commit()
    
    return jsonify({"message": "Success"}), 201

@app.route("/movements", methods = ['get'])
def get_movements():
    try:
        result = validate(request.args, GetMovements())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM TCarteFedelta WHERE CartaFedeltaID = ?", [str(result["CartaFedeltaID"])])
    cartaFedelta = cur.fetchone()

    if not cartaFedelta:
        return jsonify({'message': "Card not found"}), 404

    try:
        cur.execute("SELECT * FROM TCarteFedelta INNER JOIN TMovimenti ON TCarteFedelta.CartaFedeltaID = TMovimenti.CartaFedeltaID INNER JOIN TPremi ON TMovimenti.PremioID = TPremi.PremioID WHERE TCarteFedelta.CartaFedeltaID = ? AND TMovimenti.DataMovimento >= ? AND TMovimenti.DataMovimento <= ? ORDER BY DataMovimento DESC LIMIT ?", [str(result["CartaFedeltaID"]), str(result["DataMin"]), str(result["DataMax"]), str(result["Limit"])])
    except:
        cur.execute("SELECT * FROM TCarteFedelta INNER JOIN TMovimenti ON TCarteFedelta.CartaFedeltaID = TMovimenti.CartaFedeltaID INNER JOIN TPremi ON TMovimenti.PremioID = TPremi.PremioID WHERE TCarteFedelta.CartaFedeltaID = ? AND TMovimenti.DataMovimento >= ? AND TMovimenti.DataMovimento <= ? ORDER BY DataMovimento DESC", [str(result["CartaFedeltaID"]), str(result["DataMin"]), str(result["DataMax"])])

    response = cur.fetchall()

    myjson = []

    for r in response:
        myjson.append({
            "CartaFedeltaID": r[0],
            "Titolare": r[1],
            "MovimentoID": r[3],
            "DataMovimento": r[5],
            "TipoMovimento": r[9],
            "Premio": r[10],
            "Punti": r[11]
        })

    return myjson, 200    