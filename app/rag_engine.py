from typing import Dict, Any

class NormativeRAGEngine:
    def __init__(self):
        self.knowledge_base = {
            "sheetmetal": {
                "Falla Crítica": {
                    "norma": "IATF 16949 - Sección 8.5.2 (Trazabilidad y Control de Defectos)",
                    "diagnostico": "Fatiga estructural o microfisura por esfuerzo de troquelado excesivo.",
                    "material_actual": "Acero Estándar A36",
                    "material_recomendado": "Acero Martensítico de Alta Resistencia (MS-1200) o Aleación Ti-6Al-4V",
                    "accion_correctiva": "Detener celda de troquelado, realizar inspección por ultrasonido y ajustar presión de estampado.",
                    "requiere_validacion_humana": True
                },
                "Conforme": {
                    "norma": "ISO 9001:2015 - Sección 8.6 (Liberación de Productos)",
                    "diagnostico": "Sin defectos estructurales detectados.",
                    "material_actual": "Acero Especificado en Diseño",
                    "material_recomendado": "Mantener lote de producción actual.",
                    "accion_correctiva": "Ninguna. Liberar pieza para ensamble final.",
                    "requiere_validacion_humana": False
                }
            },
            "plastico": {
                "Falla Crítica": {
                    "norma": "IATF 16949 - Sección 8.5.1 (Control de la Producción de Ornamentaciones)",
                    "diagnostico": "Rechupe severo o deformación térmica en proceso de inyección.",
                    "material_actual": "Polipropileno (PP) Estándar",
                    "material_recomendado": "Polipropileno reforzado con 20% Fibra de Vidrio (PP-GF20) o ABS/PC Grado Automotriz",
                    "accion_correctiva": "Ajustar temperatura de molde (-15°C) y aumentar tiempo de sostenimiento de presión.",
                    "requiere_validacion_humana": True
                },
                "Conforme": {
                    "norma": "ISO 9001:2015 - Sección 8.6 (Criterios de Aceptación Estética)",
                    "diagnostico": "Acabado superficial dentro de tolerancias estéticas.",
                    "material_actual": "Polímero Especificado",
                    "material_recomendado": "Mantener parámetro de inyección.",
                    "accion_correctiva": "Liberar pieza para ensamble de interiores/exteriores.",
                    "requiere_validacion_humana": False
                }
            }
        }

    def get_recommendation(self, tipo_material: str, resultado_falla: str) -> Dict[str, Any]:
        material_key = tipo_material.lower().strip()
        if material_key not in self.knowledge_base:
            material_key = "sheetmetal"

        categoria = self.knowledge_base[material_key]
        rec = categoria.get(resultado_falla, categoria["Falla Crítica"])

        return {
            "norma_aplicada": rec["norma"],
            "diagnostico_tecnico": rec["diagnostico"],
            "material_actual": rec["material_actual"],
            "material_alta_resistencia_sugerido": rec["material_recomendado"],
            "accion_correctiva_sugerida": rec["accion_correctiva"],
            "validado_por_ingeniero_planta": False,
            "advertencia_seguridad": "ESTA RECOMENDACIÓN REQUIERE HOMOLOGACIÓN Y FIRMA DEL INGENIERO METÁLICO/POLÍMEROS ANTES DE APLICAR EN LÍNEA."
        }
