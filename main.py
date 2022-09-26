import pandas as pd
import math


# función para calcular la entropía de todo el conjunto de datos
# -----------------------------------------------------------------------
def entropia_base(conjunto_de_datos):
    p = 0
    n = 0
    objetivo = conjunto_de_datos.iloc[:, -1]
    objetivos = list(set(objetivo)) #Arma una lista mapeada sin repetición
    for i in objetivo:
        #Contamos positivos y negativos
       # print("Variable objetivo e entropia base",objetivo)
        if i == objetivos[0]:
            p = p + 1
        else:
            n = n + 1
    if p == 0 or n == 0:
        return 0
    elif p == n:
        return 1
    else:
        entropia = 0 - (
            ((p / (p + n)) * (math.log2(p / (p + n))) + (n / (p + n)) * (math.log2(n / (p + n)))))
     #   print(entropia, "Imprimimos entropia base del conjunto de datos")
        return entropia


# -----------------------------------------------------------------------
# función para calcular la entropía de los atributos
# -----------------------------------------------------------------------
def entropia(conjunto_de_datos, caracteristicas, atributos):
    p = 0
    n = 0
    objetivo = conjunto_de_datos.iloc[:, -1]
    objetivos = list(set(objetivo)) #Armamos una lista mapeada sin repeticion
    for i, j in zip(caracteristicas, objetivo): #Con la 
        #print("Imprimimos lo que traen las caracteristicas antes de zipear", caracteristicas)
        #print("Imprimimos los que traen los objetivos antes de zipear", objetivos)
        if i == atributos and j == objetivos[0]:
            p = p + 1
        elif i == atributos and j == objetivos[1]:
            n = n + 1
    if p == 0 or n == 0:
        return 0
    elif p == n:
        return 1
    else:
        entropia = 0 - (
            ((p / (p + n)) * (math.log2(p / (p + n))) + (n / (p + n)) * (math.log2(n / (p + n)))))
        #print("Imprimimos lo que traen las caracteristicas zipeadas", caracteristicas)
       
        #print("Imprimimos los que traen los objetivos zipeados", objetivos)
        #print("entropia zipeada", entropia)
        return entropia


# -----------------------------------------------------------------------
# función para comprobar la pureza y la impureza 
# -----------------------------------------------------------------------
def contador(objetivo, atributos, i):
    p = 0
    n = 0
    #Usamos set para limpiar los repetidos del conjunto que estamos contando
    objetivos = list(set(objetivo))
    #Usams zip para darle la tupla y que los agrupe
    for j, k in zip(objetivo, atributos):
        if j == objetivos[0] and k == i:
            p = p + 1
        elif j == objetivos[1] and k == i:
            n = n + 1
      #  print("Contador para p zipeado:", p)
      #  print("Contador para n zipeado:", n)
    return p, n


# -----------------------------------------------------------------------
# función que calcula la informacion de funcion_ganancia
# -----------------------------------------------------------------------
def funcion_ganancia(conjunto_de_datos, caracteristicas):
    Distintos = list(set(caracteristicas))
 #   print("funcion que calcula ganancia , Distintos", Distintos)
    ganancia = 0
    for i in Distintos:
     #   print("funcion_ganancia GANANCIA Dentro del for:", ganancia)
        ganancia = ganancia + caracteristicas.count(i) / len(caracteristicas) * entropia(conjunto_de_datos, caracteristicas, i)
    ganancia = entropia_base(conjunto_de_datos) - ganancia
  #  print("funcion_ganancia GANANCIA:", ganancia)
    return ganancia


# -----------------------------------------------------------------------
# función que genera los hijos de los atributos seleccionados que sean distintos
# -----------------------------------------------------------------------
def genera_hijos(conjunto_de_datos, atributos_index):
    distintos = list(conjunto_de_datos.iloc[:, atributos_index])
   # print( "genera hijos lista de distintos",distintos)
    hijos = dict()
  #  print("hijos diccionario", hijos)
    for i in distintos:
        hijos[i] = contador(conjunto_de_datos.iloc[:, -1], conjunto_de_datos.iloc[:, atributos_index], i)
 #   print("genera hijos --hijos", hijos)
    return hijos
    

# -----------------------------------------------------------------------
# funcion que modifica el conjunto_de_datos, aca sacamos las columnas que tienen 
# datos repetidos de nuestra muestra con iguales valores
# -----------------------------------------------------------------------
def modificar_conjunto_de_datos(conjunto_de_datos,index, caracteristicas, impuros):
    tamanio = len(conjunto_de_datos)
#print("tamaño de modificar conjunto de datos", tamanio)
    sub_datos = conjunto_de_datos[conjunto_de_datos[caracteristicas] == impuros]
  #print("Imprimimos antesssssssss  modificar_conjunto_de_datos_sub_datos", sub_datos)
    del (sub_datos[sub_datos.columns[index]])
   #print("Imprimimos modificar_conjunto_de_datos_sub_datos", sub_datos)
    return sub_datos


# -----------------------------------------------------------------------


# función que devuelve atributos con la mayor información de ganancia
# -----------------------------------------------------------------------
def mayor_ganancia(conjunto_de_datos):
    max = -1
    atributos_index = 0
    tamanio = len(conjunto_de_datos.columns) - 1
   # print("tamanio de mayor_ganancia", tamanio)
    for i in range(0, tamanio):
        caracteristicas = list(conjunto_de_datos.iloc[:, i])
      #  print("CARACTERISTICAS de mayor_ganancia", caracteristicas)
        i_g = funcion_ganancia(conjunto_de_datos, caracteristicas)
        #print("IG de mayor_ganancia", i_g)
        if max < i_g:
            max = i_g
            atributos_index = i
       # print("IG de mayor_ganancia", i_g)
    return atributos_index


# -----------------------------------------------------------------------
# función para construir el árbol de decisión
# -----------------------------------------------------------------------
def constructor_arbol(conjunto_de_datos, arbol):
    objetivo = conjunto_de_datos.iloc[:, -1]
    hijos_impuros = []
    #print("arbol",arbol)
    atributos_index = mayor_ganancia(conjunto_de_datos)
    #print("Atrubutos index", atributos_index)
    hijos = genera_hijos(conjunto_de_datos, atributos_index)
    #print("HIjos",hijos)
    arbol[conjunto_de_datos.columns[atributos_index]] = hijos
    #print("Hijos_de abajo", hijos)
    #print("Atrubutos index arbol raro", atributos_index)
    objetivos = list(set(conjunto_de_datos.iloc[:, -1]))
    #print("objetivos...", objetivos)
    for k, v in hijos.items():
        if v[0] == 0:
            arbol[k] = objetivos[1] # Es un uno
           # print("arbol_de_decision v", v)    
            #print("arbol_de_decision k", k)    
        elif v[1] == 0:
            arbol[k] = objetivos[0] #Es un cero
            #print("arbol_de_decision v", v)
           # print("arbol_de_decision k", k)  
        elif v[0] != 0 or v[1] != 0:
            hijos_impuros.append(k)
            print("arbol_de_decision hijos_impuros append", hijos_impuros)
       # print("arbol_de_decision kkkkkkkkk", arbol[k])   
    for i in hijos_impuros:
        sub_arbol = modificar_conjunto_de_datos(conjunto_de_datos,atributos_index, conjunto_de_datos.columns[atributos_index], i)
        arbol = constructor_arbol(sub_arbol, arbol)
    return arbol


# -----------------------------------------------------------------------
# funcion para main
# -----------------------------------------------------------------------
def main():
    #df = pd.read_csv("reload_Yami_3.csv")
    df = pd.read_csv("reload_Yami_10.csv")
    #df = pd.read_csv("pruebaAD3.csv")
    arbol = dict()
    resultado = constructor_arbol(df, arbol)
    for key, value in resultado.items():
        print(key, " => ", value)


# -----------------------------------------------------------------------

if __name__ == "__main__":
    main()
    
