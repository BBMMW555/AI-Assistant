import pyttsx3
from langdetect import detect
from transformers import pipeline

class Voic:
    def __init__(self):
        """تهيئة محرك تحويل النص إلى كلام"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # سرعة الكلام
        self.engine.setProperty('volume', 1.0)  # مستوى الصوت (0.0 إلى 1.0)

        # تحديد صوت يتحدث العربية إذا كان متاحًا
        voices = self.engine.getProperty('voices')
        arabic_voice_found = False
        for voice in voices:
            if 'arabic' in voice.languages or 'ar_' in voice.id:
                self.engine.setProperty('voice', voice.id)
                arabic_voice_found = True
                break
        if not arabic_voice_found:
            print("تحذير: لم يتم العثور على صوت عربي. سيتم استخدام الصوت الافتراضي.")

        # تحميل نموذج AraGPT للردود الذكية
        self.chatbot = pipeline("text-generation", model="aubmindlab/aragpt2-base")

    def speak(self, text):
        """تحويل النص إلى كلام"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"حدث خطأ أثناء تحويل النص إلى كلام: {e}")

    def detect_language(self, text):
        """الكشف عن لغة النص"""
        try:
            return detect(text)
        except Exception as e:
            print(f"حدث خطأ أثناء الكشف عن اللغة: {e}")
            return "unknown"

    def respond(self, text):
        """الرد على الرسالة باستخدام AraGPT"""
        try:
            # استخدام AraGPT لإنشاء رد ذكي
            response = self.chatbot(text, max_length=50, num_return_sequences=1)
            return response[0]['generated_text']
        except Exception as e:
            print(f"حدث خطأ أثناء إنشاء الرد: {e}")
            return "آسف، حدث خطأ أثناء معالجة طلبك."


# مثال على كيفية استخدام الكلاس
if __name__ == "__main__":
    vi = Voic()
    vi.speak("مرحبًا! أنا مساعدك الذكي.")
    print(vi.detect_language("مرحبًا، كيف حالك؟"))
    print(vi.respond("مرحبًا، كيف حالك؟"))