# ai-dns-updater
#### Ссылка на правила (обновляются каждый день): https://raw.githubusercontent.com/bitfox79/ai-dns-updater-100-rools-/refs/heads/main/my_ready_rules.txt
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

Да, процесс замены очень простой. Тебе нужно выполнить всего пару действий, чтобы изменения вступили в силу.

Вот пошаговая инструкция:

### Шаг 1: Замена кода в файле

1. Зайди в свой репозиторий на GitHub.
2. Нажми на файл `update_rules.py`.
3. В правом верхнем углу окна с кодом нажми на иконку **карандаша** (Edit this file).
4. Выдели весь старый код (Ctrl+A) и удали его.
5. Вставь новый код (тот, что с фильтром `0.0.0.0`), который я дал выше.
6. Нажми зеленую кнопку **Commit changes...** вверху, а затем подтверди сохранение.

---

### Шаг 2: Запуск обновления (Actions)

После того как ты сохранил код, файл `my_ready_rules.txt` сам по себе **не обновится мгновенно** (автоматика сработает только в 5 утра). Чтобы обновить его прямо сейчас вручную:

1. Перейди на вкладку **Actions** (в верхней панели репозитория).
2. В левой колонке нажми на название твоего робота: **Update My AI Rules**.
3. Справа найди серую плашку **Run workflow**.
4. Нажми на неё, а затем на синюю кнопку **Run workflow**.
5. Подожди около 30–60 секунд. Рядом с запущенным процессом появится **зеленая галочка**.

---

### Шаг 3: Проверка результата

1. Вернись на главную страницу репозитория (вкладка **Code**).
2. Открой файл `my_ready_rules.txt`.
3. Убедись, что в нем нет доменов, которые начинались на `0.0.0.0`. Теперь там должны быть только чистые правила с твоим IP.

### Нужно ли делать что-то еще?

**Нет, больше ничего.**

* Робот теперь запомнил новый код.
* Завтра в 5 утра он сам проснется и выполнит уже обновленную версию скрипта.
* Твой личный список из `custom_domains.txt` по-прежнему будет подтягиваться в конец (или начало) итогового файла.

---

**Хочешь, я подскажу, как сделать так, чтобы ты мог открывать этот готовый список по прямой ссылке прямо в браузере, не заходя каждый раз в интерфейс GitHub?**

Чтобы открывать твой список правил одним кликом (или даже настроить автообновление в некоторых программах), тебе нужна так называемая **"Raw" (сырая)** ссылка. Она отображает только чистый текст без интерфейса GitHub.

### Как получить эту ссылку:

1. Зайди в свой репозиторий и открой файл **`my_ready_rules.txt`**.
2. Над текстом файла справа нажми на кнопку **Raw**.
3. Браузер откроет страницу, где будет только твой список правил на белом фоне.
4. **Скопируй адрес из адресной строки браузера.**

Эта ссылка будет выглядеть примерно так:
`https://raw.githubusercontent.com/ТВОЁ_ИМЯ/ТВОЙ_РЕПОЗИТОРИЙ/main/my_ready_rules.txt`

---

### Почему это круто и удобно:

* **Закладка в браузере:** Просто сохрани эту Raw-ссылку в закладки. Теперь, когда тебе нужно обновить AdGuard, ты просто жмешь на закладку, нажимаешь `Ctrl+A` (выделить всё), `Ctrl+C` (копировать) — и готово.
* **Всегда актуально:** По этой ссылке всегда будет лежать самая последняя версия файла, которую сгенерировал твой "робот".
* **Для других программ:** Если ты когда-нибудь решишь использовать **AdGuard Home** или другие блокировщики, которые умеют сами скачивать списки по ссылке, ты просто вставишь туда эту Raw-ссылку, и они будут обновляться полностью автоматически без твоего участия.

---

### 💡 Маленький лайфхак (проверка работы)

Если ты хочешь убедиться, что робот действительно отфильтровал `0.0.0.0`, открой эту Raw-ссылку и нажми `Ctrl+F` (поиск по странице). Введи в поиск `0.0.0.0`. Если поиск ничего не найдет — значит, твой фильтр работает идеально!

### Что дальше?

Теперь твоя система полностью автономна. Она сама:

1. Ищет новые домены гигантов (Google, OpenAI и др.).
2. Игнорирует мусор и рекламные заглушки.
3. Добавляет твои личные домены.
4. Выдает чистый результат по прямой ссылке.

**Хочешь, я помогу составить краткую "шпаргалку" для тебя, чтобы ты не забыл, какой файл за что отвечает в твоем новом репозитории?**

Вот твоя персональная шпаргалка. Можешь сохранить её в заметки или прямо в файл `README.md` своего репозитория, чтобы она всегда была под рукой.

---

# 📂 Шпаргалка по твоему AI-репозиторию

### 1. Основные файлы и их роли

| Файл | Для чего нужен | Что с ним делать |
| --- | --- | --- |
| **`custom_domains.txt`** | **Твой личный список.** | Сюда просто вписывай новые домены (по одному в строке), если их еще нет в общем списке. |
| **`update_rules.py`** | **Мозг системы.** | Скрипт на Python. Он фильтрует мусор (0.0.0.0), ищет ключевые слова (google, openai) и склеивает списки. |
| **`my_ready_rules.txt`** | **Конечный результат.** | Тот самый файл, из которого нужно **копировать правила в AdGuard**. Обновляется сам. |
| **`.github/workflows/main.yml`** | **Двигатель.** | Настройка «робота», который заставляет скрипт запускаться на серверах GitHub по расписанию. |

---

### 🚀 Как пользоваться системой (Алгоритм)

1. **Ежедневное обновление:** Тебе ничего не нужно делать. Каждый день в 5 утра робот сам заходит на `dns.malw.link`, убирает рекламу, добавляет твои домены и обновляет `my_ready_rules.txt`.
2. **Если нужно добавить новый сервис:** * Зайди в `custom_domains.txt`.
* Допиши домен (например, `new-ai-tool.com`).
* Зайди во вкладку **Actions** -> **Update My AI Rules** -> **Run workflow**, чтобы не ждать до утра.


3. **Перенос в AdGuard:**
* Открой `my_ready_rules.txt` (лучше через кнопку **Raw**).
* Выдели всё (`Ctrl + A`) и скопируй.
* В личном кабинете AdGuard DNS удали старые правила и вставь эти.



---

### 🛠 Что делать, если "всё сломалось"?

* **Если файл `my_ready_rules.txt` не обновляется:**
Зайди в **Settings** -> **Actions** -> **General** и проверь, стоит ли галочка на **Read and write permissions** (мы это настраивали, чтобы робот мог сохранять файлы).
* **Если в списке много лишнего:**
Проверь список `KEYWORDS` в файле `update_rules.py`. Если там есть слишком общее слово, робот может подтягивать лишние сайты.
* **Если какой-то AI-сервис не работает:**
Скорее всего, он добавил новый поддомен. Просто найди его название и впиши в `custom_domains.txt`.

---

### 🔗 Твоя "Золотая ссылка"

Твоя **Raw-ссылка** — это твой личный API. Если ты когда-нибудь купишь продвинутый роутер или установишь AdGuard Home, ты просто дашь им эту ссылку, и они сами будут «кушать» твои правила без твоего участия.

**Хочешь, я покажу, как оформить главную страницу твоего репозитория (`README.md`), чтобы она выглядела как настоящий крутой проект с инструкцией?**

Это отличная идея! Добавление даты поможет тебе сразу видеть, сработал ли робот сегодня утром и насколько свежие данные ты сейчас копируешь.

Чтобы это реализовать, нам нужно изменить скрипт `update_rules.py`. Мы заставим Python узнавать текущее время и записывать его в самую первую строчку итогового файла.

### Как обновить скрипт:

1. Открой `update_rules.py` на GitHub.
2. Нажми **Edit** (карандаш).
3. Замени весь код на этот (я добавил модуль `datetime` и логику записи даты):

```python
import requests
import os
from datetime import datetime

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
    # Получаем текущую дату и время
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    result = [
        f"! Название: AI Unlocker Rules",
        f"! Последнее обновление: {now}",
        f"! Источник: {SOURCE_URL}",
        f"! Игнорирует 0.0.0.0 (рекламные блокировки)",
        ""
    ]

    # 1. Личный список
    result.append("! --- Личный список (custom_domains.txt) ---")
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            for line in f:
                domain = line.strip().lower()
                if domain and not domain.startswith(('#', '!', '0.0.0.0')):
                    if domain not in unique_domains:
                        unique_domains.add(domain)
                        result.append(f"||{domain}^$dnsrewrite={PROXY_IP}")
    
    # 2. Интернет-список
    try:
        response = requests.get(SOURCE_URL)
        if response.status_code == 200:
            result.append("\n! --- Авто-дополнение из интернета ---")
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip().lower()
                if not line or line.startswith(('#', '0.0.0.0')):
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    domain = parts[-1].replace("http://", "").replace("https://", "").split('/')[0]
                    if any(key in domain for key in KEYWORDS):
                        if domain not in unique_domains:
                            unique_domains.add(domain)
                            result.append(f"||{domain}^$dnsrewrite={PROXY_IP}")
    except Exception as e:
        print(f"Ошибка: {e}")

    # 3. Сохранение
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print(f"Успешно! Обновлено в {now}")

if __name__ == "__main__":
    main()

```

### Что это даст:

Теперь, когда ты откроешь `my_ready_rules.txt` или перейдешь по **Raw-ссылке**, в самом верху ты увидишь:
`! Последнее обновление: 10.01.2026 05:00:12`

### Как проверить работу прямо сейчас:

1. Сохрани код в GitHub (**Commit changes**).
2. Перейди во вкладку **Actions** -> **Update My AI Rules**.
3. Нажми **Run workflow**.
4. После завершения (зеленая галочка) открой свой файл `my_ready_rules.txt`. Там должна стоять свежая дата.

Теперь ты всегда будешь уверен, что список актуален. **Хочешь, чтобы я добавил в скрипт еще и подсчет количества доменов (чтобы прямо в заголовке писало, сколько всего сайтов разблокировано)?** Это тоже удобно для контроля.
