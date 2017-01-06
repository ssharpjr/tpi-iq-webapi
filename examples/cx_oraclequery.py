#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- mode: python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import os
import cx_Oracle

os.system('clear')  # PC testing
workorder_id = input("Scan Workorder Number: ")
# workorder_id = '10014085'

try:
    con = cx_Oracle.connect('iqms/iqtest@iqtest')
except Exception as e:
    print(e)
    print("Exiting")
    sys.exit()

cur = con.cursor()
sql = """
      SELECT v.eqno, a.itemno
      FROM (v_rt_workorders v LEFT OUTER JOIN standard s
            ON v.standard_id = s.id) LEFT OUTER JOIN arinvt a
      ON s.arinvt_id_mat = a.id
      WHERE v.workorder_id = '{wo_id}'
      """.format(wo_id=workorder_id)

try:
    cur.execute(sql)
except Exception as e:
    print(e)
    print("Exiting")
    sys.exit()

results = list(cur)

wc_id = results[0][0]
rm_item_no = results[0][1]

print("Workorder Number: " + workorder_id)
print("Press Number: " + wc_id)
print("Raw Material Item Number: " + rm_item_no)

cur.close()
con.close()
