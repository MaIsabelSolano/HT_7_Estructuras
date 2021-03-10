import itertools
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
        print('%s termina de correr en %.1f segundo.' % (nombre, env.now - inicio))
        
#def CPU_control (env, capacidad_proceso):

#def
        
def Generador_procesos(env, espacio_CPU, capacidad_proceso, tiempo_proceso):
    #se encarga de generar los procesos que se requieren hacer
    for i in range(25): #cantidad de procesos
        yield env.timeout(random.randint(*Tiempo_entre_procesos))
        env.process(proceso('Proceso %d' % i, env, espacio_CPU, capacidad_proceso, tiempo_proceso))

print ('Procesos')

#iniciar procesos y crear el ambiente
env = simpy.Environment()
espacio_CPU = simpy.Resource(env, 3)
capacidad_proceso = simpy.Container(env, Cantidad_RAM, init = Cantidad_RAM)
env.process(Generador_procesos(env, espacio_CPU, capacidad_proceso, Tiempo_Memoria))

#correr
env.run()
