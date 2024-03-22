import numpy as np
class Particule :

    ID = 1

    def __init__(self, position, acceleration, vitesse, masse, type, lifespan):
        self.position = position
        self.acceleration = acceleration
        self.vitesse = vitesse
        self.masse = masse
        self.type = type
        self.id = ID 
        ID += 1
        self.lifespan = lifespan

    def appliquer_force(self, force):
        self.acceleration = force/self.masse
        self.vitesse = np.add(self.vitesse,self.acceleration)
        self.position = np.add(self.position,self.vitesse)
        





