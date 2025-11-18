import math

def area_quadrado(lado):
    return lado * lado

def perimetro_quadrado(lado):
    return 4 * lado

def area_retangulo(base, altura):
    return base * altura

def perimetro_retangulo(base, altura):
    return 2 * (base + altura)

def area_triangulo(base, altura):
    return (base * altura) / 2

def perimetro_triangulo(lado1, lado2, lado3):
    return lado1 + lado2 + lado3

def area_circulo(raio):
    return math.pi * (raio ** 2)

def perimetro_circulo(raio):
    return 2 * math.pi * raio
