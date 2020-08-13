"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Authors: Chelsie Beavers cdb95 and Babafemi Badero bkb55
Date: December 12, 2019
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """

    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    #pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    #def getShip(self)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, source):
        """
        Initializes the attributes.
        """
        super().__init__(x=x,y=y, width=SHIP_WIDTH, height=SHIP_WIDTH,source=source)

    def _collidesShip(self,bolt):
        """
        This method returns True if the alien bolt collides with this ship

        This method returns False if bolt was not fired by the alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        # """

        left = bolt.x - BOLT_WIDTH
        right= bolt.x + BOLT_WIDTH
        bottom= bolt.y - BOLT_HEIGHT
        top= bolt.y + BOLT_HEIGHT

        if bolt.isPlayerBolt() == False:# positive bool
            if (self.contains((left,bottom)) or self.contains((left,top)) or self.contains((right,bottom)) or self.contains((right,top))):
                return True
            else:
                return False



    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """



    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBolts(self):
        return self._bolts
    def getAlien(self):
        return self._aliens

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source):
        """
        Initializes the attributes.
        """
        super().__init__(x=x, y=y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, source=source)
        #self._bolts = bolt


    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def _collidesAlien(self,bolt):
        """
        This method returns True if the player bolt collides with this alien.

        This method returns False if bolt was not fired by the player.


        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        # """
        left = bolt.x - BOLT_WIDTH
        right= bolt.x + BOLT_WIDTH
        bottom= bolt.y - BOLT_HEIGHT
        top= bolt.y + BOLT_HEIGHT

        if (self.contains((left,bottom)) or self.contains((left,top)) or self.contains((right,bottom)) or self.contains((right,top))):
            return True
        else:
            return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float
    #Attribute _speed: speed of the bolt
    #Invariant: _speed must be == BOLT_SPEED or -BOLT_SPPED


    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShipDirection(self):
        return self._shipdirection
    def getVelocity(self):
        return self._velocity
    def getShip(self):
        return self._ship

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y, shipdirection):
        #removed direction AND VELOCITY attribute
        """
        Initializes the attributes.

        Attribute shipbool:returns True if object is a ship object; False otherwise
        Invariant: must be a boolean value
        """
        self._shipdirection = shipdirection
        self._speed = BOLT_SPEED
        #self._speed = self.isPlayerBolt(direction)
        #self._velocity = velocity
        self._velocity = self._shipdirection * self._speed


        #super().__init__(x=x, y=y, width=BOLT_WIDTH, height=BOLT_HEIGHT, fillcolor='red', linecolor = 'blue',velocity=velocity, direction=direction)
        super().__init__(x=x, y=y, width=BOLT_WIDTH, height=BOLT_HEIGHT, fillcolor='red', linecolor='red',shipdirection=shipdirection, velocity=self._velocity)


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        This method determines the direction of the bolt, based who fires the bolt.
        If shipbolt is moving up the screen, it is a postive number, True, and a
        player bolt. If it is moving down the screen, it is a negative number,
        False, and an alien bolt.

        Attribute shipdirection: pos if bolt is fired by player, neg otherwise
        Invariant: must be an int greater than 0 or less than 0
        """
        # Paramter direction: tells if the bolts will travel up or down the screen.
        # Precontion: direction must be an int.

        return self._shipdirection > 0



        # if self._shipdirection == True:
        #     self._velocity = BOLT_SPEED
        # else:
        #     self._velocity = -BOLT_SPEED

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class DefLine(GPath):
    """
    A class representing a defense line
    """
    def __init__(self):
        super().__init__(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],linewidth=2, linecolor='black')

# class CollisionBool(GObject):
#     """
#     A class representing a boolean that determines if a collision has occurred
#     """
#     def __init__(self, x, y):
#         super().__init__(x=x, y=y)
