"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Authors: Chelsie Beavers cdb95 and Babafemi Badero bkb55
Date: December 12, 2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # self._right_starter = False #must be a boolean
    # self._left_starter = False #must be a boolean

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        return self._lives

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the attributes.
        """
        self._aliens = []
        self.orderAliens()
        self._ship = Ship(x=(GAME_WIDTH//2),y=SHIP_BOTTOM,source='ship.png')
        self._defLine = DefLine()
        self._time = 0
        self._bolts = []
        self._trans_sig = False #must be an int
        self._rightPosAlien = self._aliens[-1]
        self._leftPosAlien = self._aliens[0]
        self._fire = random.randint(1,BOLT_RATE)
        self._steps = 0
        self._lives = 3
        self._boom = Sound('blast1.wav')
        self._pew = Sound('pew1.wav')

    def orderAliens(self):
        """
        This method creates the aliens and adds them to the list, self._aliens.
        THis methods also properly spacs the aliens and correctly arranges
        them in their respective positions.
        """

        left_edge = ALIEN_H_SEP
        top_edge = GAME_HEIGHT - ALIEN_CEILING
        height_alien = (ALIEN_HEIGHT*ALIEN_ROWS)+(ALIEN_V_SEP * ALIEN_ROWS-1)
        bottom_edge = (top_edge - height_alien) + (ALIEN_V_SEP)
        y_pos = GAME_HEIGHT - ALIEN_CEILING - (ALIEN_HEIGHT//2)

        for row in range(ALIEN_ROWS):#range(1):
            twodimen_list = []
            if row%5 == 1 or row%5 == 2:
                source = ALIEN_IMAGES[0]
            elif row%5 == 3 or row%5 == 4:
                source = ALIEN_IMAGES[1]
            else:
                source = ALIEN_IMAGES[2]
            x_pos = ALIEN_H_SEP + (ALIEN_WIDTH//2)
            for col in range(ALIENS_IN_ROW):#range(1):
                twodimen_list.append(Alien(x_pos, y_pos,source))
                x_pos += ALIEN_H_SEP + ALIEN_WIDTH
            self._aliens.append(twodimen_list)
            y_pos -= ALIEN_HEIGHT + ALIEN_V_SEP


    def countSteps(self):
        """
        Counts the number of steps that the aliens move.
        """
        self._steps +=1
        return self._steps


    def moveAliensLeft(self):
        """
        Move aliens to the left. This method also counts the number of steps
        that the lists of aliens take and also finds the x values of the alien
        at the outer most left position.
        """

        left_end = 0 + ALIEN_WIDTH//2 + ALIEN_H_SEP
        upcoming_pos = 0
        order_acc = []

        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                each_alien = self._aliens[row][col]
                if each_alien != None:
                    order_acc.append(each_alien.x)
                    each_alien.x = each_alien.x - ALIEN_H_WALK
                    upcoming_pos = each_alien.x - ALIEN_H_WALK
                    self.countSteps()
        order_acc.sort()
        outer_left_alien = int(order_acc[0])
        if outer_left_alien <= left_end:
            self._trans_sig = False

            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                    each_alien = self._aliens[row][col]
                    if each_alien != None:
                        each_alien.y = each_alien.y - ALIEN_V_SEP

    def moveAliensRight(self):
        """ Move aliens to the right. This method also counts the number of steps
        that the lists of aliens take and also finds the x values of the alien
        at the outer most right position.
        """

        right_end = GAME_WIDTH-ALIEN_WIDTH//2
        upcoming_pos = 0
        right_order_acc = []


        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                each_alien = self._aliens[row][col]
                if self._aliens[row][col] != None:
                    right_order_acc.append(each_alien.x)
                    if each_alien != None:
                        each_alien.x = each_alien.x + ALIEN_H_WALK
                        upcoming_pos = each_alien.x + ALIEN_H_WALK
                        self.countSteps()
        right_order_acc.sort()
        outer_left_alien = int(right_order_acc[-1])
        if upcoming_pos >= right_end:
            self._trans_sig = True
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                    each_alien = self._aliens[row][col]
                    if each_alien != None:
                        each_alien.y = each_alien.y - ALIEN_V_SEP


    def ship_bolt_object(self,input):
        """
        Creates the bolts fired by the ship and adds them to self._bolts.

        Parameter input: input from the user and returns True if is held down.
        Precondition: input is a string.
        """
        self._shipbolts = []
        for col in self._bolts:
            if col.isPlayerBolt():
                self._shipbolts.append('ship')
        if len(self._shipbolts) < 1:
            if input.is_key_down('up'):
                if self._ship != None:
                    bolt = Bolt(x=self._ship.x,y=(GAME_HEIGHT-(GAME_HEIGHT-self._ship.y)), shipdirection=1)
                    self._bolts.append(bolt)
                    self._boom.play()




    def moveBolts(self,input,dt):
        """
        This method checks if the bolt is fired by the player or if it is fired
        by the aliens. Returns True if fired by the player. Returns False if fired
        by the aliens. This method also, sets the direction for the bolts (up or down).
        This method also calls the methods that creates the objects.
        """
        self.ship_bolt_object(input)
        self.alien_bolt_object(dt)
        for col in self._bolts:
            col.y = col.y + col.getVelocity()


    def removeShipBolts(self):
        """
        This method removes the bolt from self._bolts if its height
        exceeds the height of the game screen.

        Parameter input: input from the user and returns True if is held down.
        Precondition: input is a string.
        """


        bolts_acc = []
        for i in range(len(self._bolts)):
            if self._bolts[i].y <= GAME_HEIGHT:
                bolts_acc.append(self._bolts[i])
        self._bolts = bolts_acc
        self._shipbolts = []


    def botRow(self, chosencol):
        """
        Checks if the row is empty (None). Returns the bottom most row that is
        not empty. If there is no bottm most non empty, return -1.
        """
        bestRow = -1
        for row in range(len(self._aliens)):
            if self._aliens[row][chosencol] != None:
                bestRow = row
        return bestRow


    def isColEmpty(self, chosencol):
        """
        Checks if the column is empty (None). If it is empty, return True. Else,
        return false.
        """
        return self.botRow(chosencol) == -1


    def alien_bolt_object(self,dt):
        """
        Creates the bolts fired by the aliens and adds them to self._bolts.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (int or float)

        """

        num  = len(self._aliens[0])-1
        while True:
            colnum = random.randint(0, num)
            if (self.isColEmpty(colnum)==False):
                break
        chosen_alien = self._aliens[self.botRow(colnum)][colnum]

        self._time += dt
        if self._time > ALIEN_SPEED:
            if self._steps>self._fire:
                for row in range(len(self._aliens)):
                    for col in range(len(self._aliens[row])):
                        each_alien = self._aliens[row][col]
                        if self._aliens[row][col]!= None and chosen_alien.x!= None and chosen_alien.y!=None:
                            abolt = Bolt(x=chosen_alien.x,y=chosen_alien.y, shipdirection=-1)
                            self._bolts.append(abolt)
                            self._pew.play()
                            self._fire = random.randint(1, BOLT_RATE)
                self._steps = 0
                self._time = 0



    def removeAlienBolts(self):
        """
        This method removes the bolt from self._bolts if its height
        exceeds the height of the game screen.
        """

        bolts_acc = []
        for i in range(len(self._bolts)):
            if self._bolts[i].y > (GAME_HEIGHT-GAME_HEIGHT):
                bolts_acc.append(self._bolts[i])
        self._bolts = bolts_acc


    def _collisionDetection(self):
        """
        This method sets the hit ship or alien to None in its list and removes
        the bolt from self._bolts.
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt(): # added to test
                for row in range(len(self._aliens)):
                    for col in range(len(self._aliens[row])):
                        each_alien = self._aliens[row][col]
                        if each_alien != None:
                            if each_alien._collidesAlien(bolt):
                                self._aliens[row][col] = None
                                if bolt in self._bolts:
                                    self._bolts.remove(bolt)
            if self._ship != None:
                if self._ship._collidesShip(bolt):
                    self._ship = None
                    self._lives-=1
                    if bolt in self._bolts:
                        self._bolts.remove(bolt)


        # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def shipUpdate(self,input):
        """
        Changes the position of the ship.

        Parameter input: input from the user and returns True if is held down.
        Precondition: input is a string.
        """

        da = self._ship.x
        if input.is_key_down('left'):
            da = max((da - SHIP_MOVEMENT),(GAME_WIDTH-(GAME_WIDTH -SHIP_WIDTH//2)))
        if input.is_key_down('right'):
            da = min((da + SHIP_MOVEMENT), (GAME_WIDTH-SHIP_WIDTH//2))
        self._ship.x = da



    def aliensUpdate(self,dt):
        """ Calculates the time since the last frame and determines when to
        move the aliens.

        Parameter dt: time since last animation frame.
        Precondition: dt is a number (int or float)
        """

        self._time += dt
        if self._time > ALIEN_SPEED:
            if self._trans_sig:
                self.moveAliensLeft()
            else:
                self.moveAliensRight()
            self._time = 0



    def update(self,input, dt):
        """
        Animates ship, aliens, and bolts.

        Parameter input: input from the user and returns True if is held down.
        Precondition: input is a string.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a number (int or float)
        """
        if self._ship != None:
            self.shipUpdate(input)
            self.aliensUpdate(dt)
        if self._bolts != None:
            self.moveBolts(input,dt)
        self._collisionDetection()
        self._invadedLine()



    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def drawTheAliens(self, view):
        """
        Draws the Aliens in their correction positions.
        """
        len_2dlist = len(self._aliens)
        for row in range(len_2dlist):
            for col in range(len(self._aliens[row])):
                each_alien = self._aliens[row][col]
                if each_alien != None:
                    each_alien.draw(view)

    def drawTheShip(self,view):
        """
        Draws the ship.
        """

        self._invadedLine()
        if self._ship != None:
            self._ship.draw(view)

    def drawTheDefLine(self,view):
        """
        Draws the defense line.
        """

        if self._defLine != None:
            self._defLine.draw(view)


    def drawMoveBolts(self,view):
        """
        Draws bolts fired by ship and aliens
        """
        for col in self._bolts:
            if self._bolts != None and self._bolts != []:
                self.removeAlienBolts()
                self.removeShipBolts()
                col.draw(view)


    def draw(self,view):
        """
        Calls the draw functions to draw the objects created in each function.

        Parameter view :the view (inherited from GameApp)
        Precondition: must be an instance of GView
        """
        self.drawTheAliens(view)
        self.drawTheShip(view)
        self.drawTheDefLine(view)
        self.drawMoveBolts(view)



    # HELPER METHODS FOR COLLISION DETECTION


    def _invadedLine(self):
        """
        This method checks to see if any of the aliens have crossed the defense line.
        If so, it causes the ship to lose the round.
        """
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                each_alien = self._aliens[row][col]
                if each_alien != None:
                    if (each_alien.y - ALIEN_HEIGHT//2) <= DEFENSE_LINE:
                        self._ship = None
                        self._lives=0
