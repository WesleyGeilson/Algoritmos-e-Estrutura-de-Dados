import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.widgets import Slider
import numpy as np

#===================================================================================================================
#=============================== 1. Algoritmo Binary_search como um Gerador (yield) #===============================
#======================================================================================================================

def binary_search(lista ,begin, end, value):
    if(begin > end):
        yield lista, begin, end, -1, False
        return
    mid = (begin+end)//2
    
    yield lista, begin, end, mid , False
    if(value == lista[mid]):
        yield lista, begin, end, mid ,True
        return

    if(value > lista[mid]):
        yield from binary_search(lista,mid+1,end,value)

    elif(value < lista[mid]):
        yield from binary_search(lista,begin, mid-1,value)

#=======================================================================================
#=============================== Configurações iniciais #===============================
#'=======================================================================================

qtd_bar = 1000
valor_procurado = 12
lista_valores = np.sort(np.random.randint(1, 100, qtd_bar))
gerador_sort = binary_search(lista_valores, 0, len(lista_valores) - 1, valor_procurado  )  # Pega os valores gerados e taca no binary_search


# Criando a figura e os eixos
fig, ax = plt.subplots(figsize=(8, 5)) # primeiro argumento pe largura o segundo argumento é altura
plt.subplots_adjust(bottom=0.2) # Abre espaço na parte inferior para o botão
ax.set_title("binary_search Animado", fontsize=16)

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


#==============================================================================================================
#=============================== 2. Função que atualiza o gráfico a cada frame #===============================
#==============================================================================================================


def update_fig(dados):
    # Desempacotamos o que o yield enviou
    lista, begin, end, mid, encontrou = dados

    for indice, barra in enumerate(barras):
        # LÓGICA DE CORES PARA BUSCA BINÁRIA:
        if indice < begin or indice > end:
            # Fora do intervalo de busca atual (descartado)
            barra.set_color('grey') # Cinza claro
            barra.set_alpha(0.5) # Deixa mais transparente
        else:
            # Dentro do intervalo que ainda pode ter o número
            barra.set_color('beige')

        # Se for o valor correto, podemos pintar de verde, se não, azul
        if indice == mid:
            if encontrou:
                barras[mid].set_color('lightgreen')
            else:
             barras[mid].set_color('royalblue')

    return barras

#==============================================================================================================
#=============================== 3. Criando a animação #=======================================================
#==============================================================================================================


anim = animation.FuncAnimation(
    fig, 
    func=update_fig, 
    frames=gerador_sort, 
    interval=999, 
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

