from pydantic import BaseModel
from typing import List, Optional

class TaskbotInput(BaseModel):
    id: str
    nombre: str
    proposito: str
    aplicaciones: str
    interaccion: str
    frecuencia: str
    riesgo: str
    dependencias: str
    evidencia_duplicidad: str

class EvaluacionOutput(BaseModel):
    id: str
    nombre: str
    tecnologia_sugerida: str
    ola_sugerida: str
    criterio_decision: str
    analisis_tipo: str  # 'Determinista (Heurístico)' o 'Agente Cognitivo (IA)'

class ReporteGlobalSummary(BaseModel):
    total_procesados: int
    total_microservicios: int
    total_n8n: int
    total_bpm: int
    total_rpa_selectivo: int
    items: List[EvaluacionOutput]