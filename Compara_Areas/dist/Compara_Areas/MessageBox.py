from PyQt5.QtWidgets import QMessageBox , QFileDialog


class MessageBox():

    def Mensagem(mensagem,titulo,tipo,botoes):
        msgBox = QMessageBox()
        msgBox.setIcon(tipo)
        msgBox.setText(mensagem)
        msgBox.setWindowTitle(titulo)
        msgBox.setStandardButtons(botoes)
        returnValue = msgBox.exec()