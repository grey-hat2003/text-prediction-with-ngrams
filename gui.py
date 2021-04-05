from tkinter import *
import ngrams

ngrams.train_markov()

#print(ngrams.transitions)

box = Tk()
box.geometry("400x250")
box.title("N-grams word predictor")


expression = " "
next1 = StringVar()
next2 = StringVar()
next3 = StringVar()

def update(suggest):

    if(len(suggest) == 0):
        next1.set("  -  ")
        next2.set("  -  ")
        next3.set("  -  ")

    elif(len(suggest) == 1):
        next1.set(suggest[0])
        next2.set("  -  ")
        next3.set("  -  ")

    elif(len(suggest) == 2):
        next1.set(suggest[0])
        next2.set(suggest[1])
        next3.set("  -  ")

    else:
        next1.set(suggest[0])
        next2.set(suggest[1])
        next3.set(suggest[2])



def my_tracer(a,b,c):
    #print(a,b,c)
    suggest = []
    expression = str(inputText.get())
    explist = expression.rstrip().lower().split()
    #print(expression)

    if(str(inputText.get()) == ""):
        initword = ngrams.first_words_sort()
        update(initword)

    elif(len(explist) > 0):

        if(expression[-1] == " "):

            if(len(explist) == 1):
                suggest = ngrams.suggestions(explist[0])

            elif(len(explist) >= 2):
                suggest = ngrams.suggestions((explist[-2],explist[-1]))

            print(explist)
            print(suggest)

        update(suggest)


def btnClear():
    global expression
    expression = ""
    inputText.set("")


def btnClick(opr):
    global expression
    expression = str(inputText.get()) + str(opr.get()) + " "
    inputText.set(expression)
    inputField.icursor(END)

def btnAdd():
#    try:
    ngrams.update_corpus(str(inputText.get()))
    #except:
        #print("Ughh")
    txt = str(historyText.get()) + "\n" + str(inputText.get())
    historyText.set(txt)
    inputText.set("")

# DRIVER CODE _______________________________________________________________________________________

inputText = StringVar()
inputText.trace('w', my_tracer)

if(str(inputText.get()) == ""):
    initword = ngrams.first_words_sort()
    update(initword)

inputFrame = Frame(box, width = 400, height = 50)
inputFrame.pack()#side=TOP
inputField = Entry(inputFrame, font = ('calibri', 15, 'bold'), textvariable = inputText, width = 300, bg = "#eee", justify = RIGHT)
inputField.grid(row = 0, column = 0)
inputField.pack(ipady = 10)#pady=10,ipady=10

btnFrame = Frame(box, width = 400, height = 100)
btnFrame.pack()

nextl = StringVar()
nextl.set("Next Word:")
nextLabel = Label(btnFrame, textvariable = nextl, width = 11, height = 2, bd = 0)
nextLabel.grid(row = 1, column = 0, padx = 1, pady = 1)

next1btn = Button(btnFrame, textvariable = next1, width = 13, height = 2, bd = 0, relief = RAISED, borderwidth = 3, command = lambda:btnClick(next1))
next1btn.grid(row = 1, column = 1, padx = 1, pady = 1)

next2btn = Button(btnFrame, textvariable = next2, width = 13, height = 2, bd = 0, relief = RAISED, borderwidth = 3, command = lambda:btnClick(next2))
next2btn.grid(row = 1, column = 2, padx = 1, pady = 1)

next3btn = Button(btnFrame, textvariable = next3, width = 13, height = 2, bd = 0, relief = RAISED, borderwidth = 3, command = lambda:btnClick(next3))
next3btn.grid(row = 1, column = 3, padx = 1, pady = 1)

clear = Button(btnFrame, text = "Clear", width = 25, height = 3, bd = 0, relief = RAISED, borderwidth = 3, command = btnClear)
clear.grid(row = 2, column = 0, columnspan = 2, padx = 1, pady = 1)

add = Button(btnFrame, text = "Add", width = 28, height = 3, bd = 0, relief = RAISED, borderwidth = 3, command = btnAdd)
add.grid(row = 2, column = 2, padx = 1, columnspan = 2, pady = 1)

textFrame = Frame(box, width = 400, height = 20)
textFrame.pack()
historyLabel = Label(textFrame, font = ('calibri', 10, 'bold'), text = "HISTORY")
historyLabel.grid(row = 3, column = 0, pady = (10, 0))
historyText = StringVar()
history = Label(textFrame, textvariable = historyText)
history.grid(row = 4, column = 0)

box.mainloop()