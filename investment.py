import pyomo.environ as pyo
from pyomo.opt import SolverFactory

m = pyo.ConcreteModel()

# Initialize the model
# Define the set of investments and the total capital available
m.setInv = pyo.Set(initialize=['A','B','C'])
m.Capital = 100000

# Define variables
m.C = pyo.Var(m.setInv, bounds=(0,None)) # Capital fund allocated to each investment
m.R = pyo.Var(m.setInv, bounds=(0,None)) # RoI for each investment

# Define the objective function
# Objective : Maximize the total return on investment
m.obj = pyo.Objective(expr = pyo.summation(m.R), sense=pyo.maximize)

# Define constraints
m.C1 = pyo.Constraint(expr = pyo.summation(m.C) == m.Capital) # Total capital allocated must be equal to the available capital
m.C2 = pyo.Constraint(expr = m.R['A'] == 0.05*m.C['A']) # RoI for investment A is 5% of capital allocated to A
m.C3 = pyo.Constraint(expr = m.R['B'] == 0.10*m.C['B']) # RoI for investment B is 10% of capital allocated to B
m.C4 = pyo.Constraint(expr = m.R['C'] == 0.12*m.C['C']) # RoI for investment C is 12% of capital allocated to C
m.C5 = pyo.Constraint(expr = m.C['B'] <= 0.2*m.Capital) # Capital allocated to investment B must not exceed 20% of total capital
m.C6 = pyo.Constraint(expr = m.C['C'] <= 0.1*m.Capital) # Capital allocated to investment C must not exceed 10% of total capital

# Solve the model optimization problem
opt = SolverFactory('gurobi')
m.results = opt.solve(m)

# Display the results
m.pprint()
print('\n\nOF:',pyo.value(m.obj))