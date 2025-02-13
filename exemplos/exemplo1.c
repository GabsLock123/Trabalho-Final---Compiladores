#include <stdio.h>

// ================================
// Struct e Union
// ================================

// Define uma struct "Person" com campos "age" (int) e "initial" (char)
struct Person {
    int age;
    char initial;
};

// Define uma union "Data" com campos "i" (int) e "f" (float)
union Data {
    int i;
    float f;
};

// ================================
// Funções com/sem retorno e com/sem parâmetros
// ================================

// Função com retorno e com parâmetros: soma dois inteiros e retorna o resultado.
int sum(int a, int b) {
    return a + b;
}

// Função com retorno e sem parâmetros: retorna um valor fixo.
int fixedValue() {
    return 42;
}

// Função sem retorno e sem parâmetros: imprime uma mensagem.
void greet() {
    printf("Hello from greet!\n");
}

// Função sem retorno e com parâmetro: imprime os dados de uma pessoa.
void printPerson(struct Person p) {
    printf("Person: age = %d, initial = %c\n", p.age, p.initial);
}

// Função recursiva: calcula o fatorial de um número.
int factorial(int n) {
    if(n <= 1)
        return 1;
    else
        return n * factorial(n - 1);
}

// Função que usa if/else e switch/case para testar condições.
int testConditions(int x) {
    if(x % 2 == 0)
        printf("x is even\n");
    else
        printf("x is odd\n");

    int res;
    switch(x) {
        case 1:
            res = 10;
            break;
        case 2:
            res = 20;
            break;
        default:
            res = 30;
            break;
    }
    return res;
}

// Função que testa os loops: while, do/while e for.
void testLoops() {
    int i = 0;
    printf("While loop: ");
    while(i < 3) {
        printf("%d ", i);
        i = i + 1;
    }
    printf("\n");

    int j = 0;
    printf("Do-while loop: ");
    do {
        printf("%d ", j);
        j = j + 1;
    } while(j < 3);
    printf("\n");

    int k = 0;
    printf("For loop: ");
    for(k = 0; k < 3; k = k + 1) {
        printf("%d ", k);
    }
    printf("\n");
}

// ================================
// Funções de entrada/saída
// ================================

// Função que usa scanf/printf para ler e imprimir um inteiro.
void testIO() {
    int num;
    printf("Enter an integer: ");
    scanf("%d", &num);
    printf("You entered: %d\n", num);
}

// Função que usa gets e puts para ler e imprimir uma string.
// Observe que, neste exemplo, strings são vetores de char.
void testStringIO() {
    char s[100];
    printf("Enter a string (for gets): ");
    gets(s);
    puts(s);
}

// ================================
// main
// ================================
int main() {
    int i;
    int x;
    int y;
    int r;
    int fact;
    int condRes;
    
    // Teste de função com retorno e com parâmetros
    x = 10;
    y = 20;
    r = sum(x, y);
    printf("Sum of %d and %d = %d\n", x, y, r);
    
    // Teste de função com retorno e sem parâmetros
    printf("Fixed value: %d\n", fixedValue());
    
    // Teste de função sem retorno e sem parâmetros
    greet();
    
    // Teste de função que imprime uma struct
    struct Person p;
    p.age = 25;
    p.initial = 'J';
    printPerson(p);
    
    // Teste de union
    union Data d;
    d.i = 100;
    printf("Union d: i = %d\n", d.i);
    d.f = 3.14;
    printf("Union d: f = %f\n", d.f);
    
    // Teste de função recursiva: fatorial
    fact = factorial(5);
    printf("Factorial of 5 = %d\n", fact);
    
    // Teste de if/else e switch/case
    condRes = testConditions(2);
    printf("Result from testConditions(2) = %d\n", condRes);
    
    // Teste de loops
    testLoops();
    
    // Teste de entrada/saída numérica
    testIO();
    
    // Teste de entrada/saída de string
    testStringIO();
    
    // ================================
    // Teste de arrays
    // ================================
    
    // Array de inteiros
    int arr[4];
    arr[0] = 2;
    arr[1] = 4;
    arr[2] = 6;
    arr[3] = 8;
    printf("Array arr: ");
    for(i = 0; i < 4; i = i + 1) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    
    // Array de char representando uma string
    char s[20] = "Hello, world!";
    printf("String s: %s\n", s);
    
    return 0;
}
