#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy.dialects.oracle import CHAR, NUMBER, VARCHAR2
from config import config

app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#####################################################################


class Arinvt(db.Model):
    __tablename__ = 'arinvt'
    id = db.Column(NUMBER, primary_key=True)
    itemno = db.Column(CHAR)
    descrip = db.Column(CHAR)
    standard_id = db.Column(NUMBER, db.ForeignKey('standard.id'))


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


class Work_Center(db.Model):
    __tablename__ = 'work_center'
    id = db.Column(NUMBER, primary_key=True)
    eqno = db.Column(CHAR)


class V_Sched(db.Model):
    __tablename__ = 'v_sched'
    work_center_id = db.Column(NUMBER, primary_key=True)
    workorder_id = db.Column(NUMBER)
    standard_id = db.Column(NUMBER)


#####################################################################


@app.route('/wo/<int:wo_id>', methods=['GET'])
def work_order(wo_id):
    res = db.session.query(V_RT_Workorders, Arinvt).\
            filter(V_RT_Workorders.standard_id == Standard.id).\
            filter(Standard.arinvt_id_mat == Arinvt.id).\
            filter(V_RT_Workorders.workorder_id == wo_id).\
            first() or abort(404)

    eqno = res.V_RT_Workorders.eqno.rstrip()
    itemno = res.Arinvt.itemno.rstrip()
    return jsonify({'press': eqno,
                    'rmat': itemno})

@app.route('/press/<int:press_id>', methods=['GET'])
def press(press_id):
    res = db.session.query(V_RT_Workorders, Arinvt).\
            filter(V_RT_Workorders.standard_id == Standard.id).\
            filter(Standard.id == Arinvt.standard_id).\
            filter(V_RT_Workorders.eqno == str(press_id)).\
          first() or abort(404)
    res2 = db.session.query(V_RT_Workorders, Arinvt).\
            filter(V_RT_Workorders.standard_id == Standard.id).\
            filter(Standard.arinvt_id_mat == Arinvt.id).\
            filter(V_RT_Workorders.eqno == str(press_id)).\
          first() or abort(404)

    eqno = res.V_RT_Workorders.eqno.rstrip()
    wo_id = str(int(res.V_RT_Workorders.workorder_id))
    itemno = res.Arinvt.itemno.rstrip()
    descrip = res.Arinvt.descrip.rstrip()
    itemno_mat = res2.Arinvt.itemno.rstrip()
    descrip_mat = res2.Arinvt.descrip.rstrip()
    return jsonify({'press': eqno,
                    'wo_id': wo_id,
                    'itemno': itemno,
                    'descrip': descrip,
                    'itemno_mat': itemno_mat,
                    'descrip_mat': descrip_mat})


@app.route('/serial/<sn>', methods=['GET'])
def serial_number(sn):
    res = db.session.query(Master_Label).\
        filter(Master_Label.serial == sn).\
        first() or abort(404)
    itemno = res.itemno.rstrip()
    return jsonify({'itemno': itemno})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
