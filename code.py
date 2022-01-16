#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, datetime, spade, random, sys
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour

koeficijentDomacin = 2.0
koeficijentGost = 2.0


def generirajAkciju():
    akcija = random.randint(0, 5)
    if(akcija==0):
        return "G1"
    if(akcija==1):
        return "G2"
    if(akcija==2):
        return "U1"
    if(akcija==3):
        return "U2"
    if(akcija==4):
        return "CK1"
    if(akcija==5):
        return "CK2"
    if(akcija==6):
        return "ZK1"
    if(akcija==7):
        return "ZK2"

def IspisiAkciju(akcija):
    if(akcija=="G1"):
        print("Gol domaćina")
    if(akcija=="G2"):
        print("Gol gosta")
    if(akcija=="U1"):
        print("Udarac domaćina")
    if(akcija=="U2"):
        print("Udarac gosta")
    if(akcija=="CK1"):
        print("Crveni karton domaćina")
    if(akcija=="CK2"):
        print("Crveni karton gosta")
    if(akcija=="ZK1"):
        print("Žuti karton domaćina")
    if(akcija=="ZK2"):
        print("Žuti karton gosta")

def obradiPocetniKoeficijent():
    global koeficijentDomacin, koeficijentGost
    pobjedeDomacin = random.randint(0, 5)
    pobjedeGost = random.randint(0, 5)
    if(pobjedeDomacin > pobjedeGost):
        koeficijentDomacin = koeficijentDomacin - ((pobjedeDomacin-pobjedeGost) * 0.15)
        koeficijentGost = koeficijentGost + ((pobjedeDomacin-pobjedeGost) * 0.15)
    if(pobjedeGost > pobjedeDomacin):
        koeficijentDomacin = koeficijentDomacin + ((pobjedeGost-pobjedeDomacin) * 0.15)
        koeficijentGost = koeficijentGost - ((pobjedeGost-pobjedeDomacin) * 0.15)


def obradiGolDomacin():
    global koeficijentDomacin, koeficijentGost
    koeficijentGost = koeficijentGost + 0.15
    if(koeficijentDomacin >= 1.25):
        koeficijentDomacin = koeficijentDomacin - 0.15
    else:
        koeficijentDomacin = 1.1

def obradiGolGost():
    global koeficijentDomacin, koeficijentGost
    koeficijentDomacin = koeficijentDomacin + 0.15
    if(koeficijentGost >= 1.25):
        koeficijentGost = koeficijentGost - 0.15
    else:
        koeficijentGost = 1.1

def obradiUdaracDomacin():
    global koeficijentDomacin, koeficijentGost
    koeficijentGost = koeficijentGost + 0.05
    if(koeficijentDomacin >= 1.15):
        koeficijentDomacin = koeficijentDomacin - 0.05
    else:
        koeficijentDomacin = 1.1

def obradiUdaracGost():
    global koeficijentDomacin, koeficijentGost
    koeficijentDomacin = koeficijentDomacin + 0.05
    if(koeficijentGost >= 1.15):
        koeficijentGost = koeficijentGost - 0.05
    else:
        koeficijentGost = 1.1

def obradiCrveniKartonDomacin():
    global koeficijentDomacin, koeficijentGost
    koeficijentDomacin = koeficijentDomacin + 0.2
    if(koeficijentGost >= 1.3):
        koeficijentGost = koeficijentGost - 0.2
    else:
        koeficijentGost = 1.1

def obradiCrveniKartonGost():
    global koeficijentDomacin, koeficijentGost
    koeficijentGost = koeficijentGost + 0.2
    if(koeficijentDomacin >= 1.3):
        koeficijentDomacin = koeficijentDomacin - 0.2
    else:
        koeficijentDomacin = 1.1

def obradiZutiKartonDomacin():
    global koeficijentDomacin, koeficijentGost
    koeficijentDomacin = koeficijentDomacin + 0.03
    if(koeficijentGost >= 1.13):
        koeficijentGost = koeficijentGost - 0.03
    else:
        koeficijentGost = 1.1

def obradiAkciju(akcija):
    global koeficijentDomacin, koeficijentGost
    if(akcija=="G1"):
        obradiGolDomacin()
    if(akcija=="G2"):
        obradiGolGost()
    if(akcija=="U1"):
        obradiUdaracDomacin()
    if(akcija=="U2"):
        obradiUdaracGost()
    if(akcija=="CK1"):
        obradiCrveniKartonDomacin()
    if(akcija=="CK2"):
        obradiCrveniKartonGost()
    if(akcija=="ZK1"):
        obradiZutiKartonDomacin()
    if(akcija=="ZK2"):
        obradiZutiKartonGost()
    print("Domacin "+str(round(koeficijentDomacin, 2)) +" | "+str(round(koeficijentGost, 2))+" Gost")

def obradiZutiKartonGost():
    global koeficijentDomacin, koeficijentGost
    koeficijentGost = koeficijentGost + 0.03
    if(koeficijentDomacin >= 1.13):
        koeficijentDomacin = koeficijentDomacin - 0.03
    else:
        koeficijentDomacin = 1.1

class Kladionica(Agent):
    class IzracunajKoeficijent(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout = 100)
            if msg:
                obradiAkciju(msg.body)

    async def setup(self):
        print("Računam početni koeficijent!")
        obradiPocetniKoeficijent()
        print("Domacin "+str(round(koeficijentDomacin, 2)) +" | "+str(round(koeficijentGost, 2))+" Gost")

        ponasanje = self.IzracunajKoeficijent()
        self.add_behaviour(ponasanje)

class Utakmica(Agent):
    maxBrojDogadaja = random.randint(5, 15)
    trenutniBrojDogadaja = 0
    class GenerirajDogadaj(PeriodicBehaviour):
        async def run(self):
            Utakmica.trenutniBrojDogadaja = Utakmica.trenutniBrojDogadaja + 1
            if(Utakmica.trenutniBrojDogadaja > Utakmica.maxBrojDogadaja):
                print("Kraj utakmice!")
                sys.exit()
            dogadaj = generirajAkciju()
            IspisiAkciju(dogadaj)
            msg = spade.message.Message(
                to="dmahnet_prvi@rec.foi.hr",
                body=dogadaj,
                metadata={
                    "language": "croatian",
                    "performative": "inform"})
            await self.send(msg)

    async def setup(self):
        posalji=self.GenerirajDogadaj(period=5, start_at = datetime.datetime.now())
        self.add_behaviour(posalji)

if __name__ == '__main__':
    
    kladionica=Kladionica("dmahnet_prvi@rec.foi.hr", "traxdata99")
    kladionica.start()
    time.sleep(1)
    utakmica=Utakmica("dmahnet_drugi@rec.foi.hr", "traxdata99")
    utakmica.start()
    input("Press ENTER to exit.\n")
    utakmica.stop()
    kladionica.stop()
    spade.quit_spade()
