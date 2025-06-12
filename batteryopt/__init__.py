'''
batteryopt optimizes battery dispatches over power markets.
'''
from batteryopt.parameters import (battery_operation_params, market_price_params, charge_discharge_price_thresholds)
from batteryopt.variables import define_charging_variables, define_discharging_variables, define_soc_variable
from batteryopt.constraints import (disch_control_rule, disch_price_trigger_rule, 
                                    charge_control_rule, charge_price_trigger_rule,
                                    soc_rule, markets_constraint_rule, 
                                    charge_energy_lower_rule, charge_energy_upper_rule,
                                    discharge_energy_lower_rule, discharge_energy_upper_rule)
from batteryopt.objective import maximize_revenue

__all__ = [battery_operation_params, market_price_params, charge_discharge_price_thresholds,
        define_charging_variables, define_discharging_variables, define_soc_variable,
        disch_control_rule, disch_price_trigger_rule, 
        charge_control_rule, charge_price_trigger_rule,
        soc_rule, markets_constraint_rule, 
        charge_energy_lower_rule, charge_energy_upper_rule,
        discharge_energy_lower_rule, discharge_energy_upper_rule,
        maximize_revenue]


# charge_energy = model.charge_energy
# discharge_energy = model.discharge_energy
# ch_state = model.ch_state
# disch_state = model.disch_state
# soc = model.soc
# model.discharge_trigger = pyo.Constraint(model.T, rule=disch_price_trigger_rule)
# model.discharge_control = pyo.Constraint(model.T, rule=disch_control_rule)
# model.charge_trigger = pyo.Constraint(model.T, rule=charge_price_trigger_rule)
# model.charge_control = pyo.Constraint(model.T, rule=charge_control_rule)
# model.soc_con = pyo.Constraint(model.T, rule=soc_rule)
# model.operation_mode = pyo.Constraint(model.T, rule = operation_mode_constraint)


