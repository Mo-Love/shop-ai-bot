import requests
from bs4 import BeautifulSoup
import json

def scrape_bavovna():
    url = "https://bavovna.team/katalog/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Помилка доступу до сайту"

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    # Шукаємо контейнери товарів (класи можуть змінюватися, це приклад на основі стандартних сіток)
    items = soup.find_all('div', class_='product-card') # Слід уточнити клас через Inspect Element

    for item in items:
        # 1. Фото
        img_tag = item.find('img')
        img_url = img_tag.get('src') if img_tag else "Немає фото"

        # 2. Назва та посилання
        title_tag = item.find('a', class_='product-title')
        title = title_tag.text.strip() if title_tag else "Без назви"
        link = title_tag.get('href') if title_tag else ""

        # 3. Ціна
        price_tag = item.find('span', class_='price-value')
        price = price_tag.text.strip() if price_tag else "Ціна за запитом"

        # 4. Характеристики (зазвичай потребують переходу на сторінку товару)
        # Для прототипу ми можемо взяти короткий опис з картки
        desc_tag = item.find('div', class_='short-description')
        description = desc_tag.text.strip() if desc_tag else "Опис відсутній"

        products.append({
            "title": title,
            "price": price,
            "image": img_url,
            "description": description,
            "link": f"https://bavovna.team{link}"
        })

    return products

# Тестовий запуск
data = scrape_bavovna()
print(json.dumps(data[:3], indent=4, ensure_ascii=False)) # Покажемо перші 3 товари
