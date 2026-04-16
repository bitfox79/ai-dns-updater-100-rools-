import requests
import os
from datetime import datetime
from collections import defaultdict

# --- НАСТРОЙКИ ---
SOURCE_URL = "https://raw.githubusercontent.com/Internet-Helper/GeoHideDNS/refs/heads/main/hosts/hosts"
CUSTOM_FILE = "custom_domains.txt"
OUTPUT_FILE = "my_ready_rules.txt"

CATEGORIES = {
    "OPENAI": ["openai", "chatgpt", "oaistatic", "oaiusercontent", "sora.com"],
    "GOOGLE": ["google", "gemini", "googleapis", "withgoogle", "pki.goog", "notebooklm", "clients6.google"],
    "GROK": ["grok", "x.ai"],
    "DEEPL": ["deepl"],
    "CLAUDE": ["claude", "anthropic"],
    "OTHER": []
}

def get_category_name(domain):
    for name, keys in CATEGORIES.items():
        if any(k in domain for k in keys):
            return name
    return "OTHER"

def main():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # 1. Читаем домены из custom_domains.txt
    user_domains = []
    if os.path.exists(CUSTOM_FILE):
        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().lower().split()
                if parts:
                    domain = parts[-1]
                    if domain and not domain.startswith(('#', '!')):
                        if domain not in user_domains:
                            user_domains.append(domain)

    if not user_domains:
        print("Ошибка: custom_domains.txt пуст!")
        return

    # 2. Скачиваем базу — собираем ВСЕ IP для каждого домена (до 2 штук)
    source_data = defaultdict(list)  # domain -> [ip1, ip2]
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.splitlines():
                line = line.strip().lower()
                if not line or line.startswith(('#', '0.0.0.0')):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    ip, domain = parts[0], parts[1]
                    # Храним максимум 2 уникальных IP на домен
                    if ip not in source_data[domain] and len(source_data[domain]) < 2:
                        source_data[domain].append(ip)
        else:
            print(f"Ошибка HTTP: {response.status_code}")
            return
    except Exception as e:
        print(f"Ошибка загрузки базы: {e}")
        return

    # 3. Строим два списка правил
    rules_primary = []    # всегда первый IP
    rules_secondary = []  # второй IP если есть, иначе первый
    active_categories = set()

    for domain in user_domains:
        ips = source_data.get(domain)
        if not ips:
            continue  # домена нет в базе — пропускаем

        ip_primary = ips[0]
        ip_secondary = ips[1] if len(ips) > 1 else ips[0]

        rules_primary.append(f"||{domain}^$dnsrewrite={ip_primary}")
        rules_secondary.append(f"||{domain}^$dnsrewrite={ip_secondary}")
        active_categories.add(get_category_name(domain))

    # Сортируем оба списка по алфавиту
    rules_primary.sort()
    rules_secondary.sort()

    # Статистика двойных записей
    dual_count = sum(1 for d in user_domains if len(source_data.get(d, [])) > 1)
    single_count = sum(1 for d in user_domains if len(source_data.get(d, [])) == 1)
    missing_count = sum(1 for d in user_domains if not source_data.get(d))

    services_line = ", ".join(sorted(active_categories))

    # 4. Формируем итоговый файл
    result = []

    # --- Общая шапка ---
    result += [
        f"! AI Unlocker Rules (Custom List)",
        f"! Обновлено: {now}",
        f"! Сервисы: {services_line}",
        f"! Доменов с двумя IP: {dual_count} | с одним IP: {single_count} | не найдено: {missing_count}",
        f"! Всего правил в каждом списке: {len(rules_primary)}",
        f"!",
    ]

    # --- Список 1: Primary IP ---
    result += [
        f"! ============================================================",
        f"! СПИСОК 1 — PRIMARY IP (первый адрес)",
        f"! ============================================================",
    ]
    result.extend(rules_primary)

    # --- Разделитель ---
    result += [
        f"!",
        f"! ============================================================",
        f"! СПИСОК 2 — SECONDARY IP (второй адрес, или первый если один)",
        f"! ============================================================",
    ]
    result.extend(rules_secondary)

    # 5. Записываем файл
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))

    print(f"Готово!")
    print(f"  Правил в каждом списке: {len(rules_primary)}")
    print(f"  Доменов с двумя IP:     {dual_count}")
    print(f"  Доменов с одним IP:     {single_count}")
    print(f"  Не найдено в базе:      {missing_count}")
    print(f"  Файл: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
