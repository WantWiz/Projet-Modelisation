import numpy as np
import plotly.express as px

class Particule :

    ID = 1

    def __init__(self, position, acceleration, vitesse, masse, type, lifespan):
        self.position = position
        self.acceleration = acceleration
        self.vitesse = vitesse
        self.masse = masse
        self.type = type
        self.id = 1 
        #ID += 1
        self.lifespan = lifespan

    def appliquer_force(self, force, diminution):
        self.acceleration = force/self.masse
        self.vitesse = np.add(self.vitesse,self.acceleration)
        self.position = np.add(self.position,self.vitesse)
        self.lifespan -= diminution

    def estMorte(self):
        return (self.lifespan < 0)
    
        
    
        




