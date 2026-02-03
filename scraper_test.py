import requests
from bs4 import BeautifulSoup
import json

def test_parse(url):
    print(f"🔍 Починаємо сканування: {url}")
    
    # Імітуємо браузер, щоб сайт нас не заблокував
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        
        # УВАГА: Тут треба вказати правильні класи для вашого сайту
        # Наприклад, якщо кожен товар лежить у <div class="product-card">
        items = soup.find_all('div', class_='product-card') # Змініть клас на реальний
        
        for item in items:
            name = item.find('h2').text.strip() if item.find('h2') else "Назва не знайдена"
            price = item.find('span', class_='price').text.strip() if item.find('span', class_='price') else "Ціна не вказана"
            link = item.find('a')['href'] if item.find('a') else "#"
            
            products.append({
                "name": name,
                "price": price,
                "link": link
            })
        
        return products

    except Exception as e:
        return f"❌ Помилка: {e}"

# ТЕСТ (підставте посилання на реальний магазин або категорію)
URL = "https://example-shop.com/category/phones" 
results = test_parse(URL)

print(json.dumps(results, indent=4, ensure_ascii=False))
print(f"\n✅ Знайдено товарів: {len(results)}")
