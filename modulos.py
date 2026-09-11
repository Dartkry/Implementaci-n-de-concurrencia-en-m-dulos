import threading
import time
import secrets

BUFFER_SIZE = 5 
buffer_compartido = []
mutex = threading.Lock()
espacios_vacios = threading.Semaphore(BUFFER_SIZE)
datos_disponibles = threading.Semaphore(0)
RNG = secrets.SystemRandom()

def sensor_trafico(id_sensor, lecturas):
    """
    Productor: Simula un sensor de tráfico que envía datos al SIGET.
    """
    for _ in range(lecturas):
        time.sleep(RNG.uniform(0.1, 0.5))
        cantidad_vehiculos = RNG.randint(1, 50)
        dato = f"[Sensor {id_sensor} | Vehículos detectados: {cantidad_vehiculos}]"
        espacios_vacios.acquire()
        mutex.acquire()

        buffer_compartido.append(dato)
        print(f"🟢 PRODUCTOR: Sensor {id_sensor} envió datos al búfer. Búfer actual: {len(buffer_compartido)}/{BUFFER_SIZE}")
        mutex.release()
        datos_disponibles.release()

def modulo_analisis(id_modulo, lecturas_a_procesar):
    """
    Consumidor: Simula el módulo central que procesa la información de tráfico.
    """
    for _ in range(lecturas_a_procesar):
        datos_disponibles.acquire()
        mutex.acquire()
        dato_procesado = buffer_compartido.pop(0)
        print(f"🔴 CONSUMIDOR: Módulo de análisis {id_modulo} procesando: {dato_procesado}. Búfer actual: {len(buffer_compartido)}/{BUFFER_SIZE}")
        mutex.release()
        espacios_vacios.release()
        time.sleep(RNG.uniform(0.5, 1.2))

if __name__ == "__main__":
    print("=== INICIANDO SIMULACIÓN SIGET (Productor-Consumidor) ===")
    hilos_sensores = [threading.Thread(target=sensor_trafico, args=(i, 4)) for i in range(1, 4)]
    hilos_modulos = [threading.Thread(target=modulo_analisis, args=(j, 6)) for j in range(1, 3)]

    for hilo in hilos_sensores + hilos_modulos:
        hilo.start()
        
    for hilo in hilos_sensores + hilos_modulos:
        hilo.join()
        
    print("=== SIMULACIÓN SIGET FINALIZADA ===")