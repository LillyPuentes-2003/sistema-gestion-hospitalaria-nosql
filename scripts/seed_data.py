#!/usr/bin/env python3
"""
Script para poblar la base de datos MongoDB con datos de ejemplo
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de MongoDB
MONGO_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'admin')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'hospital_admin_2026')
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'hospital_nosql'

# Conectar a MongoDB
client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/')
db = client[MONGO_DB]

# Datos de ejemplo
DIAGNOSES = [
    {"code": "J00", "description": "Acute nasopharyngitis (common cold)", "category": "Respiratory"},
    {"code": "I10", "description": "Essential hypertension", "category": "Cardiovascular"},
    {"code": "E11.9", "description": "Type 2 diabetes mellitus", "category": "Metabolic"},
    {"code": "M54.5", "description": "Low back pain", "category": "Musculoskeletal"},
    {"code": "K21.9", "description": "Gastro-esophageal reflux disease", "category": "Digestive"}
]

TREATMENTS = [
    "Acetaminophen 500mg",
    "Ibuprofen 400mg",
    "Amoxicillin 500mg",
    "Omeprazole 20mg",
    "Losartan 50mg"
]

def generate_patient_histories(n=50):
    """Generar historiales clínicos de pacientes"""
    histories = []
    
    for i in range(1, n + 1):
        admission_date = datetime.now() - timedelta(days=random.randint(1, 365))
        discharge_date = admission_date + timedelta(days=random.randint(1, 10))
        
        diagnosis = random.choice(DIAGNOSES)
        
        history = {
            "patient_id": i,
            "patient_name": f"Patient {i}",
            "admission_date": admission_date,
            "discharge_date": discharge_date,
            "length_of_stay": (discharge_date - admission_date).days,
            "diagnosis": {
                "icd10_code": diagnosis["code"],
                "description": diagnosis["description"],
                "category": diagnosis["category"]
            },
            "treatments": random.sample(TREATMENTS, k=random.randint(1, 3)),
            "vital_signs": {
                "temperature": round(random.uniform(36.0, 38.5), 1),
                "heart_rate": random.randint(60, 100),
                "blood_pressure": {
                    "systolic": random.randint(110, 140),
                    "diastolic": random.randint(70, 90)
                },
                "oxygen_saturation": random.randint(95, 100)
            },
            "readmitted": random.choice([True, False]),
            "readmission_days": random.randint(1, 30) if random.random() > 0.7 else None,
            "cost": round(random.uniform(500000, 5000000), 2),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        histories.append(history)
    
    return histories

def generate_medical_analytics():
    """Generar datos de analítica médica"""
    analytics = []
    
    # Métricas por mes
    for month in range(1, 13):
        analytics.append({
            "metric_type": "monthly_admissions",
            "date": datetime(2025, month, 1),
            "value": random.randint(50, 200),
            "created_at": datetime.now()
        })
        
        analytics.append({
            "metric_type": "average_length_of_stay",
            "date": datetime(2025, month, 1),
            "value": round(random.uniform(3.0, 7.0), 2),
            "created_at": datetime.now()
        })
    
    # Métricas por categoría de diagnóstico
    for diagnosis in DIAGNOSES:
        analytics.append({
            "metric_type": "diagnosis_frequency",
            "category": diagnosis["category"],
            "icd10_code": diagnosis["code"],
            "count": random.randint(10, 100),
            "created_at": datetime.now()
        })
    
    return analytics

def seed_database():
    """Poblar la base de datos con datos de ejemplo"""
    print("🌱 Iniciando población de base de datos...")
    
    # Limpiar colecciones existentes
    print("🗑️  Limpiando colecciones existentes...")
    db.patient_histories.delete_many({})
    db.medical_analytics.delete_many({})
    db.ml_predictions.delete_many({})
    
    # Insertar historiales de pacientes
    print("📝 Insertando historiales de pacientes...")
    histories = generate_patient_histories(50)
    result = db.patient_histories.insert_many(histories)
    print(f"   ✅ {len(result.inserted_ids)} historiales insertados")
    
    # Insertar analítica médica
    print("📊 Insertando datos de analítica...")
    analytics = generate_medical_analytics()
    result = db.medical_analytics.insert_many(analytics)
    print(f"   ✅ {len(result.inserted_ids)} métricas insertadas")
    
    print("\n✅ Base de datos poblada exitosamente!")
    print(f"   📋 Historiales: {db.patient_histories.count_documents({})}")
    print(f"   📊 Analíticas: {db.medical_analytics.count_documents({})}")
    print(f"   🤖 Predicciones: {db.ml_predictions.count_documents({})}")

if __name__ == "__main__":
    seed_database()
    client.close()