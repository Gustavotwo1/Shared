import math

MATRIX_SIZE = 30

tx = 2  
ty = 1  
tz = 0 

#hared Vertex (8 vértices)
vertices = [
    (-1, -1, -1),  # v0
    ( 1, -1, -1),  # v1
    ( 1,  1, -1),  # v2
    (-1,  1, -1),  # v3
    (-1, -1,  1),  # v4
    ( 1, -1,  1),  # v5
    ( 1,  1,  1),  # v6
    (-1,  1,  1)   # v7
]

#12 arestas do cubo
arestas = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

#projeção 3D → 2D
def projetar(v):
    escala = 7
    x, y, z = v

    x = x + tx
    y = y + ty
    z = z + tz

    # Rotação simples para o cubo não parecer um quadrado chapado
    # Rotacionando em torno do eixo Y e X (30 graus)
    rad = math.radians(30)

    # Rotação em Y
    nx = x * math.cos(rad) + z * math.sin(rad)
    nz = -x * math.sin(rad) + z * math.cos(rad)

    # Rotação em X
    ny = y * math.cos(rad) - nz * math.sin(rad)

    # PROJEÇÃO ORTOGONAL (Mapear x,y,z -> x,y simplesmente ignorando o z)
    xp = nx
    yp = ny

    # Mapeamento para a matriz (SRU)
    x2d = int(xp * escala + MATRIX_SIZE / 2)
    y2d = int(yp * escala + MATRIX_SIZE / 2)

    return x2d, y2d


#criar matriz (SRU)
def criar_matriz():
    return [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]


#algoritmo DDA
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

#desenhar cubo
def desenhar_cubo():
    matriz = criar_matriz()

    for a in arestas:
        v0 = vertices[a[0]]
        v1 = vertices[a[1]]

        x0, y0 = projetar(v0)
        x1, y1 = projetar(v1)

        draw_line(x0, y0, x1, y1, matriz)
    
    # marcar origem
    origem_x = MATRIX_SIZE // 2
    origem_y = MATRIX_SIZE // 2

    matriz[origem_y][origem_x] = 'O'

    for linha in matriz:
        print(' '.join(linha))



#main

print("Cubo 3D - Shared Vertex (Python)\n")
desenhar_cubo()


#menu de tranformções
#apos a cração da funções sera chamado a desenha cubo em cada opção
while(True):
    print(''' 
    ==========Opções==========
            1: Rotacionar
            2: Transladar
            3: Escalar
            4: Cisalhar
            5: Espelhar
            6: sair\n''')

    opcao = int(input("Escolha atranformação que deseja executar: "))

    if opcao == 1:
        pass

    elif opcao == 2:
        pass

    elif opcao == 3:
        pass

    elif opcao == 4:
        pass

    elif opcao == 5:
        pass

    elif opcao == 6:
        break
    
    else:
        print("\nColoque uma opção valida!\n")

