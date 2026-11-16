def combinacoes(x):
    # Se for apenas 1 elemento retorna 1 arranjo
    if x == 1:
        return [[0]]
    else:
        # Adiciona os elementos a lista auxiliar
        aux = combinacoes(x - 1)
    pilha = []
    par = 0
    # Percorre a lista juntando os elementos nas possibilidades possíveis
    for element in aux:
        lmt = max(element) + 1
        if par == 0:
            for j in range(lmt + 1):
                pilha.append(element + [j])
        else:
            # Range invertido
            for j in range(lmt + 1)[::-1]:
                pilha.append(element + [j])
        par = par ^ 1
    return pilha


n = int(input())
# Gera as combinações de pilhas de brinquedos
possibilidades = combinacoes(n)
# Imprime a quantidade de combinações
print(len(possibilidades))
# Formata a Impressão como é pedido no problema
for item in possibilidades:
    arranjos = ''
    limit = max(item) + 1
    # Percorre os limites para descobrir em qual grupo o brinquedo pertence
    for group in range(limit):
        arranjos += '{'
        toys = ''
        for i in range(n):
            if item[i] == group:
                toys += '{0},'.format(i + 1)
        arranjos += toys[:-1]
        arranjos += '},'
    print(arranjos[:-1])
