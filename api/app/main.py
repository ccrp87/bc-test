from fastapi import FastAPI, Depends, HTTPException
from typing import List
from app.models import TaskbotInput, EvaluacionOutput, ReporteGlobalSummary
from app.repository import ReglasRepository
from app.service import MotorDecisionService

app = FastAPI(
    title="XYZ Ltda. - Motor Inteligente de Consolidación y Migración",
    description="Microservicio Core de grado empresarial para el análisis del portafolio de automatización.",
    version="1.1.0"
)

# Inyección de Dependencias del Repositorio de Datos
def get_service() -> MotorDecisionService:
    repo = ReglasRepository()
    reglas = repo.obtener_todas_las_reglas()
    return MotorDecisionService(reglas)

@app.post("/api/v1/analyze-single", response_model=EvaluacionOutput, tags=["Análisis Individual"])
def analizar_un_solo_bot(bot: TaskbotInput, service: MotorDecisionService = Depends(get_service)):
    """Analiza una única carga JSON estructurada de un taskbot."""
    try:
        return service.evaluar_taskbot(bot)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo operativo del motor: {str(e)}")

@app.post("/api/v1/analyze-batch", response_model=ReporteGlobalSummary, tags=["Procesamiento por Lotes (Batch JSON)"])
def analizar_lote_json(bots: List[TaskbotInput], service: MotorDecisionService = Depends(get_service)):
    """
    Recibe un payload JSON con una lista estructurada de taskbots,
    los evalúa en lote y genera las recomendaciones arquitectónicas.
    """
    if not bots:
        raise HTTPException(status_code=400, detail="El lote de entrada no puede estar vacío.")
    
    try:
        items_evaluados = []
        for bot_in in bots:
            res = service.evaluar_taskbot(bot_in)
            items_evaluados.append(res)
            
        # Generar Métricas Ejecutivas del Lote
        summary = ReporteGlobalSummary(
            total_procesados=len(items_evaluados),
            total_microservicios=len([x for x in items_evaluados if x.tecnologia_sugerida == "Microservicio"]),
            total_n8n=len([x for x in items_evaluados if "n8n" in x.tecnologia_sugerida]),
            total_bpm=len([x for x in items_evaluados if "BPM" in x.tecnologia_sugerida]),
            total_rpa_selectivo=len([x for x in items_evaluados if x.tecnologia_sugerida == "RPA Selectivo"]),
            items=items_evaluados
        )
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en procesamiento del lote JSON: {str(e)}")