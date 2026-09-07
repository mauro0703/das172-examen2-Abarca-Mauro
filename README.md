# AeroCargo-Matrix

## Auditoria y balance matricial de distribucion de carga en bahia de aeronave

### 1. Descripcion del problema

El piso de una bahia de carga se puede representar como una matriz de `N x M`, donde las filas representan la direccion longitudinal de proa a popa y las columnas representan la direccion transversal de izquierda a derecha. Cada posicion contiene un peso real y una capacidad maxima permitida.

El programa revisa que los datos sean coherentes, calcula el porcentaje de ocupacion de cada celda, marca las posiciones que superan el 100 %, obtiene el peso total por fila, calcula el desbalance lateral y extrae la submatriz `k x p` con mayor promedio de ocupacion.

Esto es importante porque una carga mayor a la capacidad local puede afectar la resistencia del piso y una distribucion lateral poco equilibrada puede afectar el balance de la aeronave. El objetivo del programa es apoyar esta revision usando una estructura de datos matricial sencilla y funciones separadas.

### 2. Estructura del repositorio

```text
AeroCargo-Matrix/
├── aerocargo.py
├── main.py
├── .gitignore
├── README.md
└── tests/
    └── test_aerocargo.py
```

### 3. Diagrama de flujo

El flujo principal del programa es el siguiente:

```text
                  +----------------+
                  |     INICIO     |
                  +-------+--------+
                          |
                          v
               +-----------------------+
               | Definir cargas,      |
               | capacidades,         |
               | tolerancia, k y p    |
               +----------+------------+
                          |
                          v
               +-----------------------+
               | validar_matrices()    |
               +----------+------------+
                          |
                    ¿Datos validos?
                     /          \
                   NO            SI
                   |              |
                   v              v
          +---------------+   +-----------------------+
          | Mostrar error |   | calcular_ocupacion()  |
          | y terminar    |   +----------+------------+
          +---------------+              |
                                         v
                              +-----------------------+
                              | Mostrar porcentajes  |
                              | y sobrecargas        |
                              +----------+------------+
                                         |
                                         v
                              +-----------------------+
                              | evaluar_balance()    |
                              +----------+------------+
                                         |
                                         v
                              +-----------------------+
                              | Mostrar desbalance   |
                              | y estado del balance |
                              +----------+------------+
                                         |
                                         v
                              +-------------------------+
                              | extraer_submatriz_      |
                              | critica(porcentajes,k,p)|
                              +-----------+-------------+
                                          |
                                          v
                              +-------------------------+
                              | Mostrar submatriz      |
                              | critica y resultados   |
                              +-----------+-------------+
                                          |
                                          v
                                  +---------------+
                                  |      FIN      |
                                  +---------------+
```

### 4. Arquitectura modular

```text
                 +----------------------+
                 |   cargas /           |
                 |   capacidades        |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | validar_matrices()   |
                 +----------+-----------+
                            |
                       datos validos
                            |
              +-------------+-------------+
              |                           |
              v                           v
 +------------------------+     +------------------------+
 | calcular_ocupacion()   |     | evaluar_balance()      |
 | - porcentajes          |     | - peso por fila        |
 | - sobrecargas          |     | - desbalance lateral   |
 +-----------+------------+     | - balance aprobado     |
             |                  +-----------+------------+
             v                              |
 +------------------------+                |
 | extraer_submatriz_     |<---------------+
 | critica()              |                |
 | - ventana k x p        |                |
 | - mayor promedio       |                |
 +------------------------+                |
             |
             v
       resultados finales
```

Las funciones reciben sus datos por parametros y devuelven resultados. No dependen de variables globales ni modifican las matrices que reciben.

### 5. Funciones y contratos

`validar_matrices(cargas, capacidades)`

- Entrada: dos matrices bidimensionales.
- Salida: `True` si cumplen las condiciones o `False` en caso contrario.
- Valida dimensiones iguales, minimo `2 x 2`, filas regulares, pesos `>= 0` y capacidades `> 0`.

`calcular_ocupacion(cargas, capacidades)`

- Entrada: matrices previamente validadas.
- Salida: `(porcentajes, sobrecargas)`.
- `porcentajes` conserva una estructura `N x M` y `sobrecargas` contiene coordenadas `(fila, columna)` con ocupacion mayor a `100 %`.

`evaluar_balance(cargas, tolerancia)`

- Entrada: matriz de cargas y tolerancia maxima en kg.
- Salida: `(pesos_por_fila, desbalance_lateral, balanceado)`.
- Con un numero par de columnas se comparan mitades iguales. Con un numero impar se excluye la columna central.

`extraer_submatriz_critica(porcentajes, k, p)`

- Entrada: matriz de porcentajes y dimensiones de la ventana.
- Salida: una nueva submatriz `k x p` con el mayor promedio de ocupacion.
- En empate se conserva la primera encontrada en el recorrido por filas y columnas.

### 6. Casos considerados

Se probaron casos normales y de borde: matriz minima `2 x 2`, columnas pares, columnas impares, pesos iguales a cero, pesos negativos, capacidades iguales a cero, dimensiones diferentes, filas irregulares, ventanas fuera de rango y verificacion de que las matrices de entrada no sean alteradas.

### 7. Complejidad computacional

Las funciones principales recorren la matriz por filas y columnas. Si la matriz tiene N filas y M columnas, cada celda se procesa una vez, por lo que el tiempo de ejecución de estas operaciones es O(N x M).

- `validar_matrices()`: recorre las filas y las columnas para comprobar las dimensiones y los valores de las matrices. Su complejidad es O(N x M).
- `calcular_ocupacion()`: recorre cada celda una vez para calcular el porcentaje de ocupación y detectar las sobrecargas. Su complejidad es O(N x M).
- `evaluar_balance()`: recorre las filas y sus columnas para obtener los pesos y comparar los lados de la matriz. Su complejidad es O(N x M).

Para `calcular_ocupacion()` se genera una nueva matriz de porcentajes del mismo tamaño N x M. Por esta razón, el espacio adicional utilizado para almacenar estos resultados es O(N x M).

La función `extraer_submatriz_critica()` utiliza un recorrido de las ventanas k x p posibles. Al analizar directamente cada ventana, su complejidad es:

O((N-k+1)(M-p+1)kp)

Esto se debe a que se recorren las posiciones posibles de la ventana y se calculan los valores que contiene cada submatriz.

En general, las operaciones de recorrido y transformación de las matrices utilizadas por el programa mantienen una complejidad lineal respecto a la cantidad de celdas, O(N x M), mientras que la búsqueda de la submatriz crítica depende además del tamaño de la ventana seleccionada.

### 8. Ejecución

Para ejecutar el programa principal:

```bash
python main.py

### 9. Resultado esperado con los datos de prueba

La matriz de porcentajes contiene valores como `85.0`, `78.0`, `110.0`, etc. Las celdas con mas de `100 %` se reportan como coordenadas. Tambien se muestra el peso total de cada fila, el desbalance lateral y la submatriz critica `2 x 2`.

### 10. Relacion con el contenido de clase

La implementacion utiliza listas y matrices bidimensionales y mantiene una separacion sencilla por funciones. La estructura de matrices se puede relacionar con el trabajo de NumPy visto en clase, donde se presentan arreglos multidimensionales y operaciones sobre matrices. Para la entrega principal se mantuvieron estructuras basicas de Python para que la logica del algoritmo sea visible.
