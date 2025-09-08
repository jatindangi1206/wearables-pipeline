from pydantic import BaseModel
from datetime import datetime

class BloodPressure(BaseModel):
    systolic: int
    diastolic: int
    heart_rate: int
    created_time: datetime

class HeartRate(BaseModel):
    created_time: datetime
    heart_rate: int

class Sleep(BaseModel):
    light_sleep: int
    deep_sleep: int
    rem_sleep: int
    almost_awake: int
    log_date_time: datetime
    log_end_time: datetime

class SpO2(BaseModel):
    spo2_value: float
    created_time: datetime

class Steps(BaseModel):
    steps: int
    distance: float
    calories: float
    log_date_time: datetime
    log_end_time: datetime

class Temperature(BaseModel):
    temperature: float
    created_time: datetime

class Meal(BaseModel):
    dish: str
    time: datetime
    rating: int
    customization: str

class LungFunction(BaseModel):
    fev1: float
    fev1_fvc: float
    patient_id: str