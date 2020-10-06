class SmartCalculator:
    def __init__(self):
        self.__variables = dict()

    def valid_ident(self, identifier):
        is_alpha = any(char.isalpha() for char in identifier)
        is_digit = any(char.isdigit() for char in identifier)
        if is_alpha and is_digit:
            raise TypeError("Invalid identifier")

    def evaluate(self, operation):
        values = operation.replace('+', ' ')
        values = values.replace('-', ' ')
        values = values.replace('/', ' ')
        values = values.replace('*', ' ')
        values = values.replace("**", "")
        operation = operation.replace("^", "**")
        operation = operation.replace("//", "***")
        for value in values.split():
            self.valid_ident(value)
        for varible in self.__variables.keys():
            if varible in operation:
                operation = operation.replace(varible, str(self.__variables[varible]))
        is_unknown_variable = any(char.isalpha() for char in operation)
        if is_unknown_variable:
            raise NameError("Unknown variable")
        return int(eval(operation))

    def assign(self, line):
        variable = line.split('=')
        if len(variable) > 2:
            raise TypeError("Invalid assignment")
        self.valid_ident(variable[0])
        self.__variables.update({variable[0].strip(): self.evaluate(variable[1])})
        return

    def main(self):
        line = input()
        while line != '/exit':
            try:
                if line == '/help':
                    print("The program calculates the sum of numbers")
                    line = input()
                    continue
                elif line == '':
                    line = input()
                    continue
                elif '=' in line:
                    self.assign(line)
                    line = input()
                    continue
                else:
                    print(self.evaluate(line))
                    line = input()
                    continue
            except SyntaxError as e:
                print("Invalid expression")
                line = input()
                continue
            except Exception as e:
                if line[0] == '/':
                    print("Unknown command")
                else:
                    print(e)
                line = input()
                continue
        print("Bye!")


if __name__ == '__main__':
    calc = SmartCalculator()
    calc.main()
