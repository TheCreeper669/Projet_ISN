from PySide2 import QtCore, QtWidgets, QtGui
from os import system

class MyWidget(QtWidgets.QMainWindow):
	def __init__(self, app, parent= None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.app = app

		#permet de récuperer la taille de l'écran et de resize a la bonne échelle 
		self.screenShape = QtWidgets.QDesktopWidget().screenGeometry()
		self.resize(self.screenShape.width(), self.screenShape.height())
		
		#met une image de fond adapter a la redimensionner a la taille de l'écran
		self.picture = QtGui.QPixmap("./launcher/grotte_fond.bmp") 
		self.picture = self.picture.scaled(self.screenShape.width(), self.screenShape.height(), QtCore.Qt.KeepAspectRatio)
		self.label = QtWidgets.QLabel(self) 
		self.label.setPixmap(self.picture)
		self.label.setScaledContents(True)
		self.label.setGeometry(QtCore.QRect(0, 0, self.screenShape.width(), self.screenShape.height()))

		#création des boutton avec leurs images
		self.buttonPlay = QtWidgets.QPushButton("")
		self.buttonPlay.clicked.connect(self.func_buttonPlay)
		self.buttonPlay.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.buttonPlay.setStyleSheet("QPushButton{			   border-image: url(./launcher/play.png) 0 0 0 0 stretch stretch;  border: 0px; }"
									  "QPushButton:hover:pressed {border-image: url(./launcher/play_click.png) 0 0 0 0 stretch stretch;  border: 0px; }"
									  "QPushButton:hover {		border-image: url(./launcher/play_hover.png) 0 0 0 0 stretch stretch;  border: 0px; }")

		self.buttonPlay.setFixedSize(self.screenShape.width()/6, self.screenShape.height()/12)



		self.buttonQuit = QtWidgets.QPushButton("")
		self.buttonQuit.clicked.connect(self.func_buttonQuit)		
		self.buttonQuit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.buttonQuit.setStyleSheet("QPushButton{			   border-image: url(./launcher/quit.png) 0 0 0 0 stretch stretch;  border: 0px; }"
									  "QPushButton:hover:pressed {border-image: url(./launcher/quit_click.png) 0 0 0 0 stretch stretch;  border: 0px; }"
									  "QPushButton:hover {		border-image: url(./launcher/quit_hover.png) 0 0 0 0 stretch stretch;  border: 0px; }")

		self.buttonQuit.setFixedSize(self.screenShape.width()/6, self.screenShape.height()/12)


		#self.esc = QtWidgets.QShortcut(KeyboardInterrupt)
		#self.esc.activated(exit())
		self.exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.exit)

		self.buttons_layout = QtWidgets.QVBoxLayout()
		self.buttons_layout.addWidget(self.buttonPlay)
		self.buttons_layout.setAlignment(QtCore.Qt.AlignCenter)
		self.buttons_layout.addWidget(self.buttonQuit)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.buttons_layout)

		self.central_widget = QtWidgets.QDialog()
		self.central_widget.setLayout(self.main_layout)
		self.setCentralWidget(self.central_widget)

		self.setWindowIcon(QtGui.QIcon('./launcher/image2.png'))
		self.setWindowTitle("Restez Prudent")

		self.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		



	def closeEvent(self, event):
		event.accept()

	def func_buttonPlay(self):
		#print("buttonPlay")
		self.hide()
		system("play")
		self.exit()

	def func_buttonQuit(self):
		#print("buttonQuit")
		self.exit()

	def exit(self):
		self.app.exit()



def main():
	from sys import argv
	app = QtWidgets.QApplication(argv)
	my_widget = MyWidget(app)
	my_widget.show()
	exit(app.exec_())

if __name__ == "__main__":
	main()


