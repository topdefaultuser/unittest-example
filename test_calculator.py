import unittest

import calculator



class TestStringMethods(unittest.TestCase):
    # 
    def test_empty_line_processing(self):
        input_data = ''
        output_data = 0
        error_message = 'Некорректная обработка пустой строки' 
        self.assertEqual(calculator.calculator(input_data), output_data, error_message)
        # Или можно так
        # self.assertTrue(calculator.calculator(input_data) == output_data, error_message)

    # 
    def test_pre_formatter_function(self):
        input_data = ' (2 + 12) * (3  - 22  )  +  2- 3 * 55 / 11 +(2^3 ^ 2)'
        output_data = ['(', '2', '+', '12', ')', '*', '(', '3', '-', '22', ')', '+', '2', '-', '3', '*', '55', '/', '11', '+', '(', '2', '^', '3', '^', '2', ')']
        error_message = 'Некорректная работа функции "pre_formatter"'
        self.assertEqual(calculator.pre_formatter(input_data), output_data, error_message)
 
    # 
    def test_filtration_function(self):
        input_data = 'QAZXSWEDCVFRTGBNHYUJMKIOLPqazxswedcvfrtgbnhyujmkiolp[;\\|\'],!@#$%'
        output_data = []
        error_message = 'Некорректная работа функции "filter"'
        self.assertEqual(calculator.filter(input_data), output_data, error_message)

    # 
    def test_formatter_function(self):
        input_data = ['2', '(', '2', '+', '2', ')', '(', '5', '+', '5', ')', '10', '(', '22','-', '1', ')', '1', '(', '20', '-', '2', ')', '9']
        output_data = ['2', '*', '(', '2', '+', '2', ')', '*', '(', '5', '+', '5', ')', '*', '10', '*', '(', '22', '-', '1', ')', '*', '1', '*', '(', '20', '-', '2', ')', '*', '9']
        error_message = 'Некорректная работа функции "formatter"'
        self.assertEqual(calculator.formatter(input_data), output_data, error_message)

        input_data = ['222', '+', '-', '111']
        output_data = ['222', '+', '-111']
        self.assertEqual(calculator.formatter(input_data), output_data, error_message)

    # 
    def test_float_function(self):
        input_data = '1.5'
        output_data = True
        error_message = 'Некорректная работа функции "float"'
        self.assertEqual(calculator.isfloat(input_data), output_data, error_message)

        input_data = 'd.5'
        output_data = False
        self.assertEqual(calculator.isfloat(input_data), output_data, error_message)      

    # 
    def test_converter_function(self):
        input_data = ['1', '2', '3', '4', '5', '1.4', '99.99', '0.001', '-10', '(', ')', '+', '-', '/', '^', '*']
        output_data = [1, 2, 3, 4, 5, 1.4, 99.99, 0.001, -10, '(', ')', '+', '-', '/', '^', '*']
        error_message = 'Некорректная работа функции "converter"'
        self.assertEqual(calculator.converter(input_data), output_data, error_message)

    # 
    def test_calculator(self):
        input_data = '((89+11)(5*5)-(15*15)((200-100)-(0+100)+3))+1000.1/2'
        output_data = 2325.05
        error_message = 'Некорректная работа функции "calculator"'
        self.assertEqual(calculator.calculator(input_data), output_data, error_message)

# 
if __name__ == '__main__':
    unittest.main()

