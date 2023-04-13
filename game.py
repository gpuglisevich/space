import pygame
import os
import random
import math

pygame.init()  # Mover la inicialización de Pygame aquí

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Nave Espacial")

        # Cargar imágenes
        self.backgrounds = [Background(pygame.image.load(os.path.join("assets", f"background_{i}.png")), i * -600) for i in range(1, 9)]

        self.player = Player(400, 500, pygame.transform.scale(pygame.image.load(os.path.join("assets", "rocket.png")), (64, 64)))

        self.missiles = []


        # Cargar imagen del misil
        self.missile = pygame.image.load(os.path.join("assets", "missile.png")).convert_alpha()
        self.missile = pygame.transform.rotate(self.missile, -90)  # Agregar esta línea para rotar la imagen original en 90 grados
        self.missile = pygame.transform.scale(self.missile, (48, 48))
        
        # Cargar imagen del big_misil
        self.big_missile = pygame.image.load(os.path.join("assets", "big_missile.png")).convert_alpha()
        self.big_missile = pygame.transform.rotate(self.big_missile, -90)  # Rotar la imagen original en 90 grados
        self.big_missile = pygame.transform.scale(self.big_missile, (96, 96))  # Ajusta el tamaño según lo desees
        
         # Cargar imagen de la explosion
        self.explosion_image = pygame.image.load(os.path.join("assets", "explosion.png")).convert_alpha()
        self.explosion_image = pygame.transform.scale(self.explosion_image, (64, 64))
        self.explosions = []


        print("Imagen del misil cargada.") 

        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lives = 3

    def run(self):
        print("Iniciando el juego...")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        return self.game_over_screen()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_UP]:
            self.player.move_up()
        if keys[pygame.K_DOWN]:
            self.player.move_down()

    def update(self):
        for background in self.backgrounds:
            background.update()

        if random.random() < 0.007:  # Ajusta la probabilidad según lo desees
            x = random.randint(0, 800 - self.big_missile.get_width())
            speed_y = random.uniform(5, 10)  # Ajusta la velocidad según lo desees
            diagonal = random.choice([True, False])
            if diagonal:
                speed_x = random.uniform(-5, 5)  # Ajusta la velocidad según lo desees
            else:
                speed_x = 0
            self.missiles.append(Missile(x, y=-self.big_missile.get_height(), speed_x=speed_x, speed_y=speed_y, image=self.big_missile, diagonal=diagonal))
            

        if random.random() < 0.04:
            x = random.randint(0, 800 - self.missile.get_width())
            speed_y = random.uniform(5, 10)
            diagonal = random.choice([True, False])
            if diagonal:
                speed_x = random.uniform(-8, 8)
            else:
                speed_x = 0
            self.missiles.append(Missile(x, y=-self.missile.get_height(), speed_x=speed_x, speed_y=speed_y, image=self.missile, diagonal=diagonal))

        for missile in self.missiles:
            missile.update()
            if missile.y > 600:
                self.missiles.remove(missile)
                self.score += 1
            if self.player.collide(missile):
                self.missiles.remove(missile)
                self.lives -= 1

                # Agrega una explosión
                explosion = Explosion(self.player.x, self.player.y, self.explosion_image)
                self.explosions.append(explosion)

                if self.lives == 0:
                    self.running = False

        # Actualiza las explosiones y las elimina si han terminado
        self.explosions = [explosion for explosion in self.explosions if not explosion.update()]

    def draw(self):
        for background in self.backgrounds:
            self.screen.blit(background.image, (0, background.y))

        self.screen.blit(self.player.image, (self.player.x, self.player.y))


        for missile in self.missiles:
            angle = math.atan2(missile.speed_y, missile.speed_x)  # calcula el ángulo de la dirección
            rotated_missile = pygame.transform.rotate(missile.image, math.degrees(-angle))  # rota la imagen del misil
            self.screen.blit(rotated_missile, (missile.x, missile.y))  # dibuja el misil rotado
            
             # Dibuja las explosiones
        for explosion in self.explosions:
            self.screen.blit(explosion.image, (explosion.x, explosion.y))

        self.draw_text(f"Score: {self.score}", 24, 10, 10)
        self.draw_text(f"Lives: {self.lives}", 24, 10, 40)

        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))
    
    def game_over_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("Game Over", 48, 400, 250)
        self.draw_text("Press Space to Restart", 32, 370, 300)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                        return True
            self.clock.tick(60)
     
    def reset(self):
        self.backgrounds = [Background(pygame.image.load(os.path.join("assets", f"background_{i}.png")), i * -600) for i in range(1, 9)]
        self.player = Player(400, 500, pygame.transform.scale(pygame.image.load(os.path.join("assets", "rocket.png")), (64, 64)))
        self.missiles = []
        self.score = 0
        self.lives = 3
        self.running = True       
        
class Explosion:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.frame_counter = 0

    def update(self):
        self.frame_counter += 1
        if self.frame_counter > 30:  # Duración de la explosión en cuadros
            return True  # Si ha pasado suficiente tiempo, la explosión debe eliminarse
        return False

        

class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def move_left(self):
        self.x -= 5
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += 5
        if self.x > 800 - self.image.get_width():
            self.x = 800 - self.image.get_width()

    def move_up(self):
        self.y -= 5
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += 5
        if self.y > 600 - self.image.get_height():
            self.y = 600 - self.image.get_height()

    def collide(self, missile):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()).colliderect(
            pygame.Rect(missile.x, missile.y, missile.image.get_width(), missile.image.get_height())
        )

class Missile:
    def __init__(self, x, y, speed_x, speed_y, image, diagonal):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = image
        self.diagonal = diagonal

    def update(self):
        if self.diagonal:
            self.x += self.speed_x
            self.y += self.speed_y
        else:
            self.y += self.speed_y

class Background:
    def __init__(self, image, y):
        self.image = image
        self.y = y
        self.speed = 2

    def update(self):
        self.y += self.speed
        if self.y >= 600:
            self.y = -4800 + self.y

if __name__ == "__main__":
    pygame.init()

    game = Game()

    while True:
        restart = game.run()
        if not restart:
            break

    pygame.quit()

