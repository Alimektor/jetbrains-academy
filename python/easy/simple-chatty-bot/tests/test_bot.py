import pytest
import bot

from bot import Bot


class TestBot:
    def setup(self):
        """
        Add bot to the tests
        """
        self.bot = Bot()

    def get_output(self, capsys):
        """Add output for tests to check it

        :param capsys: the fixture for streams
        :type capsys: the capture object
        :return: return out stream
        :rtype: out list
        """
        out, err = capsys.readouterr()
        return out.strip().split("\n")

    @pytest.mark.parametrize("name, year", [
        ("Alimektor", "1998"),
        ("Jack", "1996"),
        ("Johnny", "2005"),
        ("Ivan", "1972"),
    ])
    def test_greet(self, capsys, name, year):
        """Testing greet"""
        self.bot.greet(name, year)
        captured = self.get_output(capsys)
        assert captured[0] == f"Hello! My name is {name}.", f"The name should be {name}"
        assert captured[1] == f"I was created in {year}.", f"The birth year should be {year}"

    @pytest.mark.parametrize("name", ["Alimektor", "Jack", "Johnny", "Ivan"])
    def test_remind_name(self, capsys, name):
        """Test remind name

        :param capsys: the fixture for streams
        :type capsys: the capture object
        :param name: name for testing
        :type name: str
        """
        bot.input = lambda: name
        self.bot.remind_name()
        captured = self.get_output(capsys)
        lines = [
            "Please, remind me your name.",
            f"What a great name you have, {name}!"
        ]
        for expected, capture in zip(lines, captured):
            assert capture == expected, f"The line should be: {expected}"

    @pytest.mark.parametrize("numbers, age", [
        ([1, 0, 8], 85),
        ([2, 4, 8], 29),
        ([13, 4, 111], 34),
        ([63, 1, 123], 81),
    ])
    def test_guess_age(self, capsys, numbers, age):
        """Test the guessing of the age of an user

        :param capsys: the fixture for streams
        :type capsys: the capture object
        :param numbers: numbers for testing
        :type numbers: list of int
        :param age: the age of user for testing
        :type age: int
        """
        bot.input = lambda: numbers.pop(0)
        self.bot.guess_age()
        captured = self.get_output(capsys)
        lines = [
            "Let me guess your age.",
            "Enter remainders of dividing your age by 3, 5 and 7.",
            f"Your age is {age}; that's a good time to start programming!"
        ]
        for expected, capture in zip(lines, captured):
            assert capture == expected, f"The line should be: {expected}"

    @pytest.mark.parametrize("count, expected", [
        (1, ["0!", "1!"]),
        (3, ["0!", "1!", "2!", "3!"]),
        (5, ["0!", "1!", "2!", "3!", "4!", "5!"]),
        (8, ["0!", "1!", "2!", "3!", "4!", "5!", "6!", "7!", "8!"]),
    ])
    def test_count(self, capsys, count, expected):
        """Test count function

        :param capsys: the fixture for streams
        :type capsys: the capture object
        :param count: the count number
        :type count: int
        :param expected: expected result
        :type expected: list of strings
        """
        bot.input = lambda: count
        self.bot.count()
        captured = self.get_output(capsys)
        lines = [
            "Now I will prove to you that I can count to any number you want.",
            *expected
        ]
        for expected, capture in zip(lines, captured):
            assert capture == expected, f"The line should be: {expected}"

    @pytest.mark.parametrize("inputs, again_message", [
        (["1", "2"], "Please, try again."),
        (["1", "1", "3", "2"], "Please, try again."),
        (["1337", "228", "3", "2"], "Please, try again."),
        (["2"], ""),
    ])
    def test_test(self, capsys, inputs, again_message):
        """Test the test function with

        :param capsys: the fixture for streams
        :type capsys: the capture object
        :param inputs: [description]
        :type inputs: [type]
        :param again_message: [description]
        :type again_message: [type]
        """
        bot.input = lambda: inputs.pop(0)
        self.bot.test()
        captured = self.get_output(capsys)
        message = f"You must have {again_message}"
        assert any(
            again_message in capture for capture in captured) == True, message
        message = "Completed, have a nice day!"
        assert captured[-1] == message, f"The last message should be: {message}"

    def test_end(self, capsys):
        self.bot.end()
        captured = self.get_output(capsys)[0]
        message = "Congratulations, have a nice day!"
        assert captured == message, f"The last message should be {message}"

    @pytest.mark.parametrize("inputs,expected", [
        (["Marry", "1", "0", "5", "10", *(f"{i}" for i in range(10))], ("Marry", 40, 10))
    ])
    def test_main_project(self, capsys, inputs, expected):
        """Test the main function with

        :param capsys: the fixture for streams
        :type capsys: the capture object
        :param inputs: inputs for test
        :type inputs: list of strings
        :param expected: expected results
        :type expected: list of objects
        """
        bot.input = lambda: inputs.pop(0)
        bot.main()
        lines = self.get_output(capsys)
        reply = "\n".join(lines)

        length = 9 + expected[2] + 1
        message = f"You should output at least {length} lines " \
                  f"(for the count number {expected[2]}).\n" \
                  f"Lines found: {len(lines)}" \
                  f"Your output:\n" \
                  f"{reply.strip()}"
        assert len(lines) > length, message

        line_with_name = lines[3].lower()
        name = expected[0].lower()

        message = f"The name was {expected[0]}\nBut the 4-th line was:" \
                  f"\n\"{lines[3]}\n\n4-th line should contain a name of the user"
        assert name in line_with_name, message

        line_with_age = lines[6].lower()
        age = str(expected[1])

        message = "Can't find a correct age! Maybe you calculated the age wrong?\n\n" \
                  "Your line with age: \n" + "\"" + lines[6] + "\""
        assert age in line_with_age, message

        for i in range(expected[2] + 1):
            num_line = lines[i + 8].strip().replace(' ', '')
            actual_num = f'{i}!'

            message = f"Expected {i + 8}-th line: \n\"{actual_num}\"\n" \
                      f"Your {i + 8}-th line: \n\"{num_line}\""
            assert num_line == actual_num, message

        last_line = lines[-1]
        message = "Your last line should be:\n" \
                  "\"Congratulations, have a nice day!\"\n" \
                  "Found:\n\"{last_line}\""
        assert "Congratulations, have a nice day!" == last_line, message
