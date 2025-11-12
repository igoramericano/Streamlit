import operacoes as op

while True:
    try:
        n1 = int(input("Digite o primeiro número: "))
        n2 = int(input("Digite o segundo número: "))
        operacao = input("Escolha a operação (+, -, *, /): ")
    except ValueError:
        print("Erro: Entrada inválida. Digite apenas números inteiros.")
        continue

    if operacao == '+':
        resultado = op.somar(n1, n2)
        print(f'O resultado de {n1} {operacao} {n2} é: {resultado}')
    elif operacao == '-':
        resultado = op.subtrair(n1, n2)
        print(f'O resultado de {n1} {operacao} {n2} é: {resultado}')
    elif operacao == '*':
        resultado = op.multiplicar(n1, n2)
        print(f'O resultado de {n1} {operacao} {n2} é: {resultado}')
    elif operacao == '/':
        resultado = op.dividir(n1, n2)
        print(f'O resultado de {n1} {operacao} {n2} é: {resultado}')
    else:
        print("Operação inválida, digite (+, -, * ou /).")

    continuar = input("Deseja continuar? (s/n): ").lower()
    if continuar != 's':
        break

print("Programa encerrado.")