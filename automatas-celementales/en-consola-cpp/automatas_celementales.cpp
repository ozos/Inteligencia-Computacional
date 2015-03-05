/* Inteligencia computacional
    Tarea 2: Programacion de 5 reglas de automatas celulares
    Leyva Hernandez Luis Alberto 210200159
*/

#include <iostream>

#define Num_Gen 24 //numero de generaciones
#define Tam_Cuad 50  //tamaño de la cuadricula

void gen_regla(int *regla,int num_reg);
void imprimir(int mat_cel [ ][Tam_Cuad]);
void limpiar(int mat_cel [ ][Tam_Cuad]);
void generar(int *regla, int mat_cel [ ][Tam_Cuad]);

int main()
{
    int regla[8];
    int mat_cel[Num_Gen][Tam_Cuad];

    //regla 1 de 5
    limpiar(mat_cel);
    std::cout << "Regla 30" << "\n";
    gen_regla(regla,30);
    generar(regla,mat_cel);
    imprimir(mat_cel);

    //regla 2 de 5
    limpiar(mat_cel);
    std::cout << "Regla 54" << "\n";
    gen_regla(regla,54);
    generar(regla,mat_cel);
    imprimir(mat_cel);

    //regla 3 de 5
    limpiar(mat_cel);
    std::cout << "Regla 94" << "\n";
    gen_regla(regla,94);
    generar(regla,mat_cel);
    imprimir(mat_cel);

    //regla 4 de 5
    limpiar(mat_cel);
    std::cout << "Regla 182" << "\n";
    gen_regla(regla,182);
    generar(regla,mat_cel);
    imprimir(mat_cel);

    //regla 5 de 5
    limpiar(mat_cel);
    std::cout << "Regla 222" << "\n";
    gen_regla(regla,222);
    generar(regla,mat_cel);
    imprimir(mat_cel);


    return 0;
}

void limpiar(int mat_cel [ ][Tam_Cuad])
{

    for (int i=0; i<Num_Gen ; i++)
    {

        for (int j=0; j<Tam_Cuad ; j++)
        {
            mat_cel[i][j]=0;
        }
    }
}


void imprimir(int mat_cel [ ][Tam_Cuad])
{

    for (int i=0; i<Num_Gen ; i++)
    {

        for (int j=0; j<Tam_Cuad ; j++)
        {
            if (mat_cel[i][j]==1)
            {
                std::cout << "X";
            }
            else
            {
                std::cout << "-";
            }
        }
        std::cout << "\n";
    }
}

void gen_regla(int *regla,int num_reg)
{
    int num=num_reg;
    int i=7;
    while (num>0)
    {
        regla[i]=num%2;
        i--;
        num=num/2;
    }
    while(i>=0)
    {
        regla[i]=0;
        i--;
    }
    for (int l=0; l < 8; l++)
    {
        std::cout << regla[l];

    }
    std::cout << "\n";

}

void generar(int *regla,int mat_cel[][Tam_Cuad])
{
    int a,c;
    mat_cel[0][Tam_Cuad/2]=1;

    for (int i=1; i<Num_Gen; i++)
    {
        for (int j=0; j<Tam_Cuad; j++)
        {
            if(j==0)
            {
                a=Tam_Cuad-1;
            }
            else
            {
                a=j-1;
            }
            if(j==Tam_Cuad-1)
            {
                c=0;
            }
            else
            {
                c=j+1;
            }
            int dec=7-((mat_cel[i-1][a]*4)+(mat_cel[i-1][j]*2)+(mat_cel[i-1][c]));
            mat_cel[i][j]=regla[dec];
        }
    }
}
