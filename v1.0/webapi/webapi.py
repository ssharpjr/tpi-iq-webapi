#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.oracle import CHAR, NUMBER, VARCHAR2
from config import config

app = Flask(__name__)
app.config.from_object(config)
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


#####################################################################


class Arinvt(db.Model):
    __tablename__ = 'arinvt'
    id = db.Column(NUMBER, primary_key=True)
    itemno = db.Column(CHAR)
    descrip = db.Column(CHAR)


class V_RT_Workorders(db.Model):
    __tablename__ = 'v_rt_workorders'
    workorder_id = db.Column(NUMBER, primary_key=True)
    standard_id = db.Column(NUMBER, db.ForeignKey('standard.id'))
    eqno = db.Column(CHAR)


class Standard(db.Model):
    __tablename__ = 'standard'
    id = db.Column(NUMBER, primary_key=True)
    arinvt_id_mat = db.Column(NUMBER, db.ForeignKey('arinvt.id'))


class Master_Label(db.Model):
    __tablename__ = 'master_label'
    id = db.Column(NUMBER, primary_key=True)
    serial = db.Column(VARCHAR2)
    itemno = db.Column(CHAR)


#####################################################################


@app.route('/wo/<int:wo_id>', methods=['GET'])
def work_order(wo_id):
    res = db.session.query(V_RT_Workorders, Arinvt).\
          filter(V_RT_Workorders.standard_id == Standard.id).\
          filter(Standard.arinvt_id_mat == Arinvt.id).\
          filter(V_RT_Workorders.workorder_id == wo_id).\
          first() or abort(404)

    try:
        eqno = res.V_RT_Workorders.eqno.rstrip()
        itemno = res.Arinvt.itemno.rstrip()
        return jsonify({'press': eqno,
                        'rmat': itemno})
    except:
        return abort(404)


@app.route('/serial/<sn>', methods=['GET'])
def serial_number(sn):
    res = db.session.query(Master_Label).\
        filter(Master_Label.serial == sn).\
        first() or abort(404)
    try:
        itemno = res.itemno.rstrip()
        return jsonify({'itemno': itemno})
    except:
        return abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
