import numpy as np
from pyomo.environ import Param, RangeSet

def market_price_params(model, seed=42):
    """
    Define time set and energy market prices (charging and discharging).

    Parameters:
    -----------
    model : Pyomo model
        The model object to which the parameters are added.
    seed : int
        Random seed for reproducibility of generated price data.
    """
    # Set random seed for reproducibility
    np.random.seed(seed)

    # Time index: 24-hour range
    model.T = RangeSet(1, 24)

    # Simulated hourly market prices: between -5 and 15
    hourly_price = np.random.randint(-5, 15, size=24)

    # Price parameters (same for charge/discharge here; can be split later)
    price_dict = {t: float(hourly_price[t - 1]) for t in model.T}
    model.charge_price = Param(model.T, initialize=price_dict, mutable=True)
    model.discharge_price = Param(model.T, initialize=price_dict, mutable=True)

    return model

def battery_operation_params(model):
    """
    Define battery parameters:
    - storage capacity
    - power rating
    - efficiency for charging/discharging
    - initial state of charge
    """
    model.storage_capacity = Param(initialize=20.0, mutable=True, doc="Max energy storage (MWh)")
    model.power_rating = Param(initialize=10.0, mutable=True, doc="Max charge/discharge rate (MW)")
    model.charging_eff = Param(initialize=0.9, mutable=True, doc="Charging efficiency")
    model.discharging_eff = Param(initialize=0.9, mutable=True, doc="Discharging efficiency")
    model.initial_soc = Param(initialize=5.0, mutable=True, doc="Initial SOC (MWh)")

    return model

def charge_discharge_price_thresholds(model):
    """
    Define price thresholds:
    - max price for charging
    - min price for discharging
    """
    model.ch_max_threshold = Param(initialize=3.0, mutable=True, doc="Charge only if price < threshold")
    model.disch_min_threshold = Param(initialize=2.0, mutable=True, doc="Discharge only if price > threshold")

    return model
