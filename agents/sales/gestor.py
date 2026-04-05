import os
import json
import random
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class GestorAgent:
    """
    Agente Gestor (El Perro Pastor)
    Rol: Calificar el interés, manejar objeciones iniciales, agendar la llamada de cierre
    y hacer seguimiento implacable.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4.1-mini"
        
        # Simulación de respuestas de leads (para el entorno de prueba)
        self.respuestas_simuladas = [
            "Me gusta el clip, pero es muy caro.",
            "No tengo tiempo para grabar más contenido.",
            "¿Cómo funciona el proceso exactamente?",
            "Me interesa, ¿podemos hablar mañana?",
            "Ya tengo un editor que me cobra menos.",
            "Ignorado" # Simula que no respondió
        ]

    def simular_respuesta_lead(self, lead: Dict[str, Any]) -> str:
        """
        Simula la respuesta de un lead a nuestro mensaje de prospección.
        En un entorno real, esto vendría de la bandeja de entrada (Instantly/LinkedIn).
        """
        # 20% de probabilidad de ignorar
        if random.random() < 0.2:
            return "Ignorado"
        return random.choice(self.respuestas_simuladas[:-1])

    def manejar_objecion(self, lead: Dict[str, Any], respuesta_lead: str) -> Dict[str, Any]:
        """
        Utiliza OpenAI para analizar la respuesta del lead, clasificarla (objeción, interés, duda)
        y generar la respuesta adecuada para avanzar hacia la llamada (agendar).
        """
        prompt = f"""
        Eres un experto Closer de Ventas B2B (Agente Gestor).
        Tu objetivo es manejar la respuesta de un prospecto a tu mensaje inicial de prospección.
        Vendes un servicio High Ticket ($2,500) de creación de contenido (30 Reels/Shorts al mes).
        
        Perfil del Lead:
        - Nombre: {lead.get('nombre', 'Prospecto')}
        - Pain Point: {lead.get('pain_point', 'Falta de tiempo')}
        
        Respuesta del Lead: "{respuesta_lead}"
        
        Instrucciones:
        1. Analiza la respuesta y clasifícala en: "Objecion_Precio", "Objecion_Tiempo", "Duda_Proceso", "Interesado", "Rechazo".
        2. Redacta una respuesta persuasiva (máximo 3 líneas) para manejar la objeción o duda.
        3. El objetivo final de tu respuesta SIEMPRE es agendar una llamada de 10 minutos (ej: "¿Tienes 10 min mañana para mostrarte cómo funciona?").
        4. Si el lead ya está interesado, envíale el enlace de Calendly (simulado: calendly.com/tu-agencia/10min).
        
        Devuelve ÚNICAMENTE un objeto JSON con la siguiente estructura:
        {{
            "clasificacion": "Tipo de respuesta",
            "respuesta_gestor": "Tu respuesta persuasiva",
            "accion_siguiente": "Agendar Llamada" o "Seguimiento" o "Descartar",
            "estado_pipeline": "Interesado" o "Objecion" o "Agendado" o "Perdido"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en manejo de objeciones B2B. Responde solo en JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            analisis = json.loads(response.choices[0].message.content)
            return analisis
            
        except Exception as e:
            print(f"❌ [Gestor] Error al manejar objeción para {lead.get('nombre')}: {str(e)}")
            # Fallback
            return {
                "clasificacion": "Error",
                "respuesta_gestor": "Entiendo. ¿Tienes 10 minutos mañana para revisarlo rápido en una llamada?",
                "accion_siguiente": "Agendar Llamada",
                "estado_pipeline": "Objecion"
            }

    def ejecutar(self, leads_contactados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ejecuta el flujo completo del Gestor: Recibe respuestas -> Maneja objeciones -> Actualiza Pipeline
        """
        print("\n" + "="*50)
        print("🛡️ INICIANDO AGENTE GESTOR")
        print("="*50)
        
        if not leads_contactados:
            print("⚠️ [Gestor] No hay leads contactados para gestionar.")
            return []
            
        leads_gestionados = []
        
        for lead in leads_contactados:
            print(f"📞 [Gestor] Gestionando a {lead.get('nombre')}...")
            
            # 1. Simular la respuesta del lead
            respuesta_lead = self.simular_respuesta_lead(lead)
            print(f"   💬 Respuesta del lead: '{respuesta_lead}'")
            
            if respuesta_lead == "Ignorado":
                # Lógica de seguimiento (Follow-up)
                lead_actualizado = {
                    **lead,
                    "respuesta_lead": None,
                    "interaccion_gestor": {
                        "clasificacion": "Sin Respuesta",
                        "respuesta_gestor": f"Hola {lead.get('nombre')}, ¿pudiste ver el clip que te envié? Solo quiero saber si te es útil.",
                        "accion_siguiente": "Seguimiento 1",
                        "estado_pipeline": "Contactado (Follow-up)"
                    }
                }
            else:
                # 2. Manejar la objeción o interés
                interaccion = self.manejar_objecion(lead, respuesta_lead)
                print(f"   🤖 Respuesta Gestor: '{interaccion.get('respuesta_gestor')}'")
                
                # 3. Actualizar el lead
                lead_actualizado = {
                    **lead,
                    "respuesta_lead": respuesta_lead,
                    "interaccion_gestor": interaccion,
                    "estado_pipeline": interaccion.get("estado_pipeline", "En Gestión")
                }
                
            leads_gestionados.append(lead_actualizado)
            
        # Filtrar leads que avanzan al Closer (Agendados o muy Interesados)
        leads_para_closer = [l for l in leads_gestionados if l.get('estado_pipeline') in ['Agendado', 'Interesado']]
        
        print(f"✅ [Gestor] Gestión completada. {len(leads_para_closer)} leads listos para el Closer.")
        return leads_gestionados # Devolvemos todos para el reporte, el orquestador filtrará

# Ejemplo de uso independiente
if __name__ == "__main__":
    # Lead de prueba
    lead_prueba = [{
        "nombre": "Carlos Mendoza",
        "pain_point": "Tiene mucho contenido largo pero no lo aprovecha en Shorts",
        "estado_pipeline": "Contactado"
    }]
    
    agente = GestorAgent()
    resultados = agente.ejecutar(lead_prueba)
    print(json.dumps(resultados, indent=2, ensure_ascii=False))
