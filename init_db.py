import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, DateTime, ForeignKey

DATABASE_URI = 'sqlite:///clinic.db'
engine = create_engine(DATABASE_URI, echo=True)
metadata = MetaData()

# Mendefinisikan table 'patients'
patients = Table('patients', metadata, 
                 Column('patient_id', Integer, primary_key=True),
                 Column('name', String),
                 Column('age', Integer),
                 Column('medical_history', String))

# Mendifinisikan table 'appointments'
appointments = Table('appointments', metadata,
                     Column('appointment_id', Integer, primary_key=True),
                     Column('patient_id', Integer, ForeignKey("patients.patient_id", ondelete="CASCADE")),
                     Column('doctor_name', String),
                     Column('date', DateTime),
                     Column('diagnosis', String))

# Membuat Tabel
metadata.create_all(engine)

print("Database clinic.db, tabel patients dan appointments telah berhasil dibuat!")