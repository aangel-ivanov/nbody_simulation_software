from math import log, trunc
import matplotlib.pyplot as plt
from vector_class import Vec3D


class System():
    def __init__(self, size):
        self.size = size # size of system
        self.bodies = [] # all bodies in the system
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
        self.bodies.append(body)

    def accelerate_all(self): # update acceleration of every body due to every other body
        bodies_copy = self.bodies.copy() # make a copy in case bodies are removed during the loop
        
        for i in bodies_copy: 
            for j in bodies_copy: # for every body update force due to every other body
                if i != j:
                    i.accelerate(j)

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
        self.accelerate_all()
        
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
        self.position += self.velocity * 86400 # one real second is one simulation day (86400 seconds in one day)
        
        if self.trace == True:
            self.positions += [[self.position.x, self.position.y, self.position.z]]


    def draw(self): # draw marker
        self.system.ax.plot(
            self.position.x, self.position.y, self.position.z, # draw marker at body's position,
            marker="o", # marker is a circle
            markersize=self.display_size + self.position.x / 100, # size depends on x-coordinate
            color=self.color
        )

    def accelerate(self, other):
        displacement = other.position - self.position
        distance = displacement.get_length()

        acceleration = displacement.normalize() * other.mass * self.G / (distance ** 2)
        self.velocity += acceleration * 86400
