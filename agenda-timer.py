#!/usr/bin/python

from tkinter import *
from tkinter import ttk
from tkinter import font
import datetime
import json
import os
import csv


# ############################################################################
# Configuration Options

timeremaining_warning=80 # When there is only % left change the text to orange to warn the speaker
timeremaining_critical=90 # When there is only % left change the text to red to warn the speaker
fullscreen=False

color_bg="#282c34"
color_mute="#abb2bf"
color_green="#8dc270"
color_highlights="#ffffff"
second = datetime.timedelta(seconds=1)

# You should not need to change anything below
# ############################################################################
def quit(*args):
    root.destroy()

dt0 = datetime.timedelta(0)


def format_timedelta(td):
    if td < dt0:
        return '-' + format_timedelta(-td)
    else:
        # Change this to format positive timedeltas the way you want
        return str(td)


def load_contribs():
    cr = csv.reader(open('contribs_export_qt.csv', newline=''))
    contribs_d = [c[:2] +
                  [datetime.timedelta(minutes=int(c[2])),
                   datetime.timedelta(0)] for c in list(cr)]
    return contribs_d


contribs = load_contribs()
cidx = 0


def update_agenda():
    # Get the time remaining until the event
    now = datetime.datetime.now()
    realTime.set(now.strftime('%H:%M'))

    duration, elapsed = contribs[cidx][2:]
    elapsed_r = elapsed / duration

    # Set the countdown colour based on the remaining amount of time
    if elapsed_r * 100 >= timeremaining_critical:
        lblCountdownTime.configure(foreground='red')
    elif  elapsed_r * 100 >= timeremaining_warning:
        lblCountdownTime.configure(foreground='orange')
    else:
        lblCountdownTime.configure(foreground=color_green)
    # Set the text on the Tk Label for Countdown
    remainingTime.set(format_timedelta(duration - elapsed))

    percent_done.set(min(round(elapsed_r * 100), 100))
    # Trigger the countdown after 1000ms
    contribs[cidx][3] += second
    root.after(1000, update_agenda)


def goto_offset(di):
    global cidx
    try:
        current_contrib = contribs[cidx+di]
    except IndexError:
        return
    cidx += di
    try:
        next_contrib = contribs[cidx+1]
    except IndexError:
        next_contrib = None

    title, speaker, duration, elapsed = current_contrib
    sessionTitle.set(title)
    currentSpeaker.set(speaker)
    percent_done.set(round(elapsed / duration * 100))

    if next_contrib is None:
        nextTitle.set('')
    else:
        nextTitle.set(next_contrib[1] + ': ' + next_contrib[0])


# Use Tkinter to create the app window
root = Tk()
imgicon = PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(__file__)),'icon.gif'))
root.tk.call('wm', 'iconphoto', root._w, imgicon)
if (fullscreen):
    root.attributes("-fullscreen", True)
else:
    root.geometry("1024x800")
root.title("Agenda Countdown")
root.configure(background=color_bg)
root.bind("<Escape>", quit)
root.bind("x", quit)
root.bind('n', lambda *args: goto_offset(+1))
root.bind('p', lambda *args: goto_offset(-1))
style = ttk.Style()
style.theme_use('classic') # to fix bug on Mac OSX
style.configure("Red.TLabel", fg='red')


# Set the end date and time for the countdown
fntNormal = font.Font(family='Helvetica', size=60, weight='bold')
fntForCountdown = font.Font(family='Helvetica', size=80, weight='bold')
fntForTitle = font.Font(family='Helvetica', size=40, weight='bold')
fntSmall = font.Font(family='Helvetica', size=20, weight='bold')

# Create some Tkinter variables
remainingTime = StringVar()
sessionTitle = StringVar()
nextTitle= StringVar()
realTime = StringVar()
currentSpeaker = StringVar()
nextSpeaker = StringVar()
numOfSessions = IntVar()
currSession = IntVar()
i = IntVar()
percent_done = IntVar()
txtTimeRemaining = StringVar()


# Add Tkinter Labels to hold the text elements
lblRealTime = ttk.Label(root, textvariable=realTime, font=fntNormal, foreground=color_mute, background=color_bg)
lblRealTime.place(relx=0.9, rely=0.1, anchor=CENTER)

lblTimeRemaining = ttk.Label(root, textvariable=txtTimeRemaining, font=fntSmall, foreground=color_mute, background=color_bg)
lblTimeRemaining.place(relx=0.5, rely=0.45, anchor=CENTER)
txtTimeRemaining.set('Time Remaining: ')

lblTitle =  ttk.Label(root, textvariable=sessionTitle, font=fntForTitle, foreground=color_highlights, background=color_bg)
lblTitle.place(relx=0.5, rely=0.2, anchor=CENTER)

lblSpeaker =  ttk.Label(root, textvariable=currentSpeaker, font=fntForTitle, foreground=color_highlights, background=color_bg)
lblSpeaker.place(relx=0.5, rely=0.3, anchor=CENTER)

lblCountdownTime = ttk.Label(root, textvariable=remainingTime, font=fntForCountdown, foreground=color_green, background=color_bg)
lblCountdownTime.place(relx=0.5, rely=0.6, anchor=CENTER)

pbar = ttk.Progressbar(root, variable=percent_done, orient='horizontal', length=700)
pbar.place(relx=0.5, rely=0.8, anchor=CENTER)


lblNextUp =  ttk.Label(root, text='Next up:', font=fntSmall, foreground=color_mute, background=color_bg)
lblNextUp.place(relx=0.5, rely=0.9, anchor=CENTER)

lblNextTitle =  ttk.Label(root, textvariable=nextTitle, font=fntForTitle, foreground=color_highlights, background=color_bg)
lblNextTitle.place(relx=0.5, rely=0.95, anchor=CENTER)


# Run the update_agenda
goto_offset(0)
root.after(1000, update_agenda)
root.mainloop()
