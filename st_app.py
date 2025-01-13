import streamlit as st
import pandas as pd
import openai
import ast
import os
import app

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('openai_key')

with open('instructions.txt', 'r') as file:
    instruction = file.read()

def scrape(features_dict):
    result_tables = []
    if features_dict['category'] == 'house':
        try:
            st.info("Please wait for Bina.az scraping...")
            bina_results = app.handle_house_search(features_dict)
            if bina_results:
                st.write("Bina.az Scraping Results")
                st.table(pd.DataFrame(bina_results))
            else:
                st.warning("No Bina.az item found for this filter")
        except Exception as e:
            st.error(f"Error with Bina.az scraping: {e}")

    if features_dict['category'] == 'other':
        try:
            st.info("Please wait for Tap.az scraping...")
            tapaz_results = app.handle_other_search(features_dict)
            if tapaz_results:
                st.write("Tap.az Scraping Results")
                st.table(pd.DataFrame(tapaz_results))
            else:
                st.warning("No Tap.az item found for this filter")
        except Exception as e:
            st.error(f"Error with Tap.az scraping: {e}")

        try:
            st.info("Please wait for Instagram scraping...")
            instagram_results = app.handle_instagram_search(features_dict)
            if instagram_results:
                st.write("Instagram Scraping Results")
                st.table(pd.DataFrame(instagram_results))
            else:
                st.warning("No Instagram item found for this filter")
        except Exception as e:
            st.error(f"Error with Instagram scraping: {e}")

def main():
    st.title("Item Scraping App")
    user_input = st.text_input("Enter Desired Item", "")
    if st.button("Submit"):
        if user_input:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": instruction},
                              {"role": "user", "content": user_input}]
                )
                features_dict = ast.literal_eval(response['choices'][0]['message']['content'])
                scrape(features_dict)
            except Exception as e:
                st.error(f"OpenAI Error: {e}")
        else:
            st.warning("Please enter an item.")

if __name__ == "__main__":
    main()