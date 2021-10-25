from dataclasses import dataclass
import re

@dataclass
class Monomial:
  coefficient: float
  indeterminates: dict[str, int]
  degree: int

class PolynomialExpressionParser:
  # This regex is used to validate a expression
  _EXPRESSION_REGEX = r'^(([-+](?=[A-Za-z0-9]))?(\d+\.\d+|\d*)([A-Za-z](\^\d+)*)*)+$'
  # This regex is used to extract all the terms (monomials) from a expression
  _TERMS_REGEX = r'(?:(?:[-+])?(?:\d+\.\d+|\d*))(?:[A-Za-z](?:\^\d+)*)*'
  # This regex is used to extract the monomial data from a term
  _TERM_REGEX = r'([-+])?(\d+\.\d+|\d*)([A-Za-z])(?:\^(\d)+)'

  def parse(self, expression: str) -> list[Monomial]:
    if bool(re.match(self._EXPRESSION_REGEX, expression)) == False:
      raise Exception(f'Expression is not a valid polynomial: {expression}')

    expressionTerms = re.findall(self._TERMS_REGEX, expression)

    return list( map(self._parseExpressionTerm, filter(len, expressionTerms)))
    # for expressionTerm in filter(len, expressionTerms):
    #   print(expressionTerm)

  def _parseExpressionTerm(self, expressionTerm: str) -> Monomial:
    matches = re.findall(self._TERM_REGEX, expressionTerm)

    for match in matches:
      print(match)
    
    # group 0 = signal
    # group 1 = coefficient
    # group 2 = variable
    # group 3 = degree
    indeterminates: dict[str, int] = {}
 
    # print(expressionTerm)
    # print(re.findall(self._TERM_REGEX, expressionTerm))
    return Monomial(coefficient=0, indeterminates={}, degree=0)


class Polynomial:
  _terms: list[Monomial]

  def __init__(self, expression: str) -> None:
    self._terms = PolynomialExpressionParser().parse(expression=expression)
    # matched = re.match(r"^(?:(-|\+)?((\d+\.\d+)|\d)*([A-Za-z](\^\d+)?)*)+$", expression)
    # # matched = re.match(r"(-|\+)?((\d+\.\d+)|\d)*([A-Za-z](\^\d+)?)*", expression)
    # is_match = bool(matched)
    # print(is_match)
    # pass

  def __str__(self) -> str:
    return 'nice'


if __name__ == '__main__':
  # print('2x+2x ->', Polynomial('2x+2x'))
  # print('2x-2x ->', Polynomial('2x-2x'))
  # print('2+2x ->', Polynomial('2+2x'))
  # print('2-2x ->', Polynomial('2-2x'))
  # print('2xy-2 ->', Polynomial('2xy-2'))
  # print('2.5x+4y ->', Polynomial('2.5x+4y'))
  # print('2.5x^2 ->', Polynomial('2.5x^2'))
  print('2.5x^2y^3-2x^3 ->', Polynomial('2.5x^2y^3-2x^3')._terms)
  # print('2.5x^2y^3-2x^ ->', Polynomial('2.5x^2y^3-2x^'))