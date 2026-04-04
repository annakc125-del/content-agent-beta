import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class OrchestratorAgent:
    """
    Agente 1: Orquestador y Curador (El Director)
    Recibe el material, gestiona la transcripción y selecciona los mejores fragmentos.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4.1-mini"
        
    def extract_best_clips(self, transcription_text, num_clips=3):
        """
        Analiza la transcripción y extrae los mejores momentos para clips cortos.
        """
        print(f"🎬 Orquestador: Analizando transcripción para extraer {num_clips} clips...")
        
        # Cargar el prompt del sistema
        with open("prompts/orchestrator_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
            
        prompt = f"""
        Analiza la siguiente transcripción y extrae los {num_clips} mejores momentos que tengan 
        potencial viral para redes sociales (TikTok, Reels, Shorts).
        
        TRANSCRIPCIÓN:
        {transcription_text}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            print("✅ Orquestador: Clips extraídos exitosamente.")
            return result
            
        except Exception as e:
            print(f"❌ Error en Orquestador: {str(e)}")
            return None

if __name__ == "__main__":
    # Prueba simple
    agent = OrchestratorAgent()
    print("Agente Orquestador inicializado correctamente.")
