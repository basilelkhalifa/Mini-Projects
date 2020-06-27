# Sources
# https://stackoverflow.com/questions/209840/convert-two-lists-into-a-dictionary-in-python

from Tkinter import *
import mysearchengine
from bs4 import BeautifulSoup
import urllib2
import ttk


# =========== GUI Class ===========
class Gui(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        search = Searcher()
        self.banner = Label(self, text='Classroom Finder', font='Arial 15 bold', bg='blue', fg='White')
        self.url_frame = Frame(self)
        self.url_label = Label(self.url_frame, text="Url: ")
        self.url_input = Entry(self.url_frame, width=120)
        self.fetch_frame = Frame(self)
        self.fetch_statues = Label(self.fetch_frame, bg='red', width=10)
        self.fetch_button = Button(self.fetch_frame, text="Fetch", width=10, height=2, command=lambda: search.fetch(
            self.url_input.get(), self.fetch_statues, self.where_i_entry, self.room_entry, self.start_entry,
            self.end_entry, self.day_entry))
        self.filters_label = Label(self, text="Filters", bg="blue", fg="white", font="Arial 15 bold")
        self.filters_frame = Frame(self, relief=GROOVE, borderwidth=2)
        self.text_frame = Frame(self.filters_frame)
        self.where_i = Label(self.text_frame, text="Where am I?")
        self.room = Label(self.text_frame, text="Room")
        self.start = Label(self.text_frame, text="Start")
        self.day = Label(self.text_frame, text="Day")
        self.search_button = Button(self.text_frame, text="Search", width=8, command=lambda: search.search(
            self.where_i_entry, self.room_entry, self.start_entry, self.end_entry, self.day_entry, self.table))
        self.entry_frame = Frame(self.filters_frame)
        self.end_start_frame = Frame(self.entry_frame)
        self.where_i_entry = ttk.Combobox(self.entry_frame)
        self.room_entry = ttk.Combobox(self.entry_frame)
        self.start_entry = ttk.Combobox(self.end_start_frame, width=10)
        self.day_entry = ttk.Combobox(self.entry_frame)
        self.end = Label(self.end_start_frame, text="End")
        self.end_entry = ttk.Combobox(self.end_start_frame, width=10)
        self.class_result_frame = Frame(self.filters_frame, relief=GROOVE, borderwidth=2)
        self.class_result_banner = Label(self.class_result_frame, text="Classroom results", font="Arial 8 bold",
                                         bg='dim gray', fg='White')
        self.table_frame = Frame(self.class_result_frame)
        self.table = ttk.Treeview(self.table_frame, columns=("Rooms", "Traffic", "Availability", "Closeness",
                                                             "Overall Score"), show="headings", height=12)
        self.table.heading("Rooms", text="Room")
        self.table.column("Rooms", width=85)
        self.table.heading("Traffic", text="Traffic")
        self.table.column("Traffic", width=90)
        self.table.heading("Availability", text='Availability %')
        self.table.column("Availability", width=100)
        self.table.heading("Closeness", text="Closeness")
        self.table.column("Closeness", width=100)
        self.table.heading("Overall Score", text="Overall Score")
        self.table.column("Overall Score", width=100)
        self.scrollbar = Scrollbar(self.table_frame, command=self.table.yview, orient="vertical")
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.packing()

    # =========== Method that packs widgets ===========
    def packing(self):
        self.pack(fill=BOTH, expand=True)
        self.banner.pack(fill=X)
        self.url_frame.pack(pady=17)
        self.fetch_frame.pack(anchor=E, padx=25, pady=10)
        self.filters_label.pack(anchor=W, padx=5, pady=10)
        self.filters_frame.pack(anchor=W, padx=10, fill=Y, expand=True)
        self.text_frame.pack(side=LEFT, padx=15, anchor=NW)
        self.entry_frame.pack(side=LEFT, anchor=N, padx=30)
        self.start_entry.pack(side=LEFT)
        self.end.pack(side=LEFT, padx=30)
        self.end_entry.pack(side=LEFT)
        self.class_result_frame.pack(side=LEFT, anchor=NE)
        self.class_result_banner.pack(fill=X)
        self.table_frame.pack(pady=8, padx=8)
        self.table.pack(side=LEFT)
        self.scrollbar.pack(side=LEFT, fill=Y)
        for e in (self.where_i_entry, self.room_entry, self.end_start_frame, self.day_entry): e.pack(anchor=W, pady=13)
        for l in (self.where_i, self.room, self.start, self.day, self.search_button): l.pack(anchor=NW, pady=13)
        self.search_button.pack(padx=5)
        for w in (self.url_label, self.url_input): w.pack(side=LEFT, padx=5)
        for w in (self.fetch_button, self.fetch_statues): w.pack(side=RIGHT, padx=5)


# =========== Classroom Class ===========

class Classroom:
    def __init__(self, building_number, floor_number, room_number):
        self.building_number = building_number
        self.floor_number = floor_number
        self.room_number = room_number
        self.traffic_score = {}  # Key = classroom, value = score

    def get_distance_from(self, another_classroom_object):  # Gets the distance between two classroom objects
        b = abs((int(another_classroom_object.building_number) - int(self.building_number))) * 100
        f = abs((int(another_classroom_object.floor_number) - int(self.floor_number))) * 200
        r = abs((int(another_classroom_object.room_number[2:4]) - int(self.room_number[2:4]))) * 50
        closeness_value = b + f + r
        if closeness_value == 0:
            closeness_value = 100
        return closeness_value


# =========== Building Class ===========
class Building:
    def __init__(self, name):
        self.name = name
        self.classroom_objects = []  # Contains all classroom objects


# =========== Day Class ===========
class Day:
    def __init__(self, name):
        self.name = name
        self.time_slots = {}  # Contains classrooms empty for the day


# =========== Search Reusult Item Class ===========
class SearchResultItem:
    def __init__(self, classroom, closeness_score):
        self.classroom = classroom
        self.availability = 0  # Holds availability score
        self.closeness_score = closeness_score
        self.available_slots = []

    def compute_availability_scores(self, selected_start, selected_end):    # Computes Available score
        minutes = (int(selected_end.split(":")[0]) - int(selected_start.split(":")[0])) * 60
        selected_start_hour = int(selected_start.split(":")[0])
        selected_end_hour = int(selected_end.split(":")[0])
        # ========= Block of code that checks when a class is avaialable ==========
        if len(self.available_slots) == 1 and '09:00-19:00' == self.available_slots[0]:  # Empty class on selected day
            self.availability = 100
        elif len(self.available_slots) == 1:  # Checks when class is empty
            first_hour_class = self.available_slots[0].split("-")[0].split(":")[0]
            second_hour_class = self.available_slots[0].split("-")[1].split(":")[0]
            if selected_start_hour <= int(first_hour_class) and \
                    selected_end_hour >= int(second_hour_class):    # Checks if time interval has free time
                minutes_class = (int(second_hour_class) - int(first_hour_class)) * 60
                self.availability = (minutes_class / float(minutes)) * 100
            elif selected_start_hour < int(first_hour_class) and selected_end_hour <= int(second_hour_class):
                minutes_class = (selected_end_hour - int(first_hour_class)) * 60
                percent = (minutes_class / float(minutes)) * 100
                if percent > 100:
                    percent = 100
                self.availability = int(percent)
            elif selected_start_hour >= int(first_hour_class) and selected_end_hour <= int(second_hour_class):
                minutes_class = (selected_end_hour - int(first_hour_class)) * 60
                percent = (minutes_class / float(minutes)) * 100
                if percent > 100:
                    percent = 100
                self.availability = int(percent)
            else:   # Sets availability to 100 if class empty
                self.availability = 100
        elif len(self.available_slots) == 2:  # Checks when class is empty
            item_1_first_hour = int(self.available_slots[0].split("-")[0].split(":")[0])
            item_1_second_hour = int(self.available_slots[0].split("-")[1].split(":")[0])
            item_2_first_hour = int(self.available_slots[1].split("-")[0].split(":")[0])
            item_2_second_hour = int(self.available_slots[1].split("-")[1].split(":")[0])
            if selected_start_hour <= item_1_first_hour and selected_end_hour >= item_2_second_hour:
                minutes_class = ((item_1_second_hour - item_1_first_hour) + (
                        item_2_second_hour - item_2_first_hour)) * 60
                self.availability = (float(minutes_class) / minutes) * 100
            elif selected_start_hour <= item_1_first_hour and item_1_second_hour <= selected_end_hour < item_2_first_hour:
                minutes_class = (selected_end_hour - item_1_first_hour) * 60
                percent = (float(minutes_class) / minutes) * 100
                if percent > 100:
                    percent = 100
                self.availability = percent
            elif item_2_second_hour < selected_start_hour <= item_2_first_hour and selected_end_hour >= item_2_second_hour:
                self.availability = 100
        else:
            self.availability = 100


# =========== Searcher Class ===========
class Searcher:
    def __init__(self):
        self.parsed_info = {}   # Contains all data from the url
        self.buildings_objects = {}     # Contains building names and their objects
        self.rooms = []  # Contains the used rooms by courses
        self.days = {}  # Contains days of the week
        self.time = []  # Contains the time intervals (9-19)
        self.search_results_items = []   # Contains all the search items result objects
        self.overall_scores = {}    # Contains the overall score for each classroom

    def fetch(self, url, statues, where_am_i, room_entry, start, end, day_entry):   # Collects data off given url
        try:    # Controls color of statues
            statues.configure(bg='yellow')
            statues.update_idletasks()
            urllib2.urlopen(url).read()
        except: # Changes statues back to red if an error occurs
            statues.configure(bg='red')
        website = urllib2.urlopen(url).read()
        soup = BeautifulSoup(website, "html.parser")
        temp = {}
        temp_2 = {}
        # ======= Block of code that contains the table data in html
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            temp[tds[0].text] = [tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text]
        for i in temp:
            for building in ("ACAD BUILD 1", "ACAD BUILD 2", "ACAD BUILD 3", "ACAD BUILD 4", "ACAD BUILD 5",
                             "ACAD BUILD 6", "ACAD BUILD 7"):
                if building in temp[i][3]:
                    temp_2[i] = temp[i]
        statues.configure(bg='green')
        # ====== Block of code that parses the collected html
        for c in temp_2:
            day = temp_2[c][1].split()
            time = temp_2[c][2].split()
            if len(time) == 1:
                time.append(time[0])
            buildings_rooms = temp_2[c][3].split("#")
            temp = dict(zip(day, time))
            temp[buildings_rooms[0]] = buildings_rooms[1]
            temp[temp_2[c][0]] = temp_2[c][4]
            self.parsed_info[c] = temp
        classes_temp = []
        for course in self.parsed_info:
            for x in self.parsed_info[course]:
                if "ACAD BUILD" in x:
                    self.buildings_objects[x] = Building(x)
                    classes_temp.append(self.parsed_info[course][x])
        building_temp = []
        for building in self.buildings_objects.values():
            building_temp.append(building.name)
            for room in classes_temp:
                if "ACAD BUILD" in room:
                    classes_temp.remove(room)
                if room[0] in building.name:
                    building.classroom_objects.append(Classroom(room[0].split()[0], room[1], room))
            building.classroom_objects.sort()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for i in days:
            self.days[i] = (Day(i))
        for t in range(9, 20):
            self.time.append(str(t) + ":00")
        start.configure(values=self.time)
        start.current(0)
        end.configure(values=self.time)
        end.current(10)
        building_temp.sort()

        def rooms_of_chosen_building(event):    # Function called when user changes building selection (Combobox Bind)
            classes_temp = []
            room_entry.configure(values=[])
            room_entry.delete(0, END)
            for x in self.buildings_objects:
                if x == where_am_i.get():
                    values = self.buildings_objects[x].classroom_objects
                    for r in values:
                        if r.room_number[1:4] not in classes_temp:
                            classes_temp.append(r.room_number[1:4])
                        classes_temp.sort()
                    room_entry.configure(values=classes_temp)
                    room_entry.current(0)

        where_am_i.bind("<<ComboboxSelected>>", rooms_of_chosen_building)   # Binds the buildings to rooms
        where_am_i.configure(values=building_temp)
        where_am_i.current(0)
        rooms_of_chosen_building(None)
        day_entry.configure(values=days)
        day_entry.current(0)
        classes_temp.sort()

        for x in classes_temp:
            if x not in self.rooms:
                r = x.split()
                self.rooms.append(r[0])

        self.compute_traffic_scores()

    def compute_availability(self, start_time, end_time, day):  # Computes available time in each class and availability
        selected_start_time = start_time.get()                  # scores
        selected_end_time = end_time.get()
        selected_day = day.get()
        no_class_hours = {}
        # ========= Block of code that determines when the class is empty and adds it to the avaialability_slots
        for cla in self.classes_time:
            no_class_hours[cla] = []
            for day in self.classes_time[cla]:
                if day == selected_day and len(self.classes_time[cla][day]) > 1:
                    for hour_class in range(len(self.classes_time[cla][day]) - 1):
                        first_hour_split = self.classes_time[cla][day][hour_class].split("-")[1]
                        second_hour_split = self.classes_time[cla][day][hour_class + 1].split("-")[0]
                        if first_hour_split != second_hour_split:
                            no_class_hour = first_hour_split + "-" + second_hour_split
                            no_class_hours[cla].append(no_class_hour)
                elif day == selected_day and len(self.classes_time[cla][day]) == 0:
                    no_class_hours[cla].append("09:00-19:00")
                elif day == selected_day and len(self.classes_time[cla][day]) == 1:
                    first_hour = self.classes_time[cla][day][0].split("-")[0]
                    second_hour = self.classes_time[cla][day][0].split("-")[1]
                    no_class_hours[cla].append('09:00-' + first_hour)
                    no_class_hours[cla].append(second_hour + "-19:00")
                if day == selected_day and len(no_class_hours[cla]) == 0:
                    first_hour = self.classes_time[cla][day][0].split("-")[0]
                    second_hour = self.classes_time[cla][day][len(self.classes_time[cla][day]) - 1].split("-")[1]
                    if first_hour != "9:00":
                        no_class_hours[cla].append("09:00-" + first_hour)
                    no_class_hours[cla].append(second_hour + "-19:00")
        # ==== Block of code that gets the available scores
        for cla, hour_list in no_class_hours.items():
            if len(hour_list) > 0 and "09:00" not in hour_list[0]:
                morning_no_class = "09:00-" + hour_list[0].split('-')[0]
                hour_list.insert(0, morning_no_class)
            if len(hour_list) > 0 and "19:00" not in hour_list[len(hour_list) - 1]:
                afternoon_no_class = hour_list[len(hour_list) - 1].split('-')[1] + "-19:00"
                hour_list.insert(len(hour_list), afternoon_no_class)
        for cla in no_class_hours:
            if "09:00-09:00" in no_class_hours[cla]:
                no_class_hours[cla].pop(0)
            for result in self.search_results_items:
                if result.classroom == cla:
                    for time_interval in no_class_hours[cla]:
                        result.available_slots.append(time_interval)
        for result in self.search_results_items:  # removes 21:00 from list
            if result.classroom == "3001" or "7029":
                for time_interval in result.available_slots:
                    if "21:00" in time_interval:
                        result.available_slots.pop(len(result.available_slots) - 1)
        normalizer = {}  # Contains normalized scores
        for result in self.search_results_items:
            result.compute_availability_scores(selected_start_time, selected_end_time)
            normalizer[result.classroom] = result.availability
        normalized = mysearchengine.normalizescores(normalizer)  # Normalizes the scores
        for cla, score in normalized.items():
            for result in self.search_results_items:
                if cla == result.classroom:
                    result.availability = abs(round(score, 4))

    def compute_traffic_scores(self):   # Computes traffic scores
        self.classes_time = {}  # contains class num as key and time of use as its value
        for r in self.rooms:
            time = {}
            for d in self.days:
                time[d] = []
            for course in self.parsed_info.values():
                if r in course.values():
                    for x in course:
                        if x in self.days and course[x] not in time[x]:
                            time[x].append(course[x])
            self.classes_time[r] = time
        # ==== Removes time after 19:00
        for day in self.classes_time.values():
            for time in day.values():
                time.sort()
                for hour in time:
                    if hour >= "19:00-24:00":
                        time.remove(hour)
        # ==== Block of code that computes the traffic scores
        classes_traffic_num = {}  # contains class num as key and its traffic num
        for cla in self.classes_time:
            day_hour = {}
            for d in self.days:
                day_hour[d] = 0
            for day in self.classes_time[cla]:
                for time in self.classes_time[cla][day]:
                    uncut_time = time.split('-')
                    start_hour = uncut_time[0].split(":")[0]
                    end_hour = uncut_time[1].split(":")[0]
                    difference_hours = int(end_hour) - int(start_hour)
                    sum_hours = day_hour[day] + difference_hours
                    day_hour[day] = sum_hours
            classes_traffic_num[cla] = day_hour
        for cla, day_time in classes_traffic_num.items():
            for day in day_time:
                if day_time[day] == 0:
                    day_time[day] = 0.1
                traffic_num = day_time[day] / (19.0 - 9.0)
                day_time[day] = traffic_num
            normalized_dict = mysearchengine.normalizescores(day_time)
            for x in normalized_dict:
                rounded_num = round(normalized_dict[x], 4)
                normalized_dict[x] = rounded_num
            classes_traffic_num[cla] = normalized_dict

        for buildings in self.buildings_objects.values():
            for cla_object in buildings.classroom_objects:
                for cla in classes_traffic_num:
                    if cla in cla_object.room_number:
                        for day in classes_traffic_num[cla]:
                            cla_object.traffic_score[day] = classes_traffic_num[cla][day]  # (updates the classroom
                            # object's traffic score)

    def compute_closeness_scores(self, location, room):     # Computes closeness score
        # ====== Block of code that computes the closeness scores
        chosen_building_num = location.get().split()[2]
        chosen_room = chosen_building_num + room.get()
        closeness = {}
        for building in self.buildings_objects.values():
            for cla_obj in building.classroom_objects:
                if chosen_room == cla_obj.room_number:
                    current_room = cla_obj
        for building in self.buildings_objects.values():
            for cla_obj in building.classroom_objects:
                closeness[cla_obj.room_number] = current_room.get_distance_from(cla_obj)
        normalized_closeness = mysearchengine.normalizescores(closeness)
        for cla, score in normalized_closeness.items():
            self.search_results_items.append(SearchResultItem(cla, round(score, 4)))

    def search(self, location, room, start_time, end_time, selected_day, viewer):
        viewer.delete(*viewer.get_children())
        if int(end_time.get().split(":")[0]) > 19:  # Changes user input to 19:00 if greater than 19:00
            end_time.current(10)
        scores_classrooms = {}  # contains the rooms and the list of their scores
        self.compute_closeness_scores(location, room)
        self.compute_availability(start_time, end_time, selected_day)
        for result in self.search_results_items:    # Gets the availability score and closeness
            self.overall_scores[result.classroom] = result.availability + result.closeness_score
            scores_classrooms[result.classroom] = [result.availability, result.closeness_score]
        for building in self.buildings_objects.values():
            class_in_list = []  # used to prevent repeating rooms
            for cla in building.classroom_objects:
                if selected_day.get() in cla.traffic_score and cla.room_number not in class_in_list:
                    class_in_list.append(cla.room_number)
                    self.overall_scores[cla.room_number] += cla.traffic_score[selected_day.get()]
                    scores_classrooms[cla.room_number].append(cla.traffic_score[selected_day.get()])

        for cla, score in self.overall_scores.items():
            scores_classrooms[cla].append(round(score, 4))


        for cla, score_list in scores_classrooms.items():
            viewer.insert("", END, values=(cla, score_list[2], score_list[0], score_list[1], score_list[3]))


def main():
    root = Tk()
    root.geometry("950x520+100+100")
    app = Gui(root)
    root.mainloop()


main()
