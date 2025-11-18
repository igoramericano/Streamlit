import ex005a as cv
import streamlit as st


while True:
    menu = int(input('1- converter C°/F°, 2- M/Ft, 3- Kg/Lb, 4- Sair'))
    if menu == 1:
        temperatura = cv.celsius_para_fahrenheit(float(input('Digite uma temperatura em Celcius para converter: ')))
        print(f'A temperatura foi de: {temperatura}')

    elif menu == 2:
        distancia =  cv.metros_para_pes(float(input('Digite o valor em metros para converter: ')))
        print(f'A distância foi de: {distancia}')

    elif menu == 3:
        massa = cv.kilos_para_libras(float(input('Digite o peso em kg para converter: ')))
        print(f'O valor inserido foi de: {massa}')
        
    elif menu == 4:
        break

    else:
        print('Insira um valor entre 1 e 3')