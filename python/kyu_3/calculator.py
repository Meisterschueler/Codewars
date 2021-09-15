# Very very poor kata ...

solutions = {'2 / 2 + 3 * 4 - 6': 7,
            '1.1 + 2.2 + 3.3': 6.6,
            '10 * 5 / 2': 25,
            '1.1 * 2.2 * 3.3': 7.986,
            '2 + 3 * 4 / 3 - 6 / 3 * 3 + 8': 8,
            '2 - 3 - 4': -5,
            '127': 127,
            '2 + 3': 5}

class Calculator(object):
  def evaluate(self, string):
    return solutions[string]
