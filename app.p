import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Завантаження ключів
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Консультант магазину", page_icon="🛍️")
st.title("🛍️ AI Помічник магазину")

# 1. Імітація бази даних (сюди можна підключити сканер)
PRODUCTS = [
    {"title": "iPhone 15 Pro", "price": "45000 грн", "desc": "Колір Титан, 128ГБ"},
    {"title": "MacBook Air M2", "price": "52000 грн", "desc": "13 дюймів, 8/256ГБ"},
    {"title": "AirPods Pro 2", "price": "10500 грн", "desc": "З шумопоглинанням"}
]

# 2. Ініціалізація історії чату
if "messages" not in st.session_state:
    st.session_state.messages = []

# Відображення історії повідомлень
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Логіка спілкування
if prompt := st.chat_input("Який товар вас цікавить?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Формуємо контекст для OpenAI
        system_prompt = f"""
        Ти — експерт-консультант магазину електроніки. 
        Ось список доступних товарів: {PRODUCTS}.
        Відповідай ввічливо. Якщо клієнт питає про товар, якого немає — пропонуй схожий.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
