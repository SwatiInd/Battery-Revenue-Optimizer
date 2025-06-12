from pyomo.environ import Var, Binary

def define_charging_variables(model):
    """
    Define charging-related decision variables for each hour in the time set `model.T`.

    Variables:
    ----------
    model.charge_energy : Var
        Amount of energy charged in each time step (MWh), bounded by:
        0 ≤ charge_energy[t] ≤ power_rating / charging_efficiency
    model.ch_allowed : Var (Binary)
        Binary variable: 1 if charging is allowed (price < threshold), 0 otherwise
    model.ch_state : Var (Binary)
        Binary variable: 1 if the battery is charging at time t, 0 if not
    """

    # Maximum allowable charge energy (scaled by charging efficiency)
    max_charge_energy = model.power_rating / model.charging_eff
    # Charge energy variable (continuous between 0 and max)
    model.charge_energy = Var(model.T, bounds=(0, max_charge_energy))
    # Binary variable: Is charging allowed based on price threshold
    model.ch_allowed = Var(model.T, within=Binary)
    # Binary variable: Is the system actually charging
    model.ch_state = Var(model.T, within=Binary)
    
    return model

def define_discharging_variables(model):
    """
    Define discharging-related decision variables for each hour in the time set `model.T`.

    Variables:
    ----------
    model.discharge_energy : Var
        Amount of energy discharged in each time step (MWh), bounded by:
        0 ≤ discharge_energy[t] ≤ power_rating × discharging_efficiency
    model.disch_allowed : Var (Binary)
        Binary variable: 1 if discharging is allowed (price > threshold), 0 otherwise
    model.disch_state : Var (Binary)
        Binary variable: 1 if the battery is discharging at time t, 0 if not
    """

    # Maximum allowable discharge energy (scaled by discharging efficiency)
    max_discharge_energy = model.power_rating * model.discharging_eff
    # Discharge energy variable (continuous between 0 and max)
    model.discharge_energy = Var(model.T, bounds=(0, max_discharge_energy))
    # Binary variable: Is discharging allowed based on price threshold
    model.disch_allowed = Var(model.T, within=Binary)
    # Binary variable: Is the system actually discharging
    model.disch_state = Var(model.T, within=Binary)

    return model

def define_soc_variable(model):
    """
    Define the state of charge (SoC) decision variable for each time step.

    Variables:
    ----------
    model.soc : Var
        State of charge at the beginning of each time step (MWh),
        bounded by 0 and the maximum storage capacity.
        0 ≤ soc[t] ≤ storage_capacity
    """

    model.soc = Var(model.T, bounds=(0, model.storage_capacity))
    return model
