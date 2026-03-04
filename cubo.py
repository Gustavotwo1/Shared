import math

MATRIX_SIZE = 30

# =========================
# Shared Vertex (8 vértices)
# =========================
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

# 12 arestas do cubo
arestas = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

# =========================
# Projeção 3D → 2D
# =========================
def projetar(v):
    escala = 5

    x, y, z = v

    xp = x
    yp = y

    x2d = int(xp * escala + MATRIX_SIZE / 2)
    y2d = int(yp * escala + MATRIX_SIZE / 2)

    return x2d, y2d


# =========================
# Criar matriz (SRU)
# =========================
def criar_matriz():
    return [['.' for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]


# =========================
# Algoritmo DDA
# =========================
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


# =========================
# Desenhar cubo
# =========================
def desenhar_cubo():
    matriz = criar_matriz()

    for a in arestas:
        v0 = vertices[a[0]]
        v1 = vertices[a[1]]

        x0, y0 = projetar(v0)
        x1, y1 = projetar(v1)

        draw_line(x0, y0, x1, y1, matriz)

    for linha in matriz:
        print(' '.join(linha))


# =========================
# MAIN
# =========================
print("Cubo 3D - Shared Vertex (Python)\n")
desenhar_cubo()