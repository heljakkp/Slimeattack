"""
COMP.CS.100
Tekijä: Pekka Heljakka
Email: pekka.heljakka@tuni.fi
Opiskelijanumero: 150157515
"""

class Slime:
    """
    Slime class represents a slime type resource the player needs to manage.
    The class represents all of the slimes of a particular type. They can
    eat biomass, they cost the same amount of biomass to create as their
    own mass and they have a certain set rate at which they die. The class
    keeps track of how many of this slime type is available.
    """

    def __init__(self, name, death_rate, eating_rate, individual_mass):
        """
        :param name: string, name of the slime type
        :param death_rate: float, a percentage of the slimes that die each day
        :param eating_rate: int, each slime will consume this much in kg of
        biomass each day
        :param individual_mass: how much a slime weighs, also this many kg
        of biomass is needed to spawn one slime of this type
        """

        self.__name = name
        self.__count = 0
        self.__death_rate = death_rate
        self.__eating_rate = eating_rate
        self.__individual_mass = individual_mass

    def eat(self, food):
        """
        Slime will consume whatever food type is fed to it. The consumed amount
        is slime count * eating rate modifier. If not enough food is available
        to consume the max amount, slime will eat it all. Will return the
        amount of food that was consumed.
        :param food: int, whatever the manager class has set as the consumable
        :return: int, how much food was consumed by the slime.
        """
        max_food = self.__count * self.__eating_rate
        if food > max_food:
            return max_food
        else:
            return food

    def die(self):
        """
        Slimes will die at a rate depending on their death rate modifier.
        Calling this function will reduce the number of slimes by that amount
        and will return the the number of slimes died * their mass. Some
        slimes will always die, minimum is set to one except if the death
        rate is zero, when slimes don't die at all.
        :return: int, the mass of slimes that died
        """
        if self.__count == 0:
            return 0
        else:
            number_of_deaths = self.__count * self.__death_rate
            if self.__death_rate == 0:
                number_of_deaths = 0
            elif number_of_deaths < 1:
                number_of_deaths = 1
            number_of_deaths = int(number_of_deaths)
            dead_mass = number_of_deaths * self.__individual_mass
            self.__count -= number_of_deaths
        return dead_mass

    def add_slimes(self, count):
        """
        Adds to the slime count, simply increases the number and does not
        check if food is available etc.
        :param count: int, how many slimes to add
        :return:
        """
        self.__count += count

    def return_max(self, biomass):
        """
        Calculates what is the maximum amount of slimes that can be created with
        the amount of biomass given in parameter.
        :param biomass: int, total resources available
        :return: int, max number of slimes that can be built with the biomass
        """
        max_count = biomass // self.__individual_mass  # No fractions allowed
        return max_count

    def get_count(self):
        """
        Returns the slime count
        :return: int, how many slimes there are
        """
        return self.__count

    def get_mass(self):
        """
        Returns the total mass of this slime type (count * individual mass)
        :return: int, the total mass of this slime type
        """
        return self.__count * self.__individual_mass

    def get_cost(self):
        """
        How much one slime weighs, which is also the cost to build one
        :return: int, mass of one slime
        """
        return self.__individual_mass


