DEFAULT_Z_YEARS = 10
DEFAULT_X_YEARS = 20
DEFAULT_Y_YEARS = 2

def is_mosca_urgent(x_data_lifetime_years: float, y_migration_time_years: float, z_years_to_crqc: float = DEFAULT_Z_YEARS) -> bool:
    return (x_data_lifetime_years + y_migration_time_years) > z_years_to_crqc

def get_default_x_years(asset_type: str, business_criticality: str) -> float:
    if business_criticality == "critical":
        return 20.0
    elif business_criticality == "high":
        return 10.0
    elif business_criticality == "medium":
        return 5.0
    return 1.0