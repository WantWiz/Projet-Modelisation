import numpy as np
import random

class Particule:
    def __init__(self, position, acceleration, vitesse, masse, type, lifespan, coeff_x, coeff_y):
        self.position = position
        self.acceleration = acceleration
        self.vitesse = vitesse
        self.masse = masse
        self.type = type
        self.id = 1 
        self.lifespan = lifespan
        self.coeff_x = coeff_x  # Coefficient de mouvement aléatoire selon x
        self.coeff_y = coeff_y  # Coefficient de mouvement aléatoire selon y

    def appliquer_force(self, force, diminution, frottement=0):
        # Ajouter les mouvements aléatoires aux vitesses selon x et y
        self.vitesse[0] += random.uniform(-self.coeff_x, self.coeff_x)
        self.vitesse[1] += random.uniform(-self.coeff_y, self.coeff_y)

        self.acceleration = (force - np.array(self.vitesse) * frottement) / self.masse
        self.vitesse = np.add(self.vitesse, self.acceleration)
        self.position = np.add(self.position, self.vitesse)
        self.lifespan -= diminution


    def estMorte(self):
        return self.lifespan < 0
    
    def calculer_force_gravitation(self, autre_particule, G=6.674e-11):
        """Calculer la force gravitationnelle entre cette particule et une autre particule."""
        distance = np.linalg.norm(np.subtract(autre_particule.position, self.position))
        if distance == 0:
            return np.zeros(2)
        force_gravitation = (G * self.masse * autre_particule.masse) / distance
        direction = np.subtract(autre_particule.position, self.position) / distance
        
        # Ajouter une atténuation en fonction de la distance
        force_gravitation_attenuée = force_gravitation / distance
        
        return force_gravitation_attenuée * direction