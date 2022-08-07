from itertools import cycle
from vector_class import Vec3D
from nbody_classes import System, Body
from solar_system import add_SolarSystem
import matplotlib.pyplot as plt
import matplotlib.animation as animation


system = System(1000)
sim_duration = 100_000 # number of frames

# add_SolarSystem(system)

# The Sun
Body(system, mass=332_831, position=Vec3D(0, 0, 0), velocity=Vec3D(0, 0, 3.62973e-9), color='yellow', trace=True)

colors = cycle([(1, 0, 0), (0, 1, 0), (0, 0, 1)])

# Mercury
Body(system, mass=0.055239, position=Vec3D(0.387098, 0, 0), velocity=Vec3D(0, 3.16582e-7, 0), color=next(colors), trace=True)
# Venus
Body(system, mass=0.814508, position=Vec3D(0.723332, 0, 0), velocity=Vec3D(0, 2.34094e-7, 0), color=next(colors), trace=True)
# Earth
Body(system, mass=0.999398, position=Vec3D(0.999987, 0, 0), velocity=Vec3D(0, 1.99067e-7, 0), color=next(colors), trace=True)
# Mars
Body(system, mass=0.107381, position=Vec3D(1.52357, 0, 0), velocity=Vec3D(0, 1.60898e-7, 0), color=next(colors), trace=True)

# run without using animation:
# while True:
#     system.update()

def animate(i):
    return system.update()

ani = animation.FuncAnimation(
    system.fig,
    animate,
    repeat=False,
    frames=sim_duration,
    blit=False, # system.update() doesn't return anything
    interval=0, # plt.pause() in system.update() already provides interval
    )
plt.show()

# ani.save('orbital_simulation.mp4', fps=60, dpi=150)