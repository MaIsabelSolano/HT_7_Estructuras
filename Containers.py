#Algoritmos y Estructuras de Datos, código basado y obtenido de https://simpy.readthedocs.io/en/latest/topical_guides/resources.html#res-type-container
#Yong Bum Park 20117
#Maria Isabel solano 20504
import simpy
import random

class GasStation:
    def __init__(self, env):
        self.fuel_dispensers = simpy.Resource(env, capacity=2)
        self.gas_tank = simpy.Container(env, init=100, capacity=100)
        self.mon_proc = env.process(self.monitor_tank(env))

    def monitor_tank(self, env):
        while True:
            if self.gas_tank.level < 100:
                print(f'Calling tanker at {env.now}')
                env.process(tanker(env, self))
            yield env.timeout(15)


def tanker(env, gas_station):
    yield env.timeout(10)  # Need 10 Minutes to arrive
    print(f'Tanker arriving at {env.now}')
    amount = gas_station.gas_tank.capacity - gas_station.gas_tank.level
    yield gas_station.gas_tank.put(amount)


def car(name, env, gas_station):
    global totalTime
    arrivingTime = env.now
    print(f'Proceso {name} arriving at {env.now}')
    with gas_station.fuel_dispensers.request() as req:
        yield req
        print("Cantidad de gas que tiene: %s" %(gas_station.gas_tank.level))
        print(f'gas_station {name} starts refueling at {env.now}')
        yield gas_station.gas_tank.get(40)
        yield env.timeout(5)
        print(f'gas_station {name} done refueling at {env.now}')
        print("Cantidad de gas que queda: %s" %(gas_station.gas_tank.level))
    leavingTime = env.now-arrivingTime
    totalTime = totalTime + leavingTime
    print("Tiempo total transcurido: %s" %totalTime)
#es el que decide cuantas veces lo realizara
cantidad =25

def car_generator(env, gas_station):
    
    for i in range(cantidad):
        env.process(car(i, env, gas_station))
        
        yield env.timeout(5)

env = simpy.Environment()
gas_station = GasStation(env)
car_gen = env.process(car_generator(env, gas_station))
totalTime=0
env.run(10000)
#promedio de atencion por carro. 
print("Tiempo total: %s" %totalTime)
promedio = totalTime/cantidad
print("Su promedio es de: %s" %promedio)





