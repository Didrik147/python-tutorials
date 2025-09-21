import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.header('Simple Iris Flower Prediction App')
st.subheader('This app predicts the **Iris flower** type!')

st.sidebar.header('User Input Parameters')

