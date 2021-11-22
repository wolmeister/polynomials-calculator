from dataclasses import dataclass
import re

@dataclass
class Monomial:
  coefficient: float
  indeterminates: dict[str, int]
  degree: int

def parse_polynomial_expression(expression: str) -> list[Monomial]:
  # Validates if the expression is valid
  expression_regex = r'^(([-+](?=[A-Za-z0-9]))?(\d+\.\d+|\d*)([A-Za-z](\^\d+)*)*)+$'
  if bool(re.match(expression_regex, expression)) == False:
    raise Exception(f'Expression is not a valid polynomial: {expression}')

  # Find all expression terms
  terms_regex = r'(?:(?:[-+])?(?:\d+\.\d+|\d*))(?:[A-Za-z](?:\^\d+)*)*'
  expression_terms = list(filter(len, re.findall(terms_regex, expression)))

  # Parse expression terms to monomials objects
  monomials: list[Monomial] = []

  for term in expression_terms:
    coefficient = 1;
    degree = 0;
    indeterminates: dict[str, int] = {}

    # Parse coefficient
    coefficient_regex = r'^[-+]?(\d+\.\d+|\d*)?'
    coefficient_string = re.search(coefficient_regex, term)[0].replace('+', '')

    if len(coefficient_string):
      if coefficient_string == '-':
        coefficient = -1;
      else:
        coefficient = float(coefficient_string)

    # Parse indeterminates
    indeterminates_regex = r'([A-Za-z])(?:\^(\d+))?'

    for indeterminate_match in re.findall(indeterminates_regex, term):
      indeterminate_degree = 1;
      if len(indeterminate_match[1]):
        indeterminate_degree = int(indeterminate_match[1])

      indeterminates[indeterminate_match[0]] = indeterminate_degree
      degree += indeterminate_degree

    monomials.append(Monomial(coefficient=coefficient, indeterminates=indeterminates, degree=degree))

  return monomials


class Polynomial:
  _terms: list[Monomial]

  def __init__(self, expression: str) -> None:
    self._terms = parse_polynomial_expression(expression=expression)

  def __str__(self) -> str:
    return str(self._terms)

  def resolve(self, variables: dict[str, int]) -> float:
    result = 0

    for term in self._terms:
      indeterminates_result = 1

      for variable, exp in term.indeterminates.items():
        if not variable in variables:
          raise Exception(f'Variable {variable} should be specified')
        indeterminates_result *= pow(variables[variable], exp)

      result += term.coefficient * indeterminates_result
        
    return result

  def degree(self) -> int:
    return max(self._terms, key=lambda monomial: monomial.degree)


if __name__ == '__main__':
  test_items = [
    { 'expression': '1', 'variables': {} },
    { 'expression': 'x+y', 'variables': { 'x': 1, 'y': 2 } },
    { 'expression': 'x-y', 'variables': { 'x': 3, 'y': 2 } },
    { 'expression': '2x+2x', 'variables': { 'x': 1 } },
    { 'expression': '2x-2x', 'variables': { 'x': 1 } },
    { 'expression': '2+2x', 'variables': { 'x': 2 } },
    { 'expression': '2-2x', 'variables': { 'x': 2 } },
    { 'expression': '2xy-2', 'variables': { 'x': 1, 'y': 2 } },
    { 'expression': '2.5x+4y', 'variables': { 'x': 1, 'y': 2 } },
    { 'expression': '3x^2', 'variables': { 'x': 3 } },
    { 'expression': '2.5x^2', 'variables': { 'x': 4 } },
    { 'expression': '4.5x^2y^3-2x^3', 'variables': { 'x': 2, 'y': 3 } },
    { 'expression': '4.5x^2y^3-2x^3+y^6', 'variables': { 'x': 5, 'y': 3 } },
  ]

  for test_item in test_items:
    polynomial = Polynomial(test_item['expression'])
    print(f"{test_item['expression']} -> {polynomial}")
    print(f"{test_item['expression']} using {test_item['variables']} == {polynomial.resolve(test_item['variables'])}")
    print('----------')

  # print('1 ->', Polynomial('1'))
  # print('x+y ->', Polynomial('x+y'))
  # print('x-y ->', Polynomial('x-y'))
  # print('2x+2x ->', Polynomial('2x+2x'))
  # print('2x-2x ->', Polynomial('2x-2x'))
  # print('2+2x ->', Polynomial('2+2x'))
  # print('2-2x ->', Polynomial('2-2x'))
  # print('2xy-2 ->', Polynomial('2xy-2'))
  # print('2.5x+4y ->', Polynomial('2.5x+4y'))
  # print('3x^2 ->', Polynomial('3x^2'))
  # print('2.5x^2 ->', Polynomial('2.5x^2'))
  # print('4.5x^2y^3-2x^3 ->', Polynomial('4.5x^2y^3-2x^3'))
  # print('4.5x^2y^3-2x^3+y^6 ->', Polynomial('4.5x^2y^3-2x^3+y^6'))