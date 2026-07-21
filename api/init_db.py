import sqlite3
import os

def init_database():
    db_path = os.path.join("reglas.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear tabla de reglas heurísticas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reglas_migracion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            palabra_clave TEXT NOT NULL,
            tecnologia_sugerida TEXT NOT NULL,
            prioridad_evaluacion INTEGER NOT NULL
        )
    """)
    
    # Limpiar datos previos si existen para el seed
    cursor.execute("DELETE FROM reglas_migracion")
    
    # Seed de reglas basadas en la matriz de decisión y el catálogo de 50 bots
    reglas = [
        # Prioridad 1: Consolidación / Redundancia (Alta prioridad)
        ('consolidacion', 'similar a', 'Microservicio', 1),
        ('consolidacion', 'alta similitud', 'Microservicio', 1),
        ('consolidacion', 'solapa con', 'Microservicio', 1),
        ('consolidacion', 'duplicado', 'Microservicio', 1),
        ('consolidacion', 'duplicidad parcial', 'Microservicio', 1),
        ('consolidacion', 'reutiliza logica', 'Microservicio', 1),
        
        # Prioridad 2: Intervención Humana o flujos complejos
        ('intervencion_humana', 'aprobacion', 'BPM / Camunda', 2),
        ('intervencion_humana', 'ticket', 'BPM / Camunda', 2),
        ('intervencion_humana', 'plantilla excel', 'BPM / Power Platform', 2),
        ('intervencion_humana', 'asistida', 'BPM / Power Platform', 2),
        ('intervencion_humana', 'manual', 'BPM / Power Platform', 2),
        ('intervencion_humana', 'auditoria', 'BPM / Camunda', 2),
        
        # Prioridad 3: Automatización backend limpia e integraciones modernas
        ('automatizacion_agil', 'api', 'n8n Orquestador', 3),
        ('automatizacion_agil', 'bd', 'n8n Orquestador', 3),
        ('automatizacion_agil', 'email', 'n8n Orquestador', 3),
        ('automatizacion_agil', 'webhook', 'n8n Orquestador', 3),
        
        # Prioridad 4: Sistemas Obsoletos sin APIs
        ('sistemas_obsoletos', 'ui legacy', 'RPA Selectivo', 4),
        ('sistemas_obsoletos', 'portal bancario', 'RPA Selectivo', 4),
        ('sistemas_obsoletos', 'portal web', 'RPA Selectivo', 4),
        ('sistemas_obsoletos', 'client pesado', 'RPA Selectivo', 4)
    ]
    
    cursor.executemany("""
        INSERT INTO reglas_migracion (categoria, palabra_clave, tecnologia_sugerida, prioridad_evaluacion)
        VALUES (?, ?, ?, ?)
    """, reglas)
    
    conn.commit()
    conn.close()
    print("Base de datos SQLite 'reglas.db' inicializada y poblada con éxito.")

if __name__ == "__main__":
    init_database()