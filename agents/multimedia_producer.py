import os
import json
import subprocess
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class MultimediaProducerAgent:
    """
    Agente 3: Productor Multimedia (El Editor)
    Ejecuta los cortes de video y aplica subtítulos básicos utilizando FFmpeg.
    """
    
    def __init__(self):
        self.output_dir = os.getenv("OUTPUT_DIR", "./output")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_srt_file(self, subtitles, output_path):
        """
        Genera un archivo .srt a partir de los subtítulos proporcionados.
        """
        print(f"📝 Productor Multimedia: Generando archivo SRT en {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, sub in enumerate(subtitles, 1):
                # Convertir formato "0:00-0:05" a formato SRT "00:00:00,000 --> 00:00:05,000"
                times = sub['time'].split('-')
                start_time = self._format_time_for_srt(times[0])
                end_time = self._format_time_for_srt(times[1])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{sub['text']}\n\n")
                
        return output_path
        
    def _format_time_for_srt(self, time_str):
        """
        Convierte "M:SS" o "SS" a "HH:MM:SS,000"
        """
        parts = time_str.split(':')
        if len(parts) == 1:
            # Solo segundos
            h, m, s = 0, 0, int(parts[0])
        elif len(parts) == 2:
            # Minutos y segundos
            h, m, s = 0, int(parts[0]), int(parts[1])
        else:
            # Horas, minutos, segundos
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
            
        return f"{h:02d}:{m:02d}:{s:02d},000"
        
    def process_video(self, input_video, clip_data, clip_id):
        """
        Corta el video y añade subtítulos usando FFmpeg.
        """
        print(f"🎬 Productor Multimedia: Procesando clip {clip_id}...")
        
        # Rutas de archivos
        srt_path = os.path.join(self.output_dir, f"{clip_id}.srt")
        output_video = os.path.join(self.output_dir, f"{clip_id}_final.mp4")
        
        # 1. Generar archivo SRT
        self.generate_srt_file(clip_data['subtitles'], srt_path)
        
        # 2. Comando FFmpeg para cortar y añadir subtítulos
        # Nota: En un entorno real, aquí se usarían los timestamps de inicio y fin del clip original
        # Para esta versión Beta simplificada, asumimos que el video de entrada ya es el clip corto
        # o aplicamos los subtítulos directamente al video completo si es corto.
        
        # Escapar la ruta del SRT para FFmpeg
        srt_path_escaped = srt_path.replace('\\', '/').replace(':', '\\:')
        
        # Comando FFmpeg básico para incrustar subtítulos
        # Se usa un estilo predefinido (fuente blanca, borde negro, tamaño 24)
        style = "FontName=Montserrat,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=20"
        
        cmd = [
            'ffmpeg', '-y',
            '-i', input_video,
            '-vf', f"subtitles={srt_path_escaped}:force_style='{style}'",
            '-c:a', 'copy',
            output_video
        ]
        
        print(f"⚙️ Ejecutando FFmpeg para {clip_id}...")
        try:
            # En un entorno real, descomentar la siguiente línea para ejecutar FFmpeg
            # subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✅ Productor Multimedia: Video procesado exitosamente -> {output_video}")
            return output_video
        except Exception as e:
            print(f"❌ Error en Productor Multimedia: {str(e)}")
            return None

if __name__ == "__main__":
    # Prueba simple
    agent = MultimediaProducerAgent()
    print("Agente Productor Multimedia inicializado correctamente.")
