"""
COMP.CS.100
Tekijä: Pekka Heljakka
Opiskelijanumero: 150157515
"""
import slime


class ResourceManager:
    """
    Resource manager class controls and stores information on various resources
    in the game. It creates the slime objects and also has some methods which
    deal with resource consumption and conversion, like microbes eating etc.
    """

    def __init__(self, difficulty):

        # various biomass found in the world as kilograms of carbon.
        STARTING_PLANT_MASS = 450000000000000
        STARTING_ANIMAL_MASS = 2000000000000
        STARTING_HUMAN_MASS = 6000000000
        STARTING_MICROBE_MASS = 70000000000000

        #  Difficulty levels: "normal", "cheat. These affect
        #  starting resources and collection rates

        #  set initial values for resources in world
        self.plant_mass = STARTING_PLANT_MASS
        self.animal_mass = STARTING_ANIMAL_MASS
        self.human_mass = STARTING_HUMAN_MASS
        self.microbe_mass = STARTING_MICROBE_MASS

        # Give the player a small amount of biomass to begin with, biomass
        # is the primary resource
        self.biomass = 20
        if difficulty == "cheat":
            self.biomass = 1000000000

        # Slimes die at a certain rate and dead slime is converted to microbial
        # life at the rate below.
        self.dead_slime = 0
        self.__dead_slime_to_microbes = 0.2

        #  create slimes, modify stats based on difficulty

        self.__small_slime_death_rate = 0.1
        self.__small_slime_eat_rate = 50
        self.__small_slime_mass = 10

        self.__big_slime_death_rate = 0.05
        self.__big_slime_eat_rate = 10
        self.__big_slime_mass = 100

        self.__behemoth_slime_death_rate = 0.7
        self.__behemoth_slime_eat_rate = 100
        self.__behemoth_slime_mass = 3000

        self.__micro_slime_death_rate = 0.8
        self.__micro_slime_eat_rate = 2
        self.__micro_slime_mass = 1

        if difficulty == "cheat":
            self.__small_slime_death_rate = 0
            self.__small_slime_eat_rate = 5000
            self.__big_slime_death_rate = 0
            self.__big_slime_eat_rate = 5000
            self.__behemoth_slime_death_rate = 0
            self.__behemoth_slime_eat_rate = 500
            self.__micro_slime_death_rate = 0
            self.__micro_slime_eat_rate = 5000

        self.small_slime = slime.Slime("small",
                                       self.__small_slime_death_rate,
                                       self.__small_slime_eat_rate,
                                       self.__small_slime_mass)

        self.big_slime = slime.Slime("big",
                                     self.__big_slime_death_rate,
                                     self.__big_slime_eat_rate,
                                     self.__big_slime_mass)

        self.behemoth_slime = slime.Slime("behemoth",
                                          self.__behemoth_slime_death_rate,
                                          self.__behemoth_slime_eat_rate,
                                          self.__behemoth_slime_mass)

        self.micro_slime = slime.Slime("micro",
                                       self.__micro_slime_death_rate,
                                       self.__micro_slime_eat_rate,
                                       self.__micro_slime_mass)

        # Set the production values for puddles, adjust based on difficulty

        self.puddles = 0
        self.puddle_cost = 10000

        self.__puddle_prod_small = 10000
        self.__puddle_prod_big = 100
        self.__puddle_prod_behe = 10
        self.__puddle_prod_micro = 100000

        self.prod_rate_small = 0.5
        self.prod_rate_big = 0.5
        self.prod_rate_behe = 0.5
        self.prod_rate_micro = 0.5

    def slimes_eat(self):
        """
        Each slime type eats the specified type of life and returns it as
        usable biomass. This function is called once during a turn.
        :return:
        """
        small_slimes_eat = self.small_slime.eat(self.plant_mass)
        self.plant_mass -= small_slimes_eat
        self.biomass += small_slimes_eat
        big_slimes_eat = self.big_slime.eat(self.animal_mass)
        self.animal_mass -= big_slimes_eat
        self.biomass += big_slimes_eat
        behe_slimes_eat = self.behemoth_slime.eat(self.human_mass)
        self.human_mass -= behe_slimes_eat
        self.biomass += behe_slimes_eat
        micro_slimes_eat = self.micro_slime.eat(self.microbe_mass)
        self.microbe_mass -= micro_slimes_eat
        self.biomass += micro_slimes_eat

    def slimes_die(self):
        """
        All slimes die at the set rate and return as dead slime.
        :return:
        """
        self.dead_slime += self.small_slime.die()
        self.dead_slime += self.big_slime.die()
        self.dead_slime += self.behemoth_slime.die()
        self.dead_slime += self.micro_slime.die()

    def microbes_eat(self):
        """
        Dead slime mass gets converted to microbial life. Values converted
        to integers.
        :return:
        """
        microbes_eat = int(self.dead_slime * self.__dead_slime_to_microbes)
        if microbes_eat < 0:
            microbes_eat = 1
        self.microbe_mass += microbes_eat
        self.dead_slime -= microbes_eat

    def max_puddles(self):
        """
        Returns value of how many puddles can be built at maximum with the
        current resources.
        :return:
        """
        max_count = self.biomass // self.puddle_cost
        return max_count

    def build_puddles(self, count):
        """
        Builds as many puddles as indicated.
        :param count: int, how many puddles to build
        :return:
        """
        biomass_used = count * self.puddle_cost
        self.biomass -= biomass_used
        self.puddles += count

    def puddle_slime_build(self, slime_obj, target_count):
        """
        Called by puddles activating, this function is used by puddles to
        build more slimes. Puddles will try to build a set number of slimes of
        certain type, this function will build them if possible or max amount
        that can be built. Function will be called for every slime type
        separately and needs a reference to existing slime object.
        :param slime_obj: Slime object, referenc to a slime that will be built
        :param target_count: int, how many slimes a puddle is trying to build
        :return:
        """
        # Check how many slimes can be built
        max_slime_count = slime_obj.return_max(self.biomass)
        #  If enough resources to build all the slimes requested, do so
        if max_slime_count >= target_count:
            slime_obj.add_slimes(target_count)
            self.biomass -= slime_obj.get_cost() * target_count
        # If not enough resources, build as many as possible
        else:
            slime_obj.add_slimes(max_slime_count)
            self.biomass -= slime_obj.get_cost() * max_slime_count

    def puddles_activate(self):
        """
        When puddles activate, they try to build as many slimes as the set
        production rates allow. Priority is hard coded by the order in which
        the build function is called for each slime. The target is number
        of puddles * production rate for spesific slime * production rate
        which comes from the UI slider.
        :return:
        """
        small_slime_target = self.__puddle_prod_small \
                             * self.puddles \
                             * self.prod_rate_small
        small_slime_target = int(small_slime_target)
        self.puddle_slime_build(self.small_slime, small_slime_target)

        big_slime_target = self.__puddle_prod_big \
                            * self.puddles \
                            * self.prod_rate_big
        big_slime_target = int(big_slime_target)
        self.puddle_slime_build(self.big_slime, big_slime_target)

        behe_slime_target = self.__puddle_prod_behe \
                             * self.puddles \
                             * self.prod_rate_behe
        behe_slime_target = int(behe_slime_target)
        self.puddle_slime_build(self.behemoth_slime, behe_slime_target)

        micro_slime_target = self.__puddle_prod_micro \
                             * self.puddles \
                             * self.prod_rate_micro
        micro_slime_target = int(micro_slime_target)
        self.puddle_slime_build(self.micro_slime, micro_slime_target)

    def total_mass_available(self):
        """
        Returns combined biomass left in the world.
        """
        return self.plant_mass + self.animal_mass + \
               self.human_mass + self.microbe_mass
