import edge_tts

async def ovoz_yarat(text, lang, user_id, call_id):
    try:
        voice_mapping = {
            "ru": "ru-RU-SvetlanaNeural",
            "en": "en-US-JennyNeural",
            "fr": "fr-FR-DeniseNeural",
            "de": "de-DE-KatjaNeural",
            "es": "es-ES-ElviraNeural",
            "it": "it-IT-IsabellaNeural",
            "uz": "uz-UZ-SardorNeural",
            "tr": "tr-TR-AhmetNeural",
        }
        
        voice = voice_mapping.get(lang, "en-US-JennyNeural")
        filename = f"voice_{user_id}_{call_id}.mp3"
        
        communicate = edge_tts.Communicate(text=text, voice=voice)
        await communicate.save(filename)
        
        return filename
    except:
        return None