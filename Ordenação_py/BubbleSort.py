import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.widgets import Slider
import numpy as np

##=============================== 1. Algoritmo Bubble Sort como um Gerador (yield) #===============================

def bubble_sort(lista):
    size = len(lista)
    for i in range(size):
        flag = 0
        for j in range(size - i - 1):
            yield lista, j, j + 1, size - i 
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                yield lista, j, j + 1, size - i
                flag = 1
        if flag == 0:
            yield lista, -1, -1, 0 # condicao de parada antecipada
    yield lista, -1, -1, 0 # condicao de parada


#=============================== Configurações iniciais #===============================


qtd_bar = 10
lista_valores = np.random.randint(1, 50, qtd_bar) # vai de 1 a 50, e tem qtd_bar elementos
gerador_sort = bubble_sort(lista_valores)  # Pega os valores gerados e taca no bubblesort

# Criando a figura e os eixos
fig, ax = plt.subplots(figsize=(8, 5)) # primeiro argumento pe largura o segundo argumento é altura
plt.subplots_adjust(bottom=0.2) # Abre espaço na parte inferior para o botão
ax.set_title("Bubblesort Animado Sem Flags", fontsize=16)

# Desenhando as barras iniciais
barras = ax.bar(range(len(lista_valores)), lista_valores, align="edge", color='beige') #criação das barras e seus respectivos valores, align="edge" para alinha a esquerda as coisas
ax.set_xlim(0, qtd_bar) # basicamente onde começa e onde termina o gráfico no eixo x
ax.set_ylim(0, int(1.1 * max(lista_valores))) # basicamente onde começa e onde termina o gráfico no eixo y

#Para deixar sem a llinha da tabela:
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.tick_params(left=False, bottom=False) # Remove os ticks dos eixos
ax.set_xticks([]) #deixar sem os numeros x:
ax.set_yticks([]) #deixar sem os numeros y:



# ##=============================== 2. Função que atualiza o gráfico a cada frame #===============================

def update_fig(dados):
    lista, j, j_plus_1, limite_ordenado = dados

    # Atualiza as alturas e reseta as cores básicas
    for indice, valor in enumerate(lista):
        barras[indice].set_height(valor)
        
        # O índice 'i' do seu loop original define a parte final que já está ordenada.
        # Vamos pintar os que já foram ordenados de verde.
        if indice >= limite_ordenado:
            barras[indice].set_color('lightgreen')
        else:
            barras[indice].set_color('beige')

    # Pinta os elementos sendo comparados (índice j e j+1)
    if j != -1:
        barras[j].set_color('lightblue')      # Cor do índice j
        barras[j_plus_1].set_color('blue')  # Cor do índice j+1

    return barras

# ##=============================== 3. Criando a animação #===============================

# interval=200 é o tempo em milissegundos entre cada frame (velocidade)
anim = animation.FuncAnimation(
    fig, 
    func=update_fig, 
    frames=gerador_sort, 
    interval=200, 
    repeat=False, 
    cache_frame_data=False
)

# ##=============================== 4. Implementando o Botão de Pause/Play #===============================

ax_botao = plt.axes([0.4, 0.05, 0.2, 0.075]) # [esquerda, baixo, largura, altura]
botao_pause = Button(ax_botao, 'Pause / Play')

animation_state = {'rodando': True} # Usamos um dicionário para poder alterar o valor dentro da função

def toggle_pause(event):
    if animation_state['rodando']:
        anim.pause()
        animation_state['rodando'] = False
    else:
        anim.resume()
        animation_state['rodando'] = True

botao_pause.on_clicked(toggle_pause)

# Exibe tudo na tela
plt.show()

