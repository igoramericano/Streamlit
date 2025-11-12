import operacoes as op

figura = input("Digite a figura geométrica (triângulo, retângulo, círculo): ").strip().lower()
if figura == "triângulo":
    base = float(input("Digite a base do triângulo: "))
    altura = float(input("Digite a altura do triângulo: "))
    area = op.area_triangulo(base, altura)
    print(f"A área do triângulo é: {area}")
elif figura == "retângulo":
    base = float(input("Digite a base do retângulo: "))
    altura = float(input("Digite a altura do retângulo: "))
    area = op.area_retangulo(base, altura)
    print(f"A área do retângulo é: {area}")
elif figura == "círculo":
    raio = float(input("Digite o raio do círculo: "))
    area = op.area_circulo(raio)
    print(f"A área do círculo é: {area}")
elif figura == "quadrado":
    lado = float(input("Digite o lado do quadrado: "))
    area = op.area_quadrado(lado)
    print(f"A área do quadrado é: {area}")
else:
    print("Figura geométrica não reconhecida.")