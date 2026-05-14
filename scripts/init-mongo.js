// Crear la base de datos y usuario
db = db.getSiblingDB('hospital_nosql');

// Crear usuario para la base de datos
db.createUser({
  user: 'hospital_user',
  pwd: 'hospital_pass_2026',
  roles: [
    {
      role: 'readWrite',
      db: 'hospital_nosql'
    }
  ]
});

// Crear colecciones
db.createCollection('patient_histories');
db.createCollection('medical_analytics');
db.createCollection('ml_predictions');

// Crear índices para patient_histories
db.patient_histories.createIndex({ "patient_id": 1 });
db.patient_histories.createIndex({ "admission_date": -1 });
db.patient_histories.createIndex({ "diagnosis.icd10_code": 1 });

// Crear índices para medical_analytics
db.medical_analytics.createIndex({ "date": -1 });
db.medical_analytics.createIndex({ "metric_type": 1 });

// Crear índices para ml_predictions
db.ml_predictions.createIndex({ "patient_id": 1 });
db.ml_predictions.createIndex({ "prediction_date": -1 });
db.ml_predictions.createIndex({ "model_name": 1 });

print('✅ Base de datos hospital_nosql inicializada correctamente');
print('✅ Colecciones creadas: patient_histories, medical_analytics, ml_predictions');
print('✅ Índices creados exitosamente');