# Sources
# https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
# https://texthandler.com/info/remove-line-breaks-python/
# https://stackoverflow.com/questions/11768070/transform-url-string-into-normal-string-in-python-20-to-space-etc
from Tkinter import *
import urllib2
from bs4 import BeautifulSoup
import docclass


# =========== GUI ===========
class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        predictor = Predictor()  # Predictor Object
        self.banner = Label(self, text="PI Estimator Tool for SEHIR CS Projects", font='Arial 17 bold',
                            bg="light sea green", fg='White')
        self.url_input_1 = Entry(self, width=120)
        self.url_input_2 = Entry(self, width=120)
        self.fetch_button = Button(self, text="Fetch", width=10, font="Arial 10 bold", command=lambda:
                            predictor.fetch_member(self.url_input_1, self.url_input_2, self.projects, self.professor))
        self.pre_pro_frame = Frame(self)
        self.prediction_frame = Frame(self.pre_pro_frame)  # Contains the prediction label and the predicted data
        self.projects_frame = Frame(self.pre_pro_frame)   # Contains the project's listbox, scrollbar, and label
        self.listbox_scrollbar_frame = Frame(self.projects_frame)   # Contains the listbox and its scrollbar
        self.projects_label = Label(self.projects_frame, text="Projects", font='Arial 17 bold')
        self.prediction_label = Label(self.prediction_frame, text="Prediction", font='Arial 17 bold')
        self.projects = Listbox(self.listbox_scrollbar_frame, width=100, height=10, selectmode=SINGLE)
        self.professor = Label(self.prediction_frame, font='Arial 17 bold', bg="green",
                               fg='black')
        self.scrollbar = Scrollbar(self.listbox_scrollbar_frame, command=self.projects.yview, orient="vertical")
        self.projects.configure(yscrollcommand=self.scrollbar.set)
        self.packing()

    def packing(self):
        for x in (self, self.banner): x.pack(fill=X)    # Main frame and banner
        self.url_input_1.pack(pady=10)
        self.url_input_2.pack()
        self.fetch_button.pack(pady=15, expand=True)
        self.pre_pro_frame.pack(anchor=W)
        self.projects_frame.pack(side=LEFT, padx=35, anchor=N)
        for x in (self.projects_label, self.listbox_scrollbar_frame): x.pack()  # Listbox and its scrollbar
        self.projects.pack(side=LEFT)
        self.scrollbar.pack(side=LEFT, fill=Y)
        self.prediction_frame.pack()
        self.prediction_label.pack(padx=50)
        self.url_input_1.insert(END, "\t\t\t\t\t\thttp://cs.sehir.edu.tr/en/people/")   # Sets default url
        self.url_input_2.insert(END, "\t\t\t\t\t\thttp://cs.sehir.edu.tr/en/research/")  # Sets default url


# =========== Faculty Members ===========
class FacultyMember:
    def __init__(self, name, profile_url):
        self.name = name    # Prof name
        self.profile_url = profile_url
        self.publications = []


# =========== Research Projects ===========
class ResearchProject:
    def __init__(self, title, summary, pi_name):
        self.title = title
        self.summary = summary
        self.pi_name = pi_name  # Principle Investigator


# =========== Predictor ===========
class Predictor:
    def __init__(self):
        self.faculty_members = {}   # Contains Prof and their objects
        self.projects = {}  # Contains Projects and their objects

    def fetch_member(self, url_1, url_2, listbox, label):  # URL 1 contains the Profs profiles URL 2 their publications
        url = url_1.get().strip()
        content = urllib2.urlopen(url)
        soup = BeautifulSoup(content, "html.parser")
        link_profile = []
        for html in soup.find_all('div', {"class": "member"}):
            for link in html.find_all('a'):
                if "/en/profile" in link.get('href') and "http://cs.sehir.edu.tr"+ link.get('href') not in link_profile:
                    link_profile.append("http://cs.sehir.edu.tr" + link.get("href"))
        self.fetch_publications(link_profile)
        self.fetch_projects(url_2.get().strip(), listbox, label)

    def fetch_publications(self, link_profile): # Takes a list of profile links
        for profile in link_profile:    # Opens Each prof profile link
            content = urllib2.urlopen(profile)
            soup = BeautifulSoup(content, "html.parser")
            for html in soup.find_all("section", {"id": "profile"}):    # Finds Names of Profs
                for name in html.find('h3'):
                    # Gets Fullname without middle name
                    full_name = name.strip().split()[0] + ' ' + name.strip().split()[len(name.strip().split()) - 1]
                    self.faculty_members[full_name] = FacultyMember(full_name, profile)
            for html in soup.find_all("div", {"id": "flat"}):   # Finds Profs' publications
                for pub in html.find_all("li"):
                    for prof in self.faculty_members.values():
                        if prof.profile_url == profile:
                            publications = pub.text.strip().replace("\n", '')   # Gets rid of new lines and whitespace
                            prof.publications.append(publications[3:len(publications)].strip())

    def fetch_projects(self, url, listbox, label):
        titles = []  # Contains titles of projects in an ordered matter
        pi_list = []    # Contains Principle Investigators in an ordered matter
        summary_list = []   # Contains summaries in an ordered matter
        url = urllib2.urlopen(url)  # Opens URL 2
        soup = BeautifulSoup(url, "html.parser")
        for html in soup.find_all('li', {"class": "list-group-item"}):
            for title in html.find_all("h4", {"class": "bold"}):  # Finds title
                titles.append(title.text.strip())
            for pi in html.find_all("a"):   # Finds Investigator
                if pi.get("href") is not None:
                    principal = urllib2.unquote(pi.get("href"))
                    pi_list.append(principal[11:len(principal)-1].replace('-', " "))
            for summary in html.find_all("p", {"class", "gap"}):    # Finds Summary
                summary_list.append(summary.text.strip())
        temp_pro_dic = {}
        for index in range(21): # Puts the collected data to a dictionary
            temp_pro_dic[titles[index]] = ResearchProject(titles[index], summary_list[index], pi_list[index])
        for title, obj in temp_pro_dic.items():  # Gets rid of ex-faculty members
            if obj.pi_name in self.faculty_members:
                self.projects[title] = obj
        titles.sort()
        for t in titles:    # Inserts titles to the listbox
            if t in self.projects:
                listbox.insert(END, t)
        self.predict_pi(listbox, self.train_classifier(), label)

    def train_classifier(self):  # Trainer
        naive_obj = docclass.naivebayes(docclass.getwords)  # Creates Naive Object
        for prof, pub in self.faculty_members.items():
            for publication in pub.publications:
                naive_obj.train(publication, prof)  # Trains the object with the pubication and professor
        return naive_obj

    def predict_pi(self, listbox, naive, label):
        def get_selected(event):  # Runs when user
            predicted_pi = ""   # The predicted Professor
            for pro in self.projects:
                if pro == listbox.get(listbox.curselection()):
                    predicted_pi = naive.classify(pro + self.projects[pro].summary)
            for pro in self.projects.values():
                if pro.title == listbox.get(listbox.curselection()) and pro.pi_name == predicted_pi:
                    label.configure(text=pro.pi_name, bg='green')   # Turns the label green when pred is correct
                    label.pack(pady=70)
                elif pro.title == listbox.get(listbox.curselection()) and pro.pi_name != predicted_pi:
                    label.configure(text=predicted_pi, bg='red')    # Turns the label red when the pred is incorrect
                    label.pack(pady=70)
        listbox.bind("<<ListboxSelect>>", get_selected)


# =========== Root ===========
def main():
    root = Tk()
    root.geometry("950x400+100+100")
    root.title("PI Estimator Tool for SEHIR CS Projects")
    app = GUI(root)
    root.mainloop()


main()
