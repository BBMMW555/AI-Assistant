import pyaudio
from vosk import Model, KaldiRecognizer
import json

class Spee:
    def __init__(self, model_path):
        """
        تهيئة التعرف على الكلام باستخدام نموذج Vosk.
        
        :param model_path: المسار إلى نموذج Vosk.
        """
        # تحميل النموذج
        self.model = Model(model_path)
        
        # إنشاء كائن للتعرف على الكلام
        self.recognizer = KaldiRecognizer(self.model, 16000)
        
        # تهيئة تسجيل الصوت
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )
        print("تم تهيئة التعرف على الكلام بنجاح.")

    def listen(self):
        """
        الاستماع إلى الصوت وتحويله إلى نص.
        
        :return: النص الذي تم التعرف عليه.
        """
        print("يُرجى التحدث الآن...")
        while True:
            data = self.stream.read(4096, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '')

                if text:
                    print(f"تم التعرف على النص: {text}")
                    return text

    def close(self):
        """إغلاق تدفق الصوت وإطلاق الموارد."""
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("تم إغلاق تدفق الصوت بنجاح.")


# مثال على كيفية استخدام الكلاس
if __name__ == "__main__":
    sr = Spee("C:/Users/bassam/Desktop/mine_project/vosk-model-ar-0.22-linto-1.1.0")
    print(sr.listen())
    sr.close()