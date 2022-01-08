"""
COMP.CS.100
Tekijä: Pekka Heljakka
Opiskelijanumero: 150157515
"""
import tkinter

from resourcemanager import *
from tkinter import *
from functools import partial


class GameManager():
    """
    Game manager handles building the game screen UI, checks for victory
    conditions and builds the end scene UI. It also checks which buttons to
    enable and disable based on player's resources.
    """

    def __init__(self, window, difficulty, main_window):

        self.__rm = ResourceManager(difficulty)
        self.__game_window = window  # Game is played in this window
        self.__main_window = main_window  # This reference for quitting game

        # Initialise variables for victory scene and condition
        self.__victory_text = ""
        self.__vic_line = 1
        self.__game_won = False

        # initialise stats for the game manager
        self.__turn_length = 500
        if difficulty == "cheat":
            self.__turn_length = 100
        self.__day = 0

        # load all pictures
        self.__puddle_img = PhotoImage(file="puddle.gif")
        self.__small_img = PhotoImage(file="small.gif")
        self.__big_img = PhotoImage(file="big.gif")
        self.__behe_img = PhotoImage(file="behemoth.gif")
        self.__micro_img = PhotoImage(file="micro.gif")

        # This label used to count time
        self.__messages = Label(self.__game_window, text="")
        self.__messages.grid(row=1, column=1)

        # Puddle Area in UI

        self.__puddle_count = Label(self.__game_window, text="")
        self.__puddle_count.grid(row=2, column=1)
        self.__puddle_pic = Label(self.__game_window, image=self.__puddle_img)
        self.__puddle_pic.grid(row=3, column=1)

        # Puddle buttons to build 1, 10, 100, 1000 or 10000 puddles
        # Buttons are in a separate frame to prevent them from spreading out

        self.__puddle_bt_frame = tkinter.Frame(self.__game_window)
        self.__puddle_bt_frame.grid(row=4, column=1)

        self.__puddle_plusone = Button(self.__puddle_bt_frame, text="+1",
                                command=partial(self.add_puddles, 1))
        self.__puddle_plusone.grid(row=1, column=1, sticky=W)

        self.__puddle_plusten = Button(self.__puddle_bt_frame, text="+10",
                                command=partial(self.add_puddles, 10))
        self.__puddle_plusten.grid(row=1, column=2, sticky=W)

        self.__puddle_plushundred = Button(self.__puddle_bt_frame, text="+100",
                                command=partial(self.add_puddles, 100))
        self.__puddle_plushundred.grid(row=1, column=3, sticky=W)

        self.__puddle_plusthousand = Button(self.__puddle_bt_frame, text="+1000",
                                command=partial(self.add_puddles, 1000))
        self.__puddle_plusthousand.grid(row=2, column=1, sticky=W)

        self.__puddle_plustenthousand = Button(self.__puddle_bt_frame, text="+10000",
                                command=partial(self.add_puddles, 10000))
        self.__puddle_plustenthousand.grid(row=2, column=2, sticky=E)

        self.__biomass_lbl = Label(self.__game_window, text="")
        self.__biomass_lbl.grid(row=5, column=1)

        self.__dead_lbl = Label(self.__game_window, text="")
        self.__dead_lbl.grid(row=6, column=1)

        # Quit game button

        self.__quit_btn = Button(self.__game_window, text="Quit Game",
                                 command=self.quit_game)
        self.__quit_btn.grid(row=7, column=1)

        self.__puddle_info_txt = "One puddle will spawn:\n" \
                                 "10,000 small slimes\n" \
                                 "100 big slimes\n" \
                                 "10 behemoth slimes\n" \
                                 "100,000 micro slimes"
        self.__puddle_info_lbl = Label(self.__game_window,
                                       text=self.__puddle_info_txt,
                                       justify=LEFT)
        self.__puddle_info_lbl.grid(row=8, column=1)

        # Slime area
        # The text is hardcoded just because it's not likely to change anymore

        # Set small slimes
        self.__small_count = Label(self.__game_window,
                                   text="Small Slimes, cost 10 kg")
        self.__small_count.grid(row=2, column=2)
        self.__small_pic = Label(self.__game_window, image=self.__small_img)
        self.__small_pic.grid(row=3, column=2)

        # Set big slimes
        self.__big_count = Label(self.__game_window,
                                 text="Big Slimes, cost 100 kg")
        self.__big_count.grid(row=4, column=2)
        self.__big_pic = Label(self.__game_window, image=self.__big_img)
        self.__big_pic.grid(row=5, column=2)

        # Set behemoth slimes
        self.__behe_count = Label(self.__game_window,
                                  text="Behemoth Slimes, cost 3000 kg")
        self.__behe_count.grid(row=6, column=2)
        self.__behe_pic = Label(self.__game_window, image=self.__behe_img)
        self.__behe_pic.grid(row=7, column=2)

        # Set micro slimes
        self.__micro_count = Label(self.__game_window,
                                   text="Micro Slimes, cost 1 kg")
        self.__micro_count.grid(row=8, column=2)
        self.__micro_pic = Label(self.__game_window, image=self.__micro_img)
        self.__micro_pic.grid(row=9, column=2)

        # Slime button area :(

        # The placement of buttons and sliders is not optimal but neater
        # placement would need more frames which is a bit excessive for the
        # scope of this game

        # Small Slimes
        self.__small_count_lbl = Label(self.__game_window, text="")
        self.__small_count_lbl.grid(row=2, column=3)
        self.__small_frame = tkinter.Frame(self.__game_window)
        self.__small_frame.grid(row=3, column=3)

        self.__small_slider = Scale(self.__small_frame, from_=0, to=100,
                                    orient=HORIZONTAL)
        self.__small_slider.set(100)
        self.__small_slider.grid(row=2, column=1, sticky=W)
        self.__small_slider_info = Label(self.__small_frame,
                                         text="Puddle production rate (%)")
        self.__small_slider_info.grid(row=1, column=1, sticky=W)

        self.__small_plusone = Button(
            self.__small_frame, text="+1",
            command=partial(self.add_slime, 1, "small"))
        self.__small_plusone.grid(row=2, column=2,sticky=W)

        self.__small_plusten = Button(
            self.__small_frame, text="+10",
            command=partial(self.add_slime, 10, "small"))
        self.__small_plusten.grid(row=2, column=3)

        self.__small_plushundred = Button(
            self.__small_frame, text="+100",
            command=partial(self.add_slime, 100, "small"))
        self.__small_plushundred.grid(row=2, column=4)

        self.__small_plusthousand = Button(
            self.__small_frame, text="+1000",
            command=partial(self.add_slime, 1000, "small"))
        self.__small_plusthousand.grid(row=2, column=5)

        # Big slimes

        self.__big_count_lbl = Label(self.__game_window, text="")
        self.__big_count_lbl.grid(row=4, column=3)
        self.__big_frame = tkinter.Frame(self.__game_window)
        self.__big_frame.grid(row=5, column=3)

        self.__big_slider = Scale(self.__big_frame, from_=0, to=100,
                                    orient=HORIZONTAL)
        self.__big_slider.set(100)
        self.__big_slider.grid(row=2, column=1, sticky=W)
        self.__big_slider_info = Label(self.__big_frame,
                                         text="Puddle production rate (%)")
        self.__big_slider_info.grid(row=1, column=1, sticky=W)

        self.__big_plusone = Button(
            self.__big_frame, text="+1",
            command=partial(self.add_slime, 1, "big"))
        self.__big_plusone.grid(row=2, column=2, )

        self.__big_plusten = Button(
            self.__big_frame, text="+10",
            command=partial(self.add_slime, 10, "big"))
        self.__big_plusten.grid(row=2, column=3)

        self.__big_plushundred = Button(
            self.__big_frame, text="+100",
            command=partial(self.add_slime, 100, "big"))
        self.__big_plushundred.grid(row=2, column=4)

        self.__big_plusthousand = Button(
            self.__big_frame, text="+1000",
            command=partial(self.add_slime, 1000, "big"))
        self.__big_plusthousand.grid(row=2, column=5)

        # Behemoth slimes

        self.__behe_count_lbl = Label(self.__game_window, text="")
        self.__behe_count_lbl.grid(row=6, column=3)
        self.__behe_frame = tkinter.Frame(self.__game_window)
        self.__behe_frame.grid(row=7, column=3)

        self.__behe_slider = Scale(self.__behe_frame, from_=0, to=100,
                                  orient=HORIZONTAL)
        self.__behe_slider.set(100)
        self.__behe_slider.grid(row=2, column=1, sticky=W)
        self.__behe_slider_info = Label(self.__behe_frame,
                                       text="Puddle production rate (%)")
        self.__behe_slider_info.grid(row=1, column=1, sticky=W)

        self.__behe_plusone = Button(
            self.__behe_frame, text="+1",
            command=partial(self.add_slime, 1, "behe"))
        self.__behe_plusone.grid(row=2, column=2, )

        self.__behe_plusten = Button(
            self.__behe_frame, text="+10",
            command=partial(self.add_slime, 10, "behe"))
        self.__behe_plusten.grid(row=2, column=3)

        self.__behe_plushundred = Button(
            self.__behe_frame, text="+100",
            command=partial(self.add_slime, 100, "behe"))
        self.__behe_plushundred.grid(row=2, column=4)

        self.__behe_plusthousand = Button(
            self.__behe_frame, text="+1000",
            command=partial(self.add_slime, 1000, "behe"))
        self.__behe_plusthousand.grid(row=2, column=5)

        # Micro slimes

        self.__micro_count_lbl = Label(self.__game_window, text="")
        self.__micro_count_lbl.grid(row=8, column=3)
        self.__micro_frame = tkinter.Frame(self.__game_window)
        self.__micro_frame.grid(row=9, column=3)

        self.__micro_slider = Scale(self.__micro_frame, from_=0, to=100,
                                   orient=HORIZONTAL)
        self.__micro_slider.set(100)
        self.__micro_slider.grid(row=2, column=1, sticky=W)
        self.__micro_slider_info = Label(self.__micro_frame,
                                        text="Puddle production rate (%)")
        self.__micro_slider_info.grid(row=1, column=1, sticky=W)

        self.__micro_plusone = Button(
            self.__micro_frame, text="+1",
            command=partial(self.add_slime, 1, "micro"))
        self.__micro_plusone.grid(row=2, column=2, )

        self.__micro_plusten = Button(
            self.__micro_frame, text="+10",
            command=partial(self.add_slime, 10, "micro"))
        self.__micro_plusten.grid(row=2, column=3)

        self.__micro_plushundred = Button(
            self.__micro_frame, text="+100",
            command=partial(self.add_slime, 100, "micro"))
        self.__micro_plushundred.grid(row=2, column=4)

        self.__micro_plusthousand = Button(
            self.__micro_frame, text="+1000",
            command=partial(self.add_slime, 1000, "micro"))
        self.__micro_plusthousand.grid(row=2, column=5)


        # Biomass left in the world

        self.__plant_lbl = Label(self.__game_window, text="Plant mass")
        self.__plant_lbl.grid(row=2, column=4)
        self.__animal_lbl = Label(self.__game_window, text="Animal mass")
        self.__animal_lbl.grid(row=4, column=4)
        self.__human_lbl = Label(self.__game_window, text="Human mass")
        self.__human_lbl.grid(row=6, column=4)
        self.__micro_lbl = Label(self.__game_window, text="Microbial mass")
        self.__micro_lbl.grid(row=8, column=4)

        self.run_game()

    def quit_game(self):
        """
        Ends the game when in game screen
        :return:
        """
        self.__game_window.destroy()
        self.__main_window.destroy()

    def end_scene(self):
        """
        Played when player wins
        :return:
        """
        self.__end_window = Toplevel()
        self.__end_window.title("All is slime!")
        self.__end_window.geometry("500x100")
        self.__victory_text = "Congratulations, you have converted all life " \
                              "on Earth into slime."
        self.__vic_label = Label(self.__end_window, text=self.__victory_text)
        self.__vic_label.pack(pady=(10, 20))
        self.__victory_button = Button(self.__end_window, text="All is Slime!",
                                command=self.change_victory_text)
        self.__victory_button.pack()
        self.__game_window.withdraw()

    def change_victory_text(self):
        """
        This is used only while playing the end scene
        :return:
        """
        if self.__vic_line == 1:
            self.__victory_text = "However, all is not slime."
            self.__vic_line += 1
            self.__victory_button.configure(text="Slime is all!")
            self.__vic_label.configure(text=self.__victory_text)
        elif self.__vic_line == 2:
            self.__victory_text = "Biomass left on Earth: You"
            self.__vic_line += 1
            self.__vic_label.configure(text=self.__victory_text)
            self.__victory_button.configure(text="I live for the slime!")
        elif self.__vic_line == 3:
            self.__victory_text = "Biomass left on Earth: "
            self.__vic_line += 1
            self.__vic_label.configure(text=self.__victory_text)
            self.__victory_button.configure(text="I am slime!")
        elif self.__vic_line == 4:
            self.__victory_text = "Biomass left on Earth: 0"
            self.__victory_button.configure(text="*Happy slime noises*")
            self.__vic_line += 1
            self.__vic_label.configure(text=self.__victory_text)
        elif self.__vic_line == 5:
            self.__victory_text = "Thank you for playing!"
            self.__vic_line += 1
            self.__vic_label.configure(text=self.__victory_text)
        elif self.__vic_line == 6:
            self.__end_window.destroy()
            self.__game_window.destroy()
            self.__main_window.destroy()

    def add_puddles(self, count):
        """
        Builds as many puddles as the parameter indicates. This is done by
        calling the resource manager, which handles the resource calculation.
        :param count: int, how many puddles to build
        :return:
        """
        self.__rm.build_puddles(count)
        self.update_labels()
        self.update_buttons()

    def add_slime(self, count, slimetype):
        """
        The manual slime spawn buttons call this function to create more
        slimes. The check of how many slimes can be created is done in the
        button configurations, this function will simply add whatever is
        called. It then calls the resource manager to deal with the actual
        addition and biomass calculation.
        :param count: int, how many slimes to add
        :param slimetype: which type of slime to add
        :return:
        """
        if slimetype == "small":
            self.__rm.small_slime.add_slimes(count)
        elif slimetype == "big":
            self.__rm.big_slime.add_slimes(count)
        elif slimetype == "behe":
            self.__rm.behemoth_slime.add_slimes(count)
        elif slimetype == "micro":
            self.__rm.micro_slime.add_slimes(count)
        self.update_labels()
        self.update_buttons()

    def update_labels(self):
        """
        Updates all labels in the game screen.
        :return:
        """
        day_text = "Day " + str(self.__day) + " of your alien slime adventure!"
        self.__messages.configure(text= day_text)

        puddle_text = "Number of puddles (cost 10,000 kg): \n" + str(self.__rm.puddles)
        self.__puddle_count.configure(text=puddle_text)

        bm_lbl_txt = f"Biomass collected:\n {self.__rm.biomass} kg"
        self.__biomass_lbl.configure(text=bm_lbl_txt)

        dead_lbl_txt = f"Dead slime mass:\n {self.__rm.dead_slime} kg"
        self.__dead_lbl.configure(text=dead_lbl_txt)

        small_lbl_txt = f"Number of small slimes: " \
                        f"{self.__rm.small_slime.get_count()} \nTotal mass: "\
                        f"{self.__rm.small_slime.get_mass()} kg"
        self.__small_count_lbl.configure(text=small_lbl_txt)

        big_lbl_txt = f"Number of big slimes: " \
                        f"{self.__rm.big_slime.get_count()} \nTotal mass: "\
                        f"{self.__rm.big_slime.get_mass()} kg"
        self.__big_count_lbl.configure(text=big_lbl_txt)

        behe_lbl_txt = f"Number of behemoth slimes: " \
                        f"{self.__rm.behemoth_slime.get_count()} \nTotal mass: "\
                        f"{self.__rm.behemoth_slime.get_mass()} kg"
        self.__behe_count_lbl.configure(text=behe_lbl_txt)

        micro_lbl_txt = f"Number of microscopic slimes: " \
                       f"{self.__rm.micro_slime.get_count()} \nTotal mass: " \
                       f"{self.__rm.micro_slime.get_mass()} kg"
        self.__micro_count_lbl.configure(text=micro_lbl_txt)

        plant_lbl_txt = f"Total plant biomass left: \n " \
                        f"{self.__rm.plant_mass} kg"
        self.__plant_lbl.configure(text=plant_lbl_txt)
        animal_lbl_txt = f"Total animal biomass left: \n " \
                        f"{self.__rm.animal_mass} kg"
        self.__animal_lbl.configure(text=animal_lbl_txt)
        human_lbl_txt = f"Total human biomass left: \n " \
                        f"{self.__rm.human_mass} kg"
        self.__human_lbl.configure(text=human_lbl_txt)
        micro_lbl_txt = f"Total microbial biomass left: \n " \
                        f"{self.__rm.microbe_mass} kg"
        self.__micro_lbl.configure(text=micro_lbl_txt)

        # Pull values from sliders and pass them to resource manager
        small_slime_puddle_rate = self.__small_slider.get() / 100
        self.__rm.prod_rate_small = small_slime_puddle_rate

        big_slime_puddle_rate = self.__big_slider.get() / 100
        self.__rm.prod_rate_big = big_slime_puddle_rate

        behe_slime_puddle_rate = self.__behe_slider.get() / 100
        self.__rm.prod_rate_behe = behe_slime_puddle_rate

        micro_slime_puddle_rate = self.__micro_slider.get() / 100
        self.__rm.prod_rate_micro = micro_slime_puddle_rate

    def update_buttons(self):
        """
        Enables and disables the buttons in the game. If there is enough
        resources to build a slime or puddle, the button is active and can
        then call the appropriate build function. This function effectively
        works as part of the resource management.
        :return:
        """
        bm = self.__rm.biomass
        # Puddles
        max_puddles = self.__rm.max_puddles()
        self.__puddle_plustenthousand.configure(state=NORMAL)
        self.__puddle_plusthousand.configure(state=NORMAL)
        self.__puddle_plushundred.configure(state=NORMAL)
        self.__puddle_plusten.configure(state=NORMAL)
        self.__puddle_plusone.configure(state=NORMAL)
        if max_puddles < 10000:
            self.__puddle_plustenthousand.configure(state=DISABLED)
        if max_puddles < 1000:
            self.__puddle_plusthousand.configure(state=DISABLED)
        if max_puddles < 100:
            self.__puddle_plushundred.configure(state=DISABLED)
        if max_puddles < 10:
            self.__puddle_plusten.configure(state=DISABLED)
        if max_puddles < 1:
            self.__puddle_plusone.configure(state=DISABLED)

        # Slimes

        max_small = self.__rm.small_slime.return_max(bm)
        max_big = self.__rm.big_slime.return_max(bm)
        max_behe = self.__rm.behemoth_slime.return_max(bm)
        max_micro = self.__rm.micro_slime.return_max(bm)

        # Small slime buttons

        self.__small_plusthousand.configure(state=NORMAL)
        self.__small_plushundred.configure(state=NORMAL)
        self.__small_plusten.configure(state=NORMAL)
        self.__small_plusone.configure(state=NORMAL)
        if max_small < 1000:
            self.__small_plusthousand.configure(state=DISABLED)
        if max_small < 100:
            self.__small_plushundred.configure(state=DISABLED)
        if max_small < 10:
            self.__small_plusten.configure(state=DISABLED)
        if max_small < 1:
            self.__small_plusone.configure(state=DISABLED)

        # Big slime buttons

        self.__big_plusthousand.configure(state=NORMAL)
        self.__big_plushundred.configure(state=NORMAL)
        self.__big_plusten.configure(state=NORMAL)
        self.__big_plusone.configure(state=NORMAL)
        if max_big < 1000:
            self.__big_plusthousand.configure(state=DISABLED)
        if max_big < 100:
            self.__big_plushundred.configure(state=DISABLED)
        if max_big < 10:
            self.__big_plusten.configure(state=DISABLED)
        if max_big < 1:
            self.__big_plusone.configure(state=DISABLED)

        # Behemoth slime buttons

        self.__behe_plusthousand.configure(state=NORMAL)
        self.__behe_plushundred.configure(state=NORMAL)
        self.__behe_plusten.configure(state=NORMAL)
        self.__behe_plusone.configure(state=NORMAL)
        if max_behe < 1000:
            self.__behe_plusthousand.configure(state=DISABLED)
        if max_behe < 100:
            self.__behe_plushundred.configure(state=DISABLED)
        if max_behe < 10:
            self.__behe_plusten.configure(state=DISABLED)
        if max_behe < 1:
            self.__behe_plusone.configure(state=DISABLED)

        # Micro slime buttons

        self.__micro_plusthousand.configure(state=NORMAL)
        self.__micro_plushundred.configure(state=NORMAL)
        self.__micro_plusten.configure(state=NORMAL)
        self.__micro_plusone.configure(state=NORMAL)
        if max_micro < 1000:
            self.__micro_plusthousand.configure(state=DISABLED)
        if max_micro < 100:
            self.__micro_plushundred.configure(state=DISABLED)
        if max_micro < 10:
            self.__micro_plusten.configure(state=DISABLED)
        if max_micro < 1:
            self.__micro_plusone.configure(state=DISABLED)

    def run_game(self):
        """
        The timer loop which runs the game and checks for victory condition.
        The order of events is also determined here. The timer is set to
        the messages label.
        :return:
        """
        self.__day += 1
        self.__rm.microbes_eat()
        self.__rm.slimes_eat()
        self.__rm.slimes_die()
        self.__rm.puddles_activate()
        self.update_labels()
        self.update_buttons()
        if self.__rm.total_mass_available() == 0:
            self.__game_won = True
            self.end_scene()
        if not self.__game_won:
            self.__messages.after(self.__turn_length, self.run_game)



