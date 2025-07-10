import pyomo.environ as pyo
from pyomo.opt import SolverFactory

m = pyo.ConcreteModel()

#sets and parameters
m.setInv = pyo.Set(initialize=['A','B','C','D'])
m.Capital = 100000

#variables
m.C = pyo.Var(m.setInv, bounds=(0,None))
m.R = pyo.Var(m.setInv, bounds=(0,None))

#objective function
m.obj = pyo.Objective(expr = pyo.summation(m.R), sense=pyo.maximize)

#constraints
m.C1 = pyo.Constraint(expr = pyo.summation(m.C) == m.Capital)
m.C2 = pyo.Constraint(expr = m.R['A'] == 0.05*m.C['A'])
m.C3 = pyo.Constraint(expr = m.R['B'] == 0.10*m.C['B'])
m.C4 = pyo.Constraint(expr = m.R['C'] == 0.12*m.C['C'])
m.C5 = pyo.Constraint(expr = m.R['D'] == 1e-6*m.C['D']**2)

m.C6 = pyo.Constraint(expr = m.C['B'] <= 0.2*m.Capital)
m.C7 = pyo.Constraint(expr = m.C['C'] <= 0.1*m.Capital)
m.C8 = pyo.Constraint(expr = m.C['D'] <= 0.3*m.Capital)

#solve
opt = SolverFactory('gurobi')
m.results = opt.solve(m)

#print
m.pprint()
print('\n\nOF:',pyo.value(m.obj))