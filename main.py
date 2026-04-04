import os
import json
from dotenv import load_dotenv
from agents.orchestrator import OrchestratorAgent
from agents.narrative_creator import NarrativeCreatorAgent
from agents.multimedia_producer import MultimediaProducerAgent

# Cargar variables de entorno
load_dotenv()

def main():
    """
    Flujo principal del Ecosistema de Agentes de IA Beta
    """
    print("🚀 Iniciando Ecosistema de Agentes de IA Beta...")
    
    # 1. Inicializar agentes
    orchestrator = OrchestratorAgent()
    narrative_creator = NarrativeCreatorAgent()
    multimedia_producer = MultimediaProducerAgent()
    
    # 2. Cargar datos de entrada (simulando la ingesta de un webhook)
    # En un entorno real, estos datos vendrían de n8n/Make
    video_path = os.getenv("INPUT_VIDEO", "examples/video_fuente.mp4")
    transcription_path = os.getenv("INPUT_TRANSCRIPTION", "examples/transcripcion.txt")
    brand_guidelines_path = os.getenv("BRAND_GUIDELINES", "examples/manual_marca.txt")
    
    try:
        with open(transcription_path, "r", encoding="utf-8") as f:
            transcription_text = f.read()
            
        with open(brand_guidelines_path, "r", encoding="utf-8") as f:
            brand_guidelines = f.read()
            
    except FileNotFoundError as e:
        print(f"❌ Error: No se encontraron los archivos de entrada. {e}")
        print("Asegúrate de ejecutar el script desde la raíz del proyecto y que los archivos existan.")
        return
        
    # 3. Paso 1: Orquestador y Curador
    print("\n--- PASO 1: ORQUESTADOR Y CURADOR ---")
    clips_data = orchestrator.extract_best_clips(transcription_text, num_clips=2)
    
    if not clips_data:
        print("❌ Fallo en la extracción de clips. Abortando flujo.")
        return
        
    # Guardar resultados intermedios
    with open("output/clips_extraidos.json", "w", encoding="utf-8") as f:
        json.dump(clips_data, f, indent=2, ensure_ascii=False)
        
    # 4. Paso 2: Creador de Narrativa
    print("\n--- PASO 2: CREADOR DE NARRATIVA ---")
    final_content = narrative_creator.generate_scripts_and_copy(clips_data, brand_guidelines)
    
    if not final_content:
        print("❌ Fallo en la generación de narrativa. Abortando flujo.")
        return
        
    # Guardar resultados finales
    with open("output/contenido_final.json", "w", encoding="utf-8") as f:
        json.dump(final_content, f, indent=2, ensure_ascii=False)
        
    # 5. Paso 3: Productor Multimedia
    print("\n--- PASO 3: PRODUCTOR MULTIMEDIA ---")
    # Iterar sobre los clips generados (ej. clip_spanish, clip_english)
    for clip_id, clip_info in final_content.items():
        if isinstance(clip_info, dict) and 'subtitles' in clip_info:
            output_video = multimedia_producer.process_video(video_path, clip_info, clip_id)
            if output_video:
                print(f"✅ Video final generado: {output_video}")
                
    print("\n🎉 Flujo completado exitosamente. Revisa la carpeta 'output/'.")

if __name__ == "__main__":
    # Crear carpeta de salida si no existe
    os.makedirs("output", exist_ok=True)
    main()
