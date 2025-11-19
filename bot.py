from dotenv import load_dotenv
import os
load_dotenv()
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests

API_TOKEN = os.getenv("TG_TOKEN")
WEATHER_KEY = os.getenv("WEATHER_KEY")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_weather(city: str):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_KEY,
        "units": "metric",
        "lang": "ru"
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            data = response.json()
            err = data.get("message", "Ошибка")
            return {"error": err}
        data = response.json()
        main = data.get("main")
        weather_list = data.get("weather")
        temp = main["temp"]
        desc = weather_list[0]["description"]
        city_name = data["name"]
        return {
            "temp": temp,
            "desc": desc,
            "city": city_name
        }
    except Exception as e:
        return {"error": str(e)}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Напиши /weather чтобы узнать погоду")

@dp.message(Command("weather"))
async def weather_handler(message: types.Message):
    await message.answer("Напиши город:")

@dp.message()
async def city_handler(message: types.Message):
    city = message.text
    weather = get_weather(city)
    if "error" in weather:
        await message.answer(f"Ошибка: {weather['error']}")
        return
    text = (
        f"Погода в городе <b>{weather['city']}</b>\n"
        f"Температура: {weather['temp']}°C\n"
        f"Описание: {weather['desc']}"
    )
    await message.answer(text, parse_mode="HTML")

if __name__ == "__main__":
    dp.run_polling(bot)
