import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        self.temp = 0;
        self.operator = ""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QGridLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_operation = QGridLayout()
        layout_clear_equal = QGridLayout()
        layout_number = QGridLayout()
        layout_other_operation = QGridLayout()
        layout_equation_solution = QGridLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        self.equation = QLineEdit("")
        label_Line = QLabel("Number: ")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addWidget(label_Line)
        layout_equation_solution.addWidget(self.equation)

        ### 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")
        button_mod = QPushButton("%")
        button_reciprocal = QPushButton("1/x")
        button_power = QPushButton("x^2")
        button_root = QPushButton("x^2/1")

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("C")
        button_clear_entry = QPushButton("CE")
        button_backspace = QPushButton("Backspace")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        
        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_other_operation.addWidget(button_reciprocal ,0, 0)
        layout_other_operation.addWidget(button_power, 0, 1)
        layout_other_operation.addWidget(button_root, 0, 2)
        layout_operation.addWidget(button_division, 0, 0)

        layout_operation.addWidget(button_product, 1, 0)
        layout_operation.addWidget(button_minus, 2, 0)
        layout_operation.addWidget(button_plus, 3, 0)
        layout_operation.addWidget(button_equal, 4, 0)


        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가
        layout_clear_equal.addWidget(button_mod, 0, 0)
        layout_clear_equal.addWidget(button_clear_entry, 0, 1)
        layout_clear_equal.addWidget(button_clear, 0, 2)
        layout_clear_equal.addWidget(button_backspace, 0, 3)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number > 0:
                x,y = divmod(number-1, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        button_double_zero = QPushButton("+/-")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_number.addWidget(button_double_zero, 3, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution, 0, 0, 1, 4)
        main_layout.addLayout(layout_clear_equal, 1, 0, 1, 4)
        main_layout.addLayout(layout_other_operation, 2, 0, 1, 3)
        main_layout.addLayout(layout_operation, 2, 3, 5, 1)
        main_layout.addLayout(layout_number, 3, 0, 4, 3)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        self.operator = operation
        self.temp = float(equation)
        self.equation.setText("")

    def operate(self, equation):
        if self.operator == "+":
            self.operator = ""
            return self.temp + equation
        elif self.operator == "-":
            self.operator = ""
            return self.temp - equation
        elif self.operator == "*":
            self.operator = ""
            return  self.temp * equation
        elif self.operator == "/":
            self.operator = ""
            return self.temp / equation
        elif self.operator == "%":
            self.operator = ""
            return self.temp % equation
    
    def button_self_operation_clicked(self, operation):
        equation = self.equation.text()
        self.temp = float(equation)
        if operation == "1/x":
            self.temp = 1 / self.temp
        elif operation == "x^2":
            self.temp = self.temp ** 2
        elif operation == "x^2/1":
            self.temp = self.temp **(1/2)
        self.equation.setText(str(self.temp))

    def button_equal_clicked(self):
        equation = self.equation.text()
        equation = float(equation)
        solution = self.operate(equation)
        self.equation.setText(str(solution))

    def button_clear_clicked(self):
        self.temp = 0
        self.operator = ""
        self.equation.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())