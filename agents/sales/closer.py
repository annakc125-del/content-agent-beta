import os
import json
import random
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class CloserAgent:
    """
    Agente Closer (El Ejecutor)
    Rol: Cerrar la venta. En este flujo de 48h, simula ser un Agente de Voz de IA
    que realiza la llamada de 15 minutos para cobrar.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4.1-mini"
        
        # Simulación de objeciones finales en la llamada
        self.objeciones_llamada = [
            "¿Puedo pagar a plazos?",
            "¿Qué pasa si no me gustan los videos?",
            "Tengo que consultarlo con mi socio.",
            "Me parece bien, ¿dónde pago?",
            "No estoy seguro de que esto funcione para mi nicho."
        ]

    def simular_objecion_llamada(self) -> str:
        """
        Simula la objeción final del lead durante la llamada de cierre.
        """
        # 40% de probabilidad de cierre directo sin objeción
        if random.random() < 0.4:
            return "Me parece bien, ¿dónde pago?"
        return random.choice(self.objeciones_llamada[:-1])

    def generar_guion_cierre(self, lead: Dict[str, Any], objecion_final: str) -> Dict[str, Any]:
        """
        Utiliza OpenAI para generar el guion de cierre personalizado y manejar la objeción final
        con técnicas de cierre despiadadas (urgencia, escasez, ROI).
        """
        prompt = f"""
        Eres un Closer de Ventas B2B despiadado y efectivo (Agente Closer).
        Estás en una llamada de cierre con un prospecto para vender el Paquete Growth ($2,500 pago único por 3 meses de contenido).
        
        Perfil del Lead:
        - Nombre: {lead.get('nombre', 'Prospecto')}
        - Pain Point: {lead.get('pain_point', 'Falta de tiempo')}
        - Interacción previa: {lead.get('interaccion_gestor', {}).get('respuesta_gestor', 'Mostró interés')}
        
        Objeción final en la llamada: "{objecion_final}"
        
        Instrucciones:
        1. Si la objeción es "Me parece bien, ¿dónde pago?", genera el mensaje de confirmación y el enlace de Stripe.
        2. Si es otra objeción, aplica una técnica de cierre agresiva (ej: "Entiendo, pero cada día que pasa sin publicar estás perdiendo clientes. ¿Qué tarjeta usamos para empezar hoy?").
        3. Genera el enlace de pago simulado (ej: stripe.com/pay/growth-paquete).
        4. Determina si la venta se cerró o se perdió.
        
        Devuelve ÚNICAMENTE un objeto JSON con la siguiente estructura:
        {{
            "guion_cierre": "Tu respuesta final en la llamada",
            "enlace_pago": "Enlace de Stripe generado",
            "venta_cerrada": true o false,
            "revenue_generado": 2500 o 0,
            "estado_pipeline": "Cerrado Ganado" o "Cerrado Perdido"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto Closer B2B. Responde solo en JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            cierre = json.loads(response.choices[0].message.content)
            return cierre
            
        except Exception as e:
            print(f"❌ [Closer] Error al generar guion de cierre para {lead.get('nombre')}: {str(e)}")
            # Fallback
            return {
                "guion_cierre": "Perfecto, te envío el enlace de pago. ¿Qué tarjeta usamos?",
                "enlace_pago": "https://buy.stripe.com/test_growth",
                "venta_cerrada": True,
                "revenue_generado": 2500,
                "estado_pipeline": "Cerrado Ganado"
            }

    def ejecutar(self, leads_para_cierre: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ejecuta el flujo completo del Closer: Recibe leads agendados -> Simula llamada -> Cierra venta
        """
        print("\n" + "="*50)
        print("💰 INICIANDO AGENTE CLOSER")
        print("="*50)
        
        if not leads_para_cierre:
            print("⚠️ [Closer] No hay leads listos para cierre.")
            return []
            
        leads_cerrados = []
        
        for lead in leads_para_cierre:
            print(f"☎️ [Closer] Llamando a {lead.get('nombre')}...")
            
            # 1. Simular la objeción final en la llamada
            objecion_final = self.simular_objecion_llamada()
            print(f"   🗣️ Objeción del lead: '{objecion_final}'")
            
            # 2. Generar el guion de cierre y manejar la objeción
            cierre = self.generar_guion_cierre(lead, objecion_final)
            print(f"   🤖 Respuesta Closer: '{cierre.get('guion_cierre')}'")
            
            if cierre.get('venta_cerrada'):
                print(f"   🎉 ¡VENTA CERRADA! Revenue: ${cierre.get('revenue_generado')}")
            else:
                print(f"   ❌ Venta perdida.")
                
            # 3. Actualizar el lead
            lead_actualizado = {
                **lead,
                "objecion_final": objecion_final,
                "resultado_cierre": cierre,
                "estado_pipeline": cierre.get("estado_pipeline", "Cerrado Perdido")
            }
            
            leads_cerrados.append(lead_actualizado)
            
        print(f"✅ [Closer] Llamadas completadas. {len([l for l in leads_cerrados if l.get('resultado_cierre', {}).get('venta_cerrada')])} ventas cerradas.")
        return leads_cerrados

# Ejemplo de uso independiente
if __name__ == "__main__":
    # Lead de prueba
    lead_prueba = [{
        "nombre": "Carlos Mendoza",
        "pain_point": "Tiene mucho contenido largo pero no lo aprovecha en Shorts",
        "estado_pipeline": "Agendado",
        "interaccion_gestor": {
            "respuesta_gestor": "Perfecto, agendemos 10 min mañana."
        }
    }]
    
    agente = CloserAgent()
    resultados = agente.ejecutar(lead_prueba)
    print(json.dumps(resultados, indent=2, ensure_ascii=False))
