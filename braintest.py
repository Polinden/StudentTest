from interface.MainWindow import StartGUI
from dataflow.MainWorker import DataControl


dc=DataControl()
StartGUI(open=dc.StartTest, next=dc.KeepOnTest, answer=dc.Answer)