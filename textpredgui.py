from tkinter import *
import textpredmarkov
from gingerit.gingerit import GingerIt

#INITIALIZATIONS
bgcolor = "#71c5c6"#"#44a9ab"#"#071212"#"#183d3d"##"#121212"
fgcolor = "#ffffff"
inpbgcolor = "#d8eff0"#"#204f4f"# "#0d1f20"#"#1f1f1f"
inphlcolor = "#4cb6b8"#"#276162"#"#122d2e"
inpfg = "#000000"
n1color = "#5abcbe"#"#3c9799"
n2color = "#68c1c3"#"#358586"
n3color = "#76c7c9"#"#2e7374"
cacolor = "#44a9ab"
#trains the model before every launch
textpredmarkov.train_markov()
"""
print("----------------Markov Data Model----------------")
print(textpredmarkov.first_words)
print()
print(textpredmarkov.second_words)
print()
print(textpredmarkov.transitions)
"""

box = Tk()
box.geometry("400x250")
box.title("Next word predictor")
box.configure(bg=bgcolor)

expression = ""
next1 = StringVar()
next2 = StringVar()
next3 = StringVar()
historylines = []

def update(suggest):
    if(len(suggest)==0):
        next1.set("  -  ")
        next2.set("  -  ")
        next3.set("  -  ")
    elif(len(suggest)==1):
        next1.set(suggest[0])
        next2.set("  -  ")
        next3.set("  -  ")
    elif(len(suggest)==2):
        next1.set(suggest[0])
        next2.set(suggest[1])
        next3.set("  -  ")
    else:
        next1.set(suggest[0])
        next2.set(suggest[1])
        next3.set(suggest[2])

def my_tracer(a,b,c):
    #print(a,b,c)
    #print(str(inputText.get()))
    suggest = []
    expression = str(inputText.get())
    explist = expression.strip().lower().split()
    if(str(inputText.get())==""):
        initword = textpredmarkov.suggest_first_words()
        update(initword)
    elif(len(explist)>0):
        if(expression[-1]==" "):
            if(len(explist)==1):
                suggest = textpredmarkov.suggestions(explist[0])
            elif(len(explist)>=2):
                suggest = textpredmarkov.suggestions((explist[-2],explist[-1]))
        update(suggest)

def btnClear():
    global expression
    expression = ""
    inputText.set("")

def btnClick(txtvar):
    global expression
    expression = str(inputText.get()) + str(txtvar.get()) + " "
    inputText.set(expression)
    inputField.icursor(END)

def btnAdd():
    sentence = " ".join(str(inputText.get()).split()) #removes extra spaces
    result = GingerIt().parse(sentence) #corrects grammar and spellings
    sentence = str(result['result']).lower() #convert to corpus format
    textpredmarkov.update_corpus(sentence)
    historylines.append(sentence)
    sentences = ""
    if(len(historylines)<=3):
        sentences = "\n".join(historylines[-3:])
    else:
        sentences = ":\n"+"\n".join(historylines[-2:])
    historyText.set(sentences)
    inputText.set("")

inputText = StringVar()
inputText.trace('w', my_tracer)

if(str(inputText.get())==""):
    initword = textpredmarkov.suggest_first_words()
    update(initword)

inputFrame = Frame(box,width=400,height=50)
inputFrame.configure(bg=bgcolor)
inputFrame.pack()
inputField = Entry(inputFrame,font=('arial',10,'bold'),textvariable=inputText,width=300,bg=inpbgcolor,fg=inpfg,justify=RIGHT,relief="raised",bd=0,highlightbackground=inphlcolor,highlightcolor=bgcolor,highlightthickness=3)
inputField.grid(row=0,column=0)
inputField.pack(ipady=10)#pady=10,ipady=10

btnFrame = Frame(box,width=400,height=100)
btnFrame.configure(bg=bgcolor)
btnFrame.pack()

nextl = StringVar()
nextl.set("Next Word:")
nextLabel = Label(btnFrame,textvariable=nextl,font=('arial',9,'bold'),width = 11, height = 2, bd=0, bg=bgcolor, fg=fgcolor)
nextLabel.grid(row = 1, column = 0, padx = 1, pady = 1)

next1btn = Button(btnFrame,textvariable=next1,font=('arial',9,'bold'), width=13,height=2,bd=0, relief = RAISED, borderwidth = 3, command=lambda:btnClick(next1),bg=n1color, fg=fgcolor)
next1btn.grid(row = 1, column = 1, padx = 1, pady = 1)

next2btn = Button(btnFrame,textvariable=next2,font=('arial',9,'bold'), width=13,height=2,bd=0, relief = RAISED, borderwidth = 3, command=lambda:btnClick(next2),bg=n2color, fg=fgcolor)
next2btn.grid(row = 1, column = 2, padx = 1, pady = 1)

next3btn = Button(btnFrame,textvariable=next3,font=('arial',9,'bold'),width=13,height=2,bd=0, relief = RAISED, borderwidth = 3, command=lambda:btnClick(next3),bg=n3color, fg=fgcolor)
next3btn.grid(row = 1, column = 3, padx = 1, pady = 1)

clear = Button(btnFrame,text="Clear",font=('arial',9,'bold'),width=25,height=3,bd=0,relief = RAISED, borderwidth = 3, command=btnClear,bg=cacolor, fg=fgcolor)
clear.grid(row = 2, column=0, columnspan = 2, padx = 1, pady = 1)

add = Button(btnFrame,text="Add",font=('arial',9,'bold'),width=28,height=3,bd=0,relief = RAISED, borderwidth = 3, command=btnAdd,bg=cacolor, fg=fgcolor)
add.grid(row = 2, column=2, padx = 1, columnspan = 2, pady = 1)

textFrame = Frame(box,width=400,height=20)
textFrame.configure(bg=bgcolor)
textFrame.pack()
historyLabel = Label(textFrame,font=('arial',10,'bold'),text="History",bg=bgcolor, fg=fgcolor)
historyLabel.grid(row=3,column=0,pady=(10,0))
historyText = StringVar()
history = Label(textFrame,textvariable=historyText,bg=bgcolor, fg=fgcolor)
history.grid(row=4,column=0)

box.mainloop()