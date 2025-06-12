# Constraint 1: Discharging is allowed only if price > threshold
def disch_price_trigger_rule(model, t): 
    """
    Big-M constraint to activate discharging only when market price exceeds the minimum discharge threshold.
    
    If discharge_price[t] > disch_min_threshold ⇒ disch_allowed[t] = 1
    Otherwise, disch_allowed[t] can be 0.
    """
    M = 1e6  # Big-M constant
    return model.discharge_price[t] - model.disch_min_threshold >= 1e-4 - M * (1 - model.disch_allowed[t])

# Constraint 2: Discharging state is conditional on permission
def disch_control_rule(model, t):
    """
    Ensure that discharging can only occur if discharging is allowed.
    disch_state[t] ≤ disch_allowed[t]
    """
    return model.disch_state[t] <= model.disch_allowed[t]

# Constraint 3: Charging is allowed only if price < threshold
def charge_price_trigger_rule(model, t):
    """
    Big-M constraint to activate charging only when market price is below the max charge threshold.
    
    If charge_price[t] < ch_max_threshold ⇒ ch_allowed[t] = 1
    Otherwise, ch_allowed[t] can be 0.
    """
    M = 1e6
    return model.charge_price[t] - model.ch_max_threshold <= M * (1 - model.ch_allowed[t])

# Constraint 4: Charging state is conditional on permission
def charge_control_rule(model, t):
    """
    Ensure that charging can only occur if charging is allowed.
    ch_state[t] ≤ ch_allowed[t]
    """
    return model.ch_state[t] <= model.ch_allowed[t] 

# Constraint 5: Battery state of charge (SoC) dynamics
def soc_rule(model, t):
    """
    Track the battery's state of charge over time based on charging and discharging activity.

    soc[t] = soc[t-1] + (charged energy) - (discharged energy)
    At t=1, use initial state of charge instead of soc[t-1].
    """
    if t == 1:  # Initial state of charge
        return model.soc[t] == model.initial_soc + model.ch_state[t]*model.charge_energy[t] - model.disch_state[t]*model.discharge_energy[t]
    else:
        return model.soc[t] == model.soc[t-1] + model.ch_state[t]*model.charge_energy[t] - model.disch_state[t]*model.discharge_energy[t]

# Constraint 6: Battery cannot charge and discharge at the same time
def markets_constraint_rule(model, t):
    """
    Rule: Prevent simultaneous charging and discharging in the same hour.
    Ensures: ch_state[t] + disch_state[t] ≤ 1
    """
    return model.ch_state[t] + model.disch_state[t] <= 1

def charge_energy_lower_rule(model, t):
    """
    Enforce the minimum charging energy when charging is active.
    
    Ensures that:
    - When charging state (ch_state[t]) is 1, charge_energy[t] is at least epsilon (small positive value).
    - When ch_state[t] is 0, charge_energy[t] is forced to 0.
    
    Args:
        model: Pyomo model instance.
        t: Time index.
        
    Returns:
        Constraint expression for lower bound of charge energy at time t.
    """
    epsilon = 1e-4
    return model.charge_energy[t] >= epsilon * model.ch_state[t]

def charge_energy_upper_rule(model, t):
    """
    Enforce the maximum charging energy based on power rating and charging efficiency.
    
    Ensures that charge_energy[t] does not exceed:
    (power_rating / charging_efficiency) * ch_state[t]
    
    Args:
        model: Pyomo model instance.
        t: Time index.
        
    Returns:
        Constraint expression for upper bound of charge energy at time t.
    """
    return model.charge_energy[t] <= (model.power_rating / model.charging_eff) * model.ch_state[t]

def discharge_energy_lower_rule(model, t):
    """
    Enforce the minimum discharging energy when discharging is active.
    
    Ensures that:
    - When discharging state (disch_state[t]) is 1, discharge_energy[t] is at least epsilon.
    - When disch_state[t] is 0, discharge_energy[t] is 0.
    
    Args:
        model: Pyomo model instance.
        t: Time index.
        
    Returns:
        Constraint expression for lower bound of discharge energy at time t.
    """
    epsilon = 1e-4
    return model.discharge_energy[t] >= epsilon * model.disch_state[t]

def discharge_energy_upper_rule(model, t):
    """
    Enforce the maximum discharging energy based on power rating and discharging efficiency.
    
    Ensures that discharge_energy[t] does not exceed:
    (power_rating * discharging_efficiency) * disch_state[t]
    
    Args:
        model: Pyomo model instance.
        t: Time index.
        
    Returns:
        Constraint expression for upper bound of discharge energy at time t.
    """
    return model.discharge_energy[t] <= (model.power_rating * model.discharging_eff) * model.disch_state[t]


