import manipulacao_strings as ms

try:
    s = input("Digite uma string (texto): ")

    if not s.strip():
        print("A string não pode estar vazia. Por favor, digite algum texto.")
    else:
        print("\n--- Resultados ---")
        
        print("String original:", s)
        print("String invertida:", ms.inverter_string(s))
        print("Número de palavras:", ms.contar_palavras(s))
        print("É palíndromo?", ms.verificar_palindromo(s))
        print("------------------")
        
except Exception as e:
    print(f"\nOcorreu um erro inesperado! Detalhes: {e}")