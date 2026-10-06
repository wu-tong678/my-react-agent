import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=st.secrets.get("ZHIPU_API_KEY", os.getenv("ZHIPU_API_KEY")),
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

def call_llm(prompt):
    response = client.chat.completions.create(
        model="glm-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content