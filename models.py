from datetime import date
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import Column
from sqlalchemy.types import JSON
from pydantic import BaseModel


DATABASE_URL = "sqlite:///./vaccinations.db"
engine = create_engine(DATABASE_URL, echo=False)

class Vaccine(SQLModel, table=True):
    __tablename__ = "vaccines"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Number of doses in the initial (primary) series, if applicable (e.g. Hep B = 3). None if single-dose or purely recurring.
    primary_series_doses: Optional[int] = Field(default=None, gt=0)

    # Interval (years) at which the vaccine should be repeated (e.g. 1 for flu) – None if not routinely repeated.
    recurrence_interval_years: Optional[float] = Field(default=None, gt=0)

    # Interval (years) for booster after completing primary series (e.g. 10 for DPT/Tdap).
    booster_interval_years: Optional[float] = Field(default=None, gt=0)

    price_per_dose: float = Field(ge=0)
    side_effects: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    administration_route: str = Field(default="IM")  # IM, SC, Oral, etc.
    manufacturer: Optional[str] = None
    age_min: Optional[int] = Field(default=None, ge=0)  # in years
    age_max: Optional[int] = Field(default=None, ge=0)
    contraindications: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    notes: Optional[str] = None


class UserBase(SQLModel):
    first_name: str
    last_name: str
    username: str
    dob: date
    medical_id: str
    email: str
    phone: str
    address: str
    postcode: str

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass

class DoseBase(SQLModel):
    vaccine_id: int = Field(foreign_key="vaccines.id")
    user_id: int = Field(foreign_key="users.id")
    date_administered: date
    dose_number: int = Field(gt=0)
    appointment_id: Optional[int] = Field(default=None, foreign_key="appointments.id")


class Dose(DoseBase, table=True):
    __tablename__ = "doses"
    id: Optional[int] = Field(default=None, primary_key=True)


class DoseCreate(DoseBase):
    pass

class AppointmentBase(SQLModel):
    datetime: date
    user_id: int = Field(foreign_key="users.id")
    vaccine_id: int = Field(foreign_key="vaccines.id")
    branch_id: int = Field(foreign_key="branches.id")
    notes: Optional[str] = [""]



class Appointment(AppointmentBase, table=True):
    __tablename__ = "appointments"
    id: Optional[int] = Field(default=None, primary_key=True)

class AppointmentCreate(AppointmentBase):
    pass

class Branch(SQLModel, table=True):
    __tablename__ = "branches"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    postcode: str
    phone: str
    email: str
    opening_hours: List[str] = Field(default_factory=list, sa_column=Column(JSON))


def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session