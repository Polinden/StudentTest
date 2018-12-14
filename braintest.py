from interface.MainWindow import StartGUI
from dataflow.MainWorker import DataControl


dc=DataControl()
StartGUI(open=dc.StartTest, skip=dc.SkipTest, next=dc.KeepOnTest, answer=dc.Answer, save=dc.SaveResult)