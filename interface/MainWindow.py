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
        self.ClearSubFrame(self.frames['subframe'])


    def ClearSubFrame(self, sf):
        children=sf.grid_slaves()
        for child in children:
            child.destroy()



    def CreateQuestion(self):
        self.question_lable=Label(self.frames['question'], text='Питання', fg='green', width=45, anchor=W)
        self.question_lable.grid(row=0, column=0, sticky=(N, W))
        self.image_lable = Label(self.frames['question'])
        self.image_lable.grid(row=1, column=0, sticky=(W, N, E))
        self.qwest_message=Message(self.frames['question'], text=self.fmtQw(), width=350, anchor=N)
        self.qwest_message.grid(row=2, column=0, sticky=(N, S, W, E))
        self.AllRowColFlexible(self.frames['question'])
        # special case (not flex)
        self.frames['question'].grid_rowconfigure(0, weight=0)
        self.frames['question'].grid_rowconfigure(1, weight=0)


    def CreateAnswer(self):
        Label(self.frames['answer'], text='Правильна вiдповiдь', fg='green',  width=45, anchor=W).grid(row=0, column=0, columnspan=2,sticky=(N, W))
        self.next_button=Button(self.frames['answer'], text='Продовжити', state=DISABLED, command=self.Next)
        self.next_button.grid(row=2, column=0, sticky=(S, W, N, E), padx=(10, 10),pady=(20, 10))
        self.skip_button=Button(self.frames['answer'], text='Пропустити', state=DISABLED, command=self.Skip)
        self.skip_button.grid(row=2, column=1, sticky=(S, W, N, E), padx=(10, 10),pady=(20, 10))
        self.answ_message = Message(self.frames['answer'], text=self.fmtQw(), width=350, anchor=NW)
        self.answ_message.grid(row=1, column=0, columnspan=2, sticky=(N, W, E, S))
        self.AllRowColFlexible(self.frames['answer'])
        self.frames['answer'].grid_rowconfigure(2, weight=0)



    def SetCheckList(self, data=None, check=True):
        #clear frame
        self.ClearSubFrame(self.frames['subframe'])
        if not data: return
        result_set, result  = [], IntVar(0)
        for i, dat in enumerate(data):
            Message(self.frames['subframe'], text=self.fmtAw(dat), width=330, anchor=NW).grid(row=i, column=1, sticky=(N, W, E, S))
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
        self.FinalViewOfQuestionFrame(False)
        self.qwest_message['text'] = self.fmtQw(data)
        if image:
            self.image = PhotoImage(file=image)
            self.image_lable['image'] = self.image
        else:
            self.image_lable['image']=''


    def SetAnswer(self, data=''):
        self.EnableNextButton(bool(data))
        if data:
            self.EnableAnswertButton(False)
            self.EnableSkipButton(False)
        self.answ_message['text'] = self.fmtQw(data)


    def SetFinalInfo(self, data='', proc_data=None):
        self.SetCheckList()
        self.SetAnswer()
        self.SetQuestion(data)
        self.FinalViewOfQuestionFrame(True)
        self.test_menu.entryconfigure(1, state=NORMAL)
        self.MakePieChart(proc_data)


    def FinalViewOfQuestionFrame(self, st):
        if st:
            self.question_lable['text'] = 'Ваши реузльтаты теста'
            self.question_lable['fg'] = 'blue'
        else:
            self.question_lable['text'] = 'Питання'
            self.question_lable['fg'] = 'green'


    def MakePieChart(self, proc_data=None):
        grad_won, proc_won = proc_data*360, round(proc_data * 100)
        grad_loss,  proc_loss = 360-grad_won, 100-proc_won
        c = Canvas(self.frames['subframe'], width=340, height=210)
        c.grid(row=0, column=0)
        c.create_text(240, 10, fill='green', text='success={}%'.format(proc_won))
        c.create_text(240, 200, fill='red', text='failour={}%'.format(proc_loss))
        if proc_won and proc_loss:
            start_grad = 90 - grad_won//2
            c.create_arc((170, 30, 320, 180), fill="green", start=start_grad, extent=grad_won)
            c.create_arc((170, 30, 320, 180), fill="red", start=start_grad+grad_won, extent=grad_loss)
        else:
            c.create_oval(170, 30, 320, 180, fill="green" if proc_won else "red")


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

    #format question and answer
    def fmtQw(self, text=''):
        return text[:800]

    def fmtAw(self, text=''):
        return text[:200]


#thisd is an entry point
#only give it your listeners
def StartGUI(answer=None, next=None, skip=None, open=None, save=None):
    root=Tk()
    root.title('Тестування для ліцеїстів')
    root.geometry('1000x550')
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
    mf.SetQuestion(questions[0][0], image='../test_im1.png')
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
