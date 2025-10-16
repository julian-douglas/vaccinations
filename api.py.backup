from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import Session, select
from models import *
from seed_variables import seed_vaccines, seed_branches
from datetime import date

app = FastAPI(title="Vaccination API", version="0.2.0")


@app.on_event("startup")
def startup():
    init_db()
    with next(get_session()) as session:
        existing = session.exec(select(Vaccine)).first()
        if not existing:
            for v in seed_vaccines:
                session.add(Vaccine(**v))
            for b in seed_branches:
                session.add(Branch(**b))
            session.commit()


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}

#create
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    user = User(**user_in.model_dump())  # dob now a date object
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

#read
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

#update
@app.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_in: UserCreate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    user_data = user_in.model_dump()
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

#delete
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    session.delete(user)
    session.commit()
    return user

@app.get("/users", response_model=list[User])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()



@app.get("/vaccines", response_model=list[Vaccine])
def list_vaccines(session: Session = Depends(get_session)):
    return session.exec(select(Vaccine)).all()

@app.get("/vaccines/{vaccine_id}", response_model=Vaccine)
def get_vaccine(vaccine_id: int, session: Session = Depends(get_session)):
    v = session.get(Vaccine, vaccine_id)
    if not v:
        raise HTTPException(404, "Vaccine not found")
    return v

#create
@app.post("/doses", response_model=Dose, status_code=status.HTTP_201_CREATED)
def create_dose(dose_in: DoseCreate, session: Session = Depends(get_session)):
    if not session.get(User, dose_in.user_id):
        raise HTTPException(404, "User not found")
    if not session.get(Vaccine, dose_in.vaccine_id):
        raise HTTPException(404, "Vaccine not found")
    da = dose_in.date_administered
    if isinstance(da, str):
        da = date.fromisoformat(da)
    dose = Dose(**dose_in.model_dump(exclude={"date_administered"}), date_administered=da)
    session.add(dose)
    session.commit()
    session.refresh(dose)
    return dose

#read
@app.get("/doses/{dose_id}", response_model=Dose)
def get_dose(dose_id: int, session: Session = Depends(get_session)):
    dose = session.get(Dose, dose_id)
    if not dose:
        raise HTTPException(404, "Dose not found")
    return dose

#update
@app.patch("/doses/{dose_id}", response_model=Dose)
def update_dose(dose_id: int, dose_in: Dose, session: Session = Depends(get_session)):
    dose = session.get(Dose, dose_id)
    if not dose:
        raise HTTPException(404, "Dose not found")
    dose_data = dose_in.model_dump()
    for key, value in dose_data.items():
        setattr(dose, key, value)
    session.add(dose)
    session.commit()
    session.refresh(dose)
    return dose

#delete
@app.delete("/doses/{dose_id}", response_model=Dose)
def delete_dose(dose_id: int, session: Session = Depends(get_session)):
    dose = session.get(Dose, dose_id)
    if not dose:
        raise HTTPException(404, "Dose not found")
    session.delete(dose)
    session.commit()
    return dose

@app.get("/doses", response_model=list[Dose])
def list_doses(session: Session = Depends(get_session)):
    return session.exec(select(Dose)).all()


#create
@app.post("/appointments", response_model=Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment_in: AppointmentCreate, session: Session = Depends(get_session)):
    if not session.get(User, appointment_in.user_id):
        raise HTTPException(404, "User not found")
    if not session.get(Vaccine, appointment_in.vaccine_id):
        raise HTTPException(404, "Vaccine not found")
    if not session.get(Branch, appointment_in.branch_id):
        raise HTTPException(404, "Branch not found")
    appointment = Appointment(**appointment_in.model_dump())
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


#read
@app.get("/appointments/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: int, session: Session = Depends(get_session)):
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(404, "Appointment not found")
    return appointment


#update
@app.patch("/appointments/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: int, appointment_in: Appointment, session: Session = Depends(get_session)):
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(404, "Appointment not found")
    appointment_data = appointment_in.model_dump()
    for key, value in appointment_data.items():
        setattr(appointment, key, value)
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


#delete
@app.delete("/appointments/{appointment_id}", response_model=Appointment)
def delete_appointment(appointment_id: int, session: Session = Depends(get_session)):
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(404, "Appointment not found")
    session.delete(appointment)
    session.commit()
    return appointment

@app.get("/appointments", response_model=list[Appointment])
def list_appointments(session: Session = Depends(get_session)):
    return session.exec(select(Appointment)).all()

# Run: uvicorn api:app --reload