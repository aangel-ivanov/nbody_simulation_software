from vector_class import Vec3D
from nbody_classes import System, Body
from itertools import cycle

colors = cycle([(1, 0, 0), (0, 1, 0), (0, 0, 1)])

def add_SolarSystem(system):

    Body(system, mass=332_831, position=Vec3D(0, 0, 0), velocity=Vec3D(0, 0, 0), color='yellow')

    # Mercury
    Body(system, mass=0.055239, position=Vec3D(0.387098, 0, 0), velocity=Vec3D(0, 3.16582e-7, 0), color=next(colors), trace=True)
    # Venus
    Body(system, mass=0.814508, position=Vec3D(0.723332, 0, 0), velocity=Vec3D(0, 2.34094e-7, 0), color=next(colors), trace=True)
    # Earth
    Body(system, mass=0.999398, position=Vec3D(0.999987, 0, 0), velocity=Vec3D(0, 1.99067e-7, 0), color=next(colors), trace=True)
    # Mars
    Body(system, mass=0.107381, position=Vec3D(1.52357, 0, 0), velocity=Vec3D(0, 1.60898e-7, 0), color=next(colors), trace=True)
    # Jupiter
    # Body(system, mass=317.636, position=Vec3D(5.20442, 0, 0), velocity=Vec3D(0, 8.68997*(10**-8), 0), color=next(colors), trace=True)
    # Saturn
    # Body(system, mass=95.1037, position=Vec3D(9.58255, 0, 0), velocity=Vec3D(0, 6.47068*(10**-8), 0), color=next(colors))
    # Uranus
    # Body(system, mass=14.5269, position=Vec3D(19.2012, 0, 0), velocity=Vec3D(0, 4.54552*(10**-8), 0), color=next(colors))
    # Neptune
    # Body(system, mass=17.1374, position=Vec3D(30.0476, 0, 0), velocity=Vec3D(0, 3.62973*(10**-8), 0), color=next(colors))