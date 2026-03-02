#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_VERTICES 8
#define MAX_FACES 6
#define MATRIX_SIZE 30

//vértice 3D
typedef struct {
    float x, y, z;
} Vertex;

//face com 4 vértices
typedef struct {
    int v[4];
} Face;

//dados do cubo (Shared Vertex)

Vertex vertices[MAX_VERTICES] = {
    {-1, -1, -1}, // v0
    { 1, -1, -1}, // v1
    { 1,  1, -1}, // v2
    {-1,  1, -1}, // v3
    {-1, -1,  1}, // v4
    { 1, -1,  1}, // v5
    { 1,  1,  1}, // v6
    {-1,  1,  1}  // v7
};

Face faces[MAX_FACES] = {
    {{0, 1, 2, 3}}, // frente
    {{4, 5, 6, 7}}, // trás
    {{0, 1, 5, 4}}, // baixo
    {{2, 3, 7, 6}}, // cima
    {{1, 2, 6, 5}}, // direita
    {{0, 3, 7, 4}}  // esquerda
};


//funções Auxiliares

//projeção ortogonal 3D -> 2D
void projetar(Vertex v, int *x2d, int *y2d) {
    float escala = 5.0f;
    float ang = 45.0f * 3.14159265f / 180.0f; // 45 graus em radianos

    //projeção ortogonal simples
    float xp = v.x + v.z * cos(ang);
    float yp = v.y + v.z * sin(ang);

    //mapeia para coordenadas da matriz SRU
    *x2d = (int)(xp * escala) + MATRIX_SIZE / 2;
    *y2d = (int)(yp * escala) + MATRIX_SIZE / 2;
}

//limpa a matriz SRU
void limparMatriz(char m[MATRIX_SIZE][MATRIX_SIZE]) {
    for (int y = 0; y < MATRIX_SIZE; y++) {
        for (int x = 0; x < MATRIX_SIZE; x++) {
            m[y][x] = '.';
        }
    }
}

//algoritmo de Bresenham para desenhar linhas na matriz
void drawLine(int x0, int y0, int x1, int y1, char m[MATRIX_SIZE][MATRIX_SIZE]) {
    int dx = x1 - x0;
    int dy = y1 - y0;

    int steps = abs(dx) > abs(dy) ? abs(dx) : abs(dy);

    if (steps == 0) {
        if (x0 >= 0 && x0 < MATRIX_SIZE && y0 >= 0 && y0 < MATRIX_SIZE)
            m[y0][x0] = '#';
        return;
    }

    float xInc = dx / (float)steps;
    float yInc = dy / (float)steps;

    float x = x0;
    float y = y0;

    for (int i = 0; i <= steps; i++) {
        int xi = (int)(x + 0.5f);
        int yi = (int)(y + 0.5f);

        if (xi >= 0 && xi < MATRIX_SIZE && yi >= 0 && yi < MATRIX_SIZE) {
            m[yi][xi] = '#';
        }

        x += xInc;
        y += yInc;
    }
}

// desenha as arestas do cubo (wireframe)
void desenharArestas(Vertex vertices[]) {
    char matriz[MATRIX_SIZE][MATRIX_SIZE];
    limparMatriz(matriz);

    // 12 arestas do cubo (Shared Vertex)
    int arestas[12][2] = {
        {0,1}, {1,2}, {2,3}, {3,0}, // frente
        {4,5}, {5,6}, {6,7}, {7,4}, // trás
        {0,4}, {1,5}, {2,6}, {3,7}  // liga frente com trás
    };

    for (int i = 0; i < 12; i++) {
        int a = arestas[i][0];
        int b = arestas[i][1];

        int x0, y0, x1, y1;
        projetar(vertices[a], &x0, &y0);
        projetar(vertices[b], &x1, &y1);

        drawLine(x0, y0, x1, y1, matriz);
    }

    // imprime a matriz
    for (int y = 0; y < MATRIX_SIZE; y++) {
        for (int x = 0; x < MATRIX_SIZE; x++) {
            printf("%c ", matriz[y][x]);
        }
        printf("\n");
    }
}

// ======================
// Programa Principal
// ======================

int main() {
    printf("Cubo 3D com Shared Vertex (projecao ortogonal 3D -> 2D)\n\n");
    desenharArestas(vertices);
    return 0;
}