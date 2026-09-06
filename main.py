from aerocargo import (
    calcular_ocupacion,
    evaluar_balance,
    extraer_submatriz_critica,
    validar_matrices,
)


cargas = [
    [850, 780, 620, 900],
    [1000, 820, 760, 700],
    [650, 1100, 500, 850],
    [900, 760, 920, 780],
]

capacidades = [
    [1000, 1000, 1000, 1000],
    [1000, 1000, 1000, 1000],
    [1000, 1000, 1000, 1000],
    [1000, 1000, 1000, 1000],
]

tolerancia = 250
k = 2
p = 2


def mostrar_matriz(matriz, decimales=1):
    for fila in matriz:
        print("  " + "  ".join(f"{valor:.{decimales}f}" for valor in fila))


def main():
    print("AEROCARGO-MATRIX")
    print("Auditoria de distribucion de carga en bahia de aeronave\n")

    print("1. Validacion de datos")
    datos_validos = validar_matrices(cargas, capacidades)
    print("Datos validos:", datos_validos)

    if not datos_validos:
        print("No se puede continuar porque las matrices no cumplen las condiciones.")
        return

    print("\n2. Porcentaje de ocupacion por celda")
    porcentajes, sobrecargas = calcular_ocupacion(cargas, capacidades)
    mostrar_matriz(porcentajes)
    print("\nCeldas sobrecargadas (>100%):", [(i + 1, j + 1) for i, j in sobrecargas])

    print("\n3. Balance de la aeronave")
    pesos_fila, desbalance, balanceado = evaluar_balance(cargas, tolerancia)
    print("Peso total por fila:", pesos_fila)
    print(f"Desbalance lateral: {desbalance:.1f} kg")
    print(f"Tolerancia: {tolerancia:.1f} kg")
    print("Estado del balance:", "APROBADO" if balanceado else "RECHAZADO")

    print("\n4. Submatriz critica")
    critica = extraer_submatriz_critica(porcentajes, k, p)
    print(f"Ventana seleccionada: {k} x {p}")
    mostrar_matriz(critica)


if __name__ == "__main__":
    main()
