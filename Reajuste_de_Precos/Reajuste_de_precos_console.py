# Exercício 5: Reajuste Geral de Preços (Setor Comercial)

# Catálogo atual
precos = {"celular": 1500, "tablet": 2500, "notebook": 5000}

# Solicita ao usuário o percentual de aumento
percentual = float(input("Digite o percentual de aumento (ex: 10 para 10%): "))

# Aplica o reajuste em cada produto
for produto in precos:
    precos[produto] = precos[produto] * (1 + percentual / 100)

# Exibe o novo catálogo formatado
print("\nNovo catálogo de preços:")
for produto, valor in precos.items():
    print(f"{produto.capitalize()}: R$ {valor:.2f}")
