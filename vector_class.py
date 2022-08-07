import numpy as np

class Vec3D:
    def __init__(self, x=0, y=0, z=0): # 3D vector class
        self.x = x
        self.y = y
        self.z = z

    def __str__(self): # For printing
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, v):
        return Vec3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def __radd__(self, v):
        return Vec3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vec3D(self.x - v.x, self.y - v.y, self.z - v.z)

    def __rsub__(self, v):
        return Vec3D(v.x - self.x, v.y - self.y, v.z - self.y)

    def __mul__(self, n):
        return Vec3D(self.x * n, self.y * n, self.z * n)

    def __rmul__(self, n):
        return Vec3D(self.x * n, self.y * n, self.z * n)

    def __truediv__(self, n):
        return Vec3D(self.x / n, self.y / n, self.z / n)

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def get_length(self):
        return np.sqrt(self.dot(self))

    def normalize(self):
        return self / self.get_length()