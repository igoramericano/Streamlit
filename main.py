import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


#criar interface do streamlit
st.title("Análise de Ações com yFinance")
st.write(""" #App preço de ações
         ##permite analisar o desempenho de ações ao longo do tempo usando dados do yFinance.""") 