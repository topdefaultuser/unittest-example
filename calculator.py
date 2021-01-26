import doctest
import sys



"""

"""

# 
def isfloat(value):
    """
    >>> value = '1.1'
    >>> isfloat(value)
    True
    >>> value = 'e.1'
    >>> isfloat(value)
    False
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

# Убирает все пробелы и разбивает строку на список 
def pre_formatter(data):
    """
    >>> string = '  2 ^ 3.2 +    1.0+0.5'
    >>> pre_formatter(string)
    ['2', '^', '3.2', '+', '1.0', '+', '0.5']
    >>> string = '22.1 * 0.5 / 2 (1+1) ^ 2 (2-1)'
    >>> pre_formatter(string)
    ['22.1', '*', '0.5', '/', '2', '(', '1', '+', '1', ')', '^', '2', '(', '2', '-', '1', ')']
    """
    # Коррекцыя слитно написаных выражений 22+11 на 22 + 11 и так далее
    data = data.replace('+', ' + ')
    data = data.replace('-', ' - ')
    data = data.replace('*', ' * ')
    data = data.replace('/', ' / ')
    data = data.replace('^', ' ^ ')
    data = data.replace('(', ' ( ')
    data = data.replace(')', ' ) ')
    return  [value for value in data.replace('  ', ' ').split(' ') if value not in ('', ' ')]


# Фильтр пропускающий только разрешенные символы и числа
def filter(data):
    """
    >>> data = ['test', '222', '^', '3.2', '+', 'a', '1.0', '%', '+', '0.5', '!']
    >>> filter(data)
    ['222', '^', '3.2', '+', '1.0', '+', '0.5']
    """
    allowable_symbols = tuple('()^*/+-.')
    output = []

    for item in data:
        if item.isdigit():
            output.append(item)

        elif isfloat(item):
            output.append(item)

        elif item in allowable_symbols:
            output.append(item)

    return output

# Исправляет возможные ошибки
def formatter(data):
    """
    >>> data = ['(', '5', ')', '(', '5', ')']
    >>> formatter(data)
    ['(', '5', ')', '*', '(', '5', ')']
    >>> data = ['1', '(', '5', ')', '(', '5', ')', '2']
    >>> formatter(data)
    ['1', '*', '(', '5', ')', '*', '(', '5', ')', '*', '2']
    >>> data = ['2', '+', '-', '2']
    >>> formatter(data)
    ['2', '+', '-2'] 
    """
    index = 0
    while True:
        if(index == len(data)-1):
            break

        if((data[index] == ')' and data[index+1] == '(')):
            data.insert(index+1, '*')

        elif((data[index] == ')' and data[index+1].isdigit())):
            data.insert(index+1, '*')

        elif((data[index].isdigit()) and data[index+1] == '('):
            data.insert(index+1, '*')

        elif((data[index], data[index+1]) == ('+', '-')):
            data[index+1] = '-%s' % data[index+2]
            data.pop(index+2)

        index += 1

    return data

# Конвертация строковых значений в соответствии с их типом
def converter(data):
    """
    >>> data = ['222', '^', '3.2', '+', '1.0', '*', '0.5']
    >>> converter(data)
    [222, '^', 3.2, '+', 1.0, '*', 0.5]
    """
    output = []

    for item in data:
        if item.isdigit():
            output.append(int(item))
       
        elif isfloat(item):
            output.append(float(item))

        else:
            output.append(item)
        
    return output

# 
def is_number_brackets_equal(data):
    """
    >>> lst = ['(', '(', '1', '+', '1', ')', '+', '0.5', ')', '-', '1']
    >>> is_number_brackets_equal(lst)
    True
    >>> lst = ['(', '(', '1', '+', '1', ')']
    >>> is_number_brackets_equal(lst)
    False
    """
    amount_left_bracket = data.count('(')
    amount_right_bracket = data.count(')')

    if(amount_left_bracket != amount_right_bracket):    
        return False

    else:
        return True

# Рекурсивная фунция
def calculator(data):
    # Условие прерывания рекурсии
    if(isinstance(data, list) and len(data) == 1):
        return data.pop(0)

    # Если тип параметра data является строка (возможно только при первом вызове данной функции),
    # разобьет строку на список.
    if(isinstance(data, str)):
        data = pre_formatter(data)
        data = filter(data)

        if(len(data) == 0):
            return 0

        data = formatter(data)
        data = converter(data)

        if(not is_number_brackets_equal(data)):
            print('[!] Указано не одинаковое количество скобок')
            return 0

    # Проходимся по массиву и вычисляем значения в скобках
    while True:
        if '(' not in data:
            break

        start_index = data.index('(') # Стартовый индекс
        end_index = start_index+1 # первый индекс 
        while True:
            end_index = data.index(')', end_index)
            slc = data[start_index+1: end_index]

            # Проверяет не захватили ли мы лишнюю скобку
            if(is_number_brackets_equal(slc)):
                break

            end_index += 1
        
        # Вычисляем результат среза списка
        result = calculator(slc)
        # Заменяем диапазон значений между скобками на вычисленный результат
        data[start_index:end_index+1] = [result]

    # Проходимся по массиву и возвышаем во степень все числа
    # !ВАЖНО 2 ^ 3 ^ 2 = 512 Вычисление степени выполняется с права на лево.
    # 2 ^ 3 ^ 2 == 2 ^ 9(Поскольку 3 ^ 2 = 9)
    # Возможно это костыль, но лучшей реализации я не придумал.
    # Разворачиваем список, проходимся по нему в поисках символа ^
    # после нахождения индекса символа, и с учетом индекса
    # получает значения операндов (с учетом того, что мы развернули список)
    # выполняет вычисление и сохраняет результат
    # разобьет строку на список.
    data.reverse()
    while True:
        if '^' not in data:
            break
        index = data.index('^')
        lf = data.pop(index+1)
        rf = data.pop(index-1)
        # Установка значени вычесления на место первого операнда 
        data[index-1] = lf ** rf
    # И снова разворачиваем список к исходному состоянию
    data.reverse()

    # Если есть операции умножения и деления ищет первую с них 
    # (в порядке с лева на право)
    if('*' in data and '/' in data):
        a_index = data.index('*')
        b_index = data.index('/')

        if a_index < b_index:
            index = data.index('*')
            lf = data.pop(index-1)
            rf = data.pop(index)
            data[index-1] = lf*rf

        elif a_index > b_index:
            index = data.index('/')
            lf = data.pop(index-1)
            rf = data.pop(index)
            data[index-1] = lf/rf

    elif('*' in data):
        index = data.index('*')
        lf = data.pop(index-1)
        rf = data.pop(index)
        data[index-1] = lf*rf

    elif('/' in data):
        index = data.index('/')
        lf = data.pop(index-1)
        rf = data.pop(index)
        data[index-1] = lf/rf

    # Если закончились все операции умножения и деления
    # начинается работа со сложением и вычитанием
    if('*' not in data and '/' not in data):
        # Если есть операции сложения и вычитания ищет первую с них 
        # (в порядке с лева на право)
        if('+' in data and '-' in data):
            a_index = data.index('+')
            b_index = data.index('-')

            if a_index < b_index:
                index = data.index('+')
                lf = data.pop(index-1)
                rf = data.pop(index)
                data[index-1] = lf+rf

            if a_index > b_index:
                index = data.index('-')
                lf = data.pop(index-1)
                rf = data.pop(index)
                data[index-1] = lf-rf

        elif('+' in data):
            index = data.index('+')
            lf = data.pop(index-1)
            rf = data.pop(index)
            data[index-1] = lf+rf

        elif('-' in data):   
            index = data.index('-')
            lf = data.pop(index-1)
            rf = data.pop(index)
            data[index-1] = lf-rf

    return calculator(data)


# 
if (__name__ == '__main__'):
    # 
    if('--test' in sys.argv[1:]):
        # Если нужно получить полный журнал действий
        if('--full' in sys.argv[1:]):
            sys.argv.append('-v')

        # Поскольку, ожидаемые данные и результаты теста сравниваются как строки, 
        # перенос строки повлияет на корректность теста.
        # Флаг doctest.NORMALIZE_WHITESPACE поможет избежать этого
        # Флаг doctest.ELLIPSIS позволит сокращать длинные выражения(списки) для примера:
        # [1, 2, 3, 4, 5, 6, 7] можно записать как [1, 2, ..., 6, 7]  
        doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    else:
        print('[!] Доступные символы: ^, *, /, +, -, (, )')
        while True:
            input_data = input('[<] Введите ваш пример: ')
            print('[>] Результат: ', calculator(input_data))

