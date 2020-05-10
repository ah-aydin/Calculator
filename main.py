import sys
from PyQt5.QtWidgets import QApplication
from display import Window

def main():
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()
    del window, app
    exit()

if __name__ == '__main__':
    main()
