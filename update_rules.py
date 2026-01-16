import requests
import os
from datetime import datetime

# --- НАСТРОЙКИ ---
SOURCE_URL = "https://raw.githubusercontent.com/Internet-Helper/GeoHideDNS/refs/heads/main/hosts/hosts"
CUSTOM_FILE = "custom_domains.txt"
OUTPUT_FILE = "my_ready_rules.txt"
LIMIT = 1000  # Твой новый лимит

# Категории и ключевые слова для поиска в источнике
CATEGORIES = {
    "OPENAI": ["openai", "chatgpt", "oaistatic", "oaiusercontent", "sora.com"],
    "GOOGLE": ["google", "gemini", "googleapis", "withgoogle", "pki.goog", "notebooklm", "clients6.google"],
    "GROK": ["grok", "x.ai"],
    "DEEPL": ["deepl"],
    "CLAUDE": ["claude", "anthropic"],
    "OTHER": [] # Сюда попадут домены из custom_domains, не подошедшие под ключи выше
}

def main():
    unique_domains = set()
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    # Структура для хранения правил по группам
    classified_rules = {cat: [] for cat in CATEGORIES}

    # Вспомогательная функция для определения категории
    def get_category(domain):
        for cat, keywords in CATEGORIES.items():
            if any(key in domain for key in keywords):
                return cat
        return "OTHER"

    # 1. ОБРАБОТКА ЛИЧНОГО ФАЙЛА (custom_domains.txt)
    # Эти домены попадают в список первыми и имеют приоритет
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().lower().split()
                if len(parts) >= 2:
                    ip, domain = parts[0], parts[1]
                    if domain not in unique_domains:
                        unique_domains.add(domain)
                        cat = get_category(domain)
                        classified_rules[cat].append(f"||{domain}^$dnsrewrite={ip}")

    # 2. СБОР ДОМЕНОВ ИЗ ИНТЕРНЕТ-ИСТОЧНИКА
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                # Убираем лишние пробелы и приводим к нижнему регистру
                line = line.strip().lower()
                
                # Игнорируем пустые строки, комментарии и блокировки (0.0.0.0)
                if not line or line.startswith(('#', '0.0.0.0')):
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    # parts[0] — это IP прокси, parts[1] — домен
                    ip = parts[0]
                    domain = parts[1].replace("http://", "").replace("https://", "").split('/')[0]
                    
                    # Проверяем, подходит ли домен под наши ключевые слова
                    cat = get_category(domain)
                    if cat != "OTHER": # Если нашли совпадение по ключам
                        if domain not in unique_domains:
                            if len(unique_domains) < LIMIT:
                                unique_domains.add(domain)
                                classified_rules[cat].append(f"||{domain}^$dnsrewrite={ip}")
    except Exception as e:
        print(f"Ошибка при загрузке источника: {e}")

    # 3. ФОРМИРОВАНИЕ ИТОГОВОГО ФАЙЛА
    total_rules = len(unique_domains)
    result = [
        f"! AI Unlocker Rules",
        f"! Обновлено: {now}",
        f"! Правил: {total_rules} из {LIMIT}",
        f"! Формат: AdGuard DNS Rewrite",
        ""
    ]

    # Добавляем правила в файл, разделяя их красивыми заголовками
    for cat in CATEGORIES:
        if classified_rules[cat]:
            result.append(f"! --- {cat} ---")
            # Сортируем правила внутри категории для порядка
            result.extend(sorted(classified_rules[cat]))
            result.append("")

    # Записываем результат
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    
    print(f"Успешно! Собрано правил: {total_rules}")

if __name__ == "__main__":
    main()
