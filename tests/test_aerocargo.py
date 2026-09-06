import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aerocargo import (
    calcular_ocupacion,
    evaluar_balance,
    extraer_submatriz_critica,
    validar_matrices,
)


class TestAerocargo(unittest.TestCase):

    def test_validacion_correcta(self):
        cargas = [[10, 20], [30, 40]]
        capacidades = [[20, 20], [40, 40]]
        self.assertTrue(validar_matrices(cargas, capacidades))

    def test_matriz_minima_2x2(self):
        cargas = [[0, 5], [7, 8]]
        capacidades = [[10, 10], [10, 10]]
        self.assertTrue(validar_matrices(cargas, capacidades))

    def test_dimensiones_diferentes(self):
        cargas = [[10, 20], [30, 40]]
        capacidades = [[20, 20, 20], [40, 40, 40]]
        self.assertFalse(validar_matrices(cargas, capacidades))

    def test_filas_irregulares(self):
        cargas = [[10, 20], [30]]
        capacidades = [[20, 20], [40, 40]]
        self.assertFalse(validar_matrices(cargas, capacidades))

    def test_peso_negativo(self):
        cargas = [[10, -1], [30, 40]]
        capacidades = [[20, 20], [40, 40]]
        self.assertFalse(validar_matrices(cargas, capacidades))

    def test_capacidad_cero(self):
        cargas = [[10, 20], [30, 40]]
        capacidades = [[20, 0], [40, 40]]
        self.assertFalse(validar_matrices(cargas, capacidades))

    def test_ocupacion_y_sobrecarga(self):
        cargas = [[10, 25], [20, 40]]
        capacidades = [[20, 20], [40, 40]]
        porcentajes, sobrecargas = calcular_ocupacion(cargas, capacidades)
        self.assertEqual(porcentajes[0][0], 50.0)
        self.assertEqual(sobrecargas, [(0, 1)])

    def test_balance_columnas_pares(self):
        cargas = [[10, 20, 20, 10], [5, 15, 15, 5]]
        filas, desbalance, estado = evaluar_balance(cargas, 1)
        self.assertEqual(filas, [60, 40])
        self.assertEqual(desbalance, 0)
        self.assertTrue(estado)

    def test_balance_columna_impar(self):
        cargas = [[10, 100, 10], [20, 50, 20]]
        filas, desbalance, estado = evaluar_balance(cargas, 1)
        self.assertEqual(filas, [120, 90])
        self.assertEqual(desbalance, 0)
        self.assertTrue(estado)

    def test_balance_fuera_de_tolerancia(self):
        cargas = [[30, 10], [20, 10]]
        _, desbalance, estado = evaluar_balance(cargas, 5)
        self.assertEqual(desbalance, 30)
        self.assertFalse(estado)

    def test_submatriz_critica(self):
        porcentajes = [
            [50, 60, 70],
            [80, 90, 60],
            [40, 50, 60],
        ]
        critica = extraer_submatriz_critica(porcentajes, 2, 2)
        self.assertEqual(critica, [[50, 60], [80, 90]])

    def test_submatriz_fuera_de_rango(self):
        porcentajes = [[50, 60], [70, 80]]
        self.assertEqual(extraer_submatriz_critica(porcentajes, 3, 2), [])

    def test_no_modifica_entradas(self):
        cargas = [[10, 20], [30, 40]]
        capacidades = [[20, 20], [40, 40]]
        cargas_original = [fila[:] for fila in cargas]
        capacidades_original = [fila[:] for fila in capacidades]
        calcular_ocupacion(cargas, capacidades)
        self.assertEqual(cargas, cargas_original)
        self.assertEqual(capacidades, capacidades_original)


if __name__ == "__main__":
    unittest.main()
