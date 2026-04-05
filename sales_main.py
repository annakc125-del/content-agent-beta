import os
import json
from dotenv import load_dotenv
from agents.sales.sales_orchestrator import SalesOrchestrator

# Cargar variables de entorno
load_dotenv()

def main():
    """
    Script principal para ejecutar el flujo de ventas de 48 horas con los 4 Agentes de IA.
    """
    print("="*60)
    print("🤖 ECOSISTEMA DE AGENTES DE VENTAS IA (BETA) 🤖")
    print("Objetivo: 100k en 48 Horas - Nicho: Coaches e Infoproductores")
    print("="*60)
    
    # Verificar API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: No se encontró OPENAI_API_KEY en el archivo .env")
        print("Por favor, configura tu API Key antes de ejecutar el flujo de ventas.")
        return
        
    # Inicializar el Orquestador de Ventas
    orquestador = SalesOrchestrator()
    
    # Ejecutar el flujo completo simulando 5 leads iniciales (para demostración)
    # En producción, esto sería 5000 leads
    cantidad_leads_demo = 5
    print(f"\nIniciando demostración con {cantidad_leads_demo} leads...")
    
    reporte_final = orquestador.ejecutar_flujo_48h(cantidad_leads_demo)
    
    # Guardar el reporte en la carpeta de ejemplos
    output_path = "sales_examples/reporte_ventas_48h.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(reporte_final, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Reporte detallado guardado en: {output_path}")
    print("="*60)

if __name__ == "__main__":
    main()
