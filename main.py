from polynomial import Polynomial

if __name__ == '__main__':
  print(Polynomial('4.5x^2y^3-2x^3+y^6').multiply(Polynomial('4.5x^2y^3-2x^3+y^6')))
  print(Polynomial('y^6').multiply(Polynomial('y^6')))
  print(Polynomial('x^2+x+1').multiply(Polynomial('y+1')))
  print(Polynomial('x+y').multiply(Polynomial('y+x')))
  print(Polynomial('3x+y').subtract(Polynomial('2x+y')))
  print(Polynomial('x^2').sum(Polynomial('y+2x-2x^2')))
  print(Polynomial('x^2+y').subtract(Polynomial('z^3-10+2y')))
  print(Polynomial('x^2+y').subtract(Polynomial('z^3-10+2y')).resolve({ 'x': 2, 'y': 2, 'z': 3 }))