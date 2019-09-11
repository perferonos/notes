"""
This program creates notes in .json format.  It is tested before and works.
Objective:
Change this program to web site and change .json format to normal database.
"""


import datetime
import time
import json
import os.path


class notes():

    path="/home/zoolya/Общедоступные/Python_projects/"
    note=[
{"Note number":0},
    {
        "name":"",
        "theme":"",
        "text":"",
        "time":"",
        "date":""
    },
    {
        "was modified":False,
        "modifications":0
    }
    ]


    def __init__(self):
        date=datetime.datetime.today().strftime("%Y.%m.%d")
        path=self.path+"%s.json" % date # Path to .json file
        if not os.path.isfile(path):
            with open("%s.json" % date, "w") as src_file:
                json.dump([], src_file)


    def make_note(self):
        """ Creates a note. Gets a name, a theme of note and the text. Marks the date. Saves the note as .json.
        """

        num=-1

        self.note[1]["date"]=datetime.datetime.today().strftime("%Y.%m.%d")

        self.note[1]["time"]=datetime.datetime.today().strftime("%H.%M.%S")

        with open("%s.json" % self.note[1]["date"], "r") as src_file:
            src_data=json.load(src_file)

        if src_data!=[]:
            length=len(src_data)
            if len!=0:
                num=src_data[length-1][0]["Note number"]

        self.note[0]["Note number"]=num+1

        print("Enter your name: ")
        self.note[1]["name"]=str(input())

        print("Enter the theme: ")
        self.note[1]["theme"]=str(input())

        print("Enter the text: ")
        self.note[1]["text"]=str(input())

        with open("%s.json" % self.note[1]["date"], "w") as note_file:
            src_data.append(self.note)
            json.dump(src_data, note_file, indent=4)


    def show_some_last(self, number, filename):
        """ Opens .json file and shows a defined number of last notes. 
        If input data is incorrect, throws error.
        """

        with open(filename, "r") as src_file:
            src_data=json.load(src_file)
        
        data_to_red=[]

        try:
            if number>len(src_data):
                raise ValueError()
            for i in range(len(src_data)-1, len(src_data)-1-number, -1):
                self._show_note(i, src_data)
                data_to_red.append(src_data[i])
            self._redact_after_output(data_to_red, filename)
        except ValueError:
            print("Incorrect number! There is less notes than you've entered!")


    def show_some_last_from_user(self, number, user, filename):
        """ Opens .json file and shows a defined number of last notes of defined user. 
        If input data is incorrect, throws error.
        """

        with open(filename, "r") as src_file:
            src_data=json.load(src_file)
        
        flag=False
        count=0
        data_to_red=[]

        try:
            for i in range(0, len(src_data)-1):
                if  user==src_data[i][1]["name"]:
                    flag=True
                    count+=1

            if flag==False:
                raise KeyError()

            if number>len(src_data):
                raise NameError()

            if number>count:
                raise ValueError()

            i=0
            while i<len(src_data) and number>0:
                if src_data[i][1]["name"]==user:
                    self._show_note(i, src_data)
                    data_to_red.append(src_data[i])
                    number-=1
                i+=1
            self._redact_after_output(data_to_red, filename)

        except NameError:
            print("Incorrect number! There is less notes than you've entered!")
        except KeyError:
            print("Incorrect username! There is no user with such name!")
        except ValueError:
            print("Incorrect number! There is less messages from this user, than your number!")


    def show_from_date(self, usr_date):
        """ Shows all messages from defined date to today's date. 
        If the date is later than today's, throws error.
        """

        try:
            usr_date=datetime.datetime.strptime(usr_date, "%Y.%m.%d")
            notes_date=[]

            for iter_date in self._set_date_range(usr_date):
                iterator="%s.json" % datetime.datetime.strftime(iter_date, "%Y.%m.%d")
                path=self.path+iterator
                if os.path.isfile(path):
                    self.show_all(iterator)
                    with open(iterator, "r") as src_file:
                        src_data=json.load(src_file)
                    for i in range(0, len(src_data)):
                        notes_date.append(src_data[i])
            self.redact_note()

        except ValueError:
            print("Invalid date! Type the date in format: yyyy.mm.dd! Example: 2015.03.20")


    def _set_date_range(self, start):
        """ Creates a generator of date range.
        """
        try:
            date_end=datetime.datetime.today()
            if start>date_end:
                raise ValueError()
            for n in range(int((date_end-start).days)+1):
                yield start+datetime.timedelta(n)
        except ValueError:
            print("Invalid date! Your date is later than today's!")


    def show_all(self, filename):
        """ Shows all notes of defined file.
        """
        with open(filename, "r") as src_file:
            src_data=json.load(src_file)
        
        for i in range(0, len(src_data)):
            self._show_note(i, src_data)


    def redact_note(self):
        """ Allows user to redact the name, theme and text fields with 
        function _redact_after_output. 
        Changes variables: modifications and was_modified in case of changing.
        """
        try:
            print("-"*40)
            print("Do you want to redact the notes? Press [y/n]")
            answer=input()

            if answer=="n":
                return

            elif answer!="y":
                raise ValueError()

            else:
                print("-"*40)
                print("Type the date of the note. [yyyy.mm.dd]")
                answer=str(input())

                if not datetime.datetime.strptime(answer, "%Y.%m.%d"):
                    raise ValueError()

                elif not os.path.isfile(self.path+"%s.json" % answer):
                    raise NameError()

                else:
                    filename="%s.json" % answer
                    with open(filename, "r") as src_file:
                        src_data=json.load(src_file)
                    self._redact_after_output(src_data, filename)
        except ValueError:
            print("-"*40)
            print("Invalid answer! Type only the answers in description.")
        except NameError:
            print("-"*40)
            print("There is no such file!")


    def _redact_data(self, num, key, filename):
        """ Changes the value of the chosen key and inputs it into the file.
        """

        with open(filename, "r") as src_file:
            src_data=json.load(src_file)

        print("Type the changed data.")
        change=str(input())

        for j in range(0, len(src_data)):
            if src_data[j][0]["Note number"]==num:

                modifications=abs(len(change)-len(src_data[j][1][key]))

                i=0
                while i<len(change) and i<len(src_data[j][1][key]):
                    if change[i]!=src_data[j][1][key][i]:
                        modifications+=1
                    i+=1

                src_data[j][1][key]=change
                src_data[j][2]["modifications"]=modifications
                src_data[j][2]["was modified"]=True

                with open(filename, "w") as note_file:
                    json.dump(src_data, note_file, indent=4)

                break


    def _note_delete(self, num, filename):
        """ Deletes the note. Numeration does not recounts!
        """
        with open(filename, "r") as src_file:
            src_data=json.load(src_file)

        for j in range(0, len(src_data)):
            if src_data[j][0]["Note number"]==num:

                src_data.pop(j)

                with open(filename, "w") as note_file:
                    json.dump(src_data, note_file, indent=4)

                break


    def _redact_after_output(self, notes, filename):
        """ Allows user to redact the name, theme and text fields 
        with functions _node_delete and _redact_data. 
        Changes variables modifications and was_modified 
        in case of changing.
        """

        try:
            print("-"*40)
            print("Do you want to redact these notes? Press [y/n]")
            answer=input()

            if answer=="n":
                return

            elif answer!="y":
                raise ValueError()

            else:
                for i in range(0, len(notes)):
                    self._show_note(i, notes)
                length=len(notes)

                if length==0:
                    raise EOFError()

                else:
                    numbers=[]
                    for i in range(length):
                        numbers.append(notes[i][0]["Note number"])

                    print("-"*40)
                    print("Which note do you want to choose? Type the number of note.")
                    answer=int(input())

                    if answer not in numbers:
                        raise OverflowError()

                    else:
                        for i in range(length):
                            if notes[i][0]["Note number"]==answer:
                                self._show_note(i, notes)
                        num=answer

                        print("-"*40)
                        print("What do you want to do with this node? Redact: [name/theme/text]. Delete: [del]")
                        answer=input()

                        if answer=="name" or answer=="theme" or answer=="text":
                            self._redact_data(num, answer, filename)

                        elif answer=="del":
                            self._note_delete(num, filename)

                        else:
                            raise ValueError()

        except ValueError:
            print("-"*40)
            print("Invalid answer! Type only the answers in description.")
        except EOFError:
            print("-"*40)
            print("This file is empty!")
        except OverflowError:
            print("-"*40)
            print("A note with such number does not exist!")


    def _show_note(self, iter, notes):
        """ Outputs note without text.
        """
        print("-"*40)
        print("Note number: ", notes[iter][0]["Note number"])
        print("name: ", notes[iter][1]["name"])
        print("theme: ", notes[iter][1]["theme"])
        print("date: ", notes[iter][1]["date"])
        print("time: ", notes[iter][1]["time"])
        print("-"*40)


check=notes()
#check.make_note()
#check.show_some_last(2, "2019.03.28.json")
#check.show_some_last_from_user(1, "name 1", "2019.03.28.json")
#check.show_from_date("2019.03.27")
#check._redact_data(1,"name","2019.03.27.json")
#check._note_delete(5,"2019.03.27.json")
#check.redact_note()
