#Algoritmos y Estructuras de Datos, código basado y obtenido de https://simpy.readthedocs.io/en/latest/topical_guides/resources.html#res-type-container
#Yong Bum Park 20117
#Maria Isabel solano 20504
import simpy
import random

class Proceso:
    def __init__(self, env):
        self.fuel_dispensers = simpy.Resource(env, capacity=3)
        self.RAM = simpy.Container(env, init=100, capacity=1000)
        self.mon_proc = env.process(self.monitor_tank(env))

    def monitor_tank(self, env):
        while True:
            if self.RAM.level < 100:
                print(f'Calling tanker at {env.now}')
                env.process(tanker(env, self))
            yield env.timeout(15)


def tanker(env, gas_station):
    yield env.timeout(10)  # Need 10 Minutes to arrive
    print(f'Tanker arriving at {env.now}')
    amount = gas_station.RAM.capacity - gas_station.RAM.level
    yield gas_station.RAM.put(amount)


def proceso(name, env, gas_station):
    #env, name, bcs, driving_time, charge_duration
    global totalTime
    arrivingTime = env.now
    print(f'Proceso {name} llegando en {env.now}')
    with gas_station.fuel_dispensers.request() as req:
        yield req
        print("Cantidad de memoria que tiene: %s" %(gas_station.RAM.level))
        print(f'gas_station {name} starts refueling at {env.now}')
        yield gas_station.RAM.get(40)
        yield env.timeout(5)
        print(f'gas_station {name} done refueling at {env.now}')
        print("Cantidad de gas que queda: %s" %(gas_station.RAM.level))
    leavingTime = env.now-arrivingTime
    totalTime = totalTime + leavingTime
    print("Tiempo total transcurido: %s" %totalTime)


def proceso_generator(env, gas_station):
    
    for i in range(25):
        env.process(proceso(i, env, gas_station))
        #env.process(car(env, 'Car %d' % i, bcs, random.expovariate(1.0/10), tcarga))
        yield env.timeout(5)

#run simulation
env = simpy.Environment()
gas_station = Proceso(env)
random.seed(10)
proceso_gen = env.process(proceso_generator(env, gas_station))
totalTime=0
