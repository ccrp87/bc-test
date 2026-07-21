import re
from typing import List, Dict, Any
from app.models import TaskbotInput, EvaluacionOutput

class MotorDecisionService:
    def __init__(self, reglas: List[Any]):
        # Organizar las reglas cargadas desde el repositorio
        self.reglas = reglas

    def evaluar_taskbot(self, bot: TaskbotInput) -> EvaluacionOutput:
        # Texto consolidado para análisis semántico/heurístico
        texto_analisis = f"{bot.proposito} {bot.interaccion} {bot.dependencias} {bot.evidencia_duplicidad}".lower()
        
        # 1. EVALUACIÓN DETERMINISTA (Heurísticas organizadas por jerarquía de prioridad)
        # Prioridad 1: Detección de Duplicidad / Consolidación de Microservicios
        for categoria, palabra, tecnologia, prioridad in self.reglas:
            if prioridad == 1 and palabra in texto_analisis:
                return EvaluacionOutput(
                    id=bot.id,
                    nombre=bot.nombre,
                    tecnologia_sugerida=tecnologia,
                    ola_sugerida=self._calcular_ola(bot.riesgo, tecnologia),
                    criterio_decision=f"Patrón detectado por regla de duplicidad histórica ('{palabra}').",
                    analisis_tipo="Determinista (Heurístico)"
                )

        # Prioridad 2: Intervención Humana (BPM)
        for categoria, palabra, tecnologia, prioridad in self.reglas:
            if prioridad == 2 and palabra in texto_analisis:
                return EvaluacionOutput(
                    id=bot.id,
                    nombre=bot.nombre,
                    tecnologia_sugerida=tecnologia,
                    ola_sugerida=self._calcular_ola(bot.riesgo, tecnologia),
                    criterio_decision=f"Proceso requiere interacción o validación humana ('{palabra}').",
                    analisis_tipo="Determinista (Heurístico)"
                )

        # Prioridad 3 y 4: Automatización Ágil (n8n) vs UI Legacy (RPA Selectivo)
        # Nota arquitectónica: Si conviven ambas, el acoplamiento rígido de la UI obliga a priorizar RPA Selectivo
        if "ui legacy" in texto_analisis:
            return EvaluacionOutput(
                id=bot.id,
                nombre=bot.nombre,
                tecnologia_sugerida="RPA Selectivo",
                ola_sugerida="Ola 3 (Larga Cola Legacy)",
                criterio_decision="Acoplamiento crítico a interfaz gráfica de usuario sin alternativa de API expuesta.",
                analisis_tipo="Determinista (Heurístico)"
            )

        for categoria, palabra, tecnologia, prioridad in self.reglas:
            if prioridad == 3 and palabra in texto_analisis:
                return EvaluacionOutput(
                    id=bot.id,
                    nombre=bot.nombre,
                    tecnologia_sugerida=tecnologia,
                    ola_sugerida=self._calcular_ola(bot.riesgo, tecnologia),
                    criterio_decision=f"Candidato ideal para integración limpia basada en servicios y API-First ('{palabra}').",
                    analisis_tipo="Determinista (Heurístico)"
                )

        # 2. CAPA COGNITIVA ASISTIDA POR AGENTE (Fallback Semántico Inteligente)
        # Si ninguna regla dura coincide, entra el motor NLP para interpretar la ambigüedad
        return self._ejecutar_agente_cognitivo(bot)

    def _calcular_ola(self, riesgo: str, tecnologia: str) -> str:
        riesgo_clean = riesgo.lower()
        if "alto" in riesgo_clean:
            return "Ola 2 (Refactorización Crítica de Alto Riesgo)"
        elif "bajo" in riesgo_clean or "medio" in riesgo_clean:
            if tecnologia == "Microservicio" or tecnologia == "n8n Orquestador":
                return "Ola 1 (Quick Wins de Alto Valor)"
            return "Ola 2 (Refactorización de Procesos Core)"
        return "Ola 3 (Larga Cola)"

    def _ejecutar_agente_cognitivo(self, bot: TaskbotInput) -> EvaluacionOutput:
        """Simulación local procode del Agente de IA para análisis semántico complejo."""
        proposito = bot.proposito.lower()
        
        # Lógica semántica del Agente NLP integrado en código (Mock de Criterio de Agente)
        if "verificar" in proposito or "monitoreo" in proposito or "alerta" in proposito:
            tecnologia = "n8n Orquestador"
            ola = "Ola 1 (Quick Wins de Alto Valor)" if "alto" not in bot.riesgo.lower() else "Ola 2 (Refactorización Crítica)"
            criterio = "El agente cognitivo interpretó semánticamente una tarea de monitoreo/alerta asíncrona óptima para Orquestación ágil."
        elif "unificar" in proposito or "depuracion" in proposito:
            tecnologia = "Microservicio"
            ola = "Ola 2 (Refactorización de Procesos Core)"
            criterio = "El agente cognitivo analizó un requerimiento pesado de calidad de datos maestros ideal para Microservicios compartidos."
        else:
            tecnologia = "BPM / Power Platform"
            ola = "Ola 2 (Refactorización de Procesos Core)"
            criterio = "Análisis cognitivo del Agente: Patrón difuso detectado. Asignado preventivamente a plataforma de procesos corporativos bajo gobierno."

        return EvaluacionOutput(
            id=bot.id,
            nombre=bot.nombre,
            tecnologia_sugerida=tecnologia,
            ola_sugerida=ola,
            criterio_decision=criterio,
            analisis_tipo="Agente Cognitivo (IA)"
        )

    @staticmethod
    def parsear_inventario_txt(contenido_txt: str) -> List[TaskbotInput]:
        """Parser robusto basado en expresiones regulares flexibles (re.IGNORECASE) para procesar el catálogo plano."""
        bloques = contenido_txt.split("============================================================")
        bots_parseados = []
        
        for bloque in bloques:
            if "Nombre del taskbot:" not in bloque:
                continue
                
            def extraer_campo(patron, texto):
                match = re.search(patron, texto, re.IGNORECASE)
                return match.group(1).strip() if match else "No especificado"

            tb_id_match = re.search(r"Taskbot\s+(\d+)", bloque, re.IGNORECASE)
            tb_id = tb_id_match.group(1) if tb_id_match else "00"

            bot = TaskbotInput(
                id=tb_id,
                nombre=extraer_campo(r"Nombre del taskbot:\s*(.*)", bloque),
                proposito=extraer_campo(r"Proposito funcional:\s*(.*)", bloque),
                aplicaciones=extraer_campo(r"Aplicaciones involucradas:\s*(.*)", bloque),
                interaccion=extraer_campo(r"Tipo de interaccion:\s*(.*)", bloque),
                frecuencia=extraer_campo(r"Frecuencia de ejecucion:\s*(.*)", bloque),
                riesgo=extraer_campo(r"Riesgo operacional:\s*(.*)", bloque),
                dependencias=extraer_campo(r"Dependencias conocidas:\s*(.*)", bloque),
                evidencia_duplicidad=extraer_campo(r"Evidencia de duplicidad.*:\s*(.*)", bloque)
            )
            bots_parseados.append(bot)
            
        return bots_parseados