import xml.etree.ElementTree as ET
import datetime
import os
import random

class DataControl:
    """
    Controller for the dataflow of application
    Provides listiners for MainWindow
    """

    def __init__(self):
        self.data = []
        self.cur_dat = None
        self.answer_stat = []
        self.dirname = ''

    def XMLParser(self, file):
        """
        Creates the self.data as a list
        self.cur_dat[0] - question itself
        self.cur_dat[1] - image file name
        self.cur_dat[2] - multy (checkboxes) for many possible answers
        self.cur_dat[3] - list of answers to choose
        self.cur_dat[4] - list of right answers indexes (in the list above)
        :param file: XML test file
        """
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            # make TOPLIST (2 dimension)
            # Children are "question. Grandchildren are "text", "imagefile", "multy", ["answers"], ["right answers"]
            toplist = [[grandchild for grandchild in child] for child in root]
            # function to extracts text from grangchildren (if grangchildren is a list, then makes a list of texts)
            get_text = lambda gch: [ggch.text for ggch in gch] if len(gch) > 0 else gch.text
            # apply lambda to the TOPLIST
            self.data = [[*(map(get_text, child))] for child in toplist]
            random.shuffle(self.data)
        except:
            self.data = []

    def StartTest(self, mf, file):
        """
        Opens the test file and starts the show
        :param mf: MainFrame of the window
        :param file: XML file with test
        """
        self.answer_stat = []
        self.XMLParser(file)
        # check for error (try-catch in XMLParser)
        if self.data:
            self.dirname = os.path.dirname(file.name)
            self.KeepOnTest(mf)
        else:
            mf.ErrorMessage('Невірний формат файлу або помилка при його читаннi')

    def KeepOnTest(self, mf):
        """
        Continue the test on Next pressed
        :param mf: MainFrame of the window
        """
        # show status line on every step
        mf.SetResult('Ви пройшли {} питань з {}'.format(len(self.answer_stat), len(self.answer_stat) + len(self.data)))
        # if no more questions then finish
        if len(self.data) == 0:
            ok_aw, notok_aw = self.answer_stat.count(True), self.answer_stat.count(False)
            proc_data = ok_aw / (ok_aw + notok_aw)
            text_data = 'Ви закінчили тестування. Правильних відповідей - {} із {}'.format(ok_aw, notok_aw + ok_aw)
            mf.SetFinalInfo(text_data, proc_data)
        else:
            self.cur_dat = self.data.pop()
            image_path = os.path.join(self.dirname, self.cur_dat[1]) if self.cur_dat[1] else None
            mf.SetQuestion(self.cur_dat[0], image=image_path)
            mf.SetCheckList(self.cur_dat[3], self.cur_dat[2].lower() == 'yes')
            mf.SetAnswer()

    def Answer(self, mf):
        """
        Shows the right answer and evaluates results on Answer pressed
        Keep on statistics in self.answer_stats
        :param mf: MainFrame object
        """
        start_line_symbol = u'\u16EB '
        end_line_symbol = ';' + os.linesep
        # construct the right answer strings
        right_answer_text = end_line_symbol.join(
            [start_line_symbol + self.cur_dat[3][int(i) - 1] for i in self.cur_dat[4]])
        mf.SetAnswer(right_answer_text)
        # get results form MainFrame
        res = mf.GetResults()
        right_res = [*map(int, self.cur_dat[4])]  # convert list of right answers from text to list of int
        # success if  res==right_res!!!
        self.answer_stat.append(right_res == res)

    def SkipTest(self, mf):
        """
        On Skip pressed
        """
        self.answer_stat.append(False)
        self.KeepOnTest(mf)

    def SaveResult(self, mf, file):
        """
        Write results to the file on Save menu
        :param mf: MainFrame
        :param file: file to write. file is oped and closed in the MainFrame using 'with' operator
        """
        if self.answer_stat:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            text = '''     
           Шановний(на) Пан(i)!      
           Ви пройшли тестування {}.
           Ваши результати:
           1) Вірних відповідей- {}
           2) Помилкових відповідей- {}
           '''
            text = text.format(date, self.answer_stat.count(True), self.answer_stat.count(False))
            file.write(text)
