import google.generativeai as genai
from IPython.display import Markdown
import json
GOOGLE_API_KEY = "AIzaSyB_83VMQrIQnHNEcY6iDE2SUcSnsGMd1Bw"

class MedicalDataAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def create_prompt(self, text):
        return f"""
        Проаналізуй наступний медичний текст та витягни з нього інформацію у форматі JSON.
        Шукай наступні поля:
        - Ім'я
        - Призвище
        - По-батькові
        - Стать (чоловіча - 1 або жіноча - 2)
        - Дата народження (ДД.ММ.РРРР)
        - Телефон мобільний (+хххххххххххх; замість х вставляти тільки цифри)
        - Телефон домашній (хххххххххх; замість х вставляти тільки цифри)
        - Місце проживання
        - Місце роботи
        - Посада
        - Диспансерна група (так - 1 або ні - 2)
        - Захворювання, з приводу яких пацієнта було взято на диспансерний облік
        - Контингент (інваліди війни - 1; учасники війни - 2; учасники бойових дій - 3; інваліди - 4; учасники ліквідації наслідків аварії на Чорнобильській АЕС - 5; евакуйовані - 6; особи, які проживають на території зони радіоекологічного контролю, - 7; діти, які народились від батьків, які віднесені до 1, 2, 3 категорій осіб, що постраждали внаслідок Чорнобильської катастрофи, із зони відчуження, а також відселені із зон безумовного (обов'язкового) і гарантованого добровільного відселення - 8; інші пільгові категорії - 9)
        - Номер посвідчення
        - Група крові (цифрою)
        - Резус-фактор (позитивний або негативний)
        - Переливання крові (коли, скільки)
        - Цукровий діабет 
        - Інфекційні захворювання
        - Хірургічні втручання
        - Алергологічний анамнез 
        - Непереносимість лікарських препаратів (негативні побічні дії лікарських засобів, вказати яких)   

        Текст для аналізу:
        {text}

        Якщо інформації для поля немає у тексті, вставляємо ''.
        Надай відповідь лише у форматі JSON без додаткових коментарів. 
        """

    def analyze_text(self, text):
        try:
            prompt = self.create_prompt(text)
            response = self.model.generate_content(prompt)

            try:
                data = json.loads(response.text)
            except json.JSONDecodeError:
                cleaned_text = response.text.strip()
                if cleaned_text.startswith('```json'):
                    cleaned_text = cleaned_text[7:-3]
                data = json.loads(cleaned_text)

            return data
        except Exception as e:
            return {"error": f"Помилка при аналізі тексту: {str(e)}"}

        return 0


def process_medical_data(api_key, text):
    """Головна функція для обробки медичних даних"""
    analyzer = MedicalDataAnalyzer(api_key)

    # Аналіз тексту
    result = analyzer.analyze_text(text)

    # Форматування та виведення результату
    formatted_output = analyzer.format_output(result)
    return formatted_output

def process(test_text):
    # Встановіть ваш API ключ


    # Обробка тексту
    result = process_medical_data(GOOGLE_API_KEY, test_text)
    print(result)
    print(type(result))