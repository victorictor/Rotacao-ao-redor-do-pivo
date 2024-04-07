from math import degrees,atan2
from pygame.draw import line, rect
from pygame.transform import rotate, flip
from pygame.mouse import get_pos
from pygame import Vector2

def Rotacionar_no_pivot(imagem, angulo, pivot, origem): # Origem é coordenada da imagem (geralmento o centro).
    img = rotate(imagem, angulo)

    vetorSemPivot = origem - pivot # Remover as coordenadas no Vetor.
    vetorRotacionado = vetorSemPivot.rotate(-angulo) # Rotacionar somente o Vetor negativamente em sentido anti-horario ou seja (sentido horario).
    offset = pivot + vetorRotacionado # Adiciona a coordenada do Pivot nesse novo Vetor.

    #offset = pivot + (origem - pivot).rotate(-angulo) <----- Forma resumida. 

    rect = img.get_rect(center = offset) # Cria um novo Rect centralizado no vetor (offset)

    return img, rect

class SpikeBall:
    comprimentoCorrente = 32
    def __init__(self, dictReferencia, pivot,  primeiroAngulo = 0):
        self.pivot = pivot # Pivot é uma coordenada (x,y).
        self.angulo = 0
        
        offset = Vector2()      # COMPRIMENTO         # ANGULO (em pygame o y é negativo)
        offset.from_polar((self.comprimentoCorrente, -primeiroAngulo)) # atribui ao vetor "offset" um comprimento(distancia) e um angulo(direçao)
                                                                       
        self.pos = pivot  + offset # A variavel "self.pos" é o Vetor (offset) na coordenada (pivot),
                                   # ou seja esta usando o vetor na coordenada informada somando os dois.

                                   # A soma de dois vetores ou de uma coordenada com vetor, se da pela soma dos respectivos componentes:
                                    
                                   # Ex: 
                                   # (A1, A2) + (B1, B2) = (A1 + B1, A2 + B2) 
                                   # ou 
                                   # (1, 2) + (5, 6) = (1 + 5, 5 + 6) ---> novo vetor

        self.imgOrig = dictReferencia['spikeball'] # Carrega e imagem no dicionario de referencias.
        self.img = self.imgOrig # Para caso de inverter a imagem.

        self.rect = self.img.get_rect(center = self.pos) # Usamos o vetor com offset aplicado na posiçao do centro do rect.

    def update(self, dt):
        self.angulo += 50 * dt
        self.img, self.rect = Rotacionar_no_pivot(self.imgOrig, self.angulo, self.pivot, self.pos)

    def draw(self, tela):
        line(tela, (51, 57, 65), self.pivot, self.rect.center, width=3)
        line(tela, (109, 117, 141), self.pivot, self.rect.center)

        tela.blit(self.img, self.rect)

class Weapon:
    def __init__(self, dictReferencia, pivot):
        self.pivot = pivot

        self.pos = pivot + (20, 0) # Uma coordenada baseada no pivot (coord), somado 20 no x da coordenada do pivot.

        self.imgOrig = dictReferencia['weapon']
        self.imgUnflip = self.imgOrig # Imagem normal.
        self.imgflip = flip(self.imgOrig, False, True) # Imagem girada.

        self.img = self.imgOrig
        self.rect = self.img.get_rect(center = self.pos)

    def update(self, dt, centroTela):
        mousePos = Vector2(get_pos()) # Criando vetor com a posiçao do mouse (começa no canto superio esquerdo da tela).

        if mousePos.x < centroTela.x: #Caso o x do vetor do mouse for maior menor que o x do centro da tela.
            self.imgOrig = self.imgflip # Imagem orginal vai ser tornar imagem invertida.
        else:
            self.imgOrig = self.imgUnflip # Imagem orginal vai ser tornar imagem normal.

        mouseOffset = mousePos - self.pivot # Traz as coordenadas do vetor para as coordenadas do pivot.
                                            # OBS: O vetor do mouse ja tem coordenadas entao se fosse somada
                                            # a coordenada do pivot ao vetor do mouse as coordenadas do pivot iriam para
                                            # o final do vetor do mouse.

        mouseAngulo = -degrees(atan2(mouseOffset.y, mouseOffset.x)) # "atan2" retorna o angulo em radianos (por meio de pitagoras)
                                                                    # "-degrees" transforma esse radiano em graus

        self.img, self.rect = Rotacionar_no_pivot(self.imgOrig, mouseAngulo, self.pivot, self.pos)
        print(mousePos)
    def draw(self, tela):
        tela.blit(self.img, self.rect)