import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, Qt

from calculations import solve

class Window(QWidget):

    sc_window = """
        background-color: rgb(31, 31, 31);
        color: rgb(255, 255, 255);
    """

    sc_button = """
    QPushButton {
        background-color: rgb(52, 52, 52);
        color: rgb(255, 255, 255);
    }
    QPushButton:hover {
        background-color: rgb(71, 71, 71);
    }
    """

    def __init__(self):
        super().__init__()

        self.initUI()

        self.setWindowTitle('Calculator')
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        self.setStyleSheet(self.sc_window)
        self.show()

    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(2,2,2,2)
        mainLayout.setSpacing(0)

        mainLayout.addLayout(self.getOutputLayout())
        mainLayout.addLayout(self.getButtonGrid())
        self.setLayout(mainLayout)

    # Creates and returns a grid of the required buttons
    def getButtonGrid(self):
        # Defining the button layout
        btn_layout = [ 'CE', 'C', QIcon('left_arrow.png'), '/',
                    '7', '8', '9', '*',
                    '4', '5', '6', '-',
                    '1', '2', '3', '+',
                    '+/-', '0', '.', '=',]
        # Generating the positions of every button
        positions = [(i,j) for i in range(5) for j in range(4)]

        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.setSpacing(0)
        # Placing each button in the btn_layout into the grid according to its position
        for btn, pos  in zip(btn_layout, positions):
            self.addButton(grid, btn, pos)

        return grid

    # Add the button to the given layout at position pos
    def addButton(self, layout, content, pos):
        button = QPushButton()
        button.setFixedSize(100, 60)
        button.setFont(QFont('Consolas', 16))
        button.setStyleSheet(self.sc_button)
        # Checking the the button will contain text or icon
        if type(content) == QIcon:
            button.setIcon(content)
            button.setIconSize(QSize(50, 50))
            button.clicked.connect(self.backspace)
        else:
            button.setText(content)
            if content in [str(x) for x in range(10)] + ['.']:
                button.clicked.connect(lambda: self.processNumber(content))
            elif content in ['+', '-', '*', '/', '=', '+/-']:
                button.clicked.connect(lambda: self.processOperator(content))
            else:
                button.clicked.connect(lambda: self.clearOperator(content))

        layout.addWidget(button, *pos)

    def getOutputLayout(self):
        outputLayout = QVBoxLayout()

        # This string will contain the ecuation
        # It will be used in order to not display the last operator at the ecuationLabel
        self.ecuationText = ''
        # This label will contain the whole ecuation
        self.ecuationLabel = QLabel('')
        self.ecuationLabel.setFont(QFont('Consolas', 12))
        self.ecuationLabel.setFixedHeight(30)
        self.ecuationLabel.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        # This label will display the latest operator
        self.operatorLabel = QLabel('')
        self.operatorLabel.setFont(QFont('Consolas', 9))
        self.operatorLabel.setFixedHeight(10)
        self.operatorLabel.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        # This label will display the input from the buttons
        self.inputLabel = QLabel('0')
        self.inputLabel.setFont(QFont('Consolas', 16))
        self.inputLabel.setFixedHeight(50)
        self.inputLabel.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        outputLayout.addWidget(self.ecuationLabel)
        outputLayout.addWidget(self.operatorLabel)
        outputLayout.addWidget(self.inputLabel)

        return outputLayout

    def processNumber(self, val):
        if self.inputLabel.text() == '0':
            self.inputLabel.setText(val)
            return
        self.inputLabel.setText(self.inputLabel.text() + val)

    def processOperator(self, val):
        # Solve the ecuation
        if val == '=':
            # Handle the inputLabel if there is a number there
            if self.inputLabel.text() != '0':
                self.ecuationText += self.inputLabel.text()
            else:
                self.ecuationText = self.ecuationText[:-1]

            # Split the ecuationText into it's components
            number = ''
            negative = False
            ecuation_arr = []
            for c in self.ecuationText: # c = character
                if c in ['+', '-', '*', '/']:
                    if number == '' and c == '-':
                        negative = True
                        continue
                    if negative:
                        ecuation_arr.append(-float(number))
                    else:
                        ecuation_arr.append(float(number))
                    negative = False
                    ecuation_arr.append(c)
                    number = ''
                    continue
                number += c
            ecuation_arr.append(float(number))
            # Reset all the labels and the ecuation text
            self.ecuationText = ''
            self.ecuationLabel.clear()
            self.operatorLabel.clear()
            self.inputLabel.setText(str(solve(ecuation_arr))) # Show the result

        # If the input is either empty or the last character is not a digit
        # do not execute the operator
        if len(self.inputLabel.text()) == 0 or not self.inputLabel.text()[-1].isdigit():
            return
        if val in ['+', '-', '*', '/']:
            # Change the operator label to the given oprator
            self.operatorLabel.setText(val)
            # Update the ecuation
            self.ecuationText += self.inputLabel.text() + val
            self.ecuationLabel.setText(self.ecuationText[:-1])
            # Reset the input label
            self.inputLabel.setText('0')

        if val == '+/-':
            self.inputLabel.setText(str(-float(self.inputLabel.text())))

    def clearOperator(self, val):
        if val == 'CE':
            self.ecuationText = ''
            self.ecuationLabel.clear()
            self.inputLabel.setText('0')
            self.operatorLabel.clear()
        if val == 'C':
            self.inputLabel.setText('0')

    def backspace(self):
        if len(self.inputLabel.text()) == 0:
            return
        self.inputLabel.setText(self.inputLabel.text()[:-1])
        if self.inputLabel.text() == '':
            self.inputLabel.setText('0')
