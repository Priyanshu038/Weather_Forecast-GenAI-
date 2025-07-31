import streamlit as st
import requests
import openai
from datetime import datetime

# WEATHER API CALL
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("API Error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Exception occurred:", str(e))
        return None

# OPENAI DESCRIPTION GENERATOR
from openai import OpenAI  # Make sure you're using the correct import

def generate_weather_description(data, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    try:
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        prompt = f"The current weather in your city is {desc} with a temperature of {temp:.1f}°C. Write a friendly one-line summary."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating description: {e}"


# OPTIONAL: WEEKLY FORECAST MOCKUP (not used currently)
def get_weekly_forecast(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Forecast API Error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Exception occurred:", str(e))
        return None

# STREAMLIT APP MAIN
def main():
    st.sidebar.title("Weather Forecasting with LLM")
    city = st.sidebar.text_input("Enter city name", "London")

    # Using your provided keys
    weather_api_key = "de8c974f57ec8ed07bff14b8f415fe49"
    openai_api_key = "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"


    submit = st.sidebar.button("Get Weather")

    if submit:
        st.title(f"Weather Update for {city}")
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(city, weather_api_key)
            print("Weather Data:", weather_data)

            if weather_data is not None and weather_data.get("cod") == 200:
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Temperature", f"{weather_data['main']['temp']:.2f} °C")
                    st.metric("Humidity", f"{weather_data['main']['humidity']} %")

                with col2:
                    st.metric("Pressure", f"{weather_data['main']['pressure']} hPa")
                    st.metric("Wind Speed", f"{weather_data['wind']['speed']} m/s")

                weather_description = generate_weather_description(weather_data, openai_api_key)
                st.write(weather_description)

            else:
                st.error("❌ Failed to fetch weather data. Please check the city name or try again later.")

if __name__ == "__main__":
    main()
