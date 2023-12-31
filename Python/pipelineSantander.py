# -*- coding: utf-8 -*-
"""SantanderDevWeek2023.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IklKfBrVX6kKJHoikjD_XvPmSjIPP7dd

# Extract
"""

#290 291 292

import pandas as pd

df = pd.read_csv("week.csv")
user_ids = df["UserID"].tolist()

print(user_ids)

api = "https://sdw-2023-prd.up.railway.app/users"

import requests as req
import json

def get_user(id):
  response = req.get(f'{api}/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

!pip install openai

apiKey = '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'

import openai

openai.api_key = apiKey

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model= "gpt-4",
    messages=[
        {
            'role': 'system',
            'content':'Você é um especialista em markting bancário'
        },
        {
            'role': 'user',
            'content': f"Crie uma menssagem para {user['name']} sobre a importância cos investimentos e senhas seguras (máximo de 100 caracteres)"
        }
    ]
  )
  response = completion.choices[0].message.content.strip('\"') #strp tira aspas duplas da resposta

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append(
      {
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/insurance.svg",
        "description": news
      }
  )

def update(user):
  response = req.put(f"{api}/{user[id]}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  situation = update(user)
  print(f"{user} atualizado? {situation}")