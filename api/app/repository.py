import sqlite3
import os
from typing import Dict, List, Tuple

class ReglasRepository:
    def __init__(self, db_name: str = "reglas.db"):
        self.db_path = os.path.join(db_name)

    def obtener_todas_las_reglas(self) -> List[Tuple[str, str, str, int]]:
        """Devuelve una lista de tuplas ordenadas por prioridad de evaluación."""
        if not os.path.exists(self.db_path):
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT categoria, palabra_clave, tecnologia_sugerida, prioridad_evaluacion 
            FROM reglas_migracion 
            ORDER BY prioridad_evaluacion ASC
        """)
        reglas = cursor.fetchall()
        conn.close()
        return reglas