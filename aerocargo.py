"""Funciones para la auditoria de carga de una bahia de aeronave."""


def validar_matrices(cargas, capacidades):
    """Valida dimensiones, regularidad, pesos no negativos y capacidades positivas."""
    if not isinstance(cargas, list) or not isinstance(capacidades, list):
        return False
    if len(cargas) < 2 or len(capacidades) < 2:
        return False
    if any(not isinstance(fila, list) for fila in cargas + capacidades):
        return False
    if any(len(fila) < 2 for fila in cargas + capacidades):
        return False

    columnas_cargas = len(cargas[0])
    columnas_capacidades = len(capacidades[0])
    if columnas_cargas != columnas_capacidades or columnas_cargas < 2:
        return False

    if any(len(fila) != columnas_cargas for fila in cargas):
        return False
    if any(len(fila) != columnas_capacidades for fila in capacidades):
        return False

    for fila in cargas:
        for peso in fila:
            if not isinstance(peso, (int, float)) or isinstance(peso, bool) or peso < 0:
                return False

    for fila in capacidades:
        for capacidad in fila:
            if not isinstance(capacidad, (int, float)) or isinstance(capacidad, bool) or capacidad <= 0:
                return False

    return True


def calcular_ocupacion(cargas, capacidades):
    """Calcula porcentajes de ocupacion y coordenadas de celdas sobrecargadas."""
    porcentajes = []
    sobrecargas = []

    for i in range(len(cargas)):
        fila_porcentajes = []
        for j in range(len(cargas[i])):
            porcentaje = (cargas[i][j] / capacidades[i][j]) * 100.0
            fila_porcentajes.append(porcentaje)
            if porcentaje > 100.0:
                sobrecargas.append((i, j))
        porcentajes.append(fila_porcentajes)

    return porcentajes, sobrecargas


def evaluar_balance(cargas, tolerancia):
    """Devuelve pesos por fila, desbalance lateral y estado del balance."""
    filas = [sum(fila) for fila in cargas]
    columnas = len(cargas[0])
    mitad = columnas // 2

    izquierda = 0
    derecha = 0

    if columnas % 2 == 0:
        for fila in cargas:
            izquierda += sum(fila[:mitad])
            derecha += sum(fila[mitad:])
    else:
        for fila in cargas:
            izquierda += sum(fila[:mitad])
            derecha += sum(fila[mitad + 1:])

    desbalance = abs(izquierda - derecha)
    balanceado = desbalance <= tolerancia

    return filas, desbalance, balanceado


def extraer_submatriz_critica(porcentajes, k, p):
    """Extrae la ventana k x p con mayor promedio de ocupacion.

    En empate se conserva la primera ventana encontrada al recorrer de
    arriba hacia abajo y de izquierda a derecha.
    """
    if not porcentajes or k < 1 or p < 1:
        return []
    if any(len(fila) != len(porcentajes[0]) for fila in porcentajes):
        return []
    if k > len(porcentajes) or p > len(porcentajes[0]):
        return []

    mejor_promedio = None
    mejor_submatriz = []

    for i in range(len(porcentajes) - k + 1):
        for j in range(len(porcentajes[0]) - p + 1):
            ventana = [fila[j:j + p] for fila in porcentajes[i:i + k]]
            promedio = sum(sum(fila) for fila in ventana) / (k * p)

            if mejor_promedio is None or promedio > mejor_promedio:
                mejor_promedio = promedio
                mejor_submatriz = [fila[:] for fila in ventana]

    return mejor_submatriz
