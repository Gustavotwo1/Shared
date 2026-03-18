import math

MATRIX_SIZE = 45

# shared Vertex (8 vértices)
vertices = [
    (1, 1, -1),#v0
    (3, 1, -1),#v1
    (3, 3, -1),#v2
    (1, 3, -1),#v3

    (1, 1, 1),#v4
    (3, 1, 1),#v5
    (3, 3, 1),#v6
    (1, 3, 1) #v7
]

nome_Vertice = ["A", "B", "C", "D", "E", "F", "G", "H",]

# 12 arestas do cubo
# dicionario aplicando o nome de cada aresta
arestas = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

# projeção 3D → 2D
def projetar(v):
    escala = 5
    x, y, z = v

    rad = math.radians(30)

    # Rotação em Y
    nx = x * math.cos(rad) + z * math.sin(rad)
    nz = -x * math.sin(rad) + z * math.cos(rad)

    # Rotação em X
    ny = y * math.cos(rad) - nz * math.sin(rad)

    xp = nx
    yp = ny

    x2d = int(xp * escala + MATRIX_SIZE / 2)
    y2d = int(-yp * escala + MATRIX_SIZE / 2)

    return x2d, y2d


# criar matriz (SRU)
def criar_matriz():
    return [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]


# algoritmo DDA
def draw_line(x0, y0, x1, y1, matriz):
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = x0
    y = y0

    for _ in range(steps + 1):
        xi = int(round(x))
        yi = int(round(y))

        if 0 <= xi < MATRIX_SIZE and 0 <= yi < MATRIX_SIZE:
            matriz[yi][xi] = '#'

        x += x_inc
        y += y_inc


# desenhar cubo
def desenhar_cubo(vertices, matriz):
    for a in arestas:
        v0 = vertices[a[0]]
        v1 = vertices[a[1]]

        x0, y0 = projetar(v0)
        x1, y1 = projetar(v1)

        draw_line(x0, y0, x1, y1, matriz)

        #nomeando os vertices do cubo
        for i, v in enumerate(vertices):
            x, y = projetar(v)

            if 0 <= x < MATRIX_SIZE and 0 <= y < MATRIX_SIZE:
                matriz[y][x] = nome_Vertice[i]


# mostrar matriz
def mostrar_matriz(matriz):
    origem_x = MATRIX_SIZE // 2
    origem_y = MATRIX_SIZE // 2

    matriz[origem_y][origem_x] = 'O'

    for linha in matriz:
        print(' '.join(linha))


# matriz de reflexão
def matriz_espelhamento(eixo):
    if eixo == 'x':
        return [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]
    elif eixo == 'y':
        return [
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]


# aplica reflexão no vértice
def matriz_refletida(Mr, v):
    x, y, z = v
    x_ref = Mr[0][0]*x + Mr[0][1]*y + Mr[0][2]*z
    y_ref = Mr[1][0]*x + Mr[1][1]*y + Mr[1][2]*z
    z_ref = Mr[2][0]*x + Mr[2][1]*y + Mr[2][2]*z
    
    return (x_ref, y_ref, z_ref)

# ================= MAIN =================

print("Cubo 3D - Shared Vertex (Python)\n")

# desenho inicial
matriz = criar_matriz()
desenhar_cubo(vertices, matriz)
mostrar_matriz(matriz)


while True:
    print(''' 
    ==========Opções==========
            1: Rotacionar
            2: Transladar
            3: Escalar
            4: Cisalhar
            5: Espelhar
            6: sair\n''')

    opcao = int(input("Escolha a transformação: "))

    if opcao == 1:
        print("Opção não implementada ainda.\n")
    
    elif opcao == 2:
        print("Opção não implementada ainda.\n")    
    
    elif opcao == 3:
        print("Opção não implementada ainda.\n")
    
    elif opcao == 4:
        print("Opção não implementada ainda.\n")

    elif opcao == 5:
        eixo = input("Digite o eixo (x ou y): ").lower()

        if eixo in ['x', 'y']:
            Mr = matriz_espelhamento(eixo)
            


            vertices_refletidos = [
                matriz_refletida(Mr, v) for v in vertices
            ]

            # matriz nova (limpa)
            matriz = criar_matriz()

            # desenha os DOIS cubos
            desenhar_cubo(vertices, matriz)

            desenhar_cubo(vertices_refletidos, matriz)

            # mostra resultado
            mostrar_matriz(matriz)

        else:
            print("Eixo inválido!")

    elif opcao == 6:
        break

    else:
        print("Opção não implementada ainda.\n")
