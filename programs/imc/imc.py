def calculate(sex, height, weight):
  imc = weight / (height ** 2)

  degree = ''

  if imc>0 and imc<18.5:
    degree = 'abaixo do peso'
  if imc>18.6 and imc<24.9:
    degree = 'peso normal'
  if imc>25 and imc<29.9:
    degree = 'sobrepeso'
  if imc>30 and imc<34.9:
    degree = 'obesidade grau 1'
  if imc>35 and imc<39.9:
    degree = 'obesidade grau 2'
  if imc>=40:
    degree = 'obesidade grau 3'

  return str(imc) +'@'+ degree
