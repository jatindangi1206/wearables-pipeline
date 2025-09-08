# Clinical reference ranges and thresholds for health metrics

BP_REFERENCE = {
    "systolic": {"normal": (90, 120), "elevated": (120, 129), "hypertension_stage_1": (130, 139), "hypertension_stage_2": (140, 180)},
    "diastolic": {"normal": (60, 80), "elevated": (80, 89), "hypertension_stage_1": (80, 89), "hypertension_stage_2": (90, 120)},
}

HR_REFERENCE = {
    "resting": {"normal": (60, 100), "tachycardia": (100, 200), "bradycardia": (30, 60)}
}

SPO2_REFERENCE = {
    "normal": (95, 100),
    "mild_hypoxemia": (90, 94),
    "severe_hypoxemia": (0, 89)
}

TEMPERATURE_REFERENCE = {
    "normal": (36.1, 37.2),
    "fever": (37.3, 39.0),
    "hypothermia": (0, 36.0)
}

SLEEP_STAGE_REFERENCE = {
    "deep": (13, 23),  # % of total sleep time
    "rem": (20, 25),
    "light": (50, 60)
}

STEPS_REFERENCE = {
    "sedentary": (0, 4999),
    "low_active": (5000, 7499),
    "somewhat_active": (7500, 9999),
    "active": (10000, 12499),
    "highly_active": (12500, 50000)
}

# FEV1 and FEV1/FVC reference values by age/gender (simplified, real values are more granular)
LUNG_FUNCTION_REFERENCE = {
    "male": {
        "fev1": { "18-25": (4.0, 5.5), "26-35": (3.8, 5.2), "36-45": (3.5, 4.8), "46-55": (3.2, 4.5), "56-65": (2.8, 4.0), "66-80": (2.2, 3.5) },
        "fev1_fvc": (0.75, 0.85)
    },
    "female": {
        "fev1": { "18-25": (3.2, 4.3), "26-35": (3.0, 4.0), "36-45": (2.7, 3.8), "46-55": (2.4, 3.5), "56-65": (2.1, 3.0), "66-80": (1.7, 2.7) },
        "fev1_fvc": (0.75, 0.85)
    }
}

def get_fev1_range(age: int, gender: str):
    """Return FEV1 reference range for given age and gender."""
    ref = LUNG_FUNCTION_REFERENCE.get(gender.lower())
    if not ref:
        return None
    for age_range, vals in ref["fev1"].items():
        min_age, max_age = map(int, age_range.split('-'))
        if min_age <= age <= max_age:
            return vals
    return None

def get_fev1_fvc_range(gender: str):
    ref = LUNG_FUNCTION_REFERENCE.get(gender.lower())
    if not ref:
        return None
    return ref["fev1_fvc"]