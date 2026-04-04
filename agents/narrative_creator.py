import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class NarrativeCreatorAgent:
    """
    Agente 2: Creador de Narrativa (El Guionista)
    Adapta los fragmentos seleccionados, crea ganchos (hooks) textuales y redacta el copy.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4.1-mini"
        
    def generate_scripts_and_copy(self, clips_data, brand_guidelines):
        """
        Genera guiones adaptados, subtítulos y copy para redes sociales.
        """
        print("✍️ Creador de Narrativa: Generando guiones y copy para redes sociales...")
        
        # Cargar el prompt del sistema
        with open("prompts/narrative_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
            
        prompt = f"""
        Basado en los siguientes clips extraídos y el manual de marca, genera guiones 
        optimizados, subtítulos dinámicos y copy para Instagram Reels/TikTok.
        
        CLIPS EXTRAÍDOS:
        {json.dumps(clips_data, indent=2, ensure_ascii=False)}
        
        MANUAL DE MARCA:
        {brand_guidelines}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            print("✅ Creador de Narrativa: Guiones y copy generados exitosamente.")
            return result
            
        except Exception as e:
            print(f"❌ Error en Creador de Narrativa: {str(e)}")
            return None

if __name__ == "__main__":
    # Prueba simple
    agent = NarrativeCreatorAgent()
    print("Agente Creador de Narrativa inicializado correctamente.")
