# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ----------------------------------------------------- SEHIR HADI -----------------------------------------------------


# ===================================================== Variables =====================================================
import time
import random

questions = [{'What color are Zebras?': {'White with black stripes': True, 'Black with white stripes': False,
                                         'Black with red stripes': False},
              'Where was the old Campus of Sehir University?': {'Levent': False, 'Altunizade': True,
                                                                'Maltepe': False}}]

users = {'5577': {'abbas': 5.4}, '5466': {'betul': 3.2}, '5551': {'omer': 6.4}, '5634': {'basil': 10.2}, '5573':
    {'ahmed': 1.2}, '5544': {'mohammad': 0}, '5897': {'Seeham': 5}, '5022': {'Yusuf': 14.2}, '5802': {'Yusuf': 1.5},
         '5989': {'Jade': 1.0}}
total_prize = 10000

robot_players = []  # <== Stores the non-human players

all_current_players = []  # <== Stores all the players including the human one

current_player = []  # <== Stores the human player's number

terminate = []  # <== Stores "None" to end the game

total_score = []  # <== Stores the scores

answer_dictionary = {}  # <== Stores the answers in order so that it can be displayed later in the same order

incorrect = []  # <== Stores "None" when the player gets an incorrect answer so that player will be eliminated

game_ended = []  # <== Stores "None" if the game has ended to break the loop

length_of_questions = [1, 1]  # <== keeps track of how many questions there are
# =============================================== Functions of the Menu ===============================================

while True:  # Allows the players later to start the game all over again
    def back_to_main_menu():  # <== returns the user back to the main menu
        print
        print 'Going back to main menu...\n'
        time.sleep(1)
        print


    def admin_menu_1():  # <== Prize changer
        print
        total_prize_changer = input('Please type the total prize of the next competition: ')
        print
        print 'Setting Total Prize to ' + str(total_prize_changer) + '...'
        time.sleep(1.5)
        print
        print ' Done!'
        return total_prize_changer


    def admin_menu_2(ques, num_for_q, num_for_a):  # <== Displays Questions
        for diction in ques:
            for question in diction:
                num_for_q += 1
                print
                print '----- Q ' + str(num_for_q) + ': ' + question + ' -----'
                for answers in diction[question]:
                    num_for_a += 1
                    print 'Q' + str(num_for_a) + '. ' + answers + ' > ' + str(diction[question][answers])
                num_for_a = 0
                print


    def admin_menu_3(ques):  # <== Adds Questions
        print
        print "Please Provide the New Question and it's Choices"
        print
        length_of_questions.append(1)
        new_question = raw_input('- New Question: ')
        print
        correct_answer = raw_input("- Correct Answer: ")
        print
        incorrect_answer_1 = raw_input("- INCORRECT Answer : ")
        print
        incorrect_answer_2 = raw_input("- INCORRECT Answer : ")
        print
        answers_dictionary = {correct_answer: True, incorrect_answer_1: False, incorrect_answer_2: False}
        question_dictionary = {new_question: answers_dictionary}
        ques.append(question_dictionary)  # <== adds the new question to the questions' list
        print
        print 'Adding to the questions database.....'
        time.sleep(1)
        print
        print ' Done!'


    def admin_menu_4_part_1(ques, num):  # <== Deletes questions
        questions_to_be_deleted = {}
        for diction in ques:
            for key in diction:
                num += 1
                questions_to_be_deleted[key] = num
        return questions_to_be_deleted


    def admin_menu_4_part_2():
        choices = admin_menu_4_part_1(questions, 0)
        print
        for diction in questions:
            for q in diction:
                print str(choices[q]) + '. ' + q
        print
        delete_q = input('Choose a question to delete: ')
        for question in choices:
            if delete_q == choices[question]:
                deleted_question = question
                for dictionary in questions:
                    if deleted_question in dictionary:
                        dictionary.pop(deleted_question)
        print
        print 'Deleting Question ' + str(delete_q) + '...'
        time.sleep(1)
        length_of_questions.pop()
        print
        print ' DONE!'


    def admin_menu_5(dictionary):  # <== Displays users' data
        for user_num in dictionary:
            for user_name in dictionary[user_num]:
                user_balance = dictionary[user_num][user_name]
                print
                print user_name + ', ' + 'Balance: ' + str(user_balance) + ', Phone Number: ' + "'" + user_num + "'"


    def admin_section():
        global total_prize
        while True:
            print
            print 'Welcome to Sehir Hadi Admin Section, please choose one of the following options:'
            print
            print '1 - Set prize for the next competition.'
            print '2 - Display questions for the next competition.'
            print '3 - Add new question to the next competition.'
            print '4 - Delete a question from the next competition.'
            print "5 - Display users' data."
            print '6 - Log out.'
            menu_entry = input('Select a number: ')
            while menu_entry > 6:  # <== Makes sure that user only enters the given choices
                print
                print '== INVALID ENTRY =='
                print
                menu_entry = input('Select a number: ')
            if menu_entry == 1:
                total_prize = admin_menu_1()  # <== New prize
                back_to_main_menu()
            elif menu_entry == 2:
                admin_menu_2(questions, 0, 0)
                print
                raw_input('PRESS ENTER TO GO BACK TO THE MAIN MENU')  # <== Gives the user time to check the information
                back_to_main_menu()
            elif menu_entry == 3:
                admin_menu_3(questions)
                print
                back_to_main_menu()
            elif menu_entry == 4:
                admin_menu_4_part_2()
                print
                back_to_main_menu()
            elif menu_entry == 5:
                admin_menu_5(users)
                print
                raw_input('PRESS ENTER TO GO BACK TO THE MAIN MENU')  # <== Gives the user time to check the information
                back_to_main_menu()
            elif menu_entry == 6:  # <== Takes the user back to the login page
                print
                sign_in()
                break


    def welcome_user_name(user_number):  # <== User's login page
        if user_number in users:
            for user_name in users[user_number]:
                print
                print '=' * 20
                print '   Welcome ' + user_name + '!'
                print '=' * 20
                print
                print 'Competition will start soon.. get ready :)'
                print
                for seconds in range(5, 0, -1):  # <== Countdown
                    print seconds
                    time.sleep(0.65)
                print
                print 'GAME STARTING...'
                print
                time.sleep(1)
                print


    # ++++++++++++++++++++++++++++++++++++++++++++++++++ Game Starts Here ++++++++++++++++++++++++++++++++++++++++++++++
    def start_of_the_game(num_for_q, num_for_a):  # <== Handles the game's mechanics
        answers_ordered = []
        robot_answers = {}
        answered_questions = 0
        for user in users:  # <== Adds all the users in the currently playing players list
            all_current_players.append(user)
        for diction in questions:
            for question in diction:
                answered_questions += 1  # <== Counts how many questions have been answered
                players_answer = None
                q1_score = 0
                q2_score = 0  # <== Each question's score
                q3_score = 0
                num_for_q += 1  # <== number of question counter
                print '******************** Total Players: ' + str(len(all_current_players))
                print
                print '----- Q ' + str(num_for_q) + ': ' + question + ' -----'
                for answers in diction[question]:
                    num_for_a += 1
                    answer_dictionary[num_for_a] = answers
                    answer_list = ' Ans ' + str(num_for_a) + '. ' + answers
                    answers_ordered.append(answer_list)
                    print answer_list
                print
                num_for_a = 0
                if None not in incorrect:  # <== Checks if the user's previous answer if it was incorrect
                    players_answer = input("Your Answer: ")
                    if players_answer == 1:
                        q1_score += 1
                    elif players_answer == 2:
                        q2_score += 1
                    elif players_answer == 3:
                        q3_score += 1
                for robot in robot_players:  # <== Gives each non-human player an answers
                    robot_answers[robot] = random.randint(1, 3)
                for robot_score in robot_answers:
                    if robot_answers[robot_score] == 1:
                        q1_score += 1
                    elif robot_answers[robot_score] == 2:
                        q2_score += 1
                    elif robot_answers[robot_score] == 3:
                        q3_score += 1
                total_score.extend((str(q1_score), str(q2_score), str(q3_score)))  # <== Adds the total scores
                for robot in robot_answers:  # <== Checks if the non-human players' answers
                    if robot_answers[robot] in answer_dictionary and robot in all_current_players and \
                            answer_dictionary[robot_answers[robot]] in diction[question] and \
                            diction[question][answer_dictionary[robot_answers[robot]]] == False:
                        all_current_players.remove(robot)
                        robot_players.remove(robot)
                if players_answer in answer_dictionary and answer_dictionary[players_answer] in diction[question] and \
                        diction[question][answer_dictionary[players_answer]] == True:
                    print  # ^ Checks if the player's answer is correct
                    print 'Correct'
                    print
                    print 'Evaluating the responses of the other competitors....'
                    print
                    time.sleep(0.5)
                    for an_or, score, tru_fal in zip(answers_ordered, total_score, diction[question].values()):
                        print an_or, str(tru_fal) + '... Total answers:' + str(score)
                        answers_ordered = []
                if players_answer in answer_dictionary and answer_dictionary[players_answer] in diction[question] and \
                        diction[question][answer_dictionary[players_answer]] == False:
                    # ^ Checks if the player's answer is incorrect
                    for player in current_player:  # removes the player from the current playing players list
                        if player in all_current_players:
                            all_current_players.remove(player)
                    incorrect.append(None)
                    print
                    print 'Incorrect!'
                    print
                    print 'Evaluating the responses of the other competitors....'
                    print
                    time.sleep(0.5)
                    for an_or, score, tru_fal in zip(answers_ordered, total_score, diction[question].values()):
                        print an_or, str(tru_fal) + '... Total answers:' + str(score)
                        answers_ordered = []
                    print
                elif None in incorrect:
                    print
                    print 'Evaluating the responses of the other competitors....'
                    print
                    time.sleep(2.0)
                    for an_or, score, tru_fal in zip(answers_ordered, total_score, diction[question].values()):
                        print an_or, str(tru_fal) + '... Total answers:' + str(score)
                        answers_ordered = []
                robot_answers.clear()
                del total_score[:]
                if len(all_current_players) == 1:  # Announces the player's win
                    game_ended.append(None)
                    print
                    print '--- TOTAL WINNERS: 1'
                    print '--- TOTAL DISTRIBUTED PRIZE: ' + str(float(total_prize))
                    for winner in all_current_players:
                        if winner in users:
                            for user_name in users[winner]:
                                users[winner][user_name] += total_prize
                                balance = str(float(users[winner][user_name]))
                                print user_name + ' ----> ' + str(float(total_prize)) + ' - Current Balance: ' + balance
                    break
                elif len(length_of_questions) == answered_questions:  # Announces the players' win
                    game_ended.append(None)  # Adds a "None" to a list to break the loop
                    print
                    print '--- TOTAL WINNERS: ' + str(len(all_current_players))
                    print '--- TOTAL DISTRIBUTED PRIZE: ' + str(float(total_prize))
                    for player in all_current_players:
                        for user in users:
                            if user == player:
                                for winner in users[user]:
                                    users[user][winner] += (total_prize / len(all_current_players))
                                    balance = str(float(users[user][winner]))
                                    print winner + ' ----> ' + str(float(total_prize / len(all_current_players))) + \
                                        ' - Current Balance: ' + balance
                    break
            if None in game_ended:  # <== Ends the game by breaking the loop
                break


    def sign_in():
        print
        print('----- Welcome to Sehir Hadi :D -----\n')
        print
        phone_num_login = raw_input('Please type your Phone Number to sign in: ')
        if len(phone_num_login) == 4:  # <== Makes sure that only valid numbers get added to the list
            for players in users:
                if phone_num_login not in players and players not in robot_players:
                    robot_players.append(players)
            if phone_num_login in users:
                current_player.append(phone_num_login)
        if phone_num_login != '**':
            print 'Checking ' + phone_num_login + '...'
            time.sleep(0.7)
            while phone_num_login not in users:  # <== Keeps asking the user to add a valid login number
                print
                print phone_num_login + ' is not a valid phone number, please try again!'
                print
                phone_num_login = raw_input('Please type your Phone Number to sign in: ')
                if phone_num_login in users:
                    current_player.append(phone_num_login)
                if phone_num_login == '**':
                    admin_section()
                print 'Checking ' + phone_num_login + '...'
                time.sleep(0.7)
                welcome_user_name(phone_num_login)
                if phone_num_login in users:   # <== Breaks the loop
                    start_of_the_game(0, 0)
                    terminate.append(None)
                    break
        elif phone_num_login == '**':
            admin_section()
            terminate.append(None)
        if None not in terminate:
            welcome_user_name(phone_num_login)
            start_of_the_game(0, 0)


    sign_in()
    print
    print
    print 'See you later :)'
    print
    time.sleep(2.0)
