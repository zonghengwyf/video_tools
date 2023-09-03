import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
from shortGPT.config.api_db import ApiKeyManager, ApiProvider
from shortGPT.config.asset_db import AssetDatabase, AssetType
from shortGPT.engine.content_video_engine import ContentVideoEngine
from shortGPT.config.languages import Language
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule, EDGE_TTS_VOICENAME_MAPPING
OPENAI_KEY = os.environ.get('OPENAI_KEY')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
ELEVEN_LABS_KEY = os.environ.get('ELEVEN_LABS_KEY')

# Set API Keys
ApiKeyManager.set_api_key(ApiProvider.OPENAI, OPENAI_KEY)
ApiKeyManager.set_api_key(ApiProvider.PEXELS, PEXELS_KEY)

# Add Assets
AssetDatabase.add_local_asset('aidouaile', AssetType.AUDIO, "./aidouaile_zx.mp3")

video_language = Language.CHINESE
#video_language = Language.ENGLISH
#video_language = Language.SPANISH

# Configure the Voice Module
voice_name = EDGE_TTS_VOICENAME_MAPPING[video_language]['male']
voice_module = EdgeTTSVoiceModule(voice_name)

# Prepare the script
script = "当生活让你感到疲惫不堪时，不妨停下脚步，放松心情，看看周围的美好。或许是一只小鸟在树枝上欢快地歌唱，或许是一朵娇艳的鲜花在微风中轻轻摇曳，或许是一杯清香的茶在你的唇齿间缓缓流淌。生活中有太多美好的瞬间值得我们去发现和珍惜。让这些美好温暖你的心灵，让你的内心充满爱和希望，你会发现自己变得更加强大和坚定。"
#script = "Artificial intelligence is revolutionizing our world in an astonishing way. Robots and virtual assistants help us complete daily tasks and simplify our lives. In medicine, artificial intelligence allows for more accurate diagnosis and treatment progress. In the automotive industry, autonomous vehicles are changing our way of transportation. However, people have raised doubts about the impact and ethics of its use on employment. Despite facing challenges, artificial intelligence still promises an exciting and promising future. Are we ready to accept this technological advancement?"
#script = "La inteligencia artificial (IA) está revolucionando nuestro mundo de manera sorprendente. Los robots y asistentes virtuales nos ayudan en nuestras tareas diarias y simplifican nuestra vida. En la medicina, la IA permite diagnósticos más precisos y avances en tratamientos. En la industria automotriz, los vehículos autónomos están cambiando la forma en que nos desplazamos. Sin embargo, surgen interrogantes sobre el impacto en el empleo y la ética de su uso. A pesar de los desafíos, la IA promete un futuro emocionante y lleno de posibilidades. ¿Estamos preparados para abrazar este avance tecnológico?"



# Configure Content Engine
content_engine = ContentVideoEngine(voice_module, script, background_music_name='aidouaile', language=video_language)

# Generate Content
for step_num, step_logs in content_engine.makeContent():
    print(f" {step_logs}")

# Get Video Output Path
print(content_engine.get_video_output_path())
