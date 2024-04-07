import pygame as pg
from pygame import Vector2

from objetos import SpikeBall,  Weapon

tamanhoTela = Vector2(192, 108)
centroTela = tamanhoTela // 2
dictImagens = {}

class Game:
    fullscreen = True
    def __init__(self):
        pg.init()

        self.clock = pg.Clock()
        self.running = False

        self.tela = pg.display.set_mode(tamanhoTela, flags= pg.SCALED)

        self.load_images('spikeball', colorkey= 'white') # Carregando imagem da bola de espinhos.
        self.load_images('weapon', colorkey= 'white') # Carreganodo imagem da arma.

        self.spikeball = SpikeBall(dictImagens, centroTela,  primeiroAngulo= 45) # Instaciada classe da bola de espinhos
        self.weapon = Weapon(dictImagens, centroTela) # Intanciando a classe da arma, pivot = centro da tela

    def load_images(self, image_name, colorkey = None): # Carrega imagen do disco (uma vez) e as armazena em um dicionario para ser referenciada,
                                                        # ajuda no desempenho.
        image = pg.image.load(f'{image_name}.png').convert()
        
        if colorkey is not None:
            image.set_colorkey(colorkey)

        dictImagens[image_name] = image # Permite carregar a imagem no dicionario pelo nome.

    def update(self, dt):
        self.spikeball.update(dt) # Atualiza Spikeball update()
        self.weapon.update(dt, centroTela) # Atualiza Weapon update()

    def draw(self, tela):
        tela.fill('black')

        pg.draw.line(tela, 'red', (centroTela.x, 0), (centroTela.x, tamanhoTela.y))
        pg.draw.line(tela, 'red', (0, centroTela.y), (tamanhoTela.x, centroTela.y))

        self.spikeball.draw(tela) # Desenhando a Bola de espinhos.
        self.weapon.draw(tela) # Desenha arma na tela.
    
        pg.display.flip()

    # MAIN LOOP
    def run(self):
        self.running = True
        while self.running:
            
            dt =  self.clock.tick() * .001
            self.fps = self.clock.get_fps()
            pg.display.set_caption(f'FPS: {self.fps}')

            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    self.running = False

                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_ESCAPE:
                        self.running = False

                    if ev.key == pg.K_f:
                        self.fullscreen = not self.fullscreen # Inverte a boolena da variavel false ---> true e virse versa.
                        if not self.fullscreen:
                            self.tela = pg.display.set_mode(tamanhoTela, flags= pg.SCALED | pg.FULLSCREEN)
                        else:
                            self.tela = pg.display.set_mode(tamanhoTela, flags= pg.SCALED)

            self.update(dt)
            self.draw(self.tela)

if __name__ == '__main__':
    Game().run()