import numpy as np
import plotly.express as px
import Particule
import random as rd

class SystemParticules:
    def __init__(self, nb_particules, origine, duree_vie, force, type):
        self.particules = []
        for i in range(nb_particules) :
             self.particules.append(Particule.Particule(origine, force, [0.02*rd.random(), 0.02*rd.random()], 1, type, duree_vie))
        self.force = force
    def maj_affichage(self, figure):
        positionX = [p.position[0] for p in self.particules]
        positionY = [p.position[1] for p in self.particules]
