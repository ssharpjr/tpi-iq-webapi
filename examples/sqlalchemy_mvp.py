#!/usr/bin/env python3
# -*- coding utf-8 -*-
# -*- mode: python -*-

from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.oracle import NUMBER, CHAR


engine = create_engine('oracle://iqms:iqtest@iqtest',
                       echo=False
                       )

Base = declarative_base(engine)


class Arinvt(Base):
    __tablename__ = 'arinvt'

    id = Column(NUMBER, primary_key=True)
    itemno = Column(CHAR)


class V_RT_Workorders(Base):
    __tablename__ = 'v_rt_workorders'

    workorder_id = Column(NUMBER, primary_key=True)
    standard_id = Column(NUMBER, ForeignKey('standard.id'))
    eqno = Column(CHAR)


class Standard(Base):
    __tablename__ = 'standard'

    id = Column(NUMBER, primary_key=True)
    arinvt_id_mat = Column(NUMBER, ForeignKey('arinvt.id'))


def loadSession():
    """"""
    # metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    session = loadSession()
    wo_id = '9934386'  # testing.  Will be captured later
    for eqno, itemno in session.query(V_RT_Workorders, Arinvt).\
            filter(V_RT_Workorders.standard_id == Standard.id).\
            filter(Standard.arinvt_id_mat == Arinvt.id).\
            filter(V_RT_Workorders.workorder_id == wo_id).\
            all():
        print("Press Number: " + eqno.eqno)
        print("Raw Material Item Number: " + itemno.itemno)
