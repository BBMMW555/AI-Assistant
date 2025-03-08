import json
from pyarabic import araby

# نظام التعلم التكيفي
class AdaptiveLearner:
    def __init__(self):
        self.knowledge_file = "knowledge_base.json"
        self.knowledge = self.load_knowledge()
    def load_knowledge(self):
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "commands": {
                    "افتح المتصفح": {"action": "open_browser", "program": None},
                    "احفظ الملف": {"action": "save_file", "program": None}
                }
            }  
    def save_knowledge(self):
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=4)
    def learn_command(self, command, action, program_path=None):
        normalized = self.normalize_text(command)
        self.knowledge["commands"][normalized] = {
            "action": action,
            "program": program_path
        }
        self.save_knowledge()
    def normalize_text(self, text):
        """معالجة النص العربي بشكل متقدم"""
        text = araby.strip_diacritics(text)  # إزالة التشكيل
        text = araby.normalize_hamza(text)    # توحيد الهمزات
        return text.strip().lower()           # تحويل إلى حروف صغيرة
   
        """تطبيع النص العربي للمقارنة"""
        return araby.strip_diacritics(araby.normalize_hamza(text))

learner = AdaptiveLearner()