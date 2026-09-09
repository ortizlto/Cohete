PRESION_NIVEL_MAR_HPA = 1013.25   # Presion SNDM
EXPONENTE_BAROMETRICO = 0.1903
UMBRAL_ACEL_CAIDA_LIBRE = -8.0
TEMP_ALERTA_C = 80.0
TEMP_CRITICA_C = 120.0
 
def calcular_altitud(presion_hpa: float):
    if presion_hpa <= 0:
        return 0.0
 
    altitud_m = 44330.0 * (1.0 - (presion_hpa / PRESION_NIVEL_MAR_HPA) ** EXPONENTE_BAROMETRICO)
    return altitud_m
 
 
def determinar_estado_vuelo(altitud_actual: float, altitud_previa: float, aceleracion: float):

    if altitud_actual >= altitud_previa:
        return 1
    if aceleracion <= UMBRAL_ACEL_CAIDA_LIBRE:
        return 2
    else:
        return 3
 
 
def texto_estado_vuelo(codigo_estado: int):
    if codigo_estado == 1:
        return "Ascenso"
    elif codigo_estado == 2:
        return "Apogeo / Caida libre"
    elif codigo_estado == 3:
        return "Despliegue de Paracaidas"
    else:
        return "Desconocido"
 
 
def evaluar_alerta_temperatura(temp_celsius: float):
    if temp_celsius >= TEMP_CRITICA_C:
        return True, "ALARMA CRITICA: temperatura extrema"
    elif temp_celsius >= TEMP_ALERTA_C:
        return True, "ALERTA: temperatura elevada"
    else:
        return False, "Temperatura normal"
 
def leer_dato_float(mensaje: str):
    while True:
        texto = input(mensaje)
        if es_numero(texto):
            return float(texto)
        else:
            print("  Valor invalido. Ingrese un numero (ej: 1010.5).")

def es_numero(texto: str):
    if texto == "":
        return False

    inicio = 1 if texto[0] in "+-" else 0
    if inicio == len(texto):
        return False

    cantidad_puntos = 0
    cantidad_digitos = 0
    for caracter in texto[inicio:]:
        if caracter == ".":
            cantidad_puntos += 1
            if cantidad_puntos > 1:
                return False
        elif "0" <= caracter <= "9":
            cantidad_digitos += 1
        else:
            return False

    return cantidad_digitos > 0
 
## Hecho con Claude, valida el string como un numero válido, sin usar try/except ni conversiones automáticas — todo a mano, carácter por carácter.
def mostrar_reporte_segundo(tiempo: int, altitud: float, codigo_estado: int,
                             temperatura: float, alarma: bool, mensaje_alarma: str):
    estado_texto = texto_estado_vuelo(codigo_estado)
    marca_alarma = " [!] " + mensaje_alarma if alarma else ""
    print(f"t={tiempo:3d}s | altitud={altitud:9.2f} m | estado={estado_texto:<24s} "
          f"| temp={temperatura:6.2f} C{marca_alarma}")

def main():

    print("=== Sistema de Monitoreo de Vuelo - Cohete Suborbital ===")
    print("Ingrese los datos de los sensores en cada segundo.")
    print("Escriba 'fin' en el campo de presion para terminar la simulacion.\n")
 
    altitud_previa: float = 0.0
    altitud_maxima: float = 0.0
    apogeo_detectado: bool = False
 
    suma_temperaturas: float = 0.0
    contador_lecturas: int = 0
    aceleracion_maxima: float = 0.0
 
    tiempo: int = 0
    aterrizo: bool = False

    while not aterrizo:
        entrada_presion = (0, 200)(f"[t={tiempo}s] Presion (hPa) o 'fin': ")
 
        if entrada_presion.lower() == "fin":
            print("\nSimulacion finalizada por el operador.")
            break
 
        if es_numero(entrada_presion):
            presion = float(entrada_presion)
        else:
            print("  Valor invalido. Ingrese un numero (ej: 1010.5) o 'fin'.")
            continue
 
        aceleracion = leer_dato_float(f"[t={tiempo}s] Aceleracion (m/s^2): ")
        temperatura = leer_dato_float(f"[t={tiempo}s] Temperatura (C): ")
 
        # --- Procesos matematicos/logicos ---
        altitud_actual = calcular_altitud(presion)
 
        if altitud_actual > altitud_maxima:
            altitud_maxima = altitud_actual
 
        codigo_estado = determinar_estado_vuelo(altitud_actual, altitud_previa, aceleracion)
 
        if not apogeo_detectado and altitud_actual < altitud_previa:
            apogeo_detectado = True
            print(f"  >> Apogeo detectado: altitud maxima = {altitud_maxima:.2f} m")
 
        alarma, mensaje_alarma = evaluar_alerta_temperatura(temperatura)
        suma_temperaturas += temperatura
        contador_lecturas += 1
        if abs(aceleracion) > aceleracion_maxima:
            aceleracion_maxima = abs(aceleracion)
 
        mostrar_reporte_segundo(tiempo, altitud_actual, codigo_estado,
                                 temperatura, alarma, mensaje_alarma)
 
        if altitud_actual <= 0.0 and tiempo > 0:
            aterrizo = True
            print("\n  >> El cohete ha aterrizado.")
 
        altitud_previa = altitud_actual
        tiempo += 1
    temperatura_promedio = suma_temperaturas / contador_lecturas if contador_lecturas > 0 else 0.0
 
    print("\n=== Resumen de la mision ===")
    print(f"Duracion registrada:      {tiempo} s")
    print(f"Apogeo (altitud maxima):  {altitud_maxima:.2f} m")
    print(f"Temperatura promedio:     {temperatura_promedio:.2f} C")
    print(f"Aceleracion maxima:       {aceleracion_maxima:.2f} m/s^2")

if __name__ == "__main__":
    main()