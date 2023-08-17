import os
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

# Configure the Voice Module
voice_name = EDGE_TTS_VOICENAME_MAPPING[Language.SPANISH]['male']
voice_module = EdgeTTSVoiceModule(voice_name)

# Prepare the script
script = "Generate a landscape video"

# Configure Content Engine
content_engine = ContentVideoEngine(voice_module, script, background_music_name='aidouaile', language=Language.CHINESE)

# Generate Content
for step_num, step_logs in content_engine.makeContent():
    print(f" {step_logs}")

# Get Video Output Path
print(content_engine.get_video_output_path())