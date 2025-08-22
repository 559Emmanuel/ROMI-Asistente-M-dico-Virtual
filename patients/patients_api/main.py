
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, constr, conint
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ---------------------------------------------------------------------
# Configuración de base de datos (SQLite en archivo)
# ---------------------------------------------------------------------
DATABASE_URL = "sqlite:///./patients.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------
# Modelo SQLAlchemy (tabla)
# ---------------------------------------------------------------------
class PatientModel(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    age = Column(Integer, nullable=False)
    symptoms = Column(Text, nullable=False)  # texto coma-separado
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------
# Esquemas (Pydantic) para validación I/O
# ---------------------------------------------------------------------
NameStr = constr(min_length=1, max_length=120)
AgeInt = conint(ge=0, le=130)

class PatientCreate(BaseModel):
    name: NameStr = Field(..., examples=["Juan Pérez"])
    age: AgeInt = Field(..., examples=[28])
    symptoms: List[constr(min_length=1)] | constr(min_length=1) = Field(
        ..., examples=[["fiebre", "tos"]]
    )

class PatientOut(BaseModel):
    id: int
    name: str
    age: int
    symptoms: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def _symptoms_to_text(sym) -> str:
    if isinstance(sym, list):
        return ", ".join(s.strip() for s in sym if s.strip())
    return str(sym).strip()

def _text_to_list(text: str) -> List[str]:
    parts = [p.strip() for p in (text or "").split(",")]
    return [p for p in parts if p] or ([] if not text else [text])


# ---------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------
app = FastAPI(
    title="Patients API",
    description="API REST para registrar y consultar pacientes con síntomas",
    version="1.0.0",
)


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "message": "Patients API up"}


@app.post(
    "/patients",
    response_model=PatientOut,
    status_code=status.HTTP_201_CREATED,
    tags=["patients"],
)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = PatientModel(
        name=payload.name,
        age=payload.age,
        symptoms=_symptoms_to_text(payload.symptoms),
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)

    out = PatientOut.model_validate(
        {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "symptoms": _text_to_list(patient.symptoms),
            "created_at": patient.created_at,
        }
    )
    return out


@app.get(
    "/patients",
    response_model=List[PatientOut],
    tags=["patients"],
)
def list_patients(
    name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(PatientModel)
    if name:
        query = query.filter(PatientModel.name.ilike(f"%{name}%"))
    rows = query.order_by(PatientModel.id.desc()).all()
    return [
        PatientOut(
            id=r.id,
            name=r.name,
            age=r.age,
            symptoms=_text_to_list(r.symptoms),
            created_at=r.created_at,
        )
        for r in rows
    ]


@app.get(
    "/patients/{patient_id}",
    response_model=PatientOut,
    tags=["patients"],
)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    r = db.get(PatientModel, patient_id)
    if not r:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return PatientOut(
        id=r.id,
        name=r.name,
        age=r.age,
        symptoms=_text_to_list(r.symptoms),
        created_at=r.created_at,
    )
