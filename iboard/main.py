import sys
from custome_errors import *
sys.excepthook = my_excepthook
from fpdf import fpdf
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.pages=[""]
        self.content=qt.QTextEdit()
        self.content.textChanged.connect(self.onTextChanged)
        layout.addWidget(self.content)
        self.index=0

        self.setting=guiTools.QPushButton(_("settings"))
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        pageMenu=mb.addMenu(_("page"))
        newPageAction=qt1.QAction(_("new page"),self)
        pageMenu.addAction(newPageAction)
        newPageAction.triggered.connect(self.onNewPage)
        newPageAction.setShortcut("ctrl+n")
        nextPageAction=qt1.QAction(_("next page"),self)
        pageMenu.addAction(nextPageAction)
        nextPageAction.triggered.connect(self.onNextPage)
        nextPageAction.setShortcut("alt+right")
        previousPageAction=qt1.QAction(_("previous page"),self)
        pageMenu.addAction(previousPageAction)
        previousPageAction.triggered.connect(self.onPreviousPage)
        previousPageAction.setShortcut("alt+left")
        deleteCurrentPageAction=qt1.QAction(_("delete current page"),self)
        pageMenu.addAction(deleteCurrentPageAction)
        deleteCurrentPageAction.triggered.connect(self.onDeleteCurrentPage)
        deleteCurrentPageAction.setShortcut("alt+delete")
        saveAsPDFAction=qt1.QAction(_("export as pdf file"),self)
        pageMenu.addAction(saveAsPDFAction)
        saveAsPDFAction.triggered.connect(self.on_save)
        saveAsPDFAction.setShortcut("ctrl+s")
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def onTextChanged(self):
        self.pages[self.index]=self.content.toPlainText()
    def onNewPage(self):
        self.pages.append("")
        self.index=len(self.pages)-1
        self.content.setText(self.pages[self.index])
    def onNextPage(self):
        if self.index==len(self.pages)-1:
            self.index=0
        else:
            self.index+=1
        guiTools.speak(str(self.index+1))
        self.content.setText(self.pages[self.index])
    def onPreviousPage(self):
        if self.index==0:
            self.index=len(self.pages)-1
        else:
            self.index-=1
        guiTools.speak(str(self.index+1))
        self.content.setText(self.pages[self.index])
    def onDeleteCurrentPage(self):
        if self.index==0:
            guiTools.speak(_("can't delete this page"))
        else:
            self.pages.pop(self.index)
            self.onPreviousPage()
            guiTools.speak(_("page deleted"))
    def on_save(self):
        pdf=fpdf.FPDF()
        pdf.add_page()
        for page in self.pages:
            
            pdf.set_font(family="Arial")
            pdf.cell(h=500,w=500,txt=page)
        file=qt.QFileDialog(self)
        file.setAcceptMode(file.AcceptMode.AcceptSave)
        if file.exec()==file.DialogCode.Accepted:
            pdf.output(file.selectedFiles()[0])
            qt.QMessageBox.information(self,_("done"),_("saved"))

App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()