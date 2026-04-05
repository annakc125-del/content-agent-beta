import os
import json
import random
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class ProspectorAgent:
    """
    Agente Prospector (El Cazador)
    Rol: Identificar, raspar y calificar leads de alto valor (coaches e infoproductores).
    En esta versión Beta, simula la extracción de leads (ya que herramientas como Apify requieren cuentas externas)
    y utiliza OpenAI para calificar y puntuar cada lead basado en su perfil.
    """
    
    def __init__(self):
        # Inicializar cliente de OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4.1-mini"
        
        # Mercados objetivo
        self.mercados = ["USA Hispano", "España", "México"]
        
        # Base de datos simulada de leads crudos (antes de calificar)
        self.raw_leads = [
            {
                "nombre": "Carlos Mendoza",
                "plataforma": "YouTube",
                "url": "youtube.com/@carlosmendozacoach",
                "bio": "Ayudo a emprendedores a escalar a $10k/mes. +100 videos largos de masterclasses.",
                "seguidores": 45000,
                "mercado": "México",
                "actividad_shorts": "Baja"
            },
            {
                "nombre": "Laura Gómez",
                "plataforma": "LinkedIn",
                "url": "linkedin.com/in/lauragomez-finanzas",
                "bio": "Consultora Financiera B2B. Creadora del método 'Finanzas Libres'.",
                "seguidores": 12000,
                "mercado": "España",
                "actividad_shorts": "Nula"
            },
            {
                "nombre": "David Torres",
                "plataforma": "Instagram",
                "url": "instagram.com/davidtorres_fitness",
                "bio": "Coach de alto rendimiento para CEOs. Podcast semanal 'Cuerpo y Mente'.",
                "seguidores": 85000,
                "mercado": "USA Hispano",
                "actividad_shorts": "Media"
            },
            {
                "nombre": "Ana Silva",
                "plataforma": "YouTube",
                "url": "youtube.com/@anasilvamarketing",
                "bio": "Agencia de marketing digital. Tutoriales de 40 minutos sobre embudos de venta.",
                "seguidores": 25000,
                "mercado": "España",
                "actividad_shorts": "Baja"
            },
            {
                "nombre": "Miguel Ángel",
                "plataforma": "LinkedIn",
                "url": "linkedin.com/in/miguelangel-ventas",
                "bio": "Experto en ventas B2B. Autor del libro 'Cierre Despiadado'.",
                "seguidores": 8000,
                "mercado": "México",
                "actividad_shorts": "Nula"
            }
        ]

    def extraer_leads(self, cantidad: int = 5) -> List[Dict[str, Any]]:
        """
        Simula la extracción de leads usando herramientas como Apify o Phantombuster.
        """
        print(f"🔍 [Prospector] Extrayendo {cantidad} leads de LinkedIn, YouTube e Instagram...")
        # En un entorno real, aquí iría el código de scraping
        # Para la simulación, devolvemos una muestra de la base de datos
        return random.sample(self.raw_leads, min(cantidad, len(self.raw_leads)))

    def calificar_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Utiliza OpenAI para analizar el perfil del lead, asignarle una puntuación (0-100)
        y detectar su principal pain point (punto de dolor).
        """
        prompt = f"""
        Eres un experto calificador de leads B2B para una agencia de creación de contenido (Reels, Shorts, Clips).
        Tu objetivo es analizar el siguiente perfil y determinar si es un buen candidato para nuestro servicio High Ticket ($2,500 - $5,000).
        
        Perfil del Lead:
        - Nombre: {lead['nombre']}
        - Plataforma Principal: {lead['plataforma']}
        - Bio/Descripción: {lead['bio']}
        - Seguidores: {lead['seguidores']}
        - Mercado: {lead['mercado']}
        - Actividad en formatos cortos (Shorts/Reels): {lead['actividad_shorts']}
        
        Criterios de calificación (Puntuación 0-100):
        - Tiene contenido largo (podcasts, webinars, masterclasses) que se puede reutilizar (+40)
        - Tiene audiencia establecida (>10k seguidores) (+30)
        - Su actividad en formatos cortos es Baja o Nula (+30)
        
        Devuelve ÚNICAMENTE un objeto JSON con la siguiente estructura:
        {{
            "puntuacion": [número del 0 al 100],
            "calificacion": ["Frío", "Tibio", "Caliente" - Caliente es > 80],
            "pain_point": [Una frase corta describiendo su mayor problema, ej: "Tiene mucho contenido largo pero no lo aprovecha en Shorts"],
            "angulo_venta": [Una frase corta sobre cómo abordarlo]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en prospección de ventas B2B. Responde solo en JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            analisis = json.loads(response.choices[0].message.content)
            
            # Combinar los datos originales con el análisis
            lead_calificado = {**lead, **analisis}
            return lead_calificado
            
        except Exception as e:
            print(f"❌ [Prospector] Error al calificar lead {lead['nombre']}: {str(e)}")
            # Fallback en caso de error
            return {
                **lead,
                "puntuacion": 50,
                "calificacion": "Tibio",
                "pain_point": "No detectado por error de API",
                "angulo_venta": "Abordaje genérico"
            }

    def ejecutar(self, cantidad: int = 5) -> List[Dict[str, Any]]:
        """
        Ejecuta el flujo completo del Prospector: Extraer -> Calificar -> Filtrar
        """
        print("\n" + "="*50)
        print("🚀 INICIANDO AGENTE PROSPECTOR")
        print("="*50)
        
        leads_crudos = self.extraer_leads(cantidad)
        leads_calificados = []
        
        for lead in leads_crudos:
            print(f"⚙️ [Prospector] Calificando a {lead['nombre']}...")
            lead_calificado = self.calificar_lead(lead)
            leads_calificados.append(lead_calificado)
            
        # Filtrar solo los leads "Calientes" o "Tibios" (puntuación > 60)
        leads_filtrados = [l for l in leads_calificados if l.get('puntuacion', 0) > 60]
        
        print(f"✅ [Prospector] Prospección completada. {len(leads_filtrados)} leads viables encontrados.")
        return leads_filtrados

# Ejemplo de uso independiente
if __name__ == "__main__":
    agente = ProspectorAgent()
    resultados = agente.ejecutar(3)
    print(json.dumps(resultados, indent=2, ensure_ascii=False))
