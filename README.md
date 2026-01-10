# ai-dns-updater
Конечно! Давай соберем всё воедино. Теперь у тебя будет четкий план действий и готовый код.

### 📝 Твой план действий в репозитории GitHub:

Тебе нужно создать **3 файла**. Вот их названия и содержимое:

---

#### 1. Файл `custom_domains.txt`

В этот файл просто копируй домены списком. Я уже убрал IP-адреса и лишний текст для тебя. Просто создай файл и вставь это:

```text
gemini.google.com
aistudio.google.com
generativelanguage.googleapis.com
aitestkitchen.withgoogle.com
aisandbox-pa.googleapis.com
webchannel-alkalimakersuite-pa.clients6.google.com
alkalimakersuite-pa.clients6.google.com
assistant-s3-pa.googleapis.com
proactivebackend-pa.googleapis.com
robinfrontend-pa.googleapis.com
o.pki.goog
labs.google
notebooklm.google.com
jules.google.com
stitch.withgoogle.com
chatgpt.com
ab.chatgpt.com
auth.openai.com
auth0.openai.com
platform.openai.com
cdn.oaistatic.com
files.oaiusercontent.com
cdn.auth0.com
tcr9i.chat.openai.com
webrtc.chatgpt.com
android.chat.openai.com
api.openai.com
operator.chatgpt.com
sora.chatgpt.com
sora.com
videos.openai.com
ios.chat.openai.com
grok.com
accounts.x.ai
assets.grok.com
deepl.com
www.deepl.com
www2.deepl.com
login-wall.deepl.com
w.deepl.com
s.deepl.com
dict.deepl.com
ita-free.www.deepl.com
write-free.www.deepl.com
experimentation.deepl.com
experimentation-grpc.deepl.com
ita-free.app.deepl.com
shield.deepl.com
ott.deepl.com
api-free.deepl.com
backend.deepl.com
clearance.deepl.com
errortracking.deepl.com
auth.deepl.com
oneshot-free.www.deepl.com
checkout.www.deepl.com
gtm.deepl.com
claude.ai
console.anthropic.com
api.anthropic.com

```

---

#### 2. Файл `update_rules.py` ОТРЕДАКТИРОВАННЫЙ НИЖЕ

Создай этот файл и вставь туда этот «умный» код. Он сначала обработает твой список выше, а потом доберет новинки из интернета по ключевым словам.

```python
import requests
import os

# Настройки
SOURCE_URL = "https://raw.githubusercontent.com/ImMALWARE/dns.malw.link/master/hosts"
PROXY_IP = "185.87.51.182"
CUSTOM_FILE = "custom_domains.txt"
OUTPUT_FILE = "my_ready_rules.txt"

# Ключевые слова для авто-поиска новых поддоменов
KEYWORDS = [
    "openai", "chatgpt", "oaistatic", "oaiusercontent", "sora.com", 
    "google", "gemini", "googleapis", "withgoogle", "pki.goog", "notebooklm", 
    "claude", "anthropic", "grok", "x.ai", "deepl"
]

def main():
    unique_domains = set()
    result = ["! Сгенерировано автоматически: AI Unlocker", ""]

    # 1. Сначала берем домены из твоего личного файла custom_domains.txt
    result.append("! --- Личный список (custom_domains.txt) ---")
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            for line in f:
                domain = line.strip().lower()
                if domain and not domain.startswith(('#', '!', '185.', '0.')):
                    if domain not in unique_domains:
                        unique_domains.add(domain)
                        result.append(f"||{domain}^$dnsrewrite={PROXY_IP}")
    
    # 2. Затем добираем из интернета то, чего еще нет в списке
    try:
        response = requests.get(SOURCE_URL)
        if response.status_code == 200:
            result.append("\n! --- Авто-дополнение из интернета ---")
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip().lower()
                if not line or line.startswith('#'): continue
                
                parts = line.split()
                if len(parts) >= 2:
                    domain = parts[-1].replace("http://", "").replace("https://", "").split('/')[0]
                    
                    if any(key in domain for key in KEYWORDS):
                        if domain not in unique_domains:
                            unique_domains.add(domain)
                            result.append(f"||{domain}^$dnsrewrite={PROXY_IP}")
    except Exception as e:
        print(f"Ошибка сети: {e}")

    # 3. Сохраняем итоговый файл
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print(f"Успешно! Собрано {len(unique_domains)} доменов.")

if __name__ == "__main__":
    main()

```

---

#### 3. Файл `.github/workflows/main.yml`

Это сердце «робота». Создай папку `.github` (с точкой!), в ней папку `workflows`, а внутри файл `main.yml`.

```yaml
name: Update My AI Rules

on:
  schedule:
    - cron: '0 5 * * *' # Авто-запуск каждый день в 5 утра
  workflow_dispatch:   # Кнопка для ручного запуска

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install requests
      - name: Run script
        run: python update_rules.py
      - name: Commit and push changes
        run: |
          git config --global user.name 'GitHub Action'
          git config --global user.email 'action@github.com'
          git add my_ready_rules.txt
          git commit -m "Auto-update rules" || exit 0
          git push

```

---

### 🚀 Что делать после создания файлов:

1. Перейди во вкладку **Actions** в своем репозитории.
2. Нажми на **Update My AI Rules** слева.
3. Нажми кнопку **Run workflow** справа.
4. Через 30-60 секунд на главной странице твоего репозитория появится файл **`my_ready_rules.txt`**.

**Всё!** В этом файле будет готовый список. Тебе останется только копировать его содержимое и вставлять в AdGuard.

**Если захочешь добавить новый домен:** просто допиши его в `custom_domains.txt` на GitHub, нажми "Save" и снова нажми **Run workflow**. Робот всё пересоберет за тебя!

Нужно подсказать, как именно в GitHub создать папку с точкой `.github`, или ты знаешь? (Там нужно просто вводить название папки со слэшем, например: `.github/workflows/main.yml`)

так вроде все работает, единственное что, надо отредактировать немного, там в списке (на который ссылка ведет) есть адреса (путь к которым начинается на 0.0.0.0), это блокировщики рекламы, их не нужно обходить, вообще все что с 0.0.0.0 игнорировать нужно

Отличное замечание! В классических файлах `hosts` адрес `0.0.0.0` используется для того, чтобы «заглушить» (заблокировать) рекламные домены или трекеры. Если мы пропустим их через прокси, то вместо блокировки рекламы мы просто начнем её загружать через разблокировщик, что нам совсем не нужно.

Давай внесем это исправление в скрипт `update_rules.py`. Мы добавим условие: если строка начинается на `0.0.0.0`, мы её полностью игнорируем.

### Обновленный код для `update_rules.py`

Замени содержимое файла этим кодом:

```python
import requests
import os

# Настройки
SOURCE_URL = "https://raw.githubusercontent.com/ImMALWARE/dns.malw.link/master/hosts"
PROXY_IP = "185.87.51.182"
CUSTOM_FILE = "custom_domains.txt"
OUTPUT_FILE = "my_ready_rules.txt"

# Ключевые слова для авто-поиска
KEYWORDS = [
    "openai", "chatgpt", "oaistatic", "oaiusercontent", "sora.com", 
    "google", "gemini", "googleapis", "withgoogle", "pki.goog", "notebooklm", 
    "claude", "anthropic", "grok", "x.ai", "deepl"
]

def main():
    unique_domains = set()
    result = ["! Сгенерировано автоматически: AI Unlocker", "! Игнорирует 0.0.0.0 (рекламные блокировки)", ""]

    # 1. Сначала берем домены из твоего личного файла custom_domains.txt
    result.append("! --- Личный список (custom_domains.txt) ---")
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            for line in f:
                domain = line.strip().lower()
                # Пропускаем комментарии и технический мусор
                if domain and not domain.startswith(('#', '!', '0.0.0.0')):
                    if domain not in unique_domains:
                        unique_domains.add(domain)
                        result.append(f"||{domain}^$dnsrewrite={PROXY_IP}")
    
    # 2. Затем добираем из интернета новинки
    try:
        response = requests.get(SOURCE_URL)
        if response.status_code == 200:
            result.append("\n! --- Авто-дополнение из интернета ---")
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip().lower()
                
                # ГЛАВНОЕ УЛУЧШЕНИЕ: Игнорируем блокировщики (0.0.0.0) и комментарии
                if not line or line.startswith(('#', '0.0.0.0')):
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    # Домен всегда идет последним словом в строке
                    domain = parts[-1].replace("http://", "").replace("https://", "").split('/')[0]
                    
                    # Проверяем по ключевым словам
                    if any(key in domain for key in KEYWORDS):
                        if domain not in unique_domains:
                            unique_domains.add(domain)
                            result.append(f"||{domain}^$dnsrewrite={PROXY_IP}")
    except Exception as e:
        print(f"Ошибка сети: {e}")

    # 3. Сохраняем итоговый файл
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print(f"Успешно! Собрано {len(unique_domains)} доменов.")

if __name__ == "__main__":
    main()

```

### Что изменилось:

* В строке `if not line or line.startswith(('#', '0.0.0.0')):` я добавил проверку на `0.0.0.0`.
* Теперь, если скрипт видит что-то вроде `0.0.0.0 analytics.google.com`, он просто перешагнет через эту строку, потому что она предназначена для блокировки рекламы, а не для работы сервиса.

### Как обновить:

1. Зайди в свой репозиторий на GitHub.
2. Открой файл `update_rules.py`.
3. Нажми на иконку **карандаша** (Edit).
4. Сотри старый код, вставь этот новый.
5. Нажми **Commit changes**.
6. Перейди во вкладку **Actions** и снова нажми **Run workflow**, чтобы пересобрать список.

**Есть ли еще какие-то строки в исходном списке, которые показались тебе подозрительными или лишними?**
