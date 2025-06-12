import batteryopt
import pandas as pd
from pyomo.environ import ConcreteModel, Constraint
from pyomo.opt import SolverFactory
from pyomo.contrib.solver.solvers import gurobi_direct

def main():
    model = ConcreteModel()

    # Define model parameters
    model = batteryopt.battery_operation_params(model)
    model = batteryopt.market_price_params(model)
    model = batteryopt.charge_discharge_price_thresholds(model)

    # Input: battery parameters
    battery_parameters = pd.read_csv('./data/battery_parameters.csv', index_col = 'parameter')
    model.storage_capacity = battery_parameters.loc['storage_capacity', 'value']
    model.power_rating = battery_parameters.loc['power_rating', 'value']
    model.charging_eff = battery_parameters.loc['charging_eff', 'value']
    model.discharging_eff = battery_parameters.loc['discharging_eff', 'value']
    model.initial_soc = battery_parameters.loc['initial_soc', 'value']

    # Input: market price
    market_prices = pd.read_csv('./data/market_prices.csv', index_col = 'time')
    for t in market_prices.index:
        model.charge_price[t] = market_prices.loc[t, 'm1']
        model.discharge_price[t] = market_prices.loc[t, 'm1']

    # Input: charge max price and discharge min price thresholds
    price_thresholds = pd.read_csv('./data/price_thresholds.csv', index_col = 'parameter')
    model.ch_max_threshold = price_thresholds.loc['ch_max_threshold', 'price']
    model.disch_min_threshold = price_thresholds.loc['disch_min_threshold', 'price']

    # Define model decision variables
    model = batteryopt.define_charging_variables(model)
    model = batteryopt.define_discharging_variables(model)
    model = batteryopt.define_soc_variable(model)

    # Discharge price constraint
    model.discharge_trigger = Constraint(model.T, rule=batteryopt.disch_price_trigger_rule)
    model.discharge_control = Constraint(model.T, rule=batteryopt.disch_control_rule)
    # Charge price constraint
    model.charge_trigger = Constraint(model.T, rule=batteryopt.charge_price_trigger_rule)
    model.charge_control = Constraint(model.T, rule=batteryopt.charge_control_rule)
    # SOC constraint
    model.soc_con = Constraint(model.T, rule=batteryopt.soc_rule)
    # Market constraint
    model.market_con = Constraint(model.T, rule=batteryopt.markets_constraint_rule)
   # Charging energy bounds
    model.charge_lower_energy = Constraint(model.T, rule = batteryopt.charge_energy_lower_rule)
    model.charge_upper_energy = Constraint(model.T, rule = batteryopt.charge_energy_upper_rule)
   # Discharging energy bounds
    model.discharge_lower_energy = Constraint(model.T, rule = batteryopt.discharge_energy_lower_rule)
    model.discharge_upper_energy = Constraint(model.T, rule = batteryopt.discharge_energy_upper_rule)

    # Model Objective
    model = batteryopt.maximize_revenue(model)

    # Solve using Gurobi direct
    solver = SolverFactory('gurobi_direct')
    solver_results = solver.solve(model, tee=False)

    return model, solver_results

if __name__ == "__main__":
    main()