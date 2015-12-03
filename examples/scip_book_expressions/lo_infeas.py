"""
lo_infeas.py: Simple SCIP example of an infeasible linear programming:

maximize    x1 + x2
subject to  x1 - x2 <= -1
           -x1 + x2 <= -1
            x1,x2 >= 0.

Copyright (c) by Joao Pedro PEDROSO and Mikio KUBO, 2012
"""
from pyscipopt.scip import *

model = Model("lo infeas")

x1 = model.addVar(vtype="C", name="x1", obj=1)
x2 = model.addVar(vtype="C", name="x2", obj=1)

model.addConstr(x1-x2 <= -1)
model.addConstr(x2-x1 <= -1)

model.setMaximize()

model.optimize()

status = model.Status
if status == GRB.Status.OPTIMAL:
    print("Optimal value:", model.getObjVal())
    for v in model.getVars():
        print v.VarName,v.X
    exit(0)

if status == GRB.Status.UNBOUNDED or status == GRB.Status.INF_OR_UNBD:
    model.setObjective(0, GRB.MAXIMIZE)
    model.optimize()
    status = model.Status

#todo get status
if status == GRB.Status.OPTIMAL:
    print("Instance unbounded")
elif status == GRB.Status.INFEASIBLE:
    print("Infeasible instance: violated constraints are:")
    model.computeIIS()
    for c in model.getConstrs():
        if c.IISConstr:
            print(c.ConstrName)
else:
    print("Error: Solver finished with non-optimal status",status)
    from grbcodes import grbcodes
    print(grbcodes[status])