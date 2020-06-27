# Sources
#           1. https://www.programiz.com/python-programming/methods/string/strip (Line:142)
#           2. https://www.programiz.com/python-programming/methods/built-in/sorted (Line: 200+)
from Tkinter import *
from recommendations import *
import tkFileDialog


# ============== Graphical User Interface ==============
class GUI(Frame):  # Holds all GUI items
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.banner = Label(self, text="Protein Function Prediction Tool", font="caliber 25 bold",
                            bg="green", fg="white", height=2)

        self.buttons_frames = Frame(self)  # <== Frame that contains button's widgets
        self.annotations_button = Button(self.buttons_frames, text="Upload \nAnnotations", font="Arial 10 bold")
        self.evidence_button = Button(self.buttons_frames, text="Upload Evidence\n Code Values", font="Arial 10 bold")
        self.go_button = Button(self.buttons_frames, text="Upload GO File", font="Arial 10 bold")

        self.viewer_editor_frame = Frame(self)  # <== Frame that contains protein listbox and its scroller
        self.protein_frame = Frame(self.viewer_editor_frame)
        self.protein_scroll = Scrollbar(self.protein_frame)
        self.protein_viewer = Listbox(self.protein_frame, yscrollcommand=self.protein_scroll.set, width=35,
                                      selectmode=BROWSE)
        self.protein_scroll.configure(command=self.protein_viewer.yview)    # <== Binds the scrollbar to the listbox
        self.protein_label = Label(self.protein_frame, text="Protein", font="Arial 10 bold")

        self.check_var = StringVar()
        self.check_var.set("E")  # <== Sets the Euclidean checkbox as the default checkbox
        self.similarity_metric_frame = Frame(self.viewer_editor_frame)
        self.similarity_borders = Frame(self.similarity_metric_frame, highlightbackground="black", highlightthickness=2)
        self.similarity_label = Label(self.similarity_metric_frame, text="Similarity Metric", font="Arial 10 bold")
        self.check_boxes_frame = Frame(self.similarity_borders)
        self.pearson_check = Checkbutton(self.check_boxes_frame, text="Pearson", variable=self.check_var, onvalue="P")
        self.euclidean_check = Checkbutton(self.check_boxes_frame, text="Euclidean", variable=self.check_var,
                                           onvalue="E")

        self.similar_protein_frame = Frame(self.viewer_editor_frame)    # <== Frame that contains similar listbox
        self.similar_protein_scroll = Scrollbar(self.similar_protein_frame)     # <== Similar listbox's scrollbar
        self.similar_protein_viewer = Listbox(self.similar_protein_frame, height=17, width=45, selectmode=SINGLE,
                                              yscrollcommand=self.similar_protein_scroll.set)
        self.similar_protein_scroll.configure(command=self.similar_protein_viewer.yview)
        self.similar_protein_label = Label(self.similar_protein_frame, text="Similar Protein", font="Arial 10 bold")

        self.predicted_function_frame = Frame(self.viewer_editor_frame)
        self.predicted_function_scroll = Scrollbar(self.predicted_function_frame)
        self.predicted_function_viewer = Listbox(self.predicted_function_frame, width=75, selectmode=SINGLE,
                                                 yscrollcommand=self.predicted_function_scroll.set)
        self.predicted_function_scroll.configure(command=self.predicted_function_viewer.yview)
        self.predicted_function_label = Label(self.predicted_function_frame,
                                              text="Predicted Function", font="Arial 10 bold")
        self.data = Main(self.protein_viewer, self.predicted_function_viewer, self.similar_protein_viewer,
                         self.check_var, self.pearson_check, self.euclidean_check)  # Object of Data center
        self.start()

    def start(self):    # Function that packs everything and configures widgets
        self.pack(fill=BOTH, expand=True)
        self.banner.pack(fill=X)
        self.buttons_frames.pack(pady=25, padx=100)
        for button in (self.annotations_button, self.evidence_button, self.go_button): button.pack(padx=35, side=LEFT)
        self.viewer_editor_frame.pack(anchor=N, side=LEFT, expand=True)
        for frame in (self.protein_frame, self.similarity_metric_frame, self.similar_protein_frame,
                      self.predicted_function_frame): frame.pack(padx=5, side=LEFT, anchor=N, fill=Y)
        # ^ Puts the frames in a tuple then iterates through it to pack each frame
        self.protein_label.pack(anchor=N)
        for viewer_scroll in (self.protein_viewer, self.protein_scroll): viewer_scroll.pack(side=LEFT, fill=Y)
        # ^ Puts the scrolls in a tuple then iterates through it to pack each frame
        self.similarity_label.pack(anchor=N)
        self.similarity_borders.pack(fill=Y, padx=35, expand=True)
        self.check_boxes_frame.pack(padx=40, pady=20)
        for checkboxes in (self.pearson_check, self.euclidean_check): checkboxes.pack(anchor=N)
        # ^ Puts the check_boxes in a tuple then iterates through it to pack each frame
        self.similar_protein_label.pack(anchor=N)
        for viewer_scroll in (self.similar_protein_viewer, self.similar_protein_scroll):
            viewer_scroll.pack(side=LEFT, fill=Y)
        # ^ Puts the viewer and its scroll in a tuple then iterates through it to pack each frame
        self.predicted_function_label.pack()
        for viewer_scroll in (self.predicted_function_viewer, self.predicted_function_scroll):
            viewer_scroll.pack(side=LEFT, fill=Y)
        # ^ Puts the viewer and its scroll in a tuple then iterates through it to pack each frame
        self.go_button.configure(command=self.data.read_parses_go)
        self.annotations_button.configure(command=self.data.read_parses_af)
        self.evidence_button.configure(command=self.data.read_parses_ecv)
        self.pearson_check.configure(command=self.data.check_command)
        self.euclidean_check.configure(command=self.data.check_command)
        # ^ Configure  the buttons and checkboxes


# ============== Functionality Class ==============
class Functionality:  # Holds the GO id and its name
    def __init__(self, go_id, go_name):
        self.go_id = go_id
        self.go_name = go_name


# ============== Evidence Code Class ==============
class EvidenceCode:  # Holds the evidence codes' acronyms and their values
    def __init__(self, acro, num_value):
        self.acro = acro
        self.num_value = num_value


# ============== Annotations Class ==============
class Annotations:   # Holds the objects of GO (functionality) and Evidence Code
    def __init__(self, go_id, go_name, acr, num):
        self.functionality = Functionality(go_id, go_name)
        self.evidence_code = EvidenceCode(acr, num)


# ============== Proteins' Class ==============
class Protein:
    def __init__(self, protein_id, protein_name):
        self.protein_id = protein_id    # <== Protein's id from the gaf file
        self.protein_name = protein_name    # <== Protein's name from the gaf file
        self.annotations = {}   # <== Dictionary that keeps objects of annotation

    def add_obj(self, go_id, go_name, acr, acr_value):      # <== Function that allows user to add objects to dic
        self.annotations[go_id] = Annotations(go_id, go_name, acr, acr_value)


# ============== Main Logic/Data Center Class ==============
class Main:
    def __init__(self, pro_box, pre_box, sim_box, checkbox_var, pear_check, euc_check):
        self.protein_viewer = pro_box   # <== The Protein listbox
        self.check_var = checkbox_var   # <== The variable that determines which box is ticked
        self.similar_protein_viewer = sim_box   # <== The Similar Proteins listbox
        self.euclidean_check = euc_check    # <== The Euclidean checkbox
        self.pearson_check = pear_check     # <== The Pearson checkbox
        self.predicted_function_viewer = pre_box    # <== The Predicted Function listbox
        self.evidence_dictionary = {}   # <== Dictionary that holds Evidence code from ecv file
        self.go_dictionary = {}     # <== Dictionary that holds GO information from gaf file
        self.protein_dic = {}   # <== Dictionary that holds protein objects
        self.protein_nested_dic = {}    # <== Final nested dictionary that is used for the recommendation module
        self.current_id = None  # <== Determines the current GO id in go file
        self.current_name = None    # <== Determines the current name of GO in go file

    def read_parses_go(self):   # Parses Info from GO file
        self.go_file = tkFileDialog.askopenfile(initialdir="/", title="Select GO File",
                                                filetypes=[("obo files", "*.obo")])
        for line in self.go_file:
            if line.startswith("id: "):
                self.current_id = line[3:].strip()
            elif line.startswith("name: "):
                self.current_name = line[5:].strip()
            self.go_dictionary[self.current_id] = self.current_name
        self.main_logic()

    def read_parses_ecv(self):  # Parses Info from ecv file
        self.evidence_file = tkFileDialog.askopenfile(initialdir="/", title="Select Evidence Code Values File",
                                                      filetypes=[("txt files", "*.txt")])
        for line in self.evidence_file:
            self.evidence_dictionary[line.split()[0]] = line.split()[1]

    def read_parses_af(self):   # Parses Info from gaf file
        self.annotations_file = tkFileDialog.askopenfile(initialdir="/", title="Select Annotation File",
                                                         filetypes=[("gaf files", "*.gaf")])
        for line in self.annotations_file:
            if not line.startswith('!') and not line.split()[1] in self.protein_dic:
                self.protein_viewer.insert(END, line.split()[2])
                self.protein_dic[line.split()[1]] = Protein(line.split()[1], line.split()[2])
                self.protein_dic[line.split()[1]].add_obj(line.split()[3], None, line.split()[5], None)
            elif not line.startswith('!') and line.split()[1] in self.protein_dic:
                self.protein_dic[line.split()[1]].add_obj(line.split()[3], None, line.split()[5], None)

    def main_logic(self):   # Handles the dictionaries work
        for protein_obj in self.protein_dic.values():
            for go_id, name in self.go_dictionary.items():
                if go_id in protein_obj.annotations.keys():
                    protein_obj.annotations[go_id].functionality.go_name = name
        for protein_obj in self.protein_dic.values():
            for a, v in self.evidence_dictionary.items():
                for n in range(len(protein_obj.annotations.values())):
                    if a == protein_obj.annotations.values()[n].evidence_code.acro:
                        protein_obj.annotations.values()[n].evidence_code.num_value = v
        for protein in self.protein_dic:
            values_dictionary = {}
            for go in self.protein_dic[protein].annotations:
                try:  # <== Converts the evidence code's Num from string to int then float
                    values_dictionary[go] = float(int(self.protein_dic[protein].annotations[go].evidence_code.num_value))
                except ValueError:
                    values_dictionary[go] = float(self.protein_dic[protein].annotations[go].evidence_code.num_value)
                except TypeError:
                    pass    # <== Ignores the GO ids that do not exist in the gaf
            self.protein_nested_dic[protein] = values_dictionary
        self.protein_viewer.bind("<<ListboxSelect>>", self.sim_pre)

    def sim_pre(self, event):   # Function that handles the prediction and similarities
        current_selection = None    # <== Current selected protein
        name = None     # <== Similar Protein name Variable
        func = None     # <== Predicted Function name Variable
        pre_sorted = None   # <== The sorted predicted functions
        for protein in self.protein_dic:
            if self.protein_dic[protein].protein_name == self.protein_viewer.get(self.protein_viewer.
                                                                                 curselection()):
                current_selection = self.protein_dic[protein].protein_id
        if self.check_var.get() == 'E':
            self.similar_protein_viewer.delete(0, END)
            self.predicted_function_viewer.delete(0, END)
            sim = topMatches(self.protein_nested_dic, current_selection, len(self.protein_nested_dic), sim_distance)
            sim_sorted = sorted(sim, reverse=True)
            for t in sim_sorted:
                num, pro = t
                if round(num, 1) > 0:
                    for protein_obj in self.protein_dic.values():
                        if protein_obj.protein_id == pro:
                            name = protein_obj.protein_name
                    self.similar_protein_viewer.insert(END, str(round(num, 1)) + ' - ' + pro + ' - ' + name)
            pre = getRecommendations(self.protein_nested_dic, current_selection, sim_distance)
            pre_sorted = sorted(pre, reverse=True)
        elif self.check_var.get() == 'P':
            self.similar_protein_viewer.delete(0, END)
            self.predicted_function_viewer.delete(0, END)
            sim = topMatches(self.protein_nested_dic, current_selection, len(self.protein_nested_dic), sim_pearson)
            sim_sorted = sorted(sim, reverse=True)
            for t in sim_sorted:
                num, pro = t
                if round(num, 1) > 0:
                    for protein_obj in self.protein_dic.values():
                        if protein_obj.protein_id == pro:
                            name = protein_obj.protein_name
                    self.similar_protein_viewer.insert(END, str(round(num, 1)) + ' - ' + pro + ' - ' + name)
            pre = getRecommendations(self.protein_nested_dic, current_selection, sim_pearson)
            pre_sorted = sorted(pre, reverse=True)
        for t in pre_sorted:
            num, go = t
            for protein_obj in self.protein_dic.values():
                if go in protein_obj.annotations.keys():
                    func = protein_obj.annotations[go].functionality.go_name
            self.predicted_function_viewer.insert(END, str(num) + ' - ' + go + ' - ' + func)

    def check_command(self):  # Displays the predicted and similar proteins when each similarity is ticked
        self.sim_pre(None)


def main():
    root = Tk()
    application = GUI(root)
    root.geometry("1280x490")
    root.title("Protein Function Prediction Tool")
    root.mainloop()


main()
