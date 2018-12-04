from tkinter import *
import tkinter.filedialog as fdialog
import random


class MainFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.subframe = None
        #main menu
        self.CreateMenu(root)
        #create screen
        self.frames=self.CreateFrames()
        # make answers to questions list
        self.CreateCheckList()
        self.CreateQuestion()
        self.CreateAnswer()
        self.CreateResults()
        #scale full screen
        self.grid(row=0, column=0, sticky=(N, S, W, E))
        self.AllRowColFlexible(self, root)
        self.grid_rowconfigure(2, weight=0)
        #stubs
        self.RegisterListener()


    def CreateMenu(self, root):
        #master
        menu=Menu(root)
        #first level
        testmenu=Menu(menu, tearoff=0)
        aboutmenu = Menu(menu, tearoff=0)
        #sublevel
        menu.add_cascade(label='Тест', menu=testmenu)
        menu.add_cascade(label='Про програму', menu=aboutmenu)
        testmenu.add_command(label='Відкрити тест', command=self.OpenFileMenu)
        testmenu.add_command(label='Запамʼятати результати тестування', command=self.SaveFileMenu)
        testmenu.add_command(label='Вихід', command=root.quit)
        aboutmenu.add_command(label='Інформація', command=None)
        root.config(menu=menu)


    def OpenFileMenu(self):
        self.file=fdialog.askopenfile()

    def SaveFileMenu(self):
        self.file = fdialog.asksaveasfile()


    def CreateFrames(self):
        qw = Frame(self, bd=1, relief=SUNKEN)
        qw.grid(row=0, column=0, rowspan=2, sticky=(N,S,E,W))
        ts = Frame(self, bd=1, relief=SUNKEN)
        ts.grid(row=0, column=1, sticky=(N,S,E,W))
        aw = Frame(self, bd=1, relief=SUNKEN)
        aw.grid(row=1, column=1, sticky=(N,S,E,W))
        rs = Frame(self, bd=1, relief=SUNKEN)
        rs.grid(row=2, column=0, columnspan=2, sticky=(N,S,E,W))
        return {'question' : qw, 'test' : ts, 'answer' : aw, 'result' : rs}



    def CreateCheckList(self):
        Label(self.frames['test'], text='Вiдповiдi', fg='green').grid(row=0, column=0, sticky=(N, W))
        Button(self.frames['test'], text='  Вiдповiсти ', command=self.Answer).grid(row=2, column=0, sticky=(N,W),padx=(10, 10), pady=(30, 10))
        self.subframe = Frame(self.frames['test'])
        self.subframe.grid(row=1, column=0, sticky=(N, W, S, E))
        # scale to full screen (flex)
        self.AllRowColFlexible(self.frames['test'])
        # special case (not flex)
        self.frames['test'].grid_rowconfigure(0, weight=0)
        self.frames['test'].grid_columnconfigure(0, weight=0)
        self.frames['test'].grid_rowconfigure(2, weight=0)


    def SetCheckList(self, data=[], check=True):
        #clear frame
        self.ClearSubFrame(self.subframe)
        result_set = []
        result = IntVar(0)
        for i, dat in enumerate(data):
            Label(self.subframe, text=dat).grid(row=i, column=1, sticky=(N, W))
            #tkinter type to link with check-radio
            r=IntVar(0)
            result_set.append(r)
            if check:
                Checkbutton(self.subframe, variable=r).grid(row=i, column=0, sticky=(N, S, E, W))
            else:
                Radiobutton(self.subframe, variable=result, value=i+1).grid(row=i, column=0, sticky=(N, S, E, W))
        self.results=result_set if check else result


    def ClearSubFrame(self, sf):
        children=sf.grid_slaves()
        for child in children:
            child.grid_forget()
            child.destroy()


    def CreateQuestion(self):
        Label(self.frames['question'], text='Питання', fg='green').grid(row=0, column=0, sticky=(N, W))
        self.AllRowColFlexible(self.frames['question'])
        # special case (not flex)
        self.frames['question'].grid_rowconfigure(0, weight=0)
        self.qwest_message=Message(self.frames['question'], text=' '*400, width=250, anchor=N)
        self.qwest_message.grid(row=1, column=0, sticky=(N, S, W, E))


    def SetQuestion(self, data='', image=None):
        data = data.center(400, ' ')
        self.qwest_message['text'] = data
        if image:
            pass
        self.EnableNextButton(False)


    def CreateAnswer(self, data=''):
        Label(self.frames['answer'], text='Правiльна вiдповiдь', fg='green').grid(row=0, column=0, columnspan=2,sticky=(N, W))
        self.next_button=Button(self.frames['answer'], text='Продовжити', state=DISABLED, command=self.Next)
        self.next_button.grid(row=2, column=0, sticky=(S, W, N, E), padx=(10, 10),pady=(20, 10))
        self.skip_button=Button(self.frames['answer'], text='Пропустити', command=self.Skip)
        self.skip_button.grid(row=2, column=1, sticky=(S, W, N, E), padx=(10, 10),pady=(20, 10))
        self.AllRowColFlexible(self.frames['answer'])
        self.frames['answer'].grid_rowconfigure(2, weight=0)
        self.answ_message = Message(self.frames['answer'], text=' '*200, width=200, anchor=N)
        self.answ_message.grid(row=1, column=0, columnspan=2, sticky=(N, W))


    def SetAnswer(self, data=''):
        if data:
            self.EnableNextButton(True)
        data = data.center(200, ' ')
        self.answ_message['text'] = data



    def EnableNextButton(self, st):
        self.next_button.configure(state=NORMAL if st else DISABLED)

    def EnableSkipButton(self, st):
            self.skip_button.configure(state=NORMAL if st else DISABLED)


    def CreateResults(self):
        Label(self.frames['result'], text='Результати').grid(row=0, column=0, sticky=(N, W, S))
        self.AllRowColFlexible(self.frames['result'])
        self.frames['result'].grid_rowconfigure(2, weight=0)



    def AllRowColFlexible(self, *frames, **allframes):
        if allframes:
            frames=list(allframes.values())
        for frame in frames:
            cols, rows =frame.grid_size()
            for i in range(rows):
                frame.grid_rowconfigure(i, weight=1)
            for i in range(cols):
                frame.grid_columnconfigure(i, weight=1)


    def RegisterListener(self, answer=None, next=None, skip=None):
        self.answer=answer
        self.skip=skip
        self.next=next


    def Answer(self):
        if self.CheckFilledResult():
            if self.skip: self.answer(self)

    def Skip(self):
        if self.skip: self.skip(self)

    def Next(self):
        if self.next: self.next(self)

    def GetResults(self):
        try:
            if type(self.results)==list:
                return list(map(IntVar.get, self.results))
            else: return self.results.get()
        except AttributeError:
            return 0

    def CheckFilledResult(self):
        res=self.GetResults()
        if type(res)==int:
            res=[res]
        if sum(res)==0:
            return False
        else:
            return True


main_frame=None
def StartGUI(answer=None, next=None, skip=None):
    root=Tk()
    root.title('Тестування для ліцеїстів')
    root.geometry('700x500')
    global main_frame
    main_frame=MainFrame(root)
    main_frame.RegisterListener(answer, next, skip)
    mainloop()






def Test(self):
    questions=[(('Почему все вот так?'), ('Когда?', 'Где?', 'Что?', 'Когда?', 'Где?', 'Что?')),
               (('Зачем и почему все вот так?'), ('Где?', 'Что?', 'Когда?', 'Где?', 'Что?')),
               (('Зачем козлу борода и почему все вот так?'), ('И чо?', 'Что?', 'Где?', 'Что?', 'Когда?', 'Где?', 'Что?')),
               (('Почему все вот так, а не так и все вот так, а не сяк или Почему все вот так, а не так и все вот так, а не сяк?'),
                     ('Когда?', 'Где?', 'Что?', 'Когда?', 'Где?', 'Что?', 'Когда?', 'Где?', 'Что?'))]
    mode=[True, True, False, False]
    random.shuffle(mode)
    random.shuffle(questions)
    self.SetCheckList(questions[0][1], mode[0])
    self.SetQuestion(questions[0][0])
    self.SetAnswer()

def Test1(self):
    answer=['Глупо ', 'Тупо ', 'Умно ', 'Нудно ']
    random.shuffle(answer)
    str_res=self.GetResults()
    self.SetAnswer(answer[0]+str(str_res))






if __name__=='__main__':
    StartGUI(answer=Test1, next=Test, skip=Test)

