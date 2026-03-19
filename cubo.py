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

#nomeando os vértices do cubo
nome_Vertice = ["H", "G", "F", "E", "D", "C", "B", "A"]

# 12 arestas do cubo
arestas = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

# projeção 3D → 2D
def projetar(v):
    escala = 5
    x, y, z = v

    xp = x
    yp = y

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


## -------------------- -------------------- translação -------------------- ------------------ ##
def transladar(vertices, tx, ty):
    novos_vertices = []

    for (x, y, z) in vertices:
        x = x + tx
        y = y + ty
       
        novos_vertices.append((x, y, z))

    return novos_vertices
    
def mostrar_vertices(vertices, titulo):
    print(f"\n{titulo}")
    for i, (x, y, z) in enumerate(vertices):
        nome = nome_Vertice[i]
        print(f"{nome}: ({x:.2f}, {y:.2f}, {z:.2f})")


## -------------------- -------------------- Cisalhamento -------------------- ------------------ ##

def multiplicar_matriz(matriz, vetor):
    resultado = [0, 0, 0]

    for i in range(3):
        for j in range(3):
            resultado[i] += matriz[i][j] * vetor[j]

    return resultado

def calcular_centro(vertices):
    x = sum(v[0] for v in vertices) / len(vertices)
    y = sum(v[1] for v in vertices) / len(vertices)
    z = sum(v[2] for v in vertices) / len(vertices)
    return (x, y, z)

def cisalhar(tipo, s=1.8):

    global vertices

    if tipo == "yx":  # y = y + s⋅x
        matriz = [
            [1, 0, 0],
            [s, 1, 0],
            [0, 0, 1]
        ]

    elif tipo == "xy":  # x = x + s·y

        matriz = [
            [1, s, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

    elif tipo == "xz": # x muda baseado em z
        matriz = [
            [1, 0, s],
            [0, 1, 0],
            [0, 0, 1]
        ]

    else:
        print("Tipo inválido")
        return

    cx, cy, cz = calcular_centro(vertices)

    novos_vertices = []

    for v in vertices:
        x, y, z = v

        #  Translada para origem
        x -= cx
        y -= cy
        z -= cz

        #  Aplica cisalhamento
        resultado = multiplicar_matriz(matriz, [x, y, z])

        #  Volta para posição original
        x_final = resultado[0] + cx
        y_final = resultado[1] + cy
        z_final = resultado[2] + cz

        novos_vertices.append((x_final, y_final, z_final))

    vertices = novos_vertices

#-------------------- ------------------  matriz de reflexão -------------------- ------------------ ##

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
    else: # eixo 'xy'
        return [
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]


# aplica reflexão no vértice
def matriz_refletida(Mr, v):
    x, y, z = v
    x_ref = Mr[0][0]*x + Mr[0][1]*y + Mr[0][2]*z
    y_ref = Mr[1][0]*x + Mr[1][1]*y + Mr[1][2]*z
    z_ref = Mr[2][0]*x + Mr[2][1]*y + Mr[2][2]*z
    
    return (x_ref, y_ref, z_ref)

#-------------------- ------------------  matriz de rotação -------------------- ------------------ ##
def rotacionar(vertices, angulo, eixo):
    rad = math.radians(angulo)
    
    novos_vertices = []

    for v in vertices:
        x, y, z = v

        if eixo == 'x':
            y_novo = round(y * math.cos(rad) - z * math.sin(rad), 2)
            z_novo = round(y * math.sin(rad) + z * math.cos(rad), 2)
            novos_vertices.append((x, y_novo, z_novo))

        elif eixo == 'y':
            x_novo = round(x * math.cos(rad) + z * math.sin(rad), 2)
            z_novo = round(-x * math.sin(rad) + z * math.cos(rad), 2)
            novos_vertices.append((x_novo, y, z_novo))

    return novos_vertices

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
        eixo = input("Escolha o eixo (x ou y): ").lower()
        angulo = float(input("Digite o ângulo de rotação: "))

        mostrar_vertices(vertices, "Vértices Originais")    

        vertices = rotacionar(vertices, angulo, eixo)

        mostrar_vertices(vertices, "Vértices Rotacionados")

        print("\nCubo rotacionado:\n")
        matriz = criar_matriz()
        desenhar_cubo(vertices, matriz)
        mostrar_matriz(matriz)
    
    elif opcao == 2:
        tx = float(input("Digite tx: "))
        ty = float(input("Digite ty: "))

        mostrar_vertices(vertices, "Vértices Originais")

        vertices = transladar(vertices, tx, ty)
        
        matriz = criar_matriz()

        mostrar_vertices(vertices, "Vértices Transladados")
        desenhar_cubo(vertices, matriz)
        
        mostrar_matriz(matriz)
        
        
    elif opcao == 3:
        print("Opção não implementada ainda.\n")
    
    elif opcao == 4:
        relacao = input("Digite a relação de cisalhamento (xy, yx, xz): ")

        print("\nCubo 3D - Após o Cisalhamento")

        cisalhar(relacao, 0.8)
        matriz = criar_matriz()
        desenhar_cubo(vertices, matriz)
        mostrar_matriz(matriz)

    elif opcao == 5:
        eixo = input("Digite o eixo (x, y ou xy): ").lower()

        if eixo in ['x', 'y', 'xy']:
            Mr = matriz_espelhamento(eixo)
            
            vertices_refletidos = [
                matriz_refletida(Mr, v) for v in vertices
            ]

            # matriz nova (limpa)
            matriz = criar_matriz()

            # desenha os DOIS cubos
            desenhar_cubo(vertices, matriz)

            mostrar_vertices(vertices, "Vértices Originais")
            mostrar_vertices(vertices_refletidos, "Vértices Refletidos")
            
            desenhar_cubo(vertices_refletidos, matriz)

            # mostra resultado
            mostrar_matriz(matriz)

        else:
            print("Eixo inválido!")

    elif opcao == 6:
        break

    else:
        print("opção invalida.\n")
