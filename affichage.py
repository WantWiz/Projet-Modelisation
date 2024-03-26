import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import numpy as np
import SystemParticules


# Initialisation de Pygame
pygame.init()
display = (2000, 1000)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Initialisation de GLUT
glutInit()
# Création des particules
num_particles = 100
syst = SystemParticules.SystemParticules(num_particles, [0,0], 200, np.array([0, -0.001]), "normal")
particles = syst.particules

# Fonction pour dessiner une particule
def draw_particle(particle):
    glPushMatrix()
    glTranslatef(particle.position[0], particle.position[1], 0)
    glColor3fv((1, 0, 0))
    glutSolidSphere(0.03, 20, 20)
    glPopMatrix()


# Fonction principale
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for particle in particles:
            particle.appliquer_force(syst.force, 2)

            # Réinitialiser la position si la particule sort de l'écran
            if abs(particle.position[0]) > 2.0:
                particle.position[0] = random.uniform(-1, 1)
            if abs(particle.position[1]) > 2.0:
                particle.position[1] = random.uniform(-1, 1)
            if particle.estMorte():
                particles.remove(particle)

            
            draw_particle(particle)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()