"""
COMP.CS.100
Tekijä: Pekka Heljakka
Opiskelijanumero: 150157515
Projekti 5 - Graafinen käyttöliittymä
"Alien Slime Attack Game!"

---

Arvostelijalle: Tarkoitus oli tehdä kehittyneempi käyttöliittymä - pelissä
on alkuvalikko, josta voi avata peli-ikkunan, valita vaikeustason radionapilla,
käytin myös slidereita ja pelin lopussa on erillinen "loppu-scene." Lisäksi
käytin erillisiä frameja eli aika paljon tavaraa, joka ei ollut
kurssimateriaalissa. Lisäksi tavoitteena oli tehdä ajastinloopissa pyörivä
peli, joka päivittyy tietyin väliajoin.

Pelissä siis luodaan limoja, jotka syövät maapallon eliöitä. Limat maksavat
biomassaa ja klikkailemalla +1, +10 jne nappeja niitä voi tehdä manuaalisesti.
Lisäksi voi tehdä puddleja, jotka generoivat limoja automaattisesti ja vain
niiden avulla pelin voi käytännössä voittaa järjellisessä ajassa.
Limat kuolevat ja muuttuvat sitä kauttaa uudestaan mikrobeiksi, jotka pitää
syödä uudestaan. Sliderilla voi vaikuttaa kunkin limatyypin tuotantonopeuteen,
jos esim kaikki ihmiset on jo syöty, ei kannata rakentaa enempää ihmisiä
syöviä limoja. Peli päättyy kun kaikki maapallon elämä on syöty pois.

Pelin voi pelata läpi muutamassa minuutissa siten että heti kun voi, niin
klikkailee itselleen ison kasan puddleja ja heti kun joku elämänmuoto on syöty
pois niin vetäisee limantuotannon nollaksi, ettei mikrobeja kasva liikaa.
Jokainen limatyyppi on erillinen, eli yksi slider ei vaikuta toiseen mitenkään.

---

Alien Slime Attack Game is a clicker/idle game where you control alien slimes,
who are trying to convert all life on Earth into slime and biomass. The game
finishes once all life on Earth is gone. It runs in a timed loop and player
can build varioust types of slimes which consume living things, either manually
or by building slime pools, which create the slimes automatically. Slimes
will be constantly dying, and dead slime mass is converted back to microbial
life so the player needs to balance the production rates to keep the playtime
reasonable.

You can select a cheat mode where the game finishes very quickly if you want
to test things fast as all production rates are massively increased.

Player can't really lose the game, which makes sense as alien slimes rarely
lose.

"""
from tkinter import *
import gamemanager


class StartingWindow:
    """
    This is the starting window or "main menu" of the game. You can select
    the difficulty level here and start the actual game, which starts in a
    new window.
    """
    def __init__(self):
        self.__main_window = Tk()
        self.__main_window.title("Alien Slime Attack Game!")

        self.__title = PhotoImage(file="title.gif")
        self.__title_label = Label(self.__main_window, image=self.__title)
        self.__title_label.pack()


        # Radio buttons for difficulty selection
        # currently only normal and cheat mode available
        self.__difficulty_label = Label(self.__main_window,
                                        text="Choose your difficulty!")
        self.__difficulty_label.pack()
        self.__radio_var = StringVar(value="normal")
        self.__difficulty_normal = Radiobutton(self.__main_window,
                                              text="normal",
                                              variable=self.__radio_var,
                                              value="normal")
        self.__difficulty_normal.pack()
        self.__difficulty_cheat = Radiobutton(self.__main_window,
                                              text="cheat",
                                              variable=self.__radio_var,
                                              value="cheat")

        self.__difficulty_cheat.pack()

        self.__infotext = "Welcome to Alien Slime Attack Game! \n" \
            "You control alien slimes in an attempt to consume all life " \
            "on Earth! \n Your small slimes eat plants, big slimes eat " \
            "animals, behemoth slimes eat humans (yikes!) and micro slimes " \
            "eat microbes. \n You can build them using collected biomass " \
            "either manually or by building puddles which spawn all types " \
            "of slimes automatically. \n You can control the spawn rates " \
            "with sliders. \n Your slimes will keep dying and decompose " \
            "into microbial life so manage your production well.\n" \
            "The game ends when all life on Earth is nothing " \
            "but slime or material for new slimes. \n \n"
        self.__info_label = Label(self.__main_window, text=self.__infotext)
        self.__info_label.pack()

        self.__start_button = Button(self.__main_window,
                                     text="Start your alien slime adventure!",
                                     command=self.start_game)
        self.__start_button.pack(pady=20)

        self.__main_window.mainloop()

    def start_game(self):
        """
        This function opens a new window and hides the main menu window.
        It creates a game manager object, which then handles the actual
        gameplay
        :return:
        """
        difficulty = self.__radio_var.get()
        window = Toplevel()
        gm = gamemanager.GameManager(window, difficulty, self.__main_window)
        self.__main_window.withdraw()


def main():
    UI = StartingWindow()


if __name__ == "__main__":
    main()
