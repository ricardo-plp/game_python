import pygame
import random
from pygame import *



LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600




class Vaisseau(pygame.sprite.Sprite):

    # Constructeur
    def __init__(self):
        super(Vaisseau, self).__init__()
        self.surf = pygame.image.load("vaisseau.png").convert()
        self.surf.set_colorkey((116, 166, 134 ), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Mise a  jour quand le joueur appuie sur une touche
    def update(self, pressed_keys):
        # vers le haut
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        #vers le bas
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        #vers la gauche
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        #vers la droite
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # Appui sur espace : Ajout d'un missible
        if pressed_keys[K_SPACE]:
            if len(le_missile.sprites()) < 1:
                missile = Missile(self.rect.center)
                le_missile.add(missile)
                tous_sprites.add(missile)


        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN



class Missile(pygame.sprite.Sprite):

    def __init__(self, center_missile):
        global player
        super(Missile, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=center_missile
        )

    def update(self):

        self.rect.move_ip(15, 0)

        if self.rect.left > LARGEUR_ECRAN:
            self.kill()



class Enemmi(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemmi, self).__init__()
        self.surf = pygame.image.load("meteorite.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                LARGEUR_ECRAN + 50,
                random.randint(0, HAUTEUR_ECRAN),
            )
        )
        self.speed = random.randint(5, 20)


    def update(self):

        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()



class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_vaisseau):
        super(Explosion, self).__init__()
        self._compteur = 10
        self.surf = pygame.image.load("explosion.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=center_vaisseau
        )

    def update(self):
        self._compteur = self._compteur - 1
        if self._compteur == 0:
            self.kill()



clock = pygame.time.Clock()


pygame.init()
pygame.display.set_caption("Escquive les meteorites")


AJOUTE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(AJOUTE_ENEMY, 600)


ecran = pygame.display.set_mode([LARGEUR_ECRAN, HAUTEUR_ECRAN])


tous_sprites = pygame.sprite.Group()
# Le missile
le_missile = pygame.sprite.Group()
# Les ennemis
les_ennemies = pygame.sprite.Group()
# Les explosions
les_explosions = pygame.sprite.Group()


vaisseau = Vaisseau()
tous_sprites.add(vaisseau)

# Game loop
continuer = True
while continuer:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

        elif event.type == AJOUTE_ENEMY:

            nouvel_enemmi = Enemmi()

            les_ennemies.add(nouvel_enemmi)
            tous_sprites.add(nouvel_enemmi)


    ecran.fill((0, 0, 0))


    if pygame.sprite.spritecollideany(vaisseau, les_ennemies):
        vaisseau.kill()
        explosion = Explosion(vaisseau.rect.center)
        les_explosions.add(explosion)
        tous_sprites.add(explosion)
        continuer = False


    for missile in le_missile:
        liste_ennemis_touches = pygame.sprite.spritecollide(
            missile, les_ennemies, True)
        if len(liste_ennemis_touches) > 0:
            missile.kill()
        for ennemi in liste_ennemis_touches:
            explosion = Explosion(ennemi.rect.center)
            les_explosions.add(explosion)
            tous_sprites.add(explosion)


    touche_appuyee = pygame.key.get_pressed()


    vaisseau.update(touche_appuyee)
    le_missile.update()
    les_ennemies.update()
    les_explosions.update()


    for mon_sprite in tous_sprites:
        ecran.blit(mon_sprite.surf, mon_sprite.rect)


    pygame.display.flip()


    clock.tick(30)


pygame.quit()
