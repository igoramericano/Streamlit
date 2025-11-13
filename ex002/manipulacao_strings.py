def inverter_string(s):
    return s[::-1]
def contar_palavras(s):
    return len(s.split())
def verificar_palindromo(s):
    s = s.replace(" ", "").lower()
    if s == s[::-1]: 
        return Tru
    else:
        return False