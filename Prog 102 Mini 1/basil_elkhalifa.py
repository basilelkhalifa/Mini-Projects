# The following website are the sources we used to fix bugs and get solution from:
# https://www.programering.com/a/MTMyQDNwATU.html ==> How to use the xlrd and xlwt modules (used in lines:230+, 288+ )

# https://stackoverflow.com/questions/34849035/how-to-get-the-value-of-a-selected-treeview-item
# ^^^^ How to get the selected value of the tree view (used in lines: 258 )

# https://www.programiz.com/python-programming/methods/string/strip ==> Removing spaces in name, using strip()
# ^^^ (used in lines: 326)

# https://stackoverflow.com/questions/15092437/python-encoding-utf-8 ==> Turkish characters cannot be read by python
# therefore we used encode(utf-8) (used in lines: 329+)


from Tkinter import *
import ttk
import tkFileDialog
import xlrd
import xlwt


class GUI(Frame):  # ==> Class that contains only gui parts(widgets and frames)
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.app_gui()  # ==> Function that starts the gui

    def app_gui(self):
        self.app_main_label = Label(self, text="Grades Management Tool",  # ==> App's Label
                                    font='Arial 20 bold', bg='#20EB8E', fg='white')
        self.pack(fill=BOTH)  # ==> Packs the main (biggest) frame
        self.app_main_label.pack(fill=X)  # ==> Packs the app's label and fills the empty in the x axis

        button_frame = Frame(self)  # ==> Frame of that contains the "select file" button
        button_frame.pack(fill=X)  # ==> Packs the frame and expands it horizontally
        self.select_file_button = Button(button_frame, text="Select File", font='Arial 10 bold')
        self.select_file_button.pack(side=LEFT, pady=10, padx=80)  # Packs the "select file" button

        details_frame = Frame(self)  # ==> Frame that contains the widget (which contain the students' information.)
        details_frame.pack(fill=X)
        self.all_students = ttk.Treeview(details_frame)  # Widget that displays the students' grades, names, ids, etc
        self.all_students.configure(column=('1', '2'))  # Adds two columns to the widget. One already exists, 3 overall

        self.all_students.column('#0', width=100, anchor='center')  # Placing the info in the center
        self.all_students.column('1', width=100, anchor='center')  # ^^^^^^
        self.all_students.column('2', width=100, anchor='center')  # ^^^^^^

        self.all_students.heading('#0', text='ID')  # Changing the preexisting column name's to id
        self.all_students.heading('1', text='Name')
        self.all_students.heading('2', text='Surname')

        self.all_students.pack(side=LEFT, padx=10)  # Packs the widget ^

        self.show_data_button = Button(details_frame, text="Show Data", font='Arial 10 bold')
        self.show_data_button.pack(side=LEFT)  # Creates the show data button

        show_student_frame = Frame(details_frame, relief=GROOVE, borderwidth=2)
        show_student_frame.pack(anchor=NW, padx=10)
        self.show_student_label = Label(show_student_frame, text="Grades Management Tool",
                                        font='Arial 10 bold', bg='#029C9E', fg='white', width=29)
        self.show_student_label.pack(padx=1, fill=X)

        student_frame_1 = Frame(show_student_frame)
        student_frame_2 = Frame(show_student_frame)
        student_frame_3 = Frame(show_student_frame)
        student_frame_4 = Frame(show_student_frame)  # <== FRAMES THAT CONTAIN EACH INFORMATION ABOUT A STUDENT
        student_frame_1.pack(side=LEFT, fill=Y)
        student_frame_2.pack(side=LEFT, fill=Y)
        student_frame_3.pack(side=LEFT, fill=Y)
        student_frame_4.pack(side=LEFT, fill=Y)

        self.name_details = Label(student_frame_1, text="Name ", font='Arial 10 bold')
        self.student_name_var = StringVar()  # String Variable used to change the student name later on
        self.student_name = Label(student_frame_2, textvariable=self.student_name_var)
        self.name_details.pack(anchor=W, pady=10, padx=10)
        self.student_name.pack(anchor=W, pady=10, padx=10)

        self.surname_details = Label(student_frame_1, text="Surname ", font='Arial 10 bold')
        self.student_surname_var = StringVar()  # String Variable used to change the student surname later on
        self.student_surname = Label(student_frame_2, textvariable=self.student_surname_var)
        self.surname_details.pack(anchor=W, pady=10, padx=10)
        self.student_surname.pack(anchor=W, pady=10, padx=10)

        self.id_details = Label(student_frame_1, text="ID ", font='Arial 10 bold')
        self.student_id_var = StringVar()  # String Variable used to change the student id later on
        self.student_id = Label(student_frame_2, textvariable=self.student_id_var)
        self.id_details.pack(anchor=W, pady=10, padx=10)
        self.student_id.pack(anchor=W, pady=10, padx=10)

        self.dept_details = Label(student_frame_1, text="Dept ", font='Arial 10 bold')
        self.student_dept_var = StringVar()  # String Variable used to change the student department later on
        self.student_dept = Label(student_frame_2, textvariable=self.student_dept_var)
        self.dept_details.pack(anchor=W, pady=10, padx=10)
        self.student_dept.pack(anchor=W, pady=10, padx=10)

        self.gpa_details = Label(student_frame_1, text="GPA ", font='Arial 10 bold')
        self.student_gpa_var = StringVar()  # String Variable used to change the student gpa later on
        self.student_gpa = Label(student_frame_2, textvariable=self.student_gpa_var)
        self.gpa_details.pack(anchor=W, pady=10, padx=10)
        self.student_gpa.pack(anchor=W, pady=10, padx=10)

        self.m1_score = Label(student_frame_3, text="MP1 Grade: ", font='Arial 10 bold')
        self.m1_score_var = StringVar()  # String Variable used to change the student mini1 grade later on
        self.m1_student_score = Label(student_frame_4, textvariable=self.m1_score_var)
        self.m1_score.pack(anchor=W, pady=10, padx=10)
        self.m1_student_score.pack(anchor=W, pady=10, padx=10)

        self.m2_score = Label(student_frame_3, text="MP2 Grade: ", font='Arial 10 bold')
        self.m2_score_var = StringVar()  # String Variable used to change the student mini2 grade later on
        self.m2_student_score = Label(student_frame_4, textvariable=self.m2_score_var)
        self.m2_score.pack(anchor=W, pady=10, padx=10)
        self.m2_student_score.pack(anchor=W, pady=10, padx=10)

        self.m3_score = Label(student_frame_3, text="MP3 Grade: ", font='Arial 10 bold')
        self.m3_score_var = StringVar()  # String Variable used to change the student mini3 grade later on
        self.m3_student_score = Label(student_frame_4, textvariable=self.m3_score_var)
        self.m3_score.pack(anchor=W, pady=10, padx=10)
        self.m3_student_score.pack(anchor=W, pady=10, padx=10)

        self.mt_score = Label(student_frame_3, text="MT Grade: ", font='Arial 10 bold')
        self.mt_score_var = StringVar()  # String Variable used to change the student midterm grade later on
        self.mt_student_score = Label(student_frame_4, textvariable=self.mt_score_var)
        self.mt_score.pack(anchor=W, pady=10, padx=10)
        self.mt_student_score.pack(anchor=W, pady=10, padx=10)

        self.fg_score = Label(student_frame_3, text="Final Grade: ", font='Arial 10 bold')
        self.fg_score_var = StringVar()  # String Variable used to change the student final grade later on
        self.fg_student_score = Label(student_frame_4, textvariable=self.fg_score_var)
        self.fg_score.pack(anchor=W, pady=10, padx=10)
        self.fg_student_score.pack(anchor=W, pady=10, padx=10)

        grade_change_frame = Frame(self, relief=GROOVE, borderwidth=3)  # Frame that contains the widget
        grade_change_frame.pack(anchor=W, fill=X)  # (which allow the users to change info)
        grade_frame_1 = Frame(grade_change_frame)
        grade_frame_1.pack(anchor=W)
        grade_frame_2 = Frame(grade_change_frame)
        grade_frame_2.pack(anchor=W)
        grade_frame_3 = Frame(grade_change_frame)
        grade_frame_3.pack(anchor=W)
        grade_frame_4 = Frame(grade_change_frame)  # <== FRAMES THAT CONTAIN THE WIDGETS ^
        grade_frame_4.pack(anchor=W, padx=100)
        save_type_frame_1 = Frame(grade_frame_4)
        save_type_frame_1.pack(anchor=W)
        save_type_frame_2 = Frame(grade_frame_4)
        save_type_frame_2.pack(anchor=W)
        save_type_frame_3 = Frame(grade_frame_4)
        save_type_frame_3.pack(anchor=W)

        self.projects = Label(grade_frame_1, text='Projects: ')
        self.grades = Label(grade_frame_2, text='Grades: ')
        self.m1_changer = Label(grade_frame_1, text='MP1 ')
        self.m2_changer = Label(grade_frame_1, text='MP2 ')
        self.m3_changer = Label(grade_frame_1, text='MP3 ')
        self.mt_changer = Label(grade_frame_1, text='MT ')  # LABELS OF WIDGETS
        self.final_changer = Label(grade_frame_1, text='Final ')
        self.m1_entry = Entry(grade_frame_2, width=10)
        self.m2_entry = Entry(grade_frame_2, width=10)
        self.m3_entry = Entry(grade_frame_2, width=10)  # ENTRY WIDGETS
        self.mt_entry = Entry(grade_frame_2, width=10)
        self.fg_entry = Entry(grade_frame_2, width=10)

        self.projects.pack(side=LEFT, padx=20)
        self.grades.pack(side=LEFT, padx=20)
        self.m1_changer.pack(side=LEFT, padx=20)
        self.m2_changer.pack(side=LEFT, padx=20)  # PACKS ALL THE LABELS ^
        self.m3_changer.pack(side=LEFT, padx=20)
        self.mt_changer.pack(side=LEFT, padx=20)
        self.final_changer.pack(side=LEFT, padx=20)

        self.m1_entry.pack(side=LEFT, padx=5)
        self.m2_entry.pack(side=LEFT, padx=5)
        self.m3_entry.pack(side=LEFT, padx=5)  # PACKS ALL THE WIDGETS ^
        self.mt_entry.pack(side=LEFT, padx=5)
        self.fg_entry.pack(side=LEFT, padx=5)

        self.save_button = Button(grade_frame_2, text="Save Grade", font='Arial 10 bold', height=2)
        self.save_button.pack(padx=10)

        self.export = Label(grade_frame_3, text="Export As:")
        self.export.pack(anchor=W, padx=20)

        self.user_choice = StringVar()  # String variable for checkbox
        self.user_choice.set("NONE")  # Set to none initially so that checkboxes will be initially empty
        self.save_file_name = Label(save_type_frame_1, text='File Name: ')
        self.save_file_entry = Entry(save_type_frame_1, width=21)
        self.csv = Checkbutton(save_type_frame_1, text='csv', variable=self.user_choice, onvalue='CSV')
        self.txt = Checkbutton(save_type_frame_2, text='txt', variable=self.user_choice, onvalue='TXT')
        self.xls = Checkbutton(save_type_frame_3, text='xls', variable=self.user_choice, onvalue='XLS')
        self.export_button = Button(save_type_frame_2, text='Export Data', width=27)  # Button that exports new file

        self.csv.pack(side=LEFT)
        self.txt.pack(side=LEFT)
        self.xls.pack(side=LEFT)
        self.save_file_name.pack(side=LEFT, padx=5)  # PACKS WIDGETS
        self.save_file_entry.pack(side=LEFT)
        self.export_button.pack(side=LEFT, padx=10, pady=2)

        self.info_var = StringVar()  # String variables that displays the info to the user
        self.info_var.set('Program messages... ')
        self.info = Label(self, textvariable=self.info_var)
        self.info.pack(anchor=W)


class StudentObj:  # Class to create student object for each student (contains grades, names, and etc)
    def __init__(self, name, surname, section, department, gpa, mini_1, mini_2, mini_3, midterm, final):
        self.surname = surname
        self.name = name
        self.department = department
        self.mini_1 = mini_1
        self.mini_2 = mini_2
        self.mini_3 = mini_3
        self.midterm = midterm
        self.final = final
        self.gpa = gpa
        self.section = section


class AppMechanics:  # The main logic of the app
    def __init__(self, parent):
        self.gui_root = GUI(parent)  # Gui object (Creates the gui)
        self.start()  # function that handles commands
        self.file_opened = False  # Variable that tells python whether the user has opened the file or not (False:no)
        self.student_selected = False  # ^^^^^^^^^^^^^^ whether the user selected a student or not ^^^^^^^^^
        self.students_data_dic = {}  # Dictionary that contains the students' information

    def gather_data(self):  # Function that gets the file path
        try:  # <== Makes sure that the user loads the file correctly
            self.excel_file = tkFileDialog.askopenfilename(initialdir="/", title="Select Student File",
                                                           filetypes=[("Excel files", "*.xlsx")])
            self.gui_root.info_var.set('INFO: File Loaded')
            try:
                self.file_extract()
            except:
                self.gui_root.info_var.set("INFO: An ERROR has occurred! Please make sure you chose the correct file")
        except IOError:
            self.gui_root.info_var.set("INFO: Loading Failed! Please Try Again.")
            # ^^^^ Makes sure that the user chooses the right file for the program to run properly

    def file_extract(self):  # Function that gets the students' info and puts them as a student objects in a dictionary
        self.opened_file = xlrd.open_workbook(self.excel_file)
        self.file_opened = True  # Tells python that the user has opened the file (True:yes)
        self.file_sheet = self.opened_file.sheet_by_index(0)
        for r in range(1, self.file_sheet.nrows):  # <== Algorithm that splits the students' names and surnames
            student_full_name = self.file_sheet.cell(r, 1).value.split()
            student_last_name = student_full_name[len(student_full_name) - 1]
            student_full_name.pop()
            student_first_name = ''
            for name in student_full_name:
                student_first_name += name + ' '
            self.students_data_dic[int(self.file_sheet.cell(r, 0).value)] = StudentObj(student_first_name,
                                                                                       student_last_name,
                                                                                       self.file_sheet.cell(r, 2).value,
                                                                                       self.file_sheet.cell(r, 3).value,
                                                                                       self.file_sheet.cell(r, 4).value,
                                                                                       self.file_sheet.cell(r, 5).value,
                                                                                       self.file_sheet.cell(r, 6).value,
                                                                                       self.file_sheet.cell(r, 7).value,
                                                                                       self.file_sheet.cell(r, 8).value,
                                                                                       self.file_sheet.cell(r,
                                                                                                            9).value, )
        for student in self.students_data_dic:  # <== Adds the student to the widget that displays data
            self.gui_root.all_students.insert('', 'end', text=student,
                                              values=(self.students_data_dic[student].name,
                                                      self.students_data_dic[student].surname))

    def viewer(self):  # <== Function that shows the students' info in details
        for st in self.gui_root.all_students.selection():
            if self.gui_root.all_students.item(st, 'text') in self.students_data_dic.keys():
                self.student_selected = True
                self.gui_root.info_var.set('INFO: File Loaded')  # <== informs the user that the file has loaded

                self.gui_root.m1_entry.delete(0, END)
                self.gui_root.m2_entry.delete(0, END)
                self.gui_root.m3_entry.delete(0, END)   # <== Empties grades' entries
                self.gui_root.mt_entry.delete(0, END)
                self.gui_root.fg_entry.delete(0, END)
                try:
                    self.gui_root.m1_entry.insert(END, int(self.students_data_dic
                                                   [self.gui_root.all_students.item(st, 'text')].mini_1))
                    self.gui_root.m2_entry.insert(END, int(self.students_data_dic
                                                   [self.gui_root.all_students.item(st, 'text')].mini_2))
                    self.gui_root.m3_entry.insert(END, int(self.students_data_dic
                                                   [self.gui_root.all_students.item(st, 'text')].mini_3))
                    self.gui_root.mt_entry.insert(END, int(self.students_data_dic
                                                   [self.gui_root.all_students.item(st, 'text')].midterm))
                    self.gui_root.fg_entry.insert(END, int(self.students_data_dic
                                                   [self.gui_root.all_students.item(st, 'text')].final))
                except ValueError:
                    pass    # <== Ignores empty grades when converting grades to integers
                # ^^^^^^^^^ Displays grades in entries ^^^^^^^^^^

                self.gui_root.student_name_var.set(self.students_data_dic
                                                   [self.gui_root.all_students.item(st, 'text')].name
                                                   )

                self.gui_root.student_surname_var.set(self.students_data_dic
                                                      [self.gui_root.all_students.item(st, 'text')].surname)
                self.gui_root.student_dept_var.set(self.students_data_dic
                                                   [self.gui_root.all_students.item(st, 'text')].department)
                self.gui_root.student_gpa_var.set(self.students_data_dic
                                                  [self.gui_root.all_students.item(st, 'text')].gpa)
                self.gui_root.student_id_var.set(self.gui_root.all_students.item(st, 'text'))
                self.gui_root.m1_score_var.set(self.gui_root.m1_entry.get())
                self.gui_root.m2_score_var.set(self.gui_root.m2_entry.get())
                self.gui_root.m3_score_var.set(self.gui_root.m3_entry.get())
                self.gui_root.mt_score_var.set(self.gui_root.mt_entry.get())
                self.gui_root.fg_score_var.set(self.gui_root.fg_entry.get())
                # ^^^^^^^^^^^^^^^^^^^^^^^^ Changes the string var to the student's info ^^^^^^^^^^^^^^^^
        if not self.file_opened:  # <== Informs user that he/she has to select a file first
            self.gui_root.info_var.set('INFO: Please Load The File First')
        elif not self.student_selected:  # <== Informs ^^^^^^^ has to select a student
            self.gui_root.info_var.set('INFO: Please Select A Student First')

    def export_file(self):  # Function that creates new file when user saves a file
        if self.gui_root.user_choice.get() == 'XLS' and self.file_opened == True and \
                self.gui_root.save_file_entry.get() != '':
            self.gui_root.info_var.set('INFO: Saving File...')
            new_file = xlwt.Workbook(encoding='ascii')
            new_sheet = new_file.add_sheet('My Worksheet')
            new_sheet.write(0, 0, label='ID')
            new_sheet.write(0, 1, label='NAME')
            new_sheet.write(0, 2, label='SECTION')
            new_sheet.write(0, 3, label='DEPT')
            new_sheet.write(0, 4, label='GPA')
            new_sheet.write(0, 5, label='MP1')
            new_sheet.write(0, 6, label='MP2')
            new_sheet.write(0, 7, label='MP3')
            new_sheet.write(0, 8, label='MT')
            new_sheet.write(0, 9, label='FINAL')
            row_counter = 0
            for student in self.students_data_dic:
                row_counter += 1
                new_sheet.write(row_counter, 0, label=student)
                new_sheet.write(row_counter, 1, label=self.students_data_dic[student].name +
                                                      self.students_data_dic[student].surname)
                new_sheet.write(row_counter, 2, label=self.students_data_dic[student].section)
                new_sheet.write(row_counter, 3, label=self.students_data_dic[student].department)
                new_sheet.write(row_counter, 4, label=self.students_data_dic[student].gpa)
                new_sheet.write(row_counter, 5, label=self.students_data_dic[student].mini_1)
                new_sheet.write(row_counter, 6, label=self.students_data_dic[student].mini_2)
                new_sheet.write(row_counter, 7, label=self.students_data_dic[student].mini_3)
                new_sheet.write(row_counter, 8, label=self.students_data_dic[student].midterm)
                new_sheet.write(row_counter, 9, label=self.students_data_dic[student].final)
            new_file.save(self.gui_root.save_file_entry.get() + '.xls')
            self.gui_root.info_var.set('INFO: File Saved')
            self.gui_root.info_var.set('INFO: File saved as ' + self.gui_root.save_file_entry.get() + ' .xls')
        elif self.gui_root.user_choice.get() == 'TXT' and self.file_opened == True and \
                self.gui_root.save_file_entry.get() != '':
            text_file = open(self.gui_root.save_file_entry.get() + '.txt', 'w')
            for student in self.students_data_dic:
                text_file.write(
                    str(student) + ',' + self.students_data_dic[student].name.encode('utf-8').strip() + ',' +
                    self.students_data_dic[student].surname.encode('utf-8') + ',' +
                    self.students_data_dic[student].section.encode('utf-8') + ',' +
                    self.students_data_dic[student].department.encode('utf-8') + ',' +
                    str(self.students_data_dic[student].gpa) + ',' +
                    str(self.students_data_dic[student].mini_1) + ',' +
                    str(self.students_data_dic[student].mini_2) + ',' +
                    str(self.students_data_dic[student].mini_3) + ',' +
                    str(self.students_data_dic[student].midterm) + ',' +
                    str(self.students_data_dic[student].final) + '\n')
            text_file.close()
            self.gui_root.info_var.set('INFO: File saved as ' + self.gui_root.save_file_entry.get() + ' .txt')
        elif self.gui_root.user_choice.get() == 'CSV':
            self.gui_root.info_var.set("INFO: Type Not Supported")
        elif self.file_opened == False:
            self.gui_root.info_var.set('INFO: Please Load The File First')
        elif self.gui_root.user_choice.get() == 'NONE' and self.gui_root.save_file_entry.get() == '':
            self.gui_root.info_var.set('INFO: Please provide the name of the file and Select a Type.')
        elif self.gui_root.user_choice.get() == 'NONE':
            self.gui_root.info_var.set('INFO: Type Not Chosen')
        elif self.gui_root.save_file_entry.get() == '':
            self.gui_root.info_var.set('INFO: Please provide the name of the file.')
        # ^^^^^^^^^^^^^^^^ Informs user about incorrect use of the program ^^^^^^^^^^^^^

    def tree_clicked(self, event):  # <== Function to activated when user clicks on the tree view widget
        if not self.file_opened:
            self.gui_root.info_var.set('INFO: Please Load The File First')

    def save_grades(self):  # <=== Changes students info in the dictionary
        try:
            if self.file_opened and self.student_selected:
                new_grade_m1 = int(self.gui_root.m1_entry.get())
                new_grade_m2 = int(self.gui_root.m2_entry.get())
                new_grade_m3 = int(self.gui_root.m3_entry.get())    # <== Converts grades to integers if the
                new_grade_mt = int(self.gui_root.mt_entry.get())    # enter grades individually
                new_grade_fg = int(self.gui_root.fg_entry.get())

                for student in self.students_data_dic:
                    if student == int(self.gui_root.student_id_var.get()):
                        self.students_data_dic[student].mini_1 = new_grade_m1
                        self.students_data_dic[student].mini_2 = new_grade_m2
                        self.students_data_dic[student].mini_3 = new_grade_m3
                        self.students_data_dic[student].midterm = new_grade_mt
                        self.students_data_dic[student].final = new_grade_fg

                self.viewer()  # <== re-updates the student info to the new grades

            elif not self.file_opened:
                self.gui_root.info_var.set('INFO: Please Load The File First')
            elif not self.student_selected:
                self.gui_root.info_var.set('INFO: Please Select A Student First')
        except ValueError:  # <==Informs user to only add numbers
            self.gui_root.info_var.set("INFO: Warning, The Type of the Grade is incorrect.")

    def start(self):  # Function that runs everything
        self.gui_root.all_students.bind("<Button-1>", self.tree_clicked)  # <== binds the left click with the method
        self.gui_root.select_file_button.config(command=self.gather_data)
        self.gui_root.show_data_button.configure(command=self.viewer)
        self.gui_root.save_button.configure(command=self.save_grades)
        self.gui_root.export_button.configure(command=self.export_file)
        # ^^^^^^^^^^^^^ Changes the commands to the methods ^^^^^^^^^^^^^^^


def main():  # <== Creates the window
    root = Tk()
    app = AppMechanics(root)
    root.title("Grades Management Tool v1.0")
    root.mainloop()


main()
