from pyomo.environ import Objective, maximize

def maximize_revenue(model):
    """
    Define the objective function to maximize total revenue from battery operations over the time horizon.

    Revenue is earned by discharging energy at market prices and reduced by charging costs.

    Objective:
        Maximize ∑ [ (discharge_price[t] × disch_state[t] × discharge_energy[t])
                    - (charge_price[t] × ch_state[t] × charge_energy[t]) ]
    
    Args:
        model: Pyomo ConcreteModel object with defined time set and relevant variables.
    
    Returns:
        model: Pyomo model with an attached objective function.
    """

    model.obj = Objective(
        expr = sum(
            model.discharge_price[t] * model.disch_state[t] * model.discharge_energy[t] -
            model.charge_price[t]   * model.ch_state[t]     * model.charge_energy[t]
            for t in model.T
        ),
        sense = maximize
    )
    
    return model
