# SOURCES
# 1. https://stackoverflow.com/questions/32399158/read-next-line-after-a-matching-line-in-python (Line:100+)
# 2. https://www.delftstack.com/howto/python-tkinter/how-to-pass-arguments-to-tkinter-button-command/ (Line:22+)
from Tkinter import *
import ttk
import clusters
import tkFileDialog
from PIL import ImageTk, Image


# ============ GUI ============
class GUI(Frame):   # Contains GUI widgets and frames
    def __init__(self, parent):
        Frame.__init__(self, parent)
        data = DataCenter()     # Data center object
        self.banner = Label(self, text="Election Data Analysis Tool v. 1.0",
                            font="Arial 16 bold", fg='white', bg='red')
        self.election_data_button = Button(self, text='Load Election Data', height=2,
                                           width=30, relief=GROOVE, command=data.read_parse)
        self.button_frame = Frame(self)
        self.districts_button = Button(self.button_frame, text="Cluster Districts",  # Districts'clustering button
                                       command=lambda: data.cluster_districts(self.display, self.scroll_ver,
                                                                              self.scroll_hor, self.district_label,
                                                                              self.list_box, self.list_b_scroll,
                                                                              self.threshold_label, self.thr,
                                                                              self.refine),
                                       height=3, width=30, relief=GROOVE,)
        self.political_button = Button(self.button_frame, text="Cluster Political Parties",  # Parties' clustering
                                       height=3, width=30, relief=GROOVE,
                                       command=lambda: data.cluster_party(self.display, self.scroll_ver,
                                                                          self.scroll_hor, self.district_label,
                                                                          self.list_box, self.list_b_scroll,
                                                                          self.threshold_label, self.thr,
                                                                          self.refine))
        self.settings_frame = Frame(self)   # Frame containing list box, combobox, and refine button
        self.widgets_frame = Frame(self)    # Frame containing all widgets
        self.display_frame = Frame(self.widgets_frame)  # Frame containing Canvas and its scrollbars
        self.scroll_ver = Scrollbar(self.display_frame)
        self.scroll_hor = Scrollbar(self.widgets_frame)
        self.display = Canvas(self.display_frame, width=700, height=300, yscrollcommand=self.scroll_ver.set,
                              xscrollcommand=self.scroll_hor.set, scrollregion=[0,0,1200,1000])
        self.district_label = Label(self.settings_frame, text="District")
        self.list_b_scroll = Scrollbar(self.settings_frame)
        self.list_box = Listbox(self.settings_frame, yscrollcommand=self.list_b_scroll.set, selectmode=MULTIPLE)
        self.threshold_label = Label(self.settings_frame, text="Threshold")
        self.thr = ttk.Combobox(self.settings_frame, width=7, values=['0%', '1%', '10%', '20%', '30%', '40%', '50%'])
        self.thr.current(0)
        self.refine = Button(self.settings_frame, text='Refine Analysis', height=2, width=30, relief=GROOVE,
                             command=lambda: data.refine(self.list_box, self.thr, self.display))
        self.start()

    def start(self):  # Used for packing initial widgets
        self.pack(fill=BOTH, expand=True)
        self.banner.pack(fill=X)
        self.election_data_button.pack(pady=8)
        self.button_frame.pack(padx=20)
        for b in (self.districts_button, self.districts_button, self.political_button): b.pack(side=LEFT)
        for f in (self.display_frame, self.widgets_frame, self.settings_frame): f.pack()


# ============ Districts Class ============
class District:  # Contains all districts' information
    def __init__(self, district_name):
        self.district_name = district_name
        self.election_result = {}

    def add_result(self, party_acronym, vote_percentage):   # Adds Party acronym and Districts' vote percentages
        self.election_result[party_acronym] = vote_percentage


# ============ Political Party ============
class Party:    # Contains all parties' information
    def __init__(self, party_acronym):
        self.party_acronym = party_acronym
        self.election_result = {}

    def add_result(self, district_name, vote_percentage):   # Adds Districts' names and Parties' vote percentages
        self.election_result[district_name] = vote_percentage


# ============ Data Center ============
class DataCenter:   # Contains the logic of the program
    def __init__(self):
        self.districts_dictionary = {}  # Contains Districts' objects
        self.parties_dictionary = {}    # Contains Parties' objects
        self.ordered_party = []  # Used to take the exact order of Parties when written in data.txt file
        self.values = []  # Contains the selected districts in list box (contains all districts initially)
        self.election_file = None  # File containing elections' data
        self.threshold_value = 0  # Value of threshold (initially 0)
        self.opened_cluster = StringVar()  # Used to tell which clustering is being used

    def read_parse(self):
        district = None  # Used to contain district value
        self.election_file = tkFileDialog.askopenfilename(initialdir="/", title="Choose File",
                                                          filetypes=[("All Files", "*.*")])
        with open(self.election_file, 'r') as e_file:
            for line in e_file:
                if "Kaynak: " in line.strip():
                    district_temp = next(e_file)  # Reads the next line after "Kaynak"
                    district = district_temp[:len(district_temp)-1]
                    self.districts_dictionary[district] = District(district)
                if "%" in line and "BGMSZ" not in line and "Katilim" not in line:  # Gets the acronyms and percentages
                    self.districts_dictionary[district].add_result(line.split()[0], line.split()[len(line.split())-1])
                    self.parties_dictionary[line.split()[0]] = Party(line.split()[0])
            for d in self.districts_dictionary:
                for p in self.parties_dictionary:
                    if p in self.districts_dictionary[d].election_result:
                        self.parties_dictionary[p].add_result(d, self.districts_dictionary[d].election_result[p])
        for dis in self.districts_dictionary:
            self.values.append(dis)

    def writer(self, canvas, row, column, dictionary):  # Writes collected information in a data file (data.txt)
        self.ordered = []   # Row = The row that should be written when clustering (ex. Write parties in row when
        with open('data.txt', 'w') as self.out:  # districts clustering is selected)  Column = Similar to Row's logic
            for i in row:
                self.out.write('\t%s' % i)
                self.ordered.append(i)
            self.out.write('\n')
            for j in column:    
                self.out.write(j, )
                for p in self.ordered:
                    try:
                        percentage = dictionary[j].election_result[p]
                        if (percentage[1:len(percentage)]) >= self.threshold_value:
                            self.out.write('\t%s' % float(percentage[1:len(percentage)]))
                        else:
                            self.out.write('\t0', )
                    except KeyError:
                        self.out.write('\t0', )
                self.out.write('\n')
        self.clustering(canvas)

    def clustering(self, canvas):  # Clusters District or Parties
        columns, rows, percentages = clusters.readfile('data.txt')
        clust = clusters.hcluster(percentages, distance=clusters.sim_distance)
        clusters.drawdendrogram(clust, columns, jpeg='cl.jpg')
        img = ImageTk.PhotoImage(Image.open("cl.jpg"))
        canvas.create_image(20, 20, anchor=NW, image=img)
        canvas.image = img

    def packing_widgets(self, d, s_v, s_h, dis_l, l_b, l_s, thr_l, t, r):  # Packs widgets after button is clicked
        district_list = []                                                 # d = Display (canvas)
        d.pack(side=LEFT)                                                  # s_v = Vertical scrollbar
        s_v.configure(command=d.yview, orient=VERTICAL)                    # s_h = Horizontal Scrollbar
        s_h.configure(command=d.xview, orient=HORIZONTAL)                  # dis_l = "Districts" Label
        l_s.configure(command=l_b.yview, orient=VERTICAL)                  # l_b = List box
        s_v.pack(fill=Y, expand=True, side=LEFT)                           # l_s = List box scrollbar
        s_h.pack(fill=X, expand=True)                                      # thr_l = Threshold Label
        for w in (dis_l, l_b, l_s, thr_l, t, r): w.pack(side=LEFT, padx=1)  # t = Threshold
        l_s.pack(fill=Y)                                                    # r = Refine button
        l_b.delete(0, END)
        for d in self.districts_dictionary:
            district_list.append(d)
        district_list.sort()
        for d in district_list:
            l_b.insert(END, d)

    def cluster_districts(self, display, scroll_ver, scroll_hor, label_1, list_box, scroll, label_2, threshold, refine):
        self.packing_widgets(display, scroll_ver, scroll_hor, label_1, list_box, scroll, label_2, threshold, refine)
        self.writer(display, self.parties_dictionary, self.values, self.districts_dictionary)
        self.opened_cluster.set("D")    # Sets the clustering to District

    def cluster_party(self, display, scroll_ver, scroll_hor, label_1, list_box, scroll, label_2, threshold, refine):
        self.packing_widgets(display, scroll_ver, scroll_hor, label_1, list_box, scroll, label_2, threshold, refine)
        self.writer(display, self.values, self.parties_dictionary, self.parties_dictionary)
        self.opened_cluster.set("P")  # Sets the clustering to Party

    def refine(self, list_box, threshold, canvas):  # Re-updates applied settings
        self.values = [list_box.get(idx) for idx in list_box.curselection()]
        if len(self.values) == 0:
            for dis in self.districts_dictionary:
                self.values.append(dis)
        self.threshold_value = float(threshold.get()[:len(threshold.get())-1])
        if self.opened_cluster.get() == "D":  # Clusters districts when variable D
            self.writer(canvas, self.parties_dictionary, self.values, self.districts_dictionary)
        elif self.opened_cluster.get() == "P":  # Clusters parties when variable P
            self.writer(canvas, self.values, self.parties_dictionary, self.parties_dictionary)


def main():  # Tkinter window
    root = Tk()
    root.title("Clustering")
    root.geometry('850x650')
    app = GUI(root)
    root.mainloop()


main()
