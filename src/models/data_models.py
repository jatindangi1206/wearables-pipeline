from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BloodPressure(BaseModel):
    systolic: int
    diastolic: int
    heart_rate: int
    timestamp: datetime

class HeartRate(BaseModel):
    timestamp: datetime
    heart_rate: int

class Sleep(BaseModel):
    light_sleep: int
    deep_sleep: int
    rem_sleep: int
    almost_awake: int
    timestamp: datetime
    timestamp_end: datetime

class SpO2(BaseModel):
    spo2_value: float
    timestamp: datetime

class Steps(BaseModel):
    steps: int
    distance: float
    calories: float
    timestamp: datetime
    timestamp_end: datetime

class Temperature(BaseModel):
    temperature: float
    timestamp: datetime

class Meal(BaseModel):
    dish: str
    timestamp: datetime
    rating: int
    customization: str

class LungFunction(BaseModel):
    fev1: float
    fev1_fvc: float
    fvc: Optional[float] = None
    patient_id: str
    timestamp: Optional[datetime] = None