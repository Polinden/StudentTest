from tkinter import *
import tkinter.filedialog as fdialog
import random


class MainFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
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
        self.test_menu=testmenu=Menu(menu, tearoff=0)
        aboutmenu = Menu(menu, tearoff=0)
        #sublevel
        menu.add_cascade(label='Тест', menu=testmenu)
        menu.add_cascade(label='Про програму', menu=aboutmenu)
        testmenu.add_command(label='Відкрити тест', command=self.OpenFileMenu)
        testmenu.add_command(label='Запамʼятати результати тестування', command=self.SaveFileMenu, state=DISABLED)
        testmenu.add_command(label='Вихід', command=root.quit)
        aboutmenu.add_command(label='Інформація', command=None)
        root.config(menu=menu)


    def CreateFrames(self):
        qw = Frame(self, bd=1, relief=SUNKEN)
        qw.grid(row=0, column=0, rowspan=2, sticky=(N,S,E,W))
        ts = Frame(self, bd=1, relief=SUNKEN)
        ts.grid(row=0, column=1, sticky=(N,S,E,W))
        aw = Frame(self, bd=1, relief=SUNKEN)
        aw.grid(row=1, column=1, sticky=(N,S,E,W))
        rs = Frame(self, bd=1, relief=SUNKEN)
        rs.grid(row=2, column=0, columnspan=2, sticky=(N,S,E,W))
        sf = Frame(ts)
        sf.grid(row=1, column=0, sticky=(N, W, S, E))
        return {'question' : qw, 'test' : ts, 'answer' : aw, 'result' : rs, 'subframe':sf}



    def CreateCheckList(self):
        Label(self.frames['test'], text='Вiдповiдi', fg='green').grid(row=0, column=0, sticky=(N, W))
        self.answer_button=Button(self.frames['test'], text='  Вiдповiсти ', state=DISABLED, command=self.Answer)
        self.answer_button.grid(row=2, column=0, sticky=(N,W),padx=(10, 10), pady=(30, 10))
        # scale to full screen (flex)
        self.AllRowColFlexible(self.frames['test'])
        # special case (not flex)
        self.frames['test'].grid_rowconfigure(0, weight=0)
        self.frames['test'].grid_rowconfigure(2, weight=0)


    def ClearSubFrame(self, sf):
        children=sf.grid_slaves()
        for child in children:
            child.destroy()


    def CreateQuestion(self):
        self.question_lable=Label(self.frames['question'], text='Питання', fg='green')
        self.question_lable.grid(row=0, column=0, sticky=(N, W))
        self.AllRowColFlexible(self.frames['question'])
        # special case (not flex)
        self.frames['question'].grid_rowconfigure(0, weight=0)
        self.qwest_message=Message(self.frames['question'], text=' '*400, width=250, anchor=N)
        self.qwest_message.grid(row=1, column=0, sticky=(N, S, W, E))


    def CreateAnswer(self, data=''):
        Label(self.frames['answer'], text='Правильна вiдповiдь', fg='green').grid(row=0, column=0, columnspan=2,sticky=(N, W))
        self.next_button=Button(self.frames['answer'], text='Продовжити', state=DISABLED, command=self.Next)
        self.next_button.grid(row=2, column=0, sticky=(S, W, N, E), padx=(10, 10),pady=(20, 10))
        self.skip_button=Button(self.frames['answer'], text='Пропустити', state=DISABLED, command=self.Skip)
        self.skip_button.grid(row=2, column=1, sticky=(S, W, N, E), padx=(10, 10),pady=(20, 10))
        self.AllRowColFlexible(self.frames['answer'])
        self.frames['answer'].grid_rowconfigure(2, weight=0)
        self.answ_message = Message(self.frames['answer'], text=' '*200, width=200, anchor=N)
        self.answ_message.grid(row=1, column=0, columnspan=2, sticky=(N, W))



    def SetCheckList(self, data=[], check=True):
        #clear frame
        self.ClearSubFrame(self.frames['subframe'])
        result_set = []
        result = IntVar(0)
        for i, dat in enumerate(data):
            Label(self.frames['subframe'], text=dat).grid(row=i, column=1, sticky=(N, W))
            #tkinter type to link with check-radio
            r=IntVar(0)
            result_set.append(r)
            if check:
                Checkbutton(self.frames['subframe'], variable=r).grid(row=i, column=0, sticky=(N, S, E, W))
            else:
                Radiobutton(self.frames['subframe'], variable=result, value=i+1).grid(row=i, column=0, sticky=(N, S, E, W))
        self.results=result_set if check else result
        self.EnableSkipButton(bool(data))
        self.EnableAnswertButton(bool(data))


    def SetQuestion(self, data='', image=None):
        data = data.center(400, ' ')
        self.FinalViewOfQuestionFrame(False)
        self.qwest_message['text'] = data
        if image:
            pass

    def SetAnswer(self, data=''):
        self.EnableNextButton(bool(data))
        if data:
            self.EnableAnswertButton(False)
            self.EnableSkipButton(False)
        data = data.center(200, ' ')
        self.answ_message['text'] = data


    def SetFinalInfo(self, data=''):
        self.SetCheckList()
        self.SetAnswer()
        self.SetQuestion(data)
        self.FinalViewOfQuestionFrame(True)
        self.test_menu.entryconfigure(1, state=NORMAL)


    def FinalViewOfQuestionFrame(self, st):
        if st:
            self.question_lable['text'] = 'Ваши реузльтаты теста'
            self.question_lable['fg'] = 'red'
        else:
            self.question_lable['text'] = 'Питання'
            self.question_lable['fg'] = 'green'


    def EnableNextButton(self, st):
        self.next_button.configure(state=NORMAL if st else DISABLED)

    def EnableSkipButton(self, st):
            self.skip_button.configure(state=NORMAL if st else DISABLED)

    def EnableAnswertButton(self, st):
        self.answer_button.configure(state=NORMAL if st else DISABLED)

    def CreateResults(self):
        Label(self.frames['result'], text='Результати').grid(row=0, column=0, sticky=(N, W, S))
        self.AllRowColFlexible(self.frames['result'])
        self.frames['result'].grid_rowconfigure(2, weight=0)



    def AllRowColFlexible(self, *frames):
        for frame in frames:
            cols, rows =frame.grid_size()
            for i in range(rows):
                frame.grid_rowconfigure(i, weight=1)
            for i in range(cols):
                frame.grid_columnconfigure(i, weight=1)


    def RegisterListener(self, answer=None, next=None, skip=None, open=None, save=None):
        self.answer=answer
        self.skip=skip
        self.next=next
        self.open=open
        self.save=save


    def OpenFileMenu(self):
        file=fdialog.askopenfile(filetypes=[('Xml files', '.xml')], title='Вiдкрити файл з тестом')
        if file:
            with file:
                self.Open(file)

    def SaveFileMenu(self):
        file = fdialog.asksaveasfile(filetypes=[('Txt files', '.txt')], title='Обрати файл з результатом')
        if file:
            with file:
                self.Save(file)


    def Answer(self):
        if self.CheckFilledResult():
            if self.answer: self.answer(self)

    def Skip(self):
        if self.skip: self.skip(self)

    def Next(self):
        if self.next: self.next(self)

    def Open(self, file):
        if self.open: self.open(self, file)

    def Save(self, file):
        if self.save: self.save(self, file)


    def GetResults(self):
        try:
            return list(map(IntVar.get, self.results)) if isinstance(self.results, list) else self.results.get()
        except AttributeError:
            return 0

    def CheckFilledResult(self):
        res=self.GetResults()
        if isinstance(res, int):
            res=[res]
        if sum(res)==0:
            return False
        else:
            return True


#thisd is an entry point
#only give it your listeners
def StartGUI(answer=None, next=None, skip=None, open=None, save=None):
    root=Tk()
    root.title('Тестування для ліцеїстів')
    root.geometry('700x500')
    main_frame=MainFrame(root)
    main_frame.RegisterListener(answer, next, skip, open, save)
    mainloop()





###############
#For Tests Only
###############

def Test_Question(mf):
    r = random.randint(0, 10)
    if r>7:
        mf.SetFinalInfo(' Вы вааще не правы!')
        return
    questions=[(('Почему все вот так, а у рыбы хвост?'), ('Когда?', 'Где?', 'Что?', 'Когда?', 'Где?', 'Что?')),
               (('Зачем и почему все вот так, учишь-учшиь, а ничего не понимаешь?'), ('Где?', 'Что?', 'Когда?', 'Где?', 'Что?')),
               (('Зачем козлу борода и почему все вот так?'), ('И чо?', 'Что?', 'Где?', 'Что?', 'Когда?', 'Где?', 'Что?')),
               (('Почему все вот так, а не так и все вот так, а не сяк или Почему все вот так, а не так и все вот так, а не сяк?'),
                     ('Когда?', 'Где?', 'Что?', 'Когда?', 'Где?', 'Что?', 'Когда?', 'Где?', 'Что?'))]
    mode=[True, True, False, False]
    random.shuffle(mode)
    random.shuffle(questions)
    mf.SetCheckList(questions[0][1], mode[0])
    mf.SetQuestion(questions[0][0])
    mf.SetAnswer()

def Test_Answer(mf):
    answer=['Глупо ', 'Тупо ', 'Умно ', 'Нудно ']
    random.shuffle(answer)
    str_res=mf.GetResults()
    mf.SetAnswer(answer[0]+str(str_res))


def Test_Open(mf, file):
    print(file)
    Test_Question(mf)

def Test_Save(mf, file):
    print(file)
    file.write('Ну вы и натестировали!...')


if __name__=='__main__':
    StartGUI(answer=Test_Answer, next=Test_Question, skip=Test_Question, open=Test_Open, save=Test_Save)
