#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MATRIX_SIZE 30

//vértice 3D
typedef struct {
    float x, y, z;
    char id;

} Vertex;

//face com 4 vértices
typedef struct {
    int v[4];
} Face;

//dados do cubo (Shared Vertex)
Vertex vertices[8] = {
    //face frontal (z = -1)
    {-1, -1, -1, 'A'}, // v0
    { 1, -1, -1, 'B'}, // v1
    { 1,  1, -1, 'C'}, // v2
    {-1,  1, -1, 'D'}, // v3
    //face traseira (z = 1)
    {-1, -1,  1, 'E'}, // v4
    { 1, -1,  1, 'F'}, // v5
    { 1,  1,  1, 'G'}, // v6
    {-1,  1,  1, 'H'}  // v7
};

Face faces[6] = {
    {{0, 1, 2, 3}}, //frente
    {{4, 5, 6, 7}}, //trás
    {{0, 1, 5, 4}}, //baixo
    {{2, 3, 7, 6}}, //cima
    {{1, 2, 6, 5}}, //direita
    {{0, 3, 7, 4}}  //esquerda
};

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

    float x = x0;
    float y = y0;

    for (int i = 0; i <= steps; i++) {
        if (x >= 0 && x < MATRIX_SIZE && y >= 0 && y < MATRIX_SIZE)
            m[(int)y][(int)x] = '#';

        x += dx / (float)steps;
        y += dy / (float)steps;
    }
}

//desenha as arestas do cubo
void desenharArestas(Vertex vertices[]) {
    char matriz[MATRIX_SIZE][MATRIX_SIZE];
    limparMatriz(matriz);

    //12 arestas do cubo (Shared Vertex)
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

    //marcar a origem (SRU)
    int origemX = MATRIX_SIZE / 2;
    int origemY = MATRIX_SIZE / 2;

    matriz[origemY][origemX] = 'O';

    //desenhar os vértices
    for (int i = 0; i < 8; i++) {
        int x, y;
        projetar(vertices[i], &x, &y);

        if (x >= 0 && x < MATRIX_SIZE && y >= 0 && y < MATRIX_SIZE) {
            matriz[y][x] = vertices[i].id;
        }
    }

    //imprime a matriz
    for (int y = 0; y < MATRIX_SIZE; y++) {
        for (int x = 0; x < MATRIX_SIZE; x++) {
            printf("%c ", matriz[y][x]);
        }
        printf("\n");
    }
}

int main() {
    printf("Cubo 3D com Shared Vertex\n\n");
    desenharArestas(vertices);
    return 0;
}