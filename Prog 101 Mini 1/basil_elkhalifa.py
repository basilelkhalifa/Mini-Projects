# +++++++++++++++++++++++++++++++ SEHIR Turtle Cup ++++++++++++++++++++++++++++++

# Empty prints are spaces between codes vertically

# ===== IMPORTS ======
from swampy.TurtleWorld import *
from swampy.TurtleWorld import Turtle

world = TurtleWorld()
import time
import random
import math
print
print '$$$$$$$$$$$$ :D SEHIR TURTLE CUP :D $$$$$$$$$$$$'
print

while True:
    # =============== Player_1_Name ================

    def player_1():
        print '----- First Turtle -----'
        global player_1_name
        player_1_name = raw_input('Please name your Turtle: ')

    player_1()

    while player_1_name == '' :
        print
        print 'You Cannot Leave This Field Empty'
        print
        player_1()

    turtle_1 = Turtle()  # Turtle_1_Player_1

    # =============== Player_1_Color ===============

    def turtle_1_color():
        global player_1_color
        player_1_color = raw_input('Please select a color for you Turtle (red,blue,yellow)')

    turtle_1_color()

    while player_1_color == 'red' or 'yellow' or 'blue':
        if player_1_color == 'red':
            turtle_1.set_color('red')
            break
        elif player_1_color == 'blue':
            turtle_1.set_color('blue')
            break
        elif player_1_color == 'yellow':
            turtle_1.set_color('yellow')
            break
        else:
            print
            print 'Invalid Color, Please select a color from the given colors (red,blue,yellow)'
            print
            turtle_1_color()

    # =============== Player_1_Starting_Position ================

    def turtle_1_position(y):
        turtle_1.delay = 0.01
        for i in range(1):
            turtle_1.pu()
            bk(turtle_1, y)
            turtle_1.pd()

    turtle_1_position(140)

    def player_1_ready():
        print
        print ' ---------- ' + player_1_name + ' IS READY TO GO :) ' + '----------'
        print

    player_1_ready()

    # =============== Player_2_Name ===============

    def player_2():
        print '----- Second Turtle -----'
        global player_2_name
        player_2_name = raw_input('Please name your Turtle: ')

    player_2()

    while player_2_name == '':
        print
        print 'You Cannot Leave This Field Empty'
        print
        player_2()

    while player_2_name == player_1_name:
        print
        print "You Cannot Choose The Same Name As Player One's"
        print
        player_2()

    turtle_2 = Turtle()  # Turtle_2_Player_2

    # =============== Player_2_Color ===============

    def turtle_2_color():
        global player_2_color
        player_2_color = raw_input('Please select a color for you Turtle (red,blue,yellow)')

    turtle_2_color()

    while player_2_color == player_1_color:
        print
        print "You cannot pick the same color as player one's"
        print
        turtle_2_color()

    while player_2_color == 'red' or 'yellow' or 'blue':
        if player_2_color == 'red':
            turtle_2.set_color('red')
            break
        elif player_2_color == 'blue':
            turtle_2.set_color('blue')
            break
        elif player_2_color == 'yellow':
            turtle_2.set_color('yellow')
            break
        else:
            print
            print 'Invalid Color, Please select a color from the given colors (red,blue,yellow)'
            print
            turtle_2_color()

    # =============== Player_2_Starting_Position ================

    def turtle_2_position(y):
        turtle_2.delay = 0.1
        for i in range(1):
            turtle_2.pu()
            bk(turtle_2, y)
            rt(turtle_2, 90)
            fd(turtle_2, y)
            lt(turtle_2, 90)
            turtle_2.pd()

    turtle_2_position(140)

    def player_2_ready():
        print
        print ' ---------- ' + player_2_name + ' IS READY TO GO :) ' + '----------'
        print

    player_2_ready()

    # +++++++++++++++++++++++++ GAME_STARTS_HERE ++++++++++++++++++++++++++

    # ========================= TOSS ===============================

    def ready():
        print "PRESS ENTER TO START THE TOSS"
        raw_input()
        print

    ready()

    def toss():
        print 'TOSS IN PROGRESS'
        time.sleep(1.5)
        print
        print "GAME BEGINS IN:"
        for i in range(5, 0, -1):
            print i
            time.sleep(0.65)
        print
        global toss_start
        toss_start = random.randint(0, 1)

    toss()

    # ========================== Variables & Functions =========================

    # Variables:
    round_start = 0
    p1_score = 0
    p2_score = 0

    # Functions:
    # ------------TYPES_OF_STEPS------------

    # Straight Line Function
    def straight_line(turtle_name, distance):
        fd(turtle_name, distance)

    # Stairs Function
    def stairs(turtle_name, distance):
        distance = distance / 5
        for i in range(2):
            fd(turtle_name, distance)
            lt(turtle_name, 90)
            fd(turtle_name, distance)
            rt(turtle_name, 90)
        for i in range(2):
            fd(turtle_name, distance)
            rt(turtle_name, 90)
            fd(turtle_name, distance)
            lt(turtle_name, 90)
        fd(turtle_name, distance)

    def polyline(turtle_name, n, length, angle):
        for i in range(n):
            fd(turtle_name, length)
            rt(turtle_name, angle)

    # Semi Circle Function
    def semi_circle(turtle_name, r, angle):
        lt(turtle_name, 90)
        semi_c_length = 2 * math.pi * r / 2 * abs(angle) / 360
        n = int(semi_c_length / 4) + 1
        step = semi_c_length / n
        step_angle = float(angle) / n
        rt(turtle_name, step_angle / 2)
        polyline(turtle_name, n, step, step_angle)
        lt(turtle_name, step_angle / 2)
        lt(turtle_name, 180)
        turtle_name.heading = 360
        turtle_name.redraw()

    # -----------------------------------------

    def rounds():
        global round_start
        round_start += 1
        return round_start

    def winner():
        if p1_score >= 200:
            print'+++++++++++++++'
            print player_1_name + ' HAS WON!'
            print'+++++++++++++++'
        elif p2_score >= 200:
            print'+++++++++++++++'
            print player_2_name + ' HAS WON!'
            print'+++++++++++++++'

    def round_player_1():
        print "**********Round " + str(rounds()) + " **********"
        print '- ' + player_1_name + "'s" + ' score:' + str(p1_score)
        print '- ' + player_2_name + "'s" + ' score:' + str(p2_score)
        print
        global first_player_steps
        print player_1_name + "'s" + " Turn"
        print "****************************"
        first_player_steps = int(raw_input("How many steps would you like to take?: "))
        print

    def round_player_2():
        print "**********Round " + str(rounds()) + " **********"
        print '- ' + player_1_name + "'s" + ' score:' + str(p1_score)
        print '- ' + player_2_name + "'s" + ' score:' + str(p2_score)
        print
        global second_player_steps
        print player_2_name + "'s" + ' Turn'
        print "****************************"
        second_player_steps = int(raw_input("How many steps would you like to take?: "))
        print

    def player_1_high_number():  # ==> if_player_1_chooses_a_number_more_than_99
        while first_player_steps > 99:
            print
            print 'Please choose a number between (1-99)'
            print
            global round_start
            round_start = round_start - 1
            round_player_1()

    def player_2_high_number():  # ==> if_player_2_chooses_a_number_more_than_99
        while second_player_steps > 99:
            print
            print 'Please choose a number between (1-99)'
            print
            global round_start
            round_start = round_start - 1
            round_player_2()

    def player_1_luck():
        if lucky_number_1 >= random_number_1:
            steps_choice_1 = random.randint(0, 2)  # ==> the_probability_of_getting_a_different_type_of_step_for_p1
            if steps_choice_1 == 0:
                stairs(turtle_1, first_player_steps)
            elif steps_choice_1 == 1:
                semi_circle(turtle_1, first_player_steps, 180)
            elif steps_choice_1 == 2:
                straight_line(turtle_1, first_player_steps)
            print
            print "YOU SUCCEEDED :D"
            print
            global p1_score
            p1_score += first_player_steps
        elif lucky_number_1 < random_number_1:
            print
            print "YOU FAILED :("
            print

    def player_2_luck():
        if lucky_number_2 >= random_number_2:
            steps_choice_2 = random.randint(0, 2)  # ==> the_probability_of_getting_a_different_type_of_step_for_p2
            if steps_choice_2 == 0:
                stairs(turtle_2, second_player_steps)
            elif steps_choice_2 == 1:
                semi_circle(turtle_2, second_player_steps, 180)
            elif steps_choice_2 == 2:
                straight_line(turtle_2, second_player_steps)
            print
            print "YOU SUCCEEDED :D"
            print
            global p2_score
            p2_score += second_player_steps
        elif lucky_number_2 < random_number_2:
            print
            print "YOU FAILED :("
            print

    def player_1_game():
        round_player_1()

        player_1_high_number()
        global random_number_1
        random_number_1 = random.randint(1, 99)
        # Variables ===================================
        global lucky_number_1
        lucky_number_1 = (100 - first_player_steps)  # ------> possibility for player 1
        # =============================================
        player_1_luck()

        winner()


    def player_2_game():
        round_player_2()

        player_2_high_number()
        global random_number_2
        random_number_2 = random.randint(1, 99)
        # Variables ===================================
        global lucky_number_2
        lucky_number_2 = (100 - second_player_steps)  # ------> possibility for player 1
        # =============================================
        player_2_luck()

        winner()
    # ===================================================================

    # ---------------- PLAYER_ONE_FIRST ------------------

    while toss_start == 0:  # ==> Player_1_Goes_First_Here

        player_1_game()
        if 200 <= p1_score:     # ==> when the player 1 reaches 200 steps the game ends
            break
        elif 200 <= p2_score:   # ==> when the player 2 reaches 200 steps the game ends
            break

        player_2_game()
        if 200 <= p1_score:
            break
        elif 200 <= p2_score:
            break
    # ----------------------------------------------------

    # ---------------- PLAYER_TWO_FIRST ------------------

    while toss_start == 1:  # ==> Player_2_Goes_First_Here

        player_2_game()
        if 200 <= p1_score:
            break
        elif 200 <= p2_score:
            break

        player_1_game()
        if 200 <= p1_score:
            break
        elif 200 <= p2_score:
            break

    # -----------------------END_OF_GAME--------------------------
    for i in range(5):
        print
    end_of_game = raw_input('Would you like to restart the game?: ')
    if end_of_game == 'yes':
        for i in range(15):
            print
        word = TurtleWorld()
        continue
    else:
        print
        print "THANK YOU FOR PLAYING SEHIR TURTLE CUP :D"
        exit()
# ++++++++++++++++++++++++++++ GAME_ENDS ++++++++++++++++++++++++++++++++
