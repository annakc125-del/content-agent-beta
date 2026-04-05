import json
import time
from typing import List, Dict, Any
from .prospector import ProspectorAgent
from .promotor import PromotorAgent
from .gestor import GestorAgent
from .closer import CloserAgent

class SalesOrchestrator:
    """
    Orquestador de Ventas (El Director)
    Coordina los 4 agentes en secuencia para ejecutar el flujo completo de 48 horas.
    Genera el reporte de métricas final.
    """
    
    def __init__(self):
        self.prospector = ProspectorAgent()
        self.promotor = PromotorAgent()
        self.gestor = GestorAgent()
        self.closer = CloserAgent()
        
        self.metricas = {
            "leads_extraidos": 0,
            "leads_calificados": 0,
            "mensajes_enviados": 0,
            "respuestas_recibidas": 0,
            "llamadas_agendadas": 0,
            "ventas_cerradas": 0,
            "revenue_total": 0
        }

    def ejecutar_flujo_48h(self, cantidad_leads: int = 5) -> Dict[str, Any]:
        """
        Ejecuta el flujo completo de ventas simulando las 48 horas.
        """
        print("\n" + "="*60)
        print("🚀 INICIANDO FLUJO DE VENTAS: 100K EN 48 HORAS 🚀")
        print("="*60)
        
        # 1. Fase de Prospección (Horas 0-4)
        print("\n[HORAS 0-4] Fase de Prospección...")
        leads_calificados = self.prospector.ejecutar(cantidad_leads)
        self.metricas["leads_extraidos"] = cantidad_leads
        self.metricas["leads_calificados"] = len(leads_calificados)
        
        if not leads_calificados:
            print("❌ No se encontraron leads calificados. Abortando flujo.")
            return self.generar_reporte()
            
        time.sleep(1) # Simular tiempo de procesamiento
        
        # 2. Fase de Promoción (Horas 8-12)
        print("\n[HORAS 8-12] Fase de Promoción (Outreach)...")
        leads_contactados = self.promotor.ejecutar(leads_calificados)
        self.metricas["mensajes_enviados"] = len(leads_contactados)
        
        time.sleep(1)
        
        # 3. Fase de Gestión (Horas 12-24)
        print("\n[HORAS 12-24] Fase de Gestión (Manejo de Objeciones)...")
        leads_gestionados = self.gestor.ejecutar(leads_contactados)
        
        # Contar respuestas (no ignorados)
        respuestas = [l for l in leads_gestionados if l.get('respuesta_lead') != "Ignorado"]
        self.metricas["respuestas_recibidas"] = len(respuestas)
        
        # Filtrar leads para el Closer
        leads_para_cierre = [l for l in leads_gestionados if l.get('estado_pipeline') in ['Agendado', 'Interesado']]
        self.metricas["llamadas_agendadas"] = len(leads_para_cierre)
        
        time.sleep(1)
        
        # 4. Fase de Cierre (Horas 24-48)
        print("\n[HORAS 24-48] Fase de Cierre (Llamadas de Voz IA)...")
        leads_cerrados = self.closer.ejecutar(leads_para_cierre)
        
        # Calcular métricas finales
        ventas = [l for l in leads_cerrados if l.get('resultado_cierre', {}).get('venta_cerrada')]
        self.metricas["ventas_cerradas"] = len(ventas)
        self.metricas["revenue_total"] = sum(l.get('resultado_cierre', {}).get('revenue_generado', 0) for l in ventas)
        
        print("\n" + "="*60)
        print("🏁 FLUJO DE 48 HORAS COMPLETADO 🏁")
        print("="*60)
        
        return self.generar_reporte(leads_cerrados)

    def generar_reporte(self, leads_finales: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera el reporte final de métricas y el estado del pipeline.
        """
        reporte = {
            "metricas_48h": self.metricas,
            "pipeline_final": leads_finales if leads_finales else []
        }
        
        print("\n📊 REPORTE DE MÉTRICAS (48 HORAS):")
        print(f"   - Leads Extraídos: {self.metricas['leads_extraidos']}")
        print(f"   - Leads Calificados: {self.metricas['leads_calificados']}")
        print(f"   - Mensajes Enviados: {self.metricas['mensajes_enviados']}")
        print(f"   - Respuestas Recibidas: {self.metricas['respuestas_recibidas']}")
        print(f"   - Llamadas Agendadas: {self.metricas['llamadas_agendadas']}")
        print(f"   - Ventas Cerradas: {self.metricas['ventas_cerradas']}")
        print(f"   - REVENUE TOTAL: ${self.metricas['revenue_total']} USD")
        
        return reporte

# Ejemplo de uso independiente
if __name__ == "__main__":
    orquestador = SalesOrchestrator()
    reporte = orquestador.ejecutar_flujo_48h(5)
    
    # Guardar reporte de ejemplo
    with open("sales_report_example.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)
