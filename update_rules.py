import requests
import os
from datetime import datetime

# --- НАСТРОЙКИ ---
SOURCE_URL = "https://raw.githubusercontent.com/Internet-Helper/GeoHideDNS/refs/heads/main/hosts/hosts"
CUSTOM_FILE = "custom_domains.txt"
OUTPUT_FILE = "my_ready_rules.txt"
LIMIT = 100

# Категории для сортировки
CATEGORIES = {
    "OPENAI": ["openai", "chatgpt", "oaistatic", "oaiusercontent", "sora.com"],
    "GOOGLE": ["google", "gemini", "googleapis", "withgoogle", "pki.goog", "notebooklm"],
    "GROK": ["grok", "x.ai"],
    "DEEPL": ["deepl"],
    "CLAUDE": ["claude", "anthropic"],
    "OTHER": [] 
}

def main():
    user_domains = []
    source_data = {}
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    classified_rules = {cat: [] for cat in CATEGORIES}

    # 1. Читаем только те домены, которые ты сам вписал
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().lower().split()
                if parts:
                    domain = parts[-1] # Забираем домен (даже если в строке есть IP)
                    if domain and not domain.startswith(('#', '!')):
                        if domain not in user_domains and len(user_domains) < LIMIT:
                            user_domains.append(domain)

    if not user_domains:
        print("Ошибка: custom_domains.txt пуст!")
        return

    # 2. Получаем актуальную базу IP из интернета
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.splitlines():
                line = line.strip().lower()
                if not line or line.startswith(('#', '0.0.0.0')): continue
                
                parts = line.split()
                if len(parts) >= 2:
                    ip, domain = parts[0], parts[1]
                    source_data[domain] = ip
    except Exception as e:
        print(f"Ошибка загрузки базы: {e}")
        return

    # 3. Сопоставляем: берем IP из базы только для твоих доменов
    def get_category(d):
        for cat, keys in CATEGORIES.items():
            if any(k in d for k in keys): return cat
        return "OTHER"

    count = 0
    for domain in user_domains:
        if domain in source_data: # Проверяем наличие домена в источнике
            ip = source_data[domain]
            cat = get_category(domain)
            classified_rules[cat].append(f"||{domain}^$dnsrewrite={ip}")
            count += 1
        else:
            print(f"Внимание: Домен {domain} не найден в источнике и будет пропущен.")

    # 4. Записываем результат
    result = [
        f"! AI Unlocker Rules (Custom List)",
        f"! Обновлено: {now}",
        f"! Активных правил: {count} из {LIMIT}",
        ""
    ]

    for cat in CATEGORIES:
        if classified_rules[cat]:
            result.append(f"! --- {cat} ---")
            result.extend(sorted(classified_rules[cat]))
            result.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    
    print(f"Успешно! Сформировано правил: {count}")

if __name__ == "__main__":
    main()
