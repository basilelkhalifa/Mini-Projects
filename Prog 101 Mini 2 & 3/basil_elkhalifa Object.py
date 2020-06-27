import time
import random

while True:  # Repeats the game after the game ends
    class Users:  # constructs the user's information
        def __init__(self, name, balance, phone, is_disqualified=False):
            self.name = name
            self.balance = balance
            self.phone = phone
            self.is_disqualified = is_disqualified

        def print_user_stats(self):  # displays the users details when menu item 5 is selected
            print self.name + ', ' + 'Balance: ' + str(self.balance) + ', ' + 'Phone number: ' + self.phone


    class Answers:  # constructs the answers
        def __init__(self, text, answer_no, is_correct, num_answering_users=0):
            self.text = text
            self.answer_no = answer_no
            self.is_correct = is_correct
            self.num_answering_users = num_answering_users


    class Questions:  # constructs the questions
        def __init__(self, question_text, answers, correct_ans):
            self.question_text = question_text
            self.answers = answers
            self.correct_ans = correct_ans
            self.answers_list = []  # used to put the incorrect answers together
            self.users_answers = {}  # the list of robots answers
            self.answer_1 = Answers(self.answers[0], 1, False)  # answers' objects
            self.answer_2 = Answers(self.answers[1], 2, False)
            self.answer_3 = Answers(self.correct_ans, 3, True)

        def display(self, question_no, display_answers, display_correctness):
            if display_answers and display_correctness:  # displays the answers and correctness when menu item 2 is
                # chosen
                print '--- Q' + str(question_no) + ': ' + self.question_text + ' ---'
                print
                self.answers_list.extend([self.answer_1, self.answer_2, self.answer_3])
                print 'Ans' + str(self.answer_1.answer_no) + ': ' + self.answer_1.text + '>' + str(
                    self.answer_1.is_correct)
                print 'Ans' + str(self.answer_2.answer_no) + ': ' + self.answer_2.text + '>' + str(
                    self.answer_2.is_correct)
                print 'Ans' + str(self.answer_3.answer_no) + ': ' + self.answer_3.text + '>' + str(
                    self.answer_3.is_correct)
            if not display_correctness and not display_answers:  # displays the questions only
                print 'Q' + str(question_no) + '. ' + self.question_text
            if not display_answers and display_correctness:  # displays the correct answers after players make their
                # choices
                print
                self.answers_list.extend([self.answer_1, self.answer_2, self.answer_3])
                print 'Ans' + str(self.answer_1.answer_no) + ' ' + self.answer_1.text + '... ' \
                      + str(self.answer_1.num_answering_users)
                print 'Ans' + str(self.answer_2.answer_no) + ' ' + self.answer_2.text + '... ' \
                      + str(self.answer_2.num_answering_users)
                print 'Ans' + str(self.answer_3.answer_no) + ' ' + self.answer_3.text + '... ' \
                      + str(self.answer_3.num_answering_users)
                time.sleep(2.0)
            if display_answers and not display_correctness:  # displays the answers when player plays
                print '--- Q' + str(question_no) + ': ' + self.question_text + ' ---'
                print
                self.answers_list.extend([self.answer_1, self.answer_2, self.answer_3])
                print 'Ans' + str(self.answer_1.answer_no) + ': ' + self.answer_1.text
                print 'Ans' + str(self.answer_2.answer_no) + ': ' + self.answer_2.text
                print 'Ans' + str(self.answer_3.answer_no) + ': ' + self.answer_3.text

        def process_answers(self, dictionary_of_users, current_player):
            for user in dictionary_of_users:
                self.users_answers[user] = random.randint(1, 3)  # generates random answers for the non-human players
            for ai, ai_answer in self.users_answers.items():
                if ai_answer == 1:  # Checks what the robot's answer is and adds to the score for that specif question
                    self.answer_1.num_answering_users += 1
                elif ai_answer == 2:  # Checks what the robot's answer is and adds to the score for that specif question
                    self.answer_2.num_answering_users += 1
                elif ai_answer == 3:  # Checks what the robot's answer is and adds to the score for that specif question
                    self.answer_3.num_answering_users += 1
                if ai_answer == self.answers_list[(ai_answer - 1)].answer_no \
                        and not self.answers_list[(ai_answer - 1)].is_correct:
                    dictionary_of_users.pop(ai)  # ^ Checks if the robots' answers are correct and eliminates players
            if current_player == 1 and not None:  # Checks if the current player's answer is correct
                self.answer_1.num_answering_users += 1
            elif current_player == 2 and not None:  # Checks if the current player's answer is correct
                self.answer_2.num_answering_users += 1
            elif current_player == 3 and not None:  # Checks if the current player's answer is correct
                self.answer_3.num_answering_users += 1
            print 'Evaluating the responses of the other competitors....'
            time.sleep(1.2)


    class Menu:  # Constructs the main menu
        def __init__(self, list_of_menu_items, header):
            self.list_of_menu_items = list_of_menu_items
            self.header = header

        def display(self, display_header):  # displays the menu header with its items
            print
            print display_header
            print
            for item in self.list_of_menu_items:
                print str(item.number) + '. ' + item.text


    class MenItem:  # Constructs menu items
        def __init__(self, text, number):
            self.text = text
            self.number = number


    class Game:  # Builds game and starts here

        def __init__(self, prize=1000):
            self.dict_users = {}  # Dictionary of users
            self.prize = prize  # Prize for the game, can be changed later
            self.current_player = None  # Used to get the current player's details
            self.list_menu_items = []  # Stores the menu items
            self.questions_list = [Questions('What color are Zebras?', ['Black with white stripes',
                                                                        'Black with red stripes'],
                                             'White with black stripes'),
                                   Questions('Where was the old Campus of Sehir University?', ['Levent', 'Maltepe'],
                                             'Altunizade')]
            users = {'5577': {'abbas': 5.4}, '5466': {'betul': 3.2}, '5551': {'omer': 6.4}, '5634': {'basil': 10.2},
                     '5573':
                         {'ahmed': 1.2}, '5544': {'mohammad': 0}, '5897': {'Seeham': 5}, '5022': {'Yusuf': 14.2},
                     '5802': {'Yusuf': 1.5},
                     '5989': {'Jade': 1.0}}
            for num, name_balance in users.items():
                self.dict_users[num] = Users(name_balance.keys()[0], name_balance.values()[0], num)
                # ^ Adds a user and adds his/her details as a user object in values (Example: "5577": user object)

        def build_admin_menu(self):  # Builds Menu
            menu_item_1 = MenItem('Set prize for the next competition.', 1)
            menu_item_2 = MenItem('Display questions for the next competition.', 2)
            menu_item_3 = MenItem('Add new question to the next competition.', 3)
            menu_item_4 = MenItem('Delete a question from the next competition.', 4)
            menu_item_5 = MenItem("See users' data.", 5)
            menu_item_6 = MenItem('Log out.', 6)
            self.list_menu_items.extend([menu_item_1, menu_item_2, menu_item_3, menu_item_4, menu_item_5, menu_item_6])
            # ^ Adds menu items to a list

        def show_admin_menu(self):  # Displays the menu when "**" is entered
            self.build_admin_menu()
            main_menu = Menu(self.list_menu_items, 'Welcome to Sehir Hadi Admin Section, please choose '
                                                   'one of the following'
                                                   ' options:')
            while True:  # Makes an infinite loop unless if user logs out
                main_menu.display(main_menu.header)
                print
                choice = input('Select a number: ')
                if choice > 6:  # Makes sure that user chooses what is given in the menu items
                    print
                    print 'Please select a number from the given menu items'
                    print
                if choice == 1:  # Changes Prize
                    print
                    new_prize = input('Please type the total prize of the next competition: ')
                    print
                    print 'Setting Total Prize to ' + str(new_prize) + '...'
                    self.prize = new_prize
                    time.sleep(1.5)
                    print
                    print ' Done!'
                elif choice == 2:  # Displays Users' details
                    ques_num = 0
                    for question in self.questions_list:
                        ques_num += 1
                        question.display(ques_num, True, True)
                        print
                    raw_input('PRESS ENTER TO GO BACK TO THE MAIN MENU')
                elif choice == 3:  # Adds a new question
                    print
                    new_ques = raw_input('Please type the question: ')
                    correct = raw_input('Please type the CORRECT answer:')
                    incorrect_1 = raw_input('Please type an incorrect answer:')
                    incorrect_2 = raw_input('Please type an incorrect answer:')
                    self.questions_list.append(Questions(new_ques, [incorrect_1, incorrect_2], correct))
                    print
                    print 'Adding to the questions database.....'
                    time.sleep(1)
                    print
                    print ' Done!'
                elif choice == 4:  # Removes an existing question
                    ques_num = 0
                    for question in self.questions_list:
                        ques_num += 1
                        question.display(ques_num, False, False)  # Displays questions only
                    print
                    del_ques = input('Please type the number of the question to be deleted: ')
                    if del_ques == (self.questions_list.index((self.questions_list[(del_ques - 1)])) + 1):
                        self.questions_list.remove(self.questions_list[(del_ques - 1)])
                        print 'Q' + str(del_ques) + ' has been deleted successfully!'
                elif choice == 5:  # Displays users' details
                    for user in self.dict_users.values():
                        user.print_user_stats()
                elif choice == 6:  # Goes back to the login page and breaks the infinite loop
                    del self.list_menu_items[:]
                    self.login()
                    break

        def login(self):
            print
            print('----- Welcome to Sehir Hadi :D -----')
            print
            while True:  # Makes an infinite loop unless broken by entering a valid phone number
                print
                log_in = raw_input('Please type your Phone Number to sign in: ')
                print
                if log_in in self.dict_users:  # Checks if the given number is valid
                    print 'Checking ' + log_in + '...'
                    time.sleep(0.5)
                    print
                    print '=' * 20  # Welcomes the current player and breaks the loop
                    print '   Welcome ' + self.dict_users[log_in].name + '!'
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
                    self.current_player = self.dict_users.pop(log_in)
                    self.play()
                    break
                if log_in == '**':  # Displays the main menu
                    self.show_admin_menu()
                    break
                else:
                    print 'Checking ' + log_in + '...'
                    time.sleep(0.5)
                    print
                    print log_in + ' is not a valid phone number, please try again!'

        def play(self):
            ques_num = 0  # Number of questions
            eliminated = 0  # Used to check if the current player is eliminated (0 = not eliminated, eliminated > 0)
            number_players = (len(self.dict_users) + 1)  # Takes the overall number of players, including the
            # current player
            for question in self.questions_list:
                ques_num += 1
                player_answer = None  # Updates tht player's answer to None so that it does not stay the
                # same through out the game
                print
                print '************************* Total Players: ' + str(number_players)
                print
                question.display(ques_num, True, False)
                print
                if eliminated == 0:
                    player_answer = input('Your Answer: ')
                    number_players -= 1
                if eliminated > 0:
                    time.sleep(2.0)
                    question.process_answers(self.dict_users, player_answer)
                    question.display(ques_num, False, True)
                    number_players = len(self.dict_users)
                if player_answer is not None and player_answer == question.answers_list[(player_answer - 1)].answer_no \
                        and question.answers_list[(player_answer - 1)].is_correct:
                    # ^ Checks if the player's answer is correct
                    print
                    print 'CORRECT !'
                    print
                    question.process_answers(self.dict_users, player_answer)
                    question.display(ques_num, False, True)
                    number_players = len(self.dict_users) + 1
                elif not (not (player_answer is not None) or not (
                        player_answer == question.answers_list[(player_answer - 1)].answer_no) or question.answers_list[
                              (player_answer - 1)].is_correct):
                    # ^ Checks if the player's answer is incorrect
                    print
                    print 'INCORRECT !'
                    print
                    number_players = len(self.dict_users)
                    number_players -= 1
                    question.process_answers(self.dict_users, player_answer)
                    question.display(ques_num, False, True)
                    number_players -= 1
                    eliminated += 1
                if ques_num == len(self.questions_list) or number_players == 1:  # Checks who won
                    print
                    print '--- TOTAL WINNERS: ' + str(number_players)  # prints the number of winners
                    print '--- TOTAL DISTRIBUTED PRIZE: ' + str(float(self.prize))
                    for user in self.dict_users.values():
                        print user.name + ' ---> ' + str(self.prize / number_players) + ' - Current Balance: ' + \
                              str(self.prize / number_players + user.balance)
                    if eliminated == 0:  # If the current player is not eliminate, it displays the player as a winner
                        print self.current_player.name + ' ---> ' + str(self.prize / number_players) + \
                              ' - Current Balance: ' + str(self.prize / number_players + self.current_player.balance)
                        #                                            ^ Divides the prize
                    print
                    print 'See you Later :)\n'
                    time.sleep(2.5)
                    break


    a = Game()

    a.login()
