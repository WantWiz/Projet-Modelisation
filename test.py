import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Définition des couleurs
colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 1),
    (0, 0, 0),
)

# Fonction pour créer une particule
def create_particle():
    return {
        'pos': [random.uniform(-1, 1), random.uniform(-1, 1)],
        'color': random.choice(colors),
        'size': random.uniform(0.01, 0.05),
        'speed': [random.uniform(-0.005, 0.005), random.uniform(-0.005, 0.005)]
    }

# Initialisation de Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Initialisation de GLUT
glutInit()

# Création des particules
num_particles = 100
particles = [create_particle() for _ in range(num_particles)]

# Fonction pour dessiner une particule
def draw_particle(particle):
    glPushMatrix()
    glTranslatef(particle['pos'][0], particle['pos'][1], 0)
    glColor3fv(particle['color'])
    glutSolidSphere(particle['size'], 20, 20)
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
            particle['pos'][0] += particle['speed'][0]
            particle['pos'][1] += particle['speed'][1]

            # Réinitialiser la position si la particule sort de l'écran
            if abs(particle['pos'][0]) > 1.0:
                particle['pos'][0] = random.uniform(-1, 1)
            if abs(particle['pos'][1]) > 1.0:
                particle['pos'][1] = random.uniform(-1, 1)

            draw_particle(particle)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
