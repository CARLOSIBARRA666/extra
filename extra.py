# Tupla con los tipos de vehículo permitidos
TIPOS_PERMITIDOS = ("carro", "moto", "bicicleta")

# 2. Diccionario con la tarifa por hora de cada tipo
TARIFAS = {"carro": 3000, "moto": 1500, "bicicleta": 500}


# Calcula el valor a pagar
def calcular_cobro(tipo, horas, descuento=0):
    # Si estuvo menos de 1 hora, se cobra 1 hora completa
    if horas < 1:
        horas = 1
    total = TARIFAS[tipo] * horas
    # El descuento se maneja como porcentaje (ej: 10 = 10%)
    return total - (total * descuento / 100)


# Valida que la placa tenga exactamente 6 caracteres
def placa_valida(placa):
    return len(placa) == 6


# Clase Parqueadero
class Parqueadero:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.vehiculos = {}    # {placa: {"tipo": ..., "conductor": ...}}
        self.historial = []    # lista de tuplas (placa, tipo, horas, valor_pagado)

    # Ingresar un vehículo (devuelve True si lo aceptó, False si lo rechazó)
    def ingresar(self, placa, tipo, conductor):
        if len(self.vehiculos) >= self.capacidad:
            return False
        if tipo not in TIPOS_PERMITIDOS:
            return False
        if not placa_valida(placa):
            return False
        if placa in self.vehiculos:
            return False
        self.vehiculos[placa] = {"tipo": tipo, "conductor": conductor}
        return True

    # sacar un vehículo, cobrar y guardar en el historial
    def salir(self, placa, horas, descuento=0):
        if placa not in self.vehiculos:
            return None
        # Se saca del diccionario y se calcula el cobro
        tipo = self.vehiculos.pop(placa)["tipo"]
        valor = calcular_cobro(tipo, horas, descuento)
        self.historial.append((placa, tipo, horas, valor))
        return valor

    # Placas de los vehículos que están dentro
    def placas_dentro(self):
        return list(self.vehiculos.keys())

    # suma de todos los pagos del historial
    def total_recaudado(self):
        return sum(registro[3] for registro in self.historial)

    # Total recaudado por cada tipo de vehículo
    def reporte_por_tipo(self):
        reporte = {}
        for placa, tipo, horas, valor in self.historial:
            reporte[tipo] = reporte.get(tipo, 0) + valor
        return reporte


# ---------- Prueba ----------
p = Parqueadero(3)
print(p.ingresar("ABC123", "carro", "Juan"))   
print(p.ingresar("XYZ789", "moto", "Ana"))     
print(p.ingresar("ABC123", "carro", "Pedro"))    # False (ya está dentro)
print(p.ingresar("AB12", "carro", "Luis"))       # False (placa inválida)
print(p.ingresar("DEF456", "camion", "Sara"))    # False (tipo no permitido)

print(p.placas_dentro())                         # ['ABC123', 'XYZ789']
print(p.salir("ABC123", 2))                      # 6000.0
print(p.salir("XYZ789", 0.5, descuento=10))      # 1350.0
print(p.total_recaudado())                       # 7350.0
print(p.reporte_por_tipo())                      # {'carro': 6000.0, 'moto': 1350.0}