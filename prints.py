import os

def printHeader():
  os.system('cls' if os.name == 'nt' else 'clear')
  print("===================================================================================================")
  print("|| ID || TITLE || FORENAME ||     SURNAME     ||               EMAIL               ||   SALARY   ||")
  print("===================================================================================================")

def printHeaderSingle(result):
  printHeader()
  id = str(result[0])
  title = str(result[1])
  forename=str(result[2])
  surname=str(result[3])
  email=str(result[4])
  salary=str(result[5])
  print('|| '+ id+ ((2-len(id))*' ')+' || '+title[:5]+((5-len(title))*' ')+' || '+forename[:8]+((8-len(forename))*' ')+' ||   '+surname[:11]+((11-len(surname))*' ')+'   ||        '+email[:19]+((19-len(email))*' ')+'        ||  '+salary[:8]+((8-len(salary))*' ')+'  || ')
  print("===================================================================================================")

def printHeaderMultiple(results):
  printHeader()
  for result in results:
    id = str(result[0])
    title = str(result[1])
    forename=str(result[2])
    surname=str(result[3])
    email=str(result[4])
    salary=str(result[5])
    print('|| '+ id+ ((2-len(id))*' ')+' || '+title[:5]+((5-len(title))*' ')+' || '+forename[:8]+((8-len(forename))*' ')+' ||   '+surname[:11]+((11-len(surname))*' ')+'   ||        '+email[:19]+((19-len(email))*' ')+'        ||  '+salary[:8]+((8-len(salary))*' ')+'  || ')
    print("===================================================================================================")