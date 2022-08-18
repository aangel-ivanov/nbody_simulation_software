from math import log, trunc
import numpy as np
import matplotlib.pyplot as plt
from vector_class import Vec3D, Vec2D


class System():
    bodies = [] # all bodies in the system
    n = 0 # number of bodies
    def __init__(self, size):
        self.i = System.n # particle index

        self.size = size # size of system
        self.G = 1.19059e-19 # gravitational constant in AU / s^2 * earth masses

        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(
            1, # single set of axes
            1,
            subplot_kw={"projection": "3d"}, # set projection to 3d
            figsize=(6, 6) # size of figure
        )
        self.fig.tight_layout() # reduce margins at the edge of the figure
        self.ax.view_init(20, 30) # set initial perspective

    def add_body(self, body):
        System.bodies.append(body)
        System.n += 1

    def total_energy(self): # track total energy to monitor accuracy
        Energy = 0
        bodies_copy = self.bodies.copy()

        # potential energy
        for i, A in enumerate(bodies_copy):
            for B in bodies_copy[i + 1:]:
                inv_r = ((A.position.x - B.position.x) ** 2 + (A.position.y - B.position.y) ** 2 + (A.position.z - B.position.z) ** 2) ** (-0.5)
                Energy += 0.5 * A.mass * B.mass * inv_r * self.G

        # kinetic energy
        for body in bodies_copy:
            Energy += 0.5 * body.mass * ((body.velocity.x) ** 2 + (body.velocity.y) ** 2 + (body.velocity.z) ** 2)

        return Energy

    def update(self):
        # self.accelerate_all()
        
        # plot objects in order of x-coorindinate for correct layering
        self.bodies.sort(key=lambda item: item.position.x)
        for body in self.bodies:
            body.move()
            body.draw()
            
            # update trace
            if body.trace == True:
                self.ax.plot3D(
                    [elem[0] for elem in body.positions], 
                    [elem[1] for elem in body.positions], 
                    [elem[2] for elem in body.positions], 
                    color=body.color
                )

        # set limits for axes and update the plot
        # (in the update function in case they should change)
        # self.ax.set_title('Energy = ' + str(trunc(self.total_energy() / 1000)) + 'k', y=1.0, pad=-10)
        self.ax.set_xlim((-1, 1))
        self.ax.set_ylim((-1, 1))
        self.ax.set_zlim((-1, 1))
        self.ax.axis(False) # remove axes and grid
        plt.pause(0.1)
        self.ax.clear() # clear the previous frames

class Body():
    min_display_size = 3
    display_log_base = 1.4

    def __init__(
        self, 
        system,
        mass,
        position = Vec3D(0, 0, 0),
        velocity = Vec3D(0, 0, 0),
        color='white',
        trace=False
    ):
        self.system = system # connect body to a system
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = Vec3D(0, 0, 0)
        self.color = color
        self.trace = trace

        self.G = 1.19059e-19
        
        # if we are tracing we need to store all positions
        if self.trace == True:
            self.positions = [[self.position.x, self.position.y, self.position.z]]

        self.display_size = max( 
        # set marker size to be on log scale with 
        # the mass unless smaller than the min
            log(self.mass, self.display_log_base), 
            self.min_display_size
        )

        self.system.add_body(self)

    def move(self): # update position 
        # self.position += self.velocity * 86400

        dt = 86400 # one real second is one simulation day (86400 seconds in one day)
        state = np.array([self.position, self.velocity])
        self.position, self.velocity = self.RK4step(self.accelerate, state, dt)

        if self.trace == True:
            self.positions += [[self.position.x, self.position.y, self.position.z]]


    def draw(self): # draw marker
        self.system.ax.plot(
            self.position.x, self.position.y, self.position.z, # draw marker at body's position,
            marker="o", # marker is a circle
            markersize=self.display_size + self.position.x / 100, # size depends on x-coordinate
            color=self.color
        )

    def RK4step(self, f, u, dt):
        k1 = dt * f(u)
        k2 = dt * f(u + 0.5 * k1)
        k3 = dt * f(u + 0.5 * k2)
        k4 = dt * f(u + k3)
        return u + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    
    def accelerate(self, state):
        self.position, self.velocity = state

        def Newton(self, other):
            displacement = other.position - self.position
            distance = displacement.get_length()

            self.acceleration += displacement.normalize() * other.mass * self.G / (distance ** 2)

        bodies_copy = System.bodies.copy() 
        for j in bodies_copy: # for every body update force due to every other body
            if System.bodies[self.system.i] != j:
                Newton(System.bodies[self.system.i], j)
        return np.array([self.velocity, self.acceleration])

