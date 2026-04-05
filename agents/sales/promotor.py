import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class PromotorAgent:
    """
    Agente Promotor (El Francotirador)
    Rol: Iniciar el contacto en frío con mensajes hiper-personalizados y enviar la "prueba de valor".
    Recibe la lista de leads del Prospector y genera mensajes para LinkedIn DM y Email.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4.1-mini"
        
    def generar_prueba_valor(self, lead: Dict[str, Any]) -> str:
        """
        Simula la creación de un clip de muestra (la "prueba de valor").
        En un entorno real, esto llamaría al Agente Productor Multimedia.
        Aquí generamos una descripción atractiva del clip que supuestamente se creó.
        """
        tema = lead.get('bio', 'tu contenido').split('.')[0]
        return f"Clip de 45s sobre '{tema}' con subtítulos dinámicos estilo Hormozi y tu paleta de colores."

    def redactar_mensaje(self, lead: Dict[str, Any], prueba_valor: str) -> Dict[str, str]:
        """
        Utiliza OpenAI para redactar mensajes hiper-personalizados basados en el perfil del lead.
        Genera versiones en Español e Inglés, adaptadas para LinkedIn DM y Email.
        """
        prompt = f"""
        Eres un experto copywriter de ventas B2B (Agente Promotor).
        Tu objetivo es redactar mensajes de prospección en frío (Cold Outreach) para vender un servicio High Ticket ($2,500) de creación de contenido (Reels/Shorts).
        
        Perfil del Lead:
        - Nombre: {lead.get('nombre', 'Prospecto')}
        - Plataforma: {lead.get('plataforma', 'Redes Sociales')}
        - Bio: {lead.get('bio', '')}
        - Pain Point detectado: {lead.get('pain_point', 'Falta de tiempo para editar')}
        - Ángulo de venta: {lead.get('angulo_venta', 'Ahorro de tiempo y más alcance')}
        - Prueba de valor generada (Clip de muestra): {prueba_valor}
        
        Instrucciones para los mensajes:
        1. Tono: Directo, profesional, al grano, sin rodeos. Nada de "espero que estés bien".
        2. Estructura: Gancho personalizado -> El problema que notaste -> La solución (Prueba de valor) -> Llamado a la acción (CTA) de baja fricción.
        3. Longitud: Máximo 4-5 líneas.
        
        Devuelve ÚNICAMENTE un objeto JSON con la siguiente estructura:
        {{
            "linkedin_es": "Mensaje para LinkedIn DM en Español",
            "email_es_asunto": "Asunto del email en Español",
            "email_es_cuerpo": "Cuerpo del email en Español",
            "linkedin_en": "Mensaje para LinkedIn DM en Inglés",
            "email_en_asunto": "Asunto del email en Inglés",
            "email_en_cuerpo": "Cuerpo del email en Inglés"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en cold outreach B2B. Responde solo en JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.4
            )
            
            mensajes = json.loads(response.choices[0].message.content)
            return mensajes
            
        except Exception as e:
            print(f"❌ [Promotor] Error al redactar mensaje para {lead.get('nombre')}: {str(e)}")
            # Fallback
            return {
                "linkedin_es": f"Hola {lead.get('nombre')}, vi tu contenido. Hice este clip de prueba para ti: [ENLACE]. ¿Te interesa escalar esto a 30 videos al mes?",
                "email_es_asunto": "Tu contenido / Dinero sobre la mesa",
                "email_es_cuerpo": f"Hola {lead.get('nombre')}, hice este clip de prueba basado en tu último video: [ENLACE]. ¿Hablamos?",
                "linkedin_en": f"Hi {lead.get('nombre')}, saw your content. Made this sample clip for you: [LINK]. Open to scaling this to 30 videos/month?",
                "email_en_asunto": "Your content / Money on the table",
                "email_en_cuerpo": f"Hi {lead.get('nombre')}, made this sample clip based on your last video: [LINK]. Worth a chat?"
            }

    def ejecutar(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ejecuta el flujo completo del Promotor: Recibe leads -> Genera prueba de valor -> Redacta mensajes
        """
        print("\n" + "="*50)
        print("🎯 INICIANDO AGENTE PROMOTOR")
        print("="*50)
        
        if not leads:
            print("⚠️ [Promotor] No se recibieron leads para procesar.")
            return []
            
        leads_procesados = []
        
        for lead in leads:
            print(f"✍️ [Promotor] Redactando mensajes para {lead.get('nombre')}...")
            
            # 1. Generar la "prueba de valor" (simulada)
            prueba_valor = self.generar_prueba_valor(lead)
            
            # 2. Redactar los mensajes personalizados
            mensajes = self.redactar_mensaje(lead, prueba_valor)
            
            # 3. Actualizar el lead con los mensajes y cambiar su estado
            lead_actualizado = {
                **lead,
                "prueba_valor": prueba_valor,
                "mensajes_outreach": mensajes,
                "estado_pipeline": "Contactado" # Estado inicial para el Gestor
            }
            
            leads_procesados.append(lead_actualizado)
            
        print(f"✅ [Promotor] Campaña preparada para {len(leads_procesados)} leads.")
        return leads_procesados

# Ejemplo de uso independiente
if __name__ == "__main__":
    # Lead de prueba
    lead_prueba = [{
        "nombre": "Carlos Mendoza",
        "plataforma": "YouTube",
        "bio": "Ayudo a emprendedores a escalar a $10k/mes. +100 videos largos de masterclasses.",
        "pain_point": "Tiene mucho contenido largo pero no lo aprovecha en Shorts",
        "angulo_venta": "Mostrarle cómo un solo webinar puede generar 10 Shorts virales"
    }]
    
    agente = PromotorAgent()
    resultados = agente.ejecutar(lead_prueba)
    print(json.dumps(resultados, indent=2, ensure_ascii=False))
