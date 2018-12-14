from tkinter import *
import tkinter.filedialog as fdialog
import tkinter.messagebox as mbox
import textwrap
import webbrowser




class MainFrame(Frame):
    """
    MainFrame - the first ordered container for the widgets
    To be created and gets Listeners for RegisterListeners
    """

    def __init__(self, root):
        Frame.__init__(self, root)
        #makes main menu
        self.CreateMenu(root)
        self.root=root
        #create all frames
        self.frames=self.CreateFrames()
        # creates empty widgets (with no text)
        self.CreateCheckList()
        self.CreateQuestion()
        self.CreateAnswer()
        self.CreateResults()
        #scale to full screen
        self.grid(row=0, column=0, sticky=(N, S, W, E))
        self.AllRowColFlexible(self, root)
        self.grid_rowconfigure(2, weight=0)
        #register None listeners - stub
        self.RegisterListener()



    def CreateMenu(self, root):
        #basement
        menu=Menu(root)
        #first level
        self.test_menu=testmenu=Menu(menu, tearoff=0)
        aboutmenu = Menu(menu, tearoff=0)
        #second level
        menu.add_cascade(label='Тест', menu=testmenu)
        menu.add_cascade(label='Про програму', menu=aboutmenu)
        testmenu.add_command(label='Відкрити тест', command=self.OpenFileMenu)
        testmenu.add_command(label='Запамʼятати результати тестування', command=self.SaveFileMenu, state=DISABLED)
        testmenu.add_command(label='Вихід', command=root.quit)
        aboutmenu.add_command(label='Інформація', command=self.InfoDialog)
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
        """
        remove all widgets from the frame.
        clean and neat frame will be reused for answers list and checkboxes
        :param sf: frame object
        """
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


    def CreateResults(self):
        self.res_label=Label(self.frames['result'], text='Для початку тестування оберить файл (в меню)')
        self.res_label.grid(row=0, column=0, sticky=(N, W, S))
        self.AllRowColFlexible(self.frames['result'])
        self.frames['result'].grid_rowconfigure(2, weight=0)


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


    def SetResult(self, data=''):
        self.res_label['text'] = data


    def SetFinalInfo(self, data='', proc_data=None):
        self.SetCheckList()
        self.SetAnswer(' ')
        self.SetQuestion(data)
        self.EnableNextButton(False)
        self.FinalViewOfQuestionFrame(True)
        self.test_menu.entryconfigure(1, state=NORMAL)
        self.MakePieChart(proc_data)


    def FinalViewOfQuestionFrame(self, st):
        if st:
            self.question_lable['text'] = 'Ваші результати тестування'
            self.question_lable['fg'] = 'blue'
        else:
            self.question_lable['text'] = 'Питання'
            self.question_lable['fg'] = 'green'


    def MakePieChart(self, proc_data=None):
        grad_won, proc_won = proc_data*360, round(proc_data * 100)
        grad_loss,  proc_loss = 360-grad_won, 100-proc_won
        c = Canvas(self.frames['subframe'], width=340, height=210)
        c.grid(row=0, column=0)
        c.create_text(240, 10, fill='green', text='правильно={}%'.format(proc_won))
        c.create_text(240, 200, fill='red', text='помилок={}%'.format(proc_loss))
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



    def AllRowColFlexible(self, *frames):
        """
        Sets weights=1 to all children of the frame
        It is necessary for responsible growing of the window
        :param frames list of frames
        """
        for frame in frames:
            cols, rows =frame.grid_size()
            for i in range(rows):
                frame.grid_rowconfigure(i, weight=1)
            for i in range(cols):
                frame.grid_columnconfigure(i, weight=1)


    def RegisterListener(self, answer=None, next=None, skip=None, open=None, save=None):
        """
        Main connector to plug in the listeners to Buttons And Menu commands
        """
        self.answer, self.skip, self.next, self.open, self.save = answer, skip, next, open, save


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

    def InfoDialog(self):
        text='''
        Використовуйте файл тесту у форматi XML.
        Картинки покладiть в тому ж каталозi що й файл з тестом.
        Краще перевiрьте файл, за допомогою сервiсiв, 
        наприклад:  https://www.freeformatter.com. 
        Схема файлу додається: text.xsd'''
        text=textwrap.dedent(text)  #get rid of left indent it the text
        top = Toplevel(self)        #show dialog - copied from stackoferflow
        x, y = self.root.winfo_x(), self.root.winfo_y()
        top.geometry("+{}+{}".format(x + 280, y + 120)) # put it slightly right and down from root
        top.title("Про програму...")
        Message(top, text=text, justify=LEFT, anchor=NW, width=600).grid(row=0, column=0, columnspan=2, padx=30)
        run=lambda: webbrowser.open_new('https://www.freeformatter.com/xml-validator-xsd.html')
        Button(top, text="Вихiд".center(14, ' '), command=top.destroy).grid(row=1, column=0, pady=10, padx=40)
        Button(top, text="Перевiрити", command=run).grid(row=1, column=1, pady=10, padx=20)



    def GetResults(self):
        """
        Gets IntVars List for checkbox OR IntVar single variable for radiobuttons from self.results
        Then extract int values using IntVar.get()
        For checkbox creates the List of index numbers (shows which boxes are cheched).
        For radio the List with only with one integer shows which radio is selected
        :return: the List
        """
        try:
            if isinstance(self.results, list):
                checkbox_cheked_list = [*map(IntVar.get, self.results)]
                return [i + 1 for i, j in enumerate(checkbox_cheked_list) if j > 0]
            else:
                return [self.results.get()]   #if radiobutons
        except AttributeError:
            return []                         #if results are not ready for some unknown reasons



    def CheckFilledResult(self):
        """
        Checks if we selected any answer
        it is used to enable Answer button
        :return: true if selected or false if we didn't touch answers
        """
        res=self.GetResults()
        return sum(res)!=0


    #format question and answer
    #cut of too long lines
    def fmtQw(self, text=''):
        return text[:800]

    def fmtAw(self, text=''):
        return text[:200]

    def ErrorMessage(self, text=''):
        mbox.showerror("Увага", message='Помилка', detail=text)



def StartGUI(answer=None, next=None, skip=None, open=None, save=None):
    """
    The entry point to the MainWindow
    Creates a window (tkinter)
    And MainFrame on top of it
    Then register Listeners for MainFram
    Finally stats the loop of events
    :param answer, next, skip open, save are all listeners
    """
    root=Tk()
    root.title('Тестування для ліцеїстів')
    root.geometry('1000x550+150+150')
    main_frame=MainFrame(root)
    main_frame.RegisterListener(answer, next, skip, open, save)
    mainloop()





