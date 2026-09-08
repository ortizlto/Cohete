# Cohete

## 1. Análisis del Problema (Entradas / Procesos / Salidas)
<img width="476" height="131" alt="image" src="https://github.com/user-attachments/assets/1537997c-825a-4b4a-bdd4-0f82cad5900a" />
## Cálculos y decisiones lógicas que el programa aplica a cada lectura:
●	Calcular la altitud actual a partir de la presión atmosférica, mediante la fórmula barométrica.
●	Registrar la altitud máxima alcanzada (apogeo) comparando la altitud actual contra el mayor valor visto hasta el momento (variable escalar acumuladora).
●	Determinar la fase de vuelo (ascenso, apogeo/caída libre o despliegue de paracaídas) comparando la altitud actual con la altitud del segundo anterior, y usando la aceleración para distinguir caída libre de descenso frenado.
●	Detectar el instante del apogeo por primera vez (altitud_actual < altitud_previa) y activar una bandera booleana que evita volver a reportarlo.
●	Evaluar si la temperatura del motor/estructura supera los umbrales de alerta (80 °C) o crítico (120 °C) y generar el mensaje de alarma correspondiente.
●	Acumular la suma de temperaturas y el conteo de lecturas, para calcular el promedio al finalizar (sin guardar cada lectura en una lista).
●	Actualizar la aceleración máxima registrada, comparando el valor absoluto de cada lectura contra el máximo acumulado.
●	Verificar la condición de aterrizaje (altitud_actual ≤ 0 con tiempo > 0) o la orden manual de finalización ('fin') para terminar el ciclo.

## Salidas
<img width="472" height="128" alt="image" src="https://github.com/user-attachments/assets/d2f89623-13b6-44a6-a58a-d17443193971" />

# 2. Diagrama de Flujo
https://lucid.app/lucidchart/34bc382c-4a85-43d2-8030-890a289ac82b/edit?viewport_loc=-761%2C319%2C2604%2C1335%2C0_0&invitationId=inv_c700d41b-38de-4c8c-aa95-012a6bd3c295 

# Pseudocódigo
## Primero, se define una función para calcular la altitud (Esto, usando losw datos de presion proveidos en el Notion)
FUNCION calcular_altitud(presion_hpa: float):
  SI presion_hpa <= 0 ENTONCES
      RETORNAR 0.0
  FIN SI
 
  altitud = 44330 * (1 - (presion_hpa / 1013.25) ^ 0.1903)
  RETORNAR altitud
FIN FUNCION

## Segundo, se determina el estado de vuelo mediante otra función definida
FUNCION determinar_estado_vuelo(altitud_actual: float, altitud_previa: float,
                                aceleracion: (float)
  SI altitud_actual >= altitud_previa ENTONCES
      RETORNAR 1
  SINO
      SI aceleracion <= -8.0 ENTONCES
          RETORNAR 2
      SINO
          RETORNAR 3
      FIN SI
  FIN SI
FIN FUNCION

## Tercero, se define para evaluar temperatura y asi emitir alertas
FUNCION evaluar_alerta_temperatura(temp_celsius: float) == (bool, str)
  SI temp_celsius >= 120.0 ENTONCES
      RETORNAR (Verdadero, "ALARMA CRITICA: temperatura extrema")
  SINO SI temp_celsius >= 80.0 ENTONCES
      RETORNAR (Verdadero, "ALERTA: temperatura elevada")
  SINO
      RETORNAR (Falso, "Temperatura normal")
  FIN SI
FIN FUNCION
