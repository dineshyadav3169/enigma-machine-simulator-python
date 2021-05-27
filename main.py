from tkinter import *
from tkinter import messagebox
from enigma.machine import EnigmaMachine

window = Tk() #initializing program window
screenSize = "600x240" #defining program screen size
window.geometry(screenSize)
window.resizable(0, 0) #not resizable
window.title("Enigma")


#color for output
bcolors = {
    'OKCYAN': '\033[96m',
    'OKGREEN' : '\033[92m',
    'ENDC' :'\033[0m'
}


def saveBtn():
    '''Get roters, rings and plugboard settings and pass to enigma machine, print all settings'''
    roter1 = ro1.get()
    roter2 = ro2.get()
    roter3 = ro3.get()
    global roters_package
    roters = roter1 + ' ' + roter2 + ' ' + roter3 
    
    ring_seting1 = roi1.get()
    ring_seting2 = roi2.get()
    ring_seting3 = roi3.get()
    
    global ring_settings
    ring_settings = []
    ring_settings.clear()
    ring_settings.append(ring_seting1)
    ring_settings.append(ring_seting2)
    ring_settings.append(ring_seting3)
    
    plugboard_settings = plugb.get()
    
    global machine
    machine = EnigmaMachine.from_key_sheet(
           rotors=roters,
           reflector='B',
           ring_settings=ring_settings,
           plugboard_settings=plugboard_settings)
    machine.set_display('WXC')
    msg_key = machine.process_text('KCH')
    machine.set_display(msg_key)
    
    print(f"{bcolors['OKCYAN']}Roters: {roters} \t Ring Setting: {ring_settings} \t Plug Setting: {plugboard_settings}{bcolors['ENDC']}")


def clipboard():
    ''' clear clipboard , get message from input frame and copy to clipboard'''
    window.clipboard_clear()
    copy_text = inputText.get()
    window.clipboard_append(copy_text)
    print(bcolors['OKGREEN']+"Message Copied to Clipboard "+bcolors['ENDC'],copy_text)


def resetValue():
    '''reset Default values for rotors, ring_settings, plugboard_settings'''
    ro1.set('II')
    ro2.set('IV')
    ro3.set('V')
    
    roi1.set(1)
    roi2.set(20)
    roi3.set(11)
    
    plugb.set('AV BS CG DL FU HZ IN KM OW RX')
    print("Done")


def about():
    '''Show details in messagebox'''
    messagebox.showinfo('How to Use',"To Encrypt Messages: \n\t1. Save Settings\n\t2. Enter Input(Text or number)\n\t3. Click on Run \n\n\nTo Decrypt Message:\n\t1. Paste or Type Text\n\t2. Click on Run\n\t(NOTE: Sender and receiver should have same set of keys)")


def clearAll():
    '''clear input frame and set background to black'''
    inputText.set("")
    inputField['bg'] = "black"
    print("Cleared Input MainFrame")


def expand():
    '''increase height of program window'''
    if screenSize=="600x250":
        window.geometry("600x475")
    else:
        window.geometry("600x475")
        

def clearSearch(event):
    ''' clear message on input frame onclick'''
    inputField.delete(0, END)
    inputField['bg'] = "black"
    print("Ready to take Input")    


def runButton():
    ''' process message through machine, if settings not saved then show alert on input frame'''
    result = ""
    try:
        global inputText
        result = inputText.get()
        plaintext = machine.process_text(result).replace("X", " ")        
        inputText.set(plaintext)
        resetValue()
        inputField['bg'] = "orange"
        print(f'{result} -> {plaintext}')
    except:
        result = "Save Settings..."
        inputText.set(result)


#menubar for software
menubar = Menu(window,bg="white",fg="black")
filemenu = Menu(menubar, tearoff=0,bg="white",fg="black")
filemenu.add_command(label="Copy")
filemenu.add_command(label="Paste")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="Edit", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0,bg="white",fg="black")
helpmenu.add_command(label="How to Use", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)


expression = ""
inputText = StringVar()

#input Frame is outline which contains input field
inputFrame = Frame(window, width=312, height=50, bd=0, highlightbackground="orange", highlightcolor="#49A",
                    highlightthickness=2)
inputFrame.pack(side=TOP)
inputField = Entry(inputFrame, font=('arial', 25, ), textvariable=inputText, width=50,fg="white", bg="black", bd=0,
                    justify=LEFT)
inputField.grid(row=0, column=0)
inputField.pack(ipady=13)
inputField.insert(0, 'Enter Message')
inputField.bind("<Button-1>", clearSearch)

#main Frame
mainFrame = Frame(window, width=780, height=420, bg="black")
mainFrame.pack()


blank = PhotoImage(file = r"images\blank.png") #normal string will not work as windows path
blankimage = blank.subsample(4,4)
blank = Button(mainFrame, text=".", image=blankimage, fg="white", bd=0, bg="black", cursor="hand2")


blank2 = PhotoImage(file = r"images\blank.png")
blank2image = blank2.subsample(10,10)
blank2 = Button(mainFrame, text=".", image=blank2image, fg="white", bd=0, bg="black", cursor="hand2")


reset = PhotoImage(file = r"images\reset.png")
resetimage = reset.subsample(4,4)
reset = Button(mainFrame, text="AC", fg="black", image=resetimage, bd=0, bg="black", cursor="hand2",
               command=lambda: resetValue()).grid(row=0, column=0, padx=1, pady=4)


Copy = PhotoImage(file = r"images\copy.png")
Copyimage = Copy.subsample(4,4)
Copy = Button(mainFrame, text="Copy", fg="black", image=Copyimage, bd=0, bg="black", cursor="hand2",
               command=lambda: clipboard()).grid(row=0, column=1, padx=1, pady=1)
               

blank.grid(row=0, column=2, padx=1, pady=1)
clear = PhotoImage(file = r"images\clear.png")
clearimage = clear.subsample(4,4)
clear = Button(mainFrame, text="C", fg="black", image=clearimage, bd=0, bg="black", cursor="hand2",
               command=lambda: clearAll()).grid(row=0, column=3, padx=1, pady=1)


exite = PhotoImage(file = r"images\exit.png")
exiteimage = exite.subsample(4,4)
exite = Button(mainFrame, text="exit", fg="black", image=exiteimage, bd=0, bg="black", cursor="hand2",
               command=window.quit).grid(row=1, column=0, padx=1, pady=1) 


expands = PhotoImage(file = r"images\expand.png")
expandsimage = expands.subsample(4,4)
expands = Button(mainFrame, text="Expand", fg="black", image=expandsimage, bd=0, bg="black", cursor="hand2",
               command=lambda: expand()).grid(row=1, column=1, padx=1, pady=1) 


blank2.grid(row=1, column=2, padx=1, pady=1)


run = PhotoImage(file = r"images\run.png")
runimage = run.subsample(4,4)
run = Button(mainFrame, text="run", image=runimage, fg="white", bd=0, bg="black", cursor="hand2",
                command=lambda: runButton()).grid(row=1, column=3, padx=1, pady=1)


blank2.grid(row=2, column=0, padx=1, pady=1)
save = PhotoImage(file = r"images\save.png")
saveimage = save.subsample(4,4)
save = Button(mainFrame, text="save", image=saveimage, fg="white", bd=0, bg="black", cursor="hand2",
                command=lambda: saveBtn()).grid(row=3, column=0, padx=1, pady=1)



##setting default values on label
#for rotors
ro1 = StringVar()
ro2 = StringVar()
ro3 = StringVar()

ro1.set('II')
ro2.set('IV')
ro3.set('V')
Label(mainFrame, text="    Roter I      ", fg="white",bg="#49A",font=('arial', 15, )).grid(row=8,column=0)
Label(mainFrame, text="     Roter II     ", fg="white",bg="#49A",font=('arial', 15, )).grid(row=8,column=1)
Label(mainFrame, text="    Roter III    ", fg="white",bg="#49A",font=('arial', 15, )).grid(row=8,column=2)
r1 = Entry(mainFrame, textvariable=ro1,font=('arial', 15, ),width=5,fg="gray", bg="white", bd=0,justify=CENTER).grid(row=9,column=0)
r2 = Entry(mainFrame, textvariable=ro2,font=('arial', 15, ),width=5,fg="gray", bg="white", bd=0,justify=CENTER).grid(row=9,column=1)
r3 = Entry(mainFrame, textvariable=ro3,font=('arial', 15, ),width=5,fg="gray", bg="white", bd=0,justify=CENTER).grid(row=9,column=2)

#for rings
roi1 = IntVar()
roi2 = IntVar()
roi3 = IntVar()

roi1.set(1)
roi2.set(20)
roi3.set(11)
Label(mainFrame, text="RING SET I  ", fg="white",bg="#49A",font=('arial', 15, )).grid(row=10,column=0)
Label(mainFrame, text="RING SET II ", fg="white",bg="#49A",font=('arial', 15, )).grid(row=10,column=1)
Label(mainFrame, text="RING SET III", fg="white",bg="#49A",font=('arial', 15, )).grid(row=10,column=2)
ri1 = Entry(mainFrame, textvariable=roi1,font=('arial', 15, ),width=5,fg="gray", bg="white", bd=0,justify=CENTER).grid(row=11,column=0)
ri2 = Entry(mainFrame, textvariable=roi2,font=('arial', 15, ),width=5,fg="gray", bg="white", bd=0,justify=CENTER).grid(row=11,column=1)
ri3 = Entry(mainFrame, textvariable=roi3,font=('arial', 15, ),width=5,fg="gray", bg="white", bd=0,justify=CENTER).grid(row=11,column=2)

#plugboard
plugb = StringVar()
plugb.set('AV BS CG DL FU HZ IN KM OW RX')
Label(mainFrame, text="  Plugboard : ",bg="#49A",font=('arial', 15, )).grid(row=15,column=0)
plug = Entry(mainFrame, textvariable=plugb,font=('arial', 15, ),width=10,fg="gray", bg="white", bd=0,justify=LEFT).grid(row=15,column=1)


saveBtn() #initializing default setting in system
window.config(bg="#49A",menu=menubar)
window.mainloop()
