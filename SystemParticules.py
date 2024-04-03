import numpy as np
import pygame
from Particule import Particule
import random as rd

RED = (255, 0, 0)

class SystemParticules:
    def __init__(self, origine, duree_vie, force, type, nb_particules, coeff_vitesse_initiale, masse):
        self.particules = []
        self.force = force  # Stocker la force
        self.origine = origine
        self.duree_vie = duree_vie
        self.type = type
        self.temps_ecoule = 0  # Temps écoulé depuis la dernière génération de particules
        self.taux_generation = 5  # Taux de génération de particules par seconde
        self.nb_particules = nb_particules
        self.coeff_vitesse_initiale = coeff_vitesse_initiale
        self.masse = masse

    def couleur_particule(self, lifespan):
        # Calculer la proportion de durée de vie restante
        if lifespan < 0:
            ratio = 0
        else:
            ratio = min(1, lifespan / self.duree_vie)

        # Interpoler linéairement entre le rouge et le vert en fonction de la durée de vie restante
        couleur_r = int(255 * ratio)
        couleur_g = 0
        couleur_b = 0  # Valeur bleue fixée à 0

        # Retourner la couleur sous forme de tuple (R, G, B)
        return (couleur_r, couleur_g, couleur_b)

    def maj_affichage(self, screen, param_window_rect):
        particules_a_supprimer = []  # Liste pour stocker les indices des particules à supprimer
        for i, particule in enumerate(self.particules):
            if not np.isnan(particule.position).any():
                x = int(particule.position[0])
                y = int(particule.position[1])

                # Vérifier si la particule est en dehors de la fenêtre de paramètres
                if param_window_rect.collidepoint((x, y)):
                    couleur = self.couleur_particule(particule.lifespan)
                    pygame.draw.circle(screen, couleur, (x, y), particule.masse)
            
            # Vérifiez si la particule a atteint la fin de sa durée de vie
            if particule.estMorte():
                particules_a_supprimer.append(i)

        # Supprimez les particules arrivées en fin de vie de la liste
        for index in sorted(particules_a_supprimer, reverse=True):
            del self.particules[index]


    def appliquer_forces(self):
        for particule in self.particules:
            particule.appliquer_force(self.force, 0.1)

    def ajouter_particule(self, position, acceleration, vitesse, masse, type, lifespan, coeff_x, coeff_y):
        self.particules.append(Particule(position, acceleration, vitesse, masse, type, lifespan, coeff_x, coeff_y))

    def generer_particules(self):
        self.temps_ecoule += 1
        if self.temps_ecoule >= 60 / self.taux_generation:
            for _ in range(self.nb_particules):
                # Ajouter des coefficients aléatoires pour les mouvements selon x et y
                coeff_x = rd.uniform(0, 0.5)
                coeff_y = rd.uniform(0, 0.5)
                vitesse_x = self.coeff_vitesse_initiale * rd.uniform(-1, 1)
                vitesse_y = self.coeff_vitesse_initiale * rd.uniform(-1, 1)
                self.ajouter_particule(self.origine, self.force, [vitesse_x, vitesse_y], self.masse, self.type, self.duree_vie, coeff_x, coeff_y)
            self.temps_ecoule = 0


    def reinitialiser(self):
        self.particules = []  # Réinitialiser la liste des particules