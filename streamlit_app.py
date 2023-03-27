import pandas as pd
import streamlit as st
import requests
import json

st.set_page_config(layout="wide", page_title="FindSexualHealth",
        page_icon="🩺")

def report_value(provider_id, feature, key):
    requests.post(f"https://a1zrpiqu6b.execute-api.eu-west-2.amazonaws.com/alpha/report?id={provider_id}&feature={feature}&key={key}")

def clean_str(string):
    return string.replace("_", " ").title()

def display_feature(feature_dict):
    for key, value in feature_dict.items():
        report_args = (provider_id, feature, key)
        col_1, col_2, col_3 = st.columns([2,7,1])
        col_1.write(clean_str(key))
        col_2.write(value["value"])
        col_3.button("Report", key=str(report_args), on_click=report_value, args=report_args)

response = requests.get('https://a1zrpiqu6b.execute-api.eu-west-2.amazonaws.com/alpha/providers')

data = json.loads(response.content)
data = {provider["id"]: {k: v for k, v in provider.items() if k != "id"} for provider in data}
# data


provider_id = st.selectbox("Select Provider:", data.keys(), format_func=lambda x: data[x]["name"]["0"]["value"])
provider = data[provider_id]


st.title(provider["name"]["0"]["value"]) 
st.write(provider_id)

features_to_display = ["address", "opening_times", "phones", "emails", "notes", "services"]
for feature in features_to_display:
    feature_dict = provider[feature]
    st.header(clean_str(feature))
    display_feature(feature_dict=feature_dict)