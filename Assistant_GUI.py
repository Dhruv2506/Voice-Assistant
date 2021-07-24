from __future__ import print_function
import time
import emoji
import pyttsx3
from clean_desktop import clean_my_deskstop

start_time = time.time()

from tkinter import *
from threading import Thread
from urllib.request import urlopen
from PIL import Image, ImageTk
import urllib.request

quit_flag = 0


class HyperlinkManager:
    global link

    def __init__(self, text):
        self.text = text

        self.text.tag_config("hyper", foreground="white", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, link1):
        global link
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        link = link1
        # self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        minimize_window()
        Thread(target=lambda: Thread(target=open_link_1).start()).start()


def open_link_1():
    open_link(list_link[0])


def find_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def get_general_path():
    return os.path.join(os.path.join(os.environ['USERPROFILE']))


def quit_code():
    global quit_flag
    quit_flag = 1
    root.destroy()
    quit()


def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


def minimize_window():
    root.overrideredirect(False)
    root.title("Assistant")
    root.wm_state('iconic')
    Thread(target=make_maximized).start()


data_website = []


def data_websites():
    global data_website
    file = open('websites.txt', 'r')
    txt = file.read()
    txt = txt.split('\n')
    for x in txt:
        data_website.append(x)


# function for gif
class ImageLabel(Label):
    """a label that displays images, and plays them if they are gifs"""

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def GUI():
    global messageWindow, chatWindow, canvas, title_bar, photo_button, minimize_button, root
    root = Tk()

    # root override
    root.overrideredirect(True)  # turns off title bar, geometry

    # goemetry of tkinter
    root.geometry('800x550+200+90')  # set new geometry

    # make a frame for the title bar
    title_bar = Frame(root, bg='black', relief='raised', bd=2, width=800, height=40)

    # put a close button on the title bar
    photo_button = PhotoImage(file="close_button.png")
    close_button = Button(title_bar, image=photo_button, command=quit_code, bg="black", highlightthickness=0, bd=0)
    photo_title = PhotoImage(file="title.png")
    label = Label(title_bar, relief="raised", font=("Helvetica", "16"), image=photo_title, bg="black", bd=0)

    photo_minimise = PhotoImage(file="minimize_button.png")
    minimize_button = Button(title_bar, image=photo_minimise, bg="black", highlightthickness=0, bd=0,
                             command=minimize_window)

    lbl = ImageLabel(title_bar, bg="black")
    lbl.pack(side=LEFT)
    lbl.load('logo.gif')

    # pack the widgets
    title_bar.pack(fill=X)
    close_button.pack(side=RIGHT)
    minimize_button.pack(side=RIGHT)

    label.pack()

    # bind title bar motion to the move window function
    title_bar.bind('<B1-Motion>', move_window)

    IMAGE_PATH = 'wallpaper .png'
    WIDTH, HEIGTH = 400, 500

    canvas = Canvas(root, width=WIDTH, height=HEIGTH, bd=-1)
    canvas.pack(side=LEFT)

    # img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((WIDTH, HEIGTH), Image.ANTIALIAS))
    img = ImageLabel(root, bg="black")
    img.place(x=0, y=50)
    img.load('wallpaper' + str(random.randint(1, 11)) + '.gif')

    chatWindow = Text(root, bd=1, width="50", height="8", font=("Comic Sans MS", 15), bg="black")
    chatWindow.place(x=400, y=56, height=500, width=400)

    messageWindow = Text(root, bg="black", width="40", height="4", font=("Arial", 16), foreground="#3a9fbf",
                         borderwidth="0.5")
    messageWindow.place(x=0, y=500, height=50, width=400)
    messageWindow.insert(END, "Type something here...")
    messageWindow.config(insertbackground="#3a9fbf")
    messageWindow.bind('<Button-1>', func_to_remove_type)
    messageWindow.bind('<Return>', retrieve_input1)

    photo = PhotoImage(file="button.png")
    button = Button(messageWindow, image=photo, relief="raised", command=retrieve_input, bg="black", bd=1)
    button.pack(side=RIGHT)

    root.attributes('-topmost', True)
    Thread(target=all_bind).start()
    Thread(target=load_mic_image).start()
    print(time.time() - start_time)

    hour1 = int(datetime.datetime.now().hour)
    time.sleep(0.5)
    if 0 <= hour1 < 12:
        insert_in_chat_window("Good Morning Sir " + emoji.emojize(":grinning_face_with_big_eyes:"))
    elif 12 <= hour1 < 18:
        insert_in_chat_window("Good Afternoon Sir " + emoji.emojize(":grinning_face_with_big_eyes:"))
    else:
        insert_in_chat_window("Good Evening Sir " + emoji.emojize(":grinning_face_with_big_eyes:"))

    insert_in_chat_window("I am Friday. how can i help you?")
    root.mainloop()


def load_mic():
    try:
        global root
        lb2 = ImageLabel(root, bg="black")
        lb2.place(x=400, y=500)
        lb2.load('listening.gif')
    except:
        pass


def load_mic_image():
    try:
        global root
        lb2 = ImageLabel(root, bg="black")
        lb2.place(x=400, y=500)
        lb2.load('mic.png')
    except:
        pass


def import_library1():
    global random, count, sr, wikipedia, webbrowser, Path
    from itertools import count
    import random
    import speech_recognition as sr
    import wikipedia
    import webbrowser
    from pathlib import Path


def import_library2():
    global pytz, imaplib, email, decode_header, shutil, psutil, win32gui, win32con, codecs, datetime
    import datetime
    import pytz
    import imaplib
    import email
    from email.header import decode_header
    import shutil
    import psutil
    import win32gui
    import win32con
    import codecs


def import_library3():
    global requests, BeautifulSoup, urlopen, webdriver, get_close_matches, pickle, build, InstalledAppFlow, Request
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from difflib import get_close_matches
    import pickle
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request


def import_library4():
    global pyautogui, gTTS, playsound, askopenfilename, notification, fnmatch
    import pyautogui
    from gtts import gTTS
    from playsound import playsound
    from tkinter.filedialog import askopenfilename
    from plyer import notification
    import fnmatch


def import_library6():
    global os
    import os


def load_all_library():
    Thread(target=import_library6).start()
    Thread(target=import_library1).start()
    Thread(target=import_library2).start()
    Thread(target=import_library3).start()
    Thread(target=import_library4).start()


# root of tkinter window


total_time = 0
task_add_flag = 0
username = "xxxxx@gmail.com"
password = "xxxxxxx"
count_maps = 0
all_links = []
chrome_path = ""
flag = 0

# chrome path
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# pdf and write mode flag
pdf_mode_flag = 0
write_flag = 0

# data of files in laptop
data = []
data_mp3 = []
data_mp4 = []
data_code = []
data_pdf = []
data_images = []
data_songs = []
data_desktop = []
data_presentation = []


def data_of_pc():
    global data, data_mp3, data_mp4, data_code, data_pdf, data_images, data_songs, data_desktop, data_presentation

    data_videos = os.listdir("C://Users//patel//videos")
    data += data_videos

    data_desktop = os.listdir("C://Users//patel//OneDrive//Desktop")
    data += data_desktop

    data_pdf = os.listdir("C://Users//patel//OneDrive//Desktop//Files//PDF")
    data += data_pdf

    data_mp3 = os.listdir("C://Users//patel//OneDrive//Desktop//Files//MP3")
    data += data_mp3

    data_presentation = os.listdir("C://Users//patel//OneDrive//Desktop//Files//PRESENTATION")
    data += data_presentation



def get_best_response_func4():
    time.sleep(4)
    global driver
    start_time = time.time()
    query = 'black widow release date'
    driver.get('https://www.google.com/search?q=' + query)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    ans1 = soup.find_all('div', attrs={"role": "heading"})

    k_heading = 0

    for x in ans1:
        print(x.text)
        k_heading += 1
        if k_heading == 2:
            break


def check_lines():
    global line
    text2 = chatWindow.get("1.0", "end-1c")
    text2 = text2.split("\n")
    line = len(text2)


def find_all_links():
    global count_maps, all_links

    links = soup.find_all('a')

    for x in links:
        link = x.get('href')
        if 'maps' in link:
            count_maps += 1
        all_links.append(link)


ans_new = ""


def print_links(list_link):
    time.sleep(2)
    insert_in_chat_window(list_link[0])


def get_best_response_thread_func1():
    global flag, chrome_path, ans_new, list_link
    list_link = []
    k = 0
    for x in soup.select("div.kCrYT > a"):
        if k == 3:
            break
        i = str(x.get('href'))[7:]
        i = i[:i.find('&')]
        if i not in list_link:
            k += 1
            list_link.append(i)

    if 'wikipedia' in list_link[0] and flag == 0:
        temp1 = wikipedia.summary(query, sentences=3)
        insert_in_chat_window(temp1)
        speak1(temp1)
    elif 'quora' in list_link[0] and flag == 0:
        # speak1("opening quora sir")
        Thread(target=lambda: speak1("opening quora sir")).start()
        minimize_window()
        webbrowser.get(chrome_path).open(list_link[0])
        return
    elif 'youtube' in list_link[0] and flag == 0:
        list_link[0] = list_link[0].replace('%3Fv%3D', '?v=')
        Thread(target=lambda: speak1('opening youtube sir')).start()
        minimize_window()
        webbrowser.get(chrome_path).open(list_link[0])
        flag = 1
        return
    elif 'stackoverflow' in list_link[0]:
        Thread(target=lambda: speak1('opening stackoverflow sir')).start()
        minimize_window()
        webbrowser.get(chrome_path).open(list_link[0])
        flag = 1
        return

    Thread(target=print_links(list_link)).start()

    first_url = str(list_link[0])
    first_url = first_url[first_url.find('.') + 1:first_url.rfind('.')]
    last_word = query.split(" ")

    text1 = ""

    for x in range(0, len(last_word)):
        if last_word[len(last_word) - 1 - x] != "":
            text1 = last_word[len(last_word) - 1 - x]
            break

    if text1 != "" and text1.lower() in first_url.lower() and (abs(len(text1) - len(first_url)) <= 5):
        Thread(target=lambda: speak1("opening web page sir")).start()
        list_link[0] = list_link[0].replace('%3Fv%3D', '?v=')
        minimize_window()
        webbrowser.get(chrome_path).open(list_link[0])
        return

    time.sleep(0.3)

    if ans_new == "":
        speak1("opening webpage")
        minimize_window()
        webbrowser.get(chrome_path).open(list_link[0])


def get_best_response_thread_func2():
    global flag, ans_new
    ans_new = soup.find_all('div', attrs={"class": "kCrYT"})

    if 'http' not in ans_new[0].text and '.com' not in ans_new[0].text and '/' not in ans_new[0].text:
        # ans = ans.replace('\n' , " ")
        flag = 1
        if '\n' in ans_new[0]:
            insert_in_chat_window_lines(ans_new[0].text)
        else:
            insert_in_chat_window(ans_new[0].text)
        speak1(ans_new[0].text)
    else:
        if 'http' in ans_new[1].text or 'www' in ans_new[1].text or '.com' in ans_new[1].text:
            return
        flag = 1
        if '\n' in ans_new[1]:
            insert_in_chat_window_lines(ans_new[1].text)
        else:
            insert_in_chat_window(ans_new[1].text)
        speak1(ans_new[1].text)


def get_best_response_thread_func3():
    time.sleep(2)
    global flag
    if flag == 1:
        return
    if count_maps >= 3:
        for i in all_links:
            if 'maps' in i:
                if flag == 1:
                    return
                speak1("opening google maps sir")
                webbrowser.get(chrome_path).open(i)
                flag = 1
                return


def get_best_response_new(query):
    speak1("getting your best response, sir")

    global soup, count_maps, all_links, chrome_path, flag, ans_new

    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    r = requests.get('https://www.google.com/search?q=' + query)

    soup = BeautifulSoup(r.text, "html.parser")
    Thread(target=get_best_response_thread_func2).start()
    Thread(target=find_all_links).start()
    Thread(target=get_best_response_thread_func1).start()

    if flag == 0:
        Thread(target=get_best_response_thread_func3).start()
    if ans_new == "":
        Thread(target=selenium_get_best_response).start()
        Thread(target=get_best_response_func4).start()


def add_data_to_auto_completion():
    time.sleep(1)
    global search_list

    search_list = ['open downloads', 'open documents', 'open desktop', 'open downloads', 'open tkinter project',
                   'open python project', 'open videos', 'open firefox', 'open chrome', 'open google chrome',
                   'open youtube', "tell me today's news", 'tell me a joke', 'what is the time', 'what is time',
                   'open codeforces', 'open c++', 'open c plus plus', 'delete temporary files', 'clean my desktop',
                   'what i am doing ', 'clear my desktop', 'clean my downloads', 'play music', 'play songs',
                   'scroll down',
                   'full screen', 'reformat the code', 'read my emails', 'what i am doing today?', 'close', 'bye',
                   'i want to watch a video', 'next', 'scroll up', 'mute', 'next', 'read text file', 'open new window',
                   'minimize', 'maximize', 'suggest good movies', 'good movies', 'zoom in', 'zoom out',
                   'live cricket score', 'my codeforces rating', 'harry potter', 'increase volume', 'decrease volume']

    for i in data:
        search_list.append('open ' + i.lower())

    file1 = open('suggestion_autocompletion2.txt', 'r')
    x1 = file1.read()
    x1 = x1.split('\n')
    for i in x1:
        search_list.append(i)



def check_application_is_open_or_not(app):
    list = psutil.pids()
    for i in range(0, len(list)):
        try:
            p = psutil.Process(list[i])
            if p.cmdline()[0].find(app + ".exe") != -1:
                return True
        except:
            pass
    return False


def bind_right_click(event):
    # messageWindow.tag_add("background_tag", messageWindow.index(INSERT), END)
    # messageWindow.tag_config("background_tag", background="white", foreground="black")
    # messageWindow.mark_set("insert", END)
    txt = retrieve_input_for_auto_completion()
    messageWindow.delete("1.0", END)
    messageWindow.insert(END, txt)


def key(event):
    messageWindow.delete(messageWindow.index(INSERT), END)
    txt = retrieve_input_for_auto_completion()
    txt += str(event.char)
    if 'a' <= event.char <= 'z' or 'A' <= event.char <= 'Z':
        auto_complete(txt)


def auto_complete(query):
    global search_list
    string = ""
    flag1 = 1

    for x in search_list:
        flag1 = 1
        for i in range(0, min(len(x), len(query))):
            if x[i] != query[i]:
                flag1 = 0
                break
        if flag1 == 1:
            string = x
            break

    if len(query) > len(string):
        flag1 = 0

    if flag1 == 1 and string != "":
        messageWindow.insert(END, string[len(query):])
        messageWindow.tag_add("background_tag", "1." + str(len(query) - 1), "1." + str(len(string)))
        messageWindow.tag_config("background_tag", background="#2F4F4F", foreground="white")
        messageWindow.mark_set("insert", "%d.%d" % (0 + 1, len(query) - 1))


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print(hex(hwnd), win32gui.GetWindowText(hwnd))


def print_all_open_windows():
    win32gui.EnumWindows(winEnumHandler, None)


def check_minimized(title):
    window = win32gui.FindWindow(None, title)
    if window:
        tup = win32gui.GetWindowPlacement(window)
        if tup[1] == win32con.SW_SHOWMAXIMIZED:
            return "maximized"
        elif tup[1] == win32con.SW_SHOWMINIMIZED:
            return "minimized"
        elif tup[1] == win32con.SW_SHOWNORMAL:
            return "normal"


def make_maximized():
    while True:
        if check_minimized('Assistant') == 'normal':
            root.overrideredirect(True)
            break


def scrollUp():
    # speak("scrolling up sir")
    i = 0
    while i < 10:
        i = i + 1
        pyautogui.hotkey('up')


def scrollDown():
    i = 0
    while i < 10:
        i = i + 1
        pyautogui.hotkey('down')
        time.sleep(0.1)


# function to take speech input

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    r.energy_threshold = 5000
    with sr.Microphone() as source:
        print("Listening...")

        if check_minimized('Assistant') == "minimized":
            Mic_icon()
        if write_flag == 0:
            r.pause_threshold = 0.8
        else:
            r.pause_threshold = 3

        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    Thread(target=load_mic_image).start()
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except:
        print("Say that again please...")
        query = " "
    return query



def retrieve_input_for_auto_completion():
    inputValue = ""
    inputValue += messageWindow.get("1.0", "end-1c")
    return inputValue


# function to read daily tasks
def read_tasks_today():
    time.sleep(20)
    date = get_date("today")
    insert_in_chat_window(f"your tasks on {date} are")
    # Thread(target=speak).start()
    speak1(f"your tasks on {date} are")
    file_name = str(date).replace(":", "-") + "-tasks.txt"
    try:
        f = open(file_name, 'r')
        file_contents = f.read()
        if file_contents == "":
            insert_in_chat_window("No tasks added")
            speak1("No tasks added")
        else:
            insert_in_chat_window_lines(file_contents)
            speak1(file_contents)

    except:
        insert_in_chat_window("No tasks are added")
        speak1("No tasks are added")




def get_best_response(query):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2,
                                              'profile.managed_default_content_settings.javascript': 2,
                                              'profile.managed_default_content_settings.cookies': 2,
                                              'profile.managed_default_content_settings.notifications': 2,
                                              'profile.managed_default_content_settings.ads': 2})
    options.add_argument('-headless')
    speak1("Getting your best response , Sir")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com/search?q=" + query)

    links = ""

    element2 = driver.find_elements_by_xpath('//div[@class="r"]')
    for x in element2:
        links += str(x.find_element_by_xpath(".//a").get_attribute("href"))
        links += "\n"

    links = links.split("\n")

    k = 0
    for x in links:
        insert_in_chat_window(x)
        k = k + 1
        if k == 3:
            break

    first_url = str(ans[0])
    first_url = first_url[first_url.find('.') + 1:first_url.rfind('.')]

    last_word = query.split(" ")

    for x in range(0, len(last_word)):
        if last_word[len(last_word) - 1 - x] != "":
            text1 = last_word[len(last_word) - 1 - x]
            break

    if text1.lower() in first_url.lower():
        speak1("opening web page sir")
        webbrowser.get(chrome_path).open(ans[0])
        return

    if 'quora' in first_url.lower():
        speak1("opening Qoura sir")
        webbrowser.get(chrome_path).open(ans[0])
        return

    myString = ""

    if myString == "" or len(myString) <= 10:
        elements = driver.find_elements_by_class_name("e24Kjd")
        for x in elements:
            if x.text != "":
                myString += x.text + " "

    if myString != "":
        insert_in_chat_window(myString)
        speak1(myString)
        return

    myString1 = ""

    k = 0
    for x in ans:
        k = k + 1
        if k == 3:
            break
        if 'wikipedia' in x:
            try:
                myString1 += wikipedia.summary(query, sentences=3)
                insert_in_chat_window(myString1)
                speak1(myString1)
                break
            except:
                pass
        elif 'youtube' in x:
            speak1("opening youtube sir")
            webbrowser.get(chrome_path).open(x)
            return

    if myString1 != "":
        return
    # print("here.......................")
    myString = " "

    # for google dictionary
    elements1 = driver.find_elements_by_xpath('//div[@data-dobid="dfn"]')
    for x in elements1:
        if x.text != "":
            myString += x.text + " "

    # for google maps places and destinations

    if myString == "" or len(myString) <= 10:
        elements1 = driver.find_elements_by_xpath('//div[@role="heading"]')
        k = 0
        for x in elements1:
            if 'View' not in x.text and '. . .' in x.text:
                myString += x.text
                myString += "\n"
            k = k + 1
            if k >= 6:
                break

    if myString == "":
        elements1 = driver.find_element_by_xpath('//span[@class="st"]')
        myString += elements1.text

    if myString == "" or len(myString) <= 10:
        elements1 = driver.find_elements_by_xpath('//li[@class="TrT0Xe"]')
        for x in elements1:
            if x.text != "":
                myString += x.text + "\n"

    insert_in_chat_window(myString)
    speak1(myString)
    driver.quit()


def func_to_remove_type(event):
    inputValue = messageWindow.get("1.0", "end-1c")
    if 'Type' in inputValue:
        messageWindow.delete("1.0", "end")


query = ""
ans = ""


def open_downloads():
    Thread(target=lambda: speak1("Opeining Downloads Sir")).start()
    os.startfile(str(os.path.join(Path.home(), "Downloads")))
    pyautogui.hotkey('win', 'up')


def open_desktop():
    Thread(target=lambda: speak1("Opeining Desktop Sir")).start()
    os.startfile(str(os.path.join(Path.home(), "Desktop")))
    pyautogui.hotkey('win', 'up')


def open_documents():
    Thread(target=lambda: speak1("Opeining Documents Sir")).start()
    os.startfile(str(os.path.join(Path.home(), "Documents")))
    pyautogui.hotkey('win', 'up')


def open_videos():
    Thread(target=lambda: speak1("Opeining vidoes Sir")).start()
    os.startfile(str(os.path.join(Path.home(), "Videos")))
    pyautogui.hotkey('win', 'up')



def insert_in_chat_window_lines(ans1):
    ans1 = ans1.split("\n")
    for x in ans1:
        insert_in_chat_window(x)


line = 1


def open_link(url):
    webbrowser.get(chrome_path).open(url)


count_link = 0


def insert_in_chat_window(ans1):
    global line, ans, count_link

    if emoji.emojize(":grinning_face_with_big_eyes:") in ans1:
        ans = ans1[:len(ans1) - 1]
    else:
        ans = ans1

    if 'www.' in ans1 or 'http' in ans1:
        hyperlink1 = HyperlinkManager(chatWindow)
        chatWindow.insert(END, ans1 + "\n", hyperlink1.add(ans1))
    else:
        chatWindow.insert(END, ans1 + "\n")
        chatWindow.tag_add("background_tag1", str(line) + ".0", str(line) + "." + str(len(ans1)))
        chatWindow.tag_config("background_tag1", background="#1E90FF", foreground="white")

    line += 1
    # chatWindow.tag_remove("background_tag1", str(line) + ".0", str(line) + "." + str(len(ans1)))

    Thread(target=check_lines).start()

    if line >= 5:
        chatWindow.insert(END, "\n")
        line += 1

    chatWindow.see("end")


def insert_in_chat_window_voice(ans1):
    global line, ans
    # print(line)
    chatWindow.insert(END, ans1 + "\n")
    if emoji.emojize(":grinning_face_with_big_eyes:") in ans1:
        ans = ans1[:len(ans1) - 1]
    else:
        ans = ans1
    # print("doing...")
    chatWindow.tag_add("background_tag2", str(line) + ".0", str(line) + "." + str(len(ans1)))
    chatWindow.tag_config("background_tag2", background="#2F4F4F", foreground="white")
    line += 1
    # chatWindow.tag_remove("background_tag2", str(line) + ".0", str(line) + "." + str(len(ans1)))

    # Thread(target=check_lines).start()
    if line >= 5:
        chatWindow.insert(END, "\n")
        line += 1

    chatWindow.see("end")


def get_emails():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate

    imap.login(username, password)

    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 8
    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages - N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode()
                # email sender
                from_ = msg.get("From")
                subject = subject.replace("Critical security alert", " ")
                if subject == " ":
                    continue
                text = str(from_)
                text = text[0:text.find('<')]
                text = text.replace("?UTF-8?B?VWRlbXk=?= ", " ")
                text = text.replace("?utf-8?q?", "")
                text = text.replace("?=", "")
                text = text.replace("=", "")

                insert_in_chat_window("From: " + text)
                speak1("From: " + text)
                insert_in_chat_window("Subject: " + subject)
                speak1("Subject: " + subject)
    imap.close()
    imap.logout()


def get_news():
    news_url = "https://news.google.com/news/rss"
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()

    soup_page = BeautifulSoup(xml_page, "xml")
    news_list = soup_page.findAll("item")

    count = 1

    for news in news_list:
        count = count + 1
        if count == 10:
            break
        insert_in_chat_window(news.title.text)
        speak1(news.title.text)


def full_screen():
    pyautogui.hotkey('fn', 'f11')


def clean_my_deskstop():
    source = "C://Users//patel//OneDrive//Desktop>"

    elements = os.listdir(source)

    for x in elements:
        print(x)
        if '.txt' in x or '.pdf' in x or '.doc' in x:
            destination = 'C://Users//patel//OneDrive//Desktop//Files//PDF'
            try:
                shutil.move(source + f"//{x}", destination)
            except:
                os.remove(source + f"//{x}")
                pass
        elif '.pptx' in x or '.ppt' in x or '.xlsx' in x:
            destination = 'C://Users//patel//OneDrive//Desktop//Files//PRESENTATION'
            try:
                shutil.move(source + f"//{x}", destination)
            except:
                os.remove(source + f"//{x}")
                pass
        elif '.mp3' in x or '.eop' in x:
            destination = 'C://Users//patel//OneDrive//Desktop//Files//MP3'
            try:
                shutil.move(source + f"//{x}", destination)
            except:
                os.remove(source + f"//{x}")
                pass
        elif '.mp4' in x or '.mkv' in x:
            destination = 'C://Users//patel//OneDrive//Desktop//Files//MP4'
            try:
                shutil.move(source + f"//{x}", destination)
            except:
                os.remove(source + f"//{x}")
                pass
        elif '.cpp' in x or '.c' in x or '.m' in x or '.py' in x or '.js' in x or '.html' in x or '.css' in x or '.tex' in x:
            destination = 'C://Users//patel//OneDrive//Desktop//Files//CODE'
            try:
                shutil.move(source + f"//{x}", destination)
            except:
                os.remove(source + f"//{x}")
                pass
        elif '.jpg' in x or '.img' in x or '.jpeg' in x or '.gif' in x or '.png' in x or '.JPG' in x or '.PNG' in x or '.JPEG' in x or '.ico' in x:
            destination = 'C://Users//patel//OneDrive//Desktop//Files//IMAGES'
            try:
                shutil.move(source + f"//{x}", destination)
            except:
                os.remove(source + f"//{x}")
                pass
        elif '.exe' in x:
            destination = 'C://Users//patel//OneDrive//Desktop//Files//EXE'
            try:
                shutil.move(source + f"//{x}", destination)
            except:
                os.remove(source + f"//{x}")
                pass
        elif '.zip' in x:
            destination = 'C://Users//patel//OneDrive//Desktop//Files//ZIP'
            try:
                shutil.move(source + f"//{x}", destination)
            except:
                os.remove(source + f"//{x}")
                pass


def editDistDP(str1, str2, m, n):
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i  # Min. operations = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
                                   dp[i - 1][j],  # Remove
                                   dp[i - 1][j - 1])  # Replace

    return dp[m][n]


def My_get_close_matches(query, data):
    query = query.lower()
    mn = 1e10
    idx = -1
    count = 0

    for x in data:
        k = editDistDP(query, x, len(query), len(x))
        if k < mn:
            mn = k
            idx = count
        count += 1

    if mn > 10:
        return -1

    print(data[idx])

    return data[idx]


def search_data_pdf(ans):
    if ans in data_pdf:
        ans = "C://Users//patel//OneDrive//Desktop//Files//PDF//" + ans
        minimize_window()
        os.startfile(ans)
        return


def search_data_mp4(ans):
    if ans in data_mp4:
        ans = "C://Users//patel//OneDrive//Desktop//Files//MP4//" + ans
        minimize_window()
        os.startfile(ans)
        return


def search_data_mp3(ans):
    if ans in data_mp3:
        ans = "C://Users//patel//OneDrive//Desktop//Files//MP3//" + ans
        minimize_window()
        os.startfile(ans)
        return


def search_data_ppt(ans):
    if ans in data_presentation:
        ans = "C://Users//patel//OneDrive//Desktop//Files//PRESENTATION//" + ans
        minimize_window()
        os.startfile(ans)
        return


def get_files_from_pc(ans):
    Thread(target=search_data_pdf(ans)).start()
    Thread(target=search_data_mp3(ans)).start()
    Thread(target=search_data_ppt(ans)).start()
    Thread(target=search_data_mp4(ans)).start()


greetings = ['hey there', 'hello', 'hello there', 'hi', 'hey !', 'hey']
cmd4 = ['open youtube', 'i want to watch a video']
cmd1 = ['open browser', 'open google', 'google', 'open google chrome', 'open chrome', 'chrome']
k_music = 0
ans_thank_you = ["glad i could help you", "Welcome"]

write_flag = 0


def output_text():
    global task_add_flag, add_task_date, query, k_music

    if task_add_flag == 1 and ('close' not in query):
        add_tasks(query)
        insert_in_chat_window(f"Adding this task")
        speak1("Adding this task")
        return

    if task_add_flag == 1 and ('close' in query):
        task_add_flag = 0
        return

    if k_music == 1 and 'next' in query:
        music_dir = 'C://Users// patel//OneDrive//Desktop//Songs'
        songs = os.listdir(music_dir)
        r = random.choice(songs)
        print("playing.....")
        os.startfile(os.path.join(music_dir, r))
        return

    query = query.lower()
    if 'hi' == query or 'hello' in query or 'good morning' in query or 'good afternoon' in query or 'good evening' in query or query in greetings or 'hey' == query:
        str = greetings[random.randint(0, len(greetings) - 1)]
        insert_in_chat_window(str)
        speak1(str)
    elif 'open' in query and ('downloads' in query or 'download' in query):
        open_downloads()
        minimize_window()
    elif 'open' in query and ('documents' in query or 'document' in query):
        open_documents()
        minimize_window()
    elif 'open' in query and ('desktop' in query or 'home' in query):
        open_desktop()
        minimize_window()
    elif 'close' in query:
        speak1("closing it sir")
        pyautogui.hotkey('alt', 'f4')
    elif 'open youtube' in query or 'i want to watch a video' in query:
        speak1("opening youtube sir")
        minimize_window()
        webbrowser.get(chrome_path).open("www.youtube.com")
    elif query in cmd1:
        speak1("opening google sir")
        minimize_window()
        webbrowser.get(chrome_path).open("")
    elif 'play music' in query or 'play song' in query:
        speak1("playing music sir")
        music_dir = 'C://Users// patel//OneDrive//Desktop//Files//MP3'
        songs = os.listdir(music_dir)
        r = random.choice(songs)
        os.startfile(os.path.join(music_dir, r))
        k_music = 1
    elif 'what is the time' in query or 'which time it is' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak1(f"Sir the time is {strTime}")
    elif 'who are you' in query or 'what is your name' in query:
        speak1(
            "I am friday. Dhruv patel created me in corona virus lock-down. i am new way "
            "to talk to laptop.")
    elif 'bye' in query or 'see you later' in query or 'good bye' in query or 'quit' in query or 'exit' in query:
        speak1("Good bye , have a nice day")
        quit_code()
    elif 'thank you' in query:
        speak1(ans_thank_you[random.randint(0, 1)])
    elif 'new window' in query:
        speak1("opening new window sir")
        pyautogui.hotkey('ctrl', 'n')
    elif 'minimize' in query or 'minimise' in query:
        speak1("minimizing the window sir")
        minimize_window()
    elif 'scroll up' in query or 'up' in query or 'aap' in query or 'app' in query:
        scrollUp()
    elif 'last tab' in query or 'tab' in query:
        minimize_window()
        pyautogui.hotkey('alt', 'tab')
    elif ('tell' in query or 'what' in query) and 'news' in query:
        get_news()
    elif 'mute' in query:
        pyautogui.hotkey("volumemute")
    elif 'increase' in query and 'volume' in query:
        for x in range(0, 5):
            pyautogui.hotkey("volumeup")
    elif 'decrease' in query and 'volume' in query:
        for x in range(0, 5):
            pyautogui.hotkey("volumedown")
    elif 'full screen' in query:
        pyautogui.hotkey("fn", "f11")
    elif 'write' in query or 'right' in query and 'for me' in query:
        global write_flag
        x = 0
        while x < 15:
            r = sr.Recognizer()
            write_flag = 1
            query = takeCommand().lower()
            pyautogui.typewrite(query, interval=0.15)
            write_flag = 0
            x = x + 1

            if 'stop' in query or 'close' in query or 'exit' in query:
                break
    elif 'zoom' in query and 'in' in query:
        pyautogui.hotkey('ctrl', '+')
    elif 'zoom' in query and 'out' in query:
        pyautogui.hotkey('ctrl', '-')
    elif 'full screen' in query:
        full_screen()
    elif 'emails' in query or 'read my emails' in query or 'email' in query:
        speak1("Reading your recent emails")
        get_emails()
    elif 'open' in query and query[0] == 'o':
        global data_website
        query = query.replace('open', '')
        query = query.replace(' ', '')
        flag_site = 0
        for x in data_website:
            if query in x:
                speak1(f'opening {query}')
                minimize_window()
                Thread(target=open_link(x)).start()
                flag_site = 1
                break

        if flag_site == 0:
            speak1("Searching for file in PC")
            try:
                get_files_from_pc(My_get_close_matches(query, data))
            except:
                speak1("No file found")

    elif 'clean my desktop' in query or 'clean my downloads' in query or 'clean my download' in query or 'clear my ' \
                                                                                                         'desktop' in \
            query:
        if 'desktop' in query:
            speak1('cleaning your desktop sir ')
        else:
            speak1('cleaning your downloads sir')

        clean_my_deskstop()
    else:
        if query != " ":
            get_best_response_new(query)


def speak():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(ans)
    engine.runAndWait()


def speak1(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    try:
        engine.runAndWait()
    except:
        pass


def retrieve_input():
    global search_list, line
    inputValue = messageWindow.get("1.0", "end-1c")
    inputValue = inputValue.replace("\n", "")
    chatWindow.insert(END, inputValue + "\n")
    chatWindow.tag_add("background_tag", str(line) + ".0", str(line) + "." + str(len(inputValue)))
    chatWindow.tag_config("background_tag", background="#2F4F4F", foreground="white")
    line += 1
    messageWindow.delete("1.0", "end")

    global query
    query = inputValue
    Thread(target=output_text).start()
    if inputValue not in search_list:
        search_list.append(inputValue)
        file2 = open('suggestion_autocompletion2.txt', 'a')
        file2.write(inputValue + "\n")
        file2.close()

    if line >= 5:
        chatWindow.insert(END, "\n")
        line += 1

    chatWindow.see("end")


def retrieve_input1(event):
    global search_list, line
    inputValue = messageWindow.get("1.0", "end-1c")
    inputValue = inputValue.replace("\n", "")
    chatWindow.insert(END, inputValue + "\n")
    chatWindow.tag_add("background_tag", str(line) + ".0", str(line) + "." + str(len(inputValue)))
    chatWindow.tag_config("background_tag", background="#2F4F4F", foreground="white")
    line += 1
    # chatWindow.tag_remove("background_tag", str(line) + ".0", str(line) + "." + str(len(inputValue)))
    messageWindow.delete("1.0", "end")

    global query
    query = inputValue

    Thread(target=output_text).start()

    if line >= 5:
        chatWindow.insert(END, "\n")
        line += 1

    if inputValue not in search_list:
        search_list.append(inputValue)
        file2 = open('suggestion_autocompletion2.txt', 'a')
        file2.write(inputValue + "\n")
        file2.close()

    chatWindow.see("end")


def all_bind():
    time.sleep(3)
    Thread(target=lambda: messageWindow.bind("<Key>", key)).start()
    Thread(target=lambda: messageWindow.bind("<Right>", bind_right_click)).start()


def take_voice_input():
    global query, quit_flag
    time.sleep(5)
    while True:
        voice_input = takeCommand()
        if quit_flag == 1:
            break
        if voice_input != " ":
            insert_in_chat_window_voice(voice_input)
        query = voice_input.lower()
        output_text()


def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak1("Good Morning sir")
    elif 12 <= hour < 18:
        speak1("Good Afternoon sir")
    else:
        speak1("Good evening sir")
    speak1("I am Friday. how can i help you?")


if __name__ == '__main__':
    Thread(target=GUI).start()
    Thread(target=load_all_library).start()
    Thread(target=add_data_to_auto_completion).start()
    Thread(target=data_of_pc).start()
    Thread(target=take_voice_input).start()
    Thread(target=data_websites).start()
    Thread(target=wish).start()


