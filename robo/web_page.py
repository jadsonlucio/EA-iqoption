import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QGridLayout,QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView


class widget_principal(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('Simple')
        self.iniciar_componentes()
        self.show()
    def iniciar_componentes(self):
        self.grid=QGridLayout()

        self.text=QLineEdit()
        self.web_widget=QWebEngineView()
        self.botao_confirm=QPushButton(text="Carregar")
        self.grid.addWidget(self.text,0,0)
        self.grid.addWidget(self.botao_confirm, 0, 1)
        self.grid.addWidget(self.web_widget,1,0)

        self.botao_confirm.clicked.connect(self.carregar_url)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.setLayout(self.grid)

    def carregar_url(self):
        url=self.text.text()
        print(url)
        self.web_widget.showFullScreen()
        self.web_widget.load(QUrl(url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget=widget_principal()
    app.exec_()
    pass