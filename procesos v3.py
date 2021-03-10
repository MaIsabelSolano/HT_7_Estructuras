#Algoritmos y Estructuras de Datos
#Yong Bum Park 20117
#Maria Isabel solano 20504
import simpy
import random

#configuración
random.seed(15)
Cantidad_RAM = 100
Memoria_Para_Proceso = random.randint(1,10)
limites_proceso = [1,10]
Tiempo_Memoria = random.expovariate(1.0/10)
Tiempo_entre_procesos = [1,10]
Capacidad_CPU = 3

#para cambiar
Cant_Procesos = 25

def proceso(nombre, env, espacio_CPU, capacidad_proceso, tiempo_proceso):
    
    lim_proceso = random.randint(*limites_proceso)
    print ('%s admitido al sitema operativo a las %.1f' % (nombre, env.now))
    with espacio_CPU.request() as req:
        inicio = env.now #inicio con el tiempo
        yield req #pedir un espacio
        
        Memoria_a_usar = Cantidad_RAM - lim_proceso #memoria que el proceso requiere
        yield capacidad_proceso.get(Memoria_a_usar) #pedir la memoria a usar
        
        yield env.timeout(tiempo_proceso) #tiempo que se tarda
        
        #impresión de lo que está pasando
        tiempo_tardado_por_proceso = env.now - inicio
        print('%s termina de correr en %.1f segundo.' % (nombre, tiempo_tardado_por_proceso))
        totalTime =+ tiempo_tardado_por_proceso
        
def CPU_control (env, capacidad_proceso):
    while True:
        if capacidad_proceso.level / capacidad_proceso.capacity * 100 < 10:
            print ('Desocupando espacio a las %d' % env.now)
            yield env.process(Recuparar_memoria(env,capacidad_proceso))
        yield env.timeout(10)
        
def Recuparar_memoria(env, capacidad_proceso):
    yield env.timeout(10)
    print('memoria recuperada a %d' % env.now)
    cant = capacidad_proceso.capacity - capacidad_proceso.level
    yield capacidad_proceso.put(cant)
            

#def
        
def Generador_procesos(env, espacio_CPU, capacidad_proceso, tiempo_proceso):
    #se encarga de generar los procesos que se requieren hacer
    for i in range(Cant_Procesos): #cantidad de procesos
        yield env.timeout(random.randint(*Tiempo_entre_procesos))
        env.process(proceso('Proceso %d' % i, env, espacio_CPU, capacidad_proceso, tiempo_proceso))

print ('Procesos')

#iniciar procesos y crear el ambiente
env = simpy.Environment()
espacio_CPU = simpy.Resource(env, Capacidad_CPU)
capacidad_proceso = simpy.Container(env, Cantidad_RAM, init = Cantidad_RAM)
env.process(CPU_control(env, capacidad_proceso))
env.process(Generador_procesos(env, espacio_CPU, capacidad_proceso, Tiempo_Memoria))
totalTime=0

#correr
env.run()

#promedio de atencion por procesoro. 
print("Tiempo total: %s" %totalTime)
promedio = totalTime/Cant_Procesos
print("Su promedio es de: %s" %promedio)
