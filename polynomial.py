from __future__ import annotations
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
    coefficient = float(1);
    degree = 0;
    indeterminates: dict[str, int] = {}

    # Parse coefficient
    coefficient_regex = r'^[-+]?(\d+\.\d+|\d*)?'
    coefficient_string = re.search(coefficient_regex, term)[0].replace('+', '')

    if len(coefficient_string):
      if coefficient_string == '-':
        coefficient = float(-1);
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

def simplify_polynomial(polynomial: Polynomial) -> Polynomial:
  grouped_terms_map: dict[tuple[str, int], list[Monomial]] = {}

  for term in polynomial._terms:
    key = tuple(sorted(term.indeterminates.items()))

    if key not in grouped_terms_map:
      grouped_terms_map[key] = []

    grouped_terms_map[key].append(term)

  result = Polynomial('')
  
  for grouped_terms in grouped_terms_map.values():
    coefficient = float(0)

    for grouped_term in grouped_terms:
      coefficient += grouped_term.coefficient

    if coefficient != 0:
      result._terms.append(Monomial(coefficient=coefficient,degree=grouped_terms[0].degree,indeterminates=grouped_terms[0].indeterminates))
      

  return result


class Polynomial:
  _terms: list[Monomial]

  def __init__(self, expression: str) -> None:
    self._terms = parse_polynomial_expression(expression=expression)

  def __str__(self) -> str:
    if len(self._terms) == 0:
      return '0'

    result = '';

    for term in self._terms:
      # Parse signal
      if term.coefficient >= 0 and len(result) > 0:
        result += '+'
      # Parse coefficient
      if term.coefficient != 1 or len(term.indeterminates) == 0:
          if term.coefficient.is_integer():
              if term.coefficient != -1:
                result += str(int(term.coefficient))
              else:
                result += '-'
          else:
            result += str(term.coefficient)
      # Parse indeterminates
      for variable, exp in term.indeterminates.items():
        result += variable
        if exp != 1:
          result += '^' + str(exp)

    return result

  def sum(self, polynomial: Polynomial) -> Polynomial:
    grouped_terms_map: dict[tuple[str, int], list[Monomial]] = {}

    # Group terms
    for term in self._terms + polynomial._terms:
        key = tuple(sorted(term.indeterminates.items()))

        if key not in grouped_terms_map:
          grouped_terms_map[key] = []

        grouped_terms_map[key].append(term)

    result = Polynomial('')

    # Sum all grouped terms
    for grouped_terms in grouped_terms_map.values():
      coefficient = float(0)

      for grouped_term in grouped_terms:
        coefficient += grouped_term.coefficient

      result._terms.append(Monomial(coefficient=coefficient,degree=grouped_terms[0].degree,indeterminates=grouped_terms[0].indeterminates))

    return simplify_polynomial(result)

  def subtract(self, polynomial: Polynomial) -> Polynomial:
    # Invert the signal of all the terms from the subtrahend
    subtrahend = Polynomial('')
    subtrahend._terms = polynomial._terms.copy()

    for term in subtrahend._terms:
      term.coefficient *= -1

    return self.sum(subtrahend)

  def multiply(self, other: Polynomial) -> Polynomial:
    result = Polynomial('')

    for term in self._terms:
      for other_term in other._terms:
        coefficient = 0
        degree = 0
        indeterminates: dict[str, int] = {}

        # Multiply coefficient
        coefficient = term.coefficient * other_term.coefficient

        # Gather all indeterminates variables
        all_variables: set[str] = set()

        for variable in term.indeterminates.keys():
          all_variables.add(variable)

        for variable in other_term.indeterminates.keys():
          all_variables.add(variable)

        # Calculate indeterminates
        for variable in all_variables:
          if variable in term.indeterminates and variable in other_term.indeterminates:
            indeterminates[variable] = term.indeterminates[variable] + other_term.indeterminates[variable]
          elif variable in term.indeterminates:
            indeterminates[variable] = term.indeterminates[variable]
          elif variable in other_term.indeterminates:
            indeterminates[variable] = other_term.indeterminates[variable]

        result._terms.append(Monomial(coefficient=coefficient, degree=degree, indeterminates=indeterminates))

    return simplify_polynomial(result)

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
