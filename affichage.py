import pygame
import numpy as np
from pygame.locals import *
from SystemParticules import SystemParticules
import pygame_gui

# Couleurs
BLACK = (0, 0, 0)

# Paramètres de la simulation
largeur, hauteur = 1100, 800

# Initialisation Pygame
pygame.init()

# Création de la fenêtre principale
screen = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Simulation de particules")

# Création du gestionnaire d'interface utilisateur pour la fenêtre principale
manager = pygame_gui.UIManager((largeur, hauteur))

# Création de la sous-fenêtre pour la simulation de particules
simulation_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0, 0, largeur - 250, hauteur),
                                                manager=manager)


parametres = {
    'Durée de vie': 5,
    'Force X': 0,
    'Force Y': 0.1,
    'Type': 'type1',
    'Nombre de particules': 10,
    'Coeff. vitesse initiale': 2,
    'Masse': 2,
    'Coeff. mouvement aléatoire X': 0.5,  
    'Coeff. mouvement aléatoire Y': 0.5  
}

# Calcul de la largeur nécessaire pour afficher tous les éléments
param_window_width = 250

# Calcul de la hauteur nécessaire pour afficher tous les éléments
param_window_height = max(400, len(parametres) * 40 + 120 + 120)  # Ajouter 120 pixels pour les boutons

# Création de la sous-fenêtre pour les champs de texte avec la nouvelle taille
parametres_window = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(largeur - param_window_width, 0, param_window_width, param_window_height),
    manager=manager)

# Champs de texte pour les paramètres
input_fields = {}
for i, (param_name, param_value) in enumerate(parametres.items()):
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10 + i * 40), (80, 30)),
                                        text=param_name + ":",
                                        manager=manager,
                                        container=parametres_window)
    input_fields[param_name] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 10 + i * 40), (120, 30)),
                                                                   manager=manager,
                                                                   container=parametres_window)
    input_fields[param_name].set_text(str(param_value))

# Bouton pour mettre à jour les paramètres
update_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 40 + len(parametres) * 40), (230, 30)),
                                             text='Mettre à jour',
                                             manager=manager,
                                             container=parametres_window)

# Bouton pour réinitialiser la simulation
reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 80 + len(parametres) * 40), (230, 30)),
                                            text='Réinitialiser',
                                            manager=manager,
                                            container=parametres_window)


# Liste des systèmes de particules
systemes_particules = []

# Bouton pour mettre en pause/reprendre la simulation
pause_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 160 + len(parametres) * 40), (230, 30)),  # Placer juste après le bouton de réinitialisation
    text='Pause',
    manager=manager,
    container=parametres_window)

# État de la simulation (True pour en cours, False pour en pause)
simulation_running = True

# Liste pour stocker les positions des particules du dernier état lorsque la simulation est en pause
dernier_etat_positions = []

# Boucle principale
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and simulation_window.rect.collidepoint(event.pos):
            if event.button == 1:  # Clic gauche
                pos = np.array(event.pos)
                systeme_particules = SystemParticules(
                    pos, 
                    parametres['Durée de vie'],
                    np.array([parametres['Force X'], parametres['Force Y']]),
                    parametres['Type'],
                    parametres['Nombre de particules'],
                    parametres['Coeff. vitesse initiale'],
                    parametres['Masse']
                )
                systemes_particules.append(systeme_particules)
        elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == update_button:
                for param_name, field in input_fields.items():
                    try:
                        if param_name == 'Nombre de particules':
                            parametres[param_name] = int(field.get_text())  # Convertir en entier
                        elif param_name.startswith('Coeff.'):
                            parametres[param_name] = float(field.get_text())  # Garder comme float pour les coefficients de mouvement aléatoire
                        else:
                            parametres[param_name] = float(field.get_text())  # Garder comme float pour les autres paramètres
                    except ValueError:
                        pass
            elif event.ui_element == reset_button:
                for systeme_particules in systemes_particules:
                    systeme_particules.reinitialiser()
            elif event.ui_element == pause_button:
                if simulation_running:
                    pause_button.set_text('Reprendre')
                    # Si la simulation est mise en pause, stockez uniquement les positions du dernier état
                    dernier_etat_positions = [[[particule.position.copy() for particule in systeme_particules.particules] for systeme_particules in systemes_particules]]
                else:
                    pause_button.set_text('Pause')

                simulation_running = not simulation_running


        # Transmettre les événements d'interface utilisateur au gestionnaire d'interface utilisateur
        manager.process_events(event)

    # Mise à jour des champs de texte
    manager.update(time_delta)

    # Effacer l'écran
    screen.fill(BLACK)

    # Rafraîchir l'interface utilisateur
    manager.draw_ui(screen)

    # Mettre à jour et afficher les systèmes de particules
    if simulation_running:
        for systeme_particules in systemes_particules:
            systeme_particules.duree_vie = parametres['Durée de vie']
            systeme_particules.force = np.array([parametres['Force X'], parametres['Force Y']])
            systeme_particules.type = parametres['Type']
            systeme_particules.nb_particules = parametres['Nombre de particules']
            systeme_particules.coeff_vitesse_initiale = parametres['Coeff. vitesse initiale']
            systeme_particules.masse = parametres['Masse']
            systeme_particules.generer_particules()
            systeme_particules.appliquer_forces()
            systeme_particules.maj_affichage(screen, simulation_window.rect)
    else:
        # Affichez les particules en utilisant les positions du dernier état stocké
        for etat_particule in dernier_etat_positions:
            for systeme_particules, positions in zip(systemes_particules, etat_particule):
                for position in positions:
                    # Affichez les particules à partir de l'état stocké
                    x = int(position[0])
                    y = int(position[1])
                    couleur = systeme_particules.couleur_particule(systeme_particules.duree_vie)
                    pygame.draw.circle(screen, couleur, (x, y), systeme_particules.masse)

    # Rafraîchir l'affichage
    pygame.display.flip()

pygame.quit()
