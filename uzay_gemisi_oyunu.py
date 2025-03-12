import pygame  
import random
from abc import ABC, abstractmethod

pygame.init()


clock = pygame.time.Clock()

OYUNCU_RESIM = "/Users/mehmetsa00/Desktop/nesne tab1/resimler/uzay_gemisi.png"  
DUSMAN_RESIM = "/Users/mehmetsa00/Desktop/nesne tab1/resimler/dusman1.png"
ARKAPLAN_RESIM = "/Users/mehmetsa00/Desktop/nesne tab1/resimler/uzay_arkaplan.png"
MERMI_RESIM = "/Users/mehmetsa00/Desktop/nesne tab1/resimler/roket.png" 


class Ekran:
    __genislik = 1000  
    __yukseklik = 600  

    @staticmethod
    def get_boyut():
        return Ekran.__genislik, Ekran.__yukseklik
ekran = pygame.display.set_mode(Ekran.get_boyut())


arka_plan = pygame.image.load(ARKAPLAN_RESIM)
arka_plan = pygame.transform.scale(arka_plan, Ekran.get_boyut())


class Renkler:
    BEYAZ = (255, 255, 255)     
    SIYAH = (0, 0, 0)        
    KIRMIZI = (255, 0, 0)    
    YESIL = (0, 255, 0)      
    MAVI = (0, 0, 255)       


class Karakterler(ABC):
    def __init__(self, x, y, genislik, yukseklik, color):
        self._image = pygame.Surface((genislik, yukseklik))
        self._image.fill(color)
        self._şekil = self._image.get_rect()
        self._şekil.center = (x, y)

    @abstractmethod
    def guncelleme(self):
        pass

    def ciz(self, ekran):
        ekran.blit(self._image, self._şekil)

    def get_şekil(self):
        return self._şekil  


class Player(Karakterler):
    def __init__(self):
        genislik, yukseklik = Ekran.get_boyut()
        super().__init__(genislik // 2, yukseklik - 50, 50, 50, Renkler.YESIL)
        self.__hiz = 5
        self.can = 3

        self._image = pygame.image.load(OYUNCU_RESIM)
        self._image = pygame.transform.scale(self._image, (60, 60))

    def guncelleme(self):
        keys = pygame.key.get_pressed()
        şekil = self.get_şekil()
        if keys[pygame.K_LEFT] and şekil.left > 0:
            şekil.x -= self.__hiz
        if keys[pygame.K_RIGHT] and şekil.right < Ekran.get_boyut()[0]:
            şekil.x += self.__hiz

    def ates_et(self):
        şekil = self.get_şekil()
        mermi = Mermi(şekil.centerx, şekil.top)
        tum_karakterler.append(mermi)
        mermiler.append(mermi)


class Dusman(Karakterler):
    def __init__(self):
        genislik, yukseklik = Ekran.get_boyut()
        super().__init__(random.randint(0, genislik - 50), random.randint(-100, -40), 50, 50, Renkler.KIRMIZI)
        self.__hiz = random.randint(2, 5)

        self._image = pygame.image.load(DUSMAN_RESIM)
        self._image = pygame.transform.scale(self._image, (50, 50))

    def guncelleme(self):
        şekil = self.get_şekil()
        şekil.y += self.__hiz
        if şekil.top > Ekran.get_boyut()[1]:
            şekil.x = random.randint(0, Ekran.get_boyut()[0] - şekil.width)
            şekil.y = random.randint(-100, -40)


class Mermi(Karakterler):
    def __init__(self, x, y):
        super().__init__(x, y, 5, 10, Renkler.MAVI)
        self.__hiz = 7

        self._image = pygame.image.load(MERMI_RESIM)
        self._image = pygame.transform.scale(self._image, (15, 30)) 

    def guncelleme(self):
        şekil = self.get_şekil()
        şekil.y -= self.__hiz
        if şekil.bottom < 0:
            self.oldurme()

    def oldurme(self):
        if self in tum_karakterler:
            tum_karakterler.remove(self)
        if self in mermiler:
            mermiler.remove(self)


class Patlama(Karakterler):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, Renkler.SIYAH)
        self.çevreler = [pygame.image.load(f"/Users/mehmetsa00/Desktop/nesne tab1/resimler/patlama{i}.png") for i in range(1, 4)]
        self.çevre = 0
        self.animasyon_bitti = False

    def guncelleme(self):
        if self.çevre < len(self.çevreler):
            self._image = pygame.transform.scale(self.çevreler[self.çevre], (50, 50))
            self.çevre += 1
        else:
            self.animasyon_bitti = True
            if self in tum_karakterler:
                tum_karakterler.remove(self)


class Game:
    def __init__(self):
        self.__calisma = True
        self._puan = 0
        self.__font = pygame.font.SysFont(None, 36)

        self.kalp = pygame.image.load("/Users/mehmetsa00/Desktop/nesne tab1/resimler/kalp.png")
        self.kalp = pygame.transform.scale(self.kalp, (30, 30))

        global tum_karakterler, mermiler, Dusmanlar
        tum_karakterler = []
        mermiler = []
        Dusmanlar = []

        self.__player = Player()
        tum_karakterler.append(self.__player)

        for _ in range(10):
            dusman = Dusman()
            tum_karakterler.append(dusman)
            Dusmanlar.append(dusman)

    def islem_yap(self):
        for islem in pygame.event.get():
            if islem.type == pygame.QUIT:
                self.__calisma = False
            if islem.type == pygame.KEYDOWN:
                if islem.key == pygame.K_SPACE:
                    self.__player.ates_et()

    def carpma_kontrol(self):
        for mermi in mermiler:
            for dusman in Dusmanlar:
                if mermi.get_şekil().colliderect(dusman.get_şekil()):
                    self._puan += 10
                    patlama = Patlama(dusman.get_şekil().centerx, dusman.get_şekil().centery)
                    tum_karakterler.append(patlama)
                    dusman.get_şekil().x = random.randint(0, Ekran.get_boyut()[0] - dusman.get_şekil().width)
                    dusman.get_şekil().y = random.randint(-100, -40)
                    mermi.oldurme()

        for dusman in Dusmanlar:
            if self.__player.get_şekil().colliderect(dusman.get_şekil()):
                self.__player.can -= 1
                dusman.get_şekil().x = random.randint(0, Ekran.get_boyut()[0] - dusman.get_şekil().width)
                dusman.get_şekil().y = random.randint(-100, -40)
                if self.__player.can <= 0:
                    self.__calisma = False
                    self.oyun_bitti()

    def oyun_bitti(self):
        while True:
            ekran.fill(Renkler.SIYAH)
            font = pygame.font.SysFont(None, 72)
            mesaj = font.render("OYUN BİTTİ", True, Renkler.KIRMIZI)
            puan_mesaj = font.render(f"Puan: {self._puan}", True, Renkler.BEYAZ)

            ekran.blit(mesaj, (Ekran.get_boyut()[0] // 2 - mesaj.get_width() // 2, Ekran.get_boyut()[1] // 3))
            ekran.blit(puan_mesaj, (Ekran.get_boyut()[0] // 2 - puan_mesaj.get_width() // 2, Ekran.get_boyut()[1] // 2))

            tekrar_oyna_rect = pygame.Rect(Ekran.get_boyut()[0] // 2 - 100, Ekran.get_boyut()[1] // 2 + 100, 200, 50)
            cik_rect = pygame.Rect(Ekran.get_boyut()[0] // 2 - 100, Ekran.get_boyut()[1] // 2 + 180, 200, 50)

            pygame.draw.rect(ekran, Renkler.YESIL, tekrar_oyna_rect)
            pygame.draw.rect(ekran, Renkler.KIRMIZI, cik_rect)

            tekrar_oyna_yazi = self.__font.render("Tekrar Oyna", True, Renkler.BEYAZ)
            cik_yazi = self.__font.render("Çık", True, Renkler.BEYAZ)

            ekran.blit(tekrar_oyna_yazi, (tekrar_oyna_rect.centerx - tekrar_oyna_yazi.get_width() // 2, tekrar_oyna_rect.centery - tekrar_oyna_yazi.get_height() // 2))
            ekran.blit(cik_yazi, (cik_rect.centerx - cik_yazi.get_width() // 2, cik_rect.centery - cik_yazi.get_height() // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if tekrar_oyna_rect.collidepoint(event.pos):
                        self.__init__()
                        self.calistir()
                    elif cik_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()

    def guncelleme(self):
        for karakter in tum_karakterler:
            karakter.guncelleme()
        self.carpma_kontrol()

    def ciz(self):
        ekran.blit(arka_plan, (0, 0))
        for karakter in tum_karakterler:
            karakter.ciz(ekran)

        puan_durumu = self.__font.render(f"Puan: {self._puan}", True, Renkler.BEYAZ)
        ekran.blit(puan_durumu, (10, 10))

        for i in range(self.__player.can):
            ekran.blit(self.kalp, (Ekran.get_boyut()[0] - (40 * (i + 1)), 10))

    def calistir(self):
        while self.__calisma:
            self.islem_yap()
            self.guncelleme()
            self.ciz()
            pygame.display.flip()
            clock.tick(60)

# Oyunu başlat
game = Game()
game.calistir()
