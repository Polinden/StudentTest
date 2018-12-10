import xml.etree.ElementTree as ET


class DataControl:

   def __init__(self):
        self.data=[]
        self.cur_dat=None
        self.answer_stat=[]


   def XMLParser(self, file):
        tree = ET.parse(file)
        root = tree.getroot()        
        d=[[grandchild for grandchild in child] for child in root]
        get_text=lambda ch: [gch.text for gch in ch] if len(ch)>0 else ch.text  
        self.data=[[*map(get_text, child)] for child in d]

   def StartTest(self, mf, file):
        self.XMLParser(file)
        self.answer_stat=[]
        self.KeepOnTest(mf)

 
   def KeepOnTest(self, mf):
        if len(self.data)==0:
           #finish
           ok_aw, notok_aw=self.answer_stat.count(True), self.answer_stat.count(False)
           mf.SetFinalInfo('You have got {} right answer form {}'.format(ok_aw, notok_aw+ok_aw))
        else:
           self.cur_dat= self.data.pop()
           mf.SetAnswer()
           mf.SetQuestion(self.cur_dat[0], image=self.cur_dat[1])
           mf.SetCheckList(self.cur_dat[3], self.cur_dat[2].lower()=='yes') 

           
   def Answer(self, mf):
       right_text='; '.join([self.cur_dat[3][int(i)-1] for i in self.cur_dat[4]])     
       mf.SetAnswer(right_text)
       res=mf.GetResults()     
       if isinstance(res, list): 
          res=[i+1 for i,_ in enumerate(res) if _>0]
       else: 
          res=[res]  
       #success if  res==right_res!!!
       right_res=[int(i) for i in self.cur_dat[4]]
       self.answer_stat.append(right_res==res)


         
         
         
