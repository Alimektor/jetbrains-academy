class RegexEngine:
    def __is_dot(self, pattern, character):
        return pattern == "." and character != ""

    def __is_empty(self, pattern, character):
        return pattern == "" or (character == "" and pattern == "")

    def __is_equal(self, pattern, character):
        return pattern == character

    def __match_character(self, pattern_character, character):
        return self.__is_dot(pattern_character, character)\
               or self.__is_equal(pattern_character, character) \
               or self.__is_empty(pattern_character, character)

    def __match_string(self, pattern, input_string):
        if not pattern:
            return True
        if pattern[0] == "$" and not input_string:
            return True
        if pattern[0:1] == "\\" and pattern[1:2] == "\\":
            return self.__match_string(pattern[2:], input_string)
        if pattern[0:1] == "\\" and pattern[1:2] in "^.?*+$":
            input_string = input_string.replace(pattern[1:2], "A")
            pattern = pattern.replace(pattern[1:2], "A")
            return self.__match_string(pattern[1:], input_string)
        if pattern[0] == "?":
            return self.__match_string(pattern[1:], input_string)
        if (pattern[0] == "*" or pattern[0] == "+") and input_string[0:1] == input_string[1:2]:
            return self.__match_string(pattern, input_string[1:])
        if pattern[0] == "*" or pattern[0] == "+":
            return self.__match_string(pattern[1:], input_string[1:]) or self.__match_string(pattern[1:], input_string)
        elif input_string:
            if self.__match_character(pattern[0], input_string[0]):
                return self.__match_string(pattern[1:], input_string[1:])
            elif pattern[1:2] == "?" or pattern[1:2] == "*":
                return self.__match_string(pattern[2:], input_string)
            else:
                return False
        else:
            return False

    def match(self, pattern, input_string):
        if not pattern:
            return True
        elif input_string:
            if pattern[0] == "^":
                return self.__match_string(pattern[1:], input_string)
            if self.__match_string(pattern, input_string):
                return True
            else:
                return self.match(pattern, input_string[1:])
        else:
            return False


if __name__ == '__main__':
    pattern, input_string = input().split("|")
    print(RegexEngine().match(pattern, input_string))
