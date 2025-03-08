import pyttsx3

class MultiLangTTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

    def set_voice_by_lang(self, lang='ar'):
        """تعيين الصوت بناءً على اللغة"""
        for voice in self.voices:
            if lang == 'ar' and ('ar' in voice.languages or 'arabic' in voice.name.lower()):
                self.engine.setProperty('voice', voice.id)
                print(f"تم تعيين الصوت العربي: {voice.name}")
                return
            elif lang == 'en' and ('en' in voice.languages or 'english' in voice.name.lower()):
                self.engine.setProperty('voice', voice.id)
                print(f"تم تعيين الصوت الإنجليزي: {voice.name}")
                return
        raise Exception(f"لم يتم العثور على صوت للغة: {lang}")

    def speak(self, text, lang='ar'):
        """توليف الكلام باللغة المحددة"""
        self.set_voice_by_lang(lang)
        self.engine.say(text)
        self.engine.runAndWait()