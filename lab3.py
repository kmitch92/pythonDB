from operator import index
import sqlite3
import os
import time

############ TO-DO ###############
#                                #
#  add drop table functionality  #
#  add confirm for big choices   #
#  use imports not one big page  #
#  add admin username and pass   #
#  check for tips on CLI beaut   #
#                                #
##################################



class DBOperations:

# Adds EmployeeID as auto-incrementing primary key. This removes potential for insert errors.  
  current_tables = []
  target_table = ''
  sql_create_table1 = "CREATE TABLE IF NOT EXISTS "     
  sql_create_table2 = """ (
     EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT, Title VARCHAR(5), Forename VARCHAR(30), Surname VARCHAR(30), Email VARCHAR(80), SALARY INTEGER
  );"""     
  sql_insert = """INSERT INTO Employees (Title,Forename,Surname,Email,Salary)
  VALUES
  ("""
  sql_select_all = "SELECT * FROM Employees;"
  sql_search = "SELECT * FROM Employees WHERE "
  sql_update_data = """UPDATE Employees
  SET """
  sql_delete_data = "DELETE FROM "
  sql_drop_table = ""
 
  def __init__(self):
    try:
      self.conn = sqlite3.connect("DBEmployees.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table1,'Employees',self.sql_create_table2)
      self.current_tables.append('Employees')
      self.target_table = self.current_tables[0]
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("DBEmployees.db")
    self.cur = self.conn.cursor()

  def create_table(self):
    try:
      os.system('cls' if os.name == 'nt' else 'clear')
      print ("*****************************************************************\n")
      print("Current existing tables: ")
      for table, index in self.current_tables:
        print(str(index+1)+". "+table)
      new_table = input("Please enter the name of the table that you would like to CREATE: ")
      self.get_connection()
      self.cur.execute(self.sql_create_table1+ new_table+ self.sql_create_table2)
      self.current_tables.append(new_table)
      self.conn.commit()
      print("Table created successfully")
      input("Press 'ENTER' to exit: ")
    except Exception as e:
      print(e)
      input("Press 'ENTER' to exit: ")
    finally: 
      self.conn.close()

  
    #     elif answer == 'n':
    #       input("Press 'ENTER' to return to the main menu")
    #   else:
    #     print ("Employee not found")
    #     input("Press 'ENTER' to exit: ")


  def select_table(self):
    try:
      os.system('cls' if os.name == 'nt' else 'clear')
      for val, index in self.current_tables:
        print((index+1)+': Table: ' + val)
      table_select = ''
      while int(table_select) not in range(len(self.current_tables)):
        table_select=str(input('Select target table number: '))

      print("Changed target table")
      input("Press 'ENTER' to exit: ")
    except Exception as e:
      print(e)
      input("Press 'ENTER' to exit: ")
    finally:
      self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      emp = Employee()
      emp.set_title(str(input("Enter employee title: ")))
      emp.set_forename(str(input("Enter employee forename: ")))
      emp.set_surname(str(input("Enter employee surname: ")))
      emp.set_email(str(input("Enter employee email: ")))
      emp.set_salary(int(input("Enter employee salary: ")))    
      print(self.sql_insert + ' ,'.join(str(emp).split('\n')) + ');')

      self.cur.execute(self.sql_insert + ' "'+'" ,"'.join(str(emp).split('\n')) + '");')
      self.conn.commit()
      print("Inserted data successfully")
      input("Press 'ENTER' to exit: ")
    except Exception as e:
      print(e)
      input("Press 'ENTER' to exit: ")
    finally:
      self.conn.close()

  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      results = self.cur.fetchall()
      printHeaderMultiple(results)
      input("Press 'ENTER' to exit: ")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()
    
  def search_data(self):
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      terms = {1: "EmployeeID", 2: "Title", 3:"Forename",4:"Surname",5:"Email",6:"Salary"}
      print ("*****************************************************************")
      print("Select attribute to search by: \n")
      print (" 1. Employee ID")
      print (" 2. Employee Title")
      print (" 3. Forename")
      print (" 4. Surname")
      print (" 5. Email")
      print (" 6. Salary")
      print (" 7. Exit\n")
      key = int(input("Enter Selection: "))
      searchTerm = terms[key]
      modifier = ' = '
      os.system('cls' if os.name == 'nt' else 'clear')
      if int(key) == 6:
        mods = {1: " > ", 2: " >= ", 3: " = ", 4:" < ", 5:" <= "}
        print ("*****************************************************************")
        print("Choose search modifier: \n")
        print(" 1. Salary GREATER than VALUE")
        print(" 2. Salary GREATER than OR EQUAL to VALUE")
        print(" 3. Salary EQUAL to VALUE")
        print(" 4. Salary LESS than VALUE")
        print(" 5. Salary LESS than OR EQUAL to VALUE\n")
        modKey = int(input("Enter search modifier value: "))
        modifier=mods[modKey]
 
      searchValue = input("Enter query value: ")
      sqlSearchStringEnd = searchTerm+modifier+searchValue +";"
      self.cur.execute(self.sql_search + sqlSearchStringEnd)
      results = self.cur.fetchall()
      if type(results) == type(list()):
        printHeaderMultiple(results)
        input("Press 'ENTER' to exit: ")

      else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print ("No Record")
        print(sqlSearchStringEnd)
        input("Press 'ENTER' to exit: ")
        os.system('cls' if os.name == 'nt' else 'clear')
            
    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  def update_data(self):
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      print ("*****************************************************************\n")
      print("Please enter the employee ID for the record that you would like to UPDATE : ")
      empID = int(input("Employee ID: "))
      self.cur.execute(self.sql_search+"EmployeeID="+str(empID)+";")
      result = self.cur.fetchone()
      if type(result)==type(tuple()):
        print ("Employee found")
        terms = {"Title":False, "Forename":False, "Surname":False, "Email":False, "Salary":False}
        boolA,boolB,boolC,boolD,boolE='','','','',''

        printHeaderSingle(result)
        while boolA not in ['y', 'n']:
          boolA = input("Do you want to update 'Title'? (y/n): ")
        if boolA == 'y':
          terms['Title']=input("Enter updated value: ")

        printHeaderSingle(result)
        while boolB not in ['y', 'n']:
          boolB = input("Do you want to update 'Forename'? (y/n): ")
        if boolB == 'y':
          terms['Forename']=input("Enter updated value: ")  

        printHeaderSingle(result)
        while boolC not in ['y', 'n']:
          boolC = input("Do you want to update 'Surname'? (y/n): ")
        if boolC == 'y':
          terms['Surname']=input("Enter updated value: ")

        printHeaderSingle(result)
        while boolD not in ['y', 'n']:
          boolD = input("Do you want to update 'Email'? (y/n): ")
        if boolD == 'y':
          terms['Email']=input("Enter updated value: ")

        printHeaderSingle(result)
        while boolE not in ['y', 'n']:
          boolE = input("Do you want to update 'Salary'? (y/n): ")
        if boolE == 'y':
          terms['Salary']=str(input("Enter updated value: "))
    

        sqlStatement = self.sql_update_data
        for key in terms:
          if terms[key]:
            sqlStatement += (str(key)+'="'+str(terms[key])+'", ')
        sqlStatement = sqlStatement[:-2]
        sqlStatement += (' WHERE EmployeeID = ' + str(empID)+ ' RETURNING *;')  
        self.cur.execute(sqlStatement)
        result = self.cur.fetchone()
        if type(result)==type(tuple()):
          self.conn.commit()
          printHeaderSingle(result)
          print("Employees updated.")
          input('Press "ENTER" to exit: ')
        else:
          print ("Something went wrong.")
          input("Press 'ENTER' to exit: ")

      else:
        print ("Cannot find this record in the database")
        input("Press 'ENTER' to exit: ")

    except Exception as e:
      print(e)
      input("Press 'ENTER' to exit: ")
    finally:
      self.conn.close()

# Define Delete_data method to delete data from the table. The user will need to input the employee id to delete the corrosponding record. 
  def delete_data(self):
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      print ("*****************************************************************\n")
      print("Please enter the employee ID for the record that you would like to DELETE : ")
      empID = int(input("Employee ID: "))
      self.cur.execute(self.sql_search+"EmployeeID="+str(empID)+";")
      result = self.cur.fetchone()
      if type(result)==type(tuple()):
        print ("Employee found")
        printHeaderSingle(result)
        answer=''
        while answer not in ['y','n']:
          answer =input("Do you want to DELETE this record? (y/n): ")
        if answer == 'y':
          self.cur.execute(self.sql_delete_data+'WHERE EmployeeID='+ str(empID)+';')
          self.conn.commit()
          printHeaderSingle(result)
          print("Record deleted.")
          input('Press "ENTER" to exit: ')
  
        elif answer == 'n':
          input("Press 'ENTER' to return to the main menu")
      else:
        print ("Employee not found")
        input("Press 'ENTER' to exit: ")
    except Exception as e:
      print(e)
      input("Press 'ENTER' to exit: ")
    finally: 
      self.conn.close()

    
class Employee:
  def __init__(self):
#    self.employeeID = 0
    self.Title = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0

  # def set_employee_id(self, employeeID):
  #   self.employeeID = employeeID

  def set_title(self, Title):
    self.Title = Title

  def set_forename(self,forename):
   self.forename = forename
  
  def set_surname(self,surname):
    self.surname = surname

  def set_email(self,email):
    self.email = email
  
  def set_salary(self,salary):
    self.salary = salary
  
  # def get_employee_id(self):
  #   return self.employeeId

  def get_title(self):
    return self.Title
  
  def get_forename(self):
    return self.forename
  
  def get_surname(self):
    return self.surname
  
  def get_email(self):
    return self.email
  
  def get_salary(self):
    return self.salary

  def __str__(self):
    return str(self.Title+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary))

# Various Print Statements

def printHeader():
  os.system('cls' if os.name == 'nt' else 'clear')
  print("===================================================================================================")
  print("|| ID || TITLE || FORENAME ||     SURNAME     ||               EMAIL               ||   SALARY   ||")
  print("===================================================================================================")

def printHeaderSingle(result):
  os.system('cls' if os.name == 'nt' else 'clear')
  print("===================================================================================================")
  print("|| ID || TITLE || FORENAME ||     SURNAME     ||               EMAIL               ||   SALARY   ||")
  print("===================================================================================================")
  id = str(result[0])
  title = str(result[1])
  forename=str(result[2])
  surname=str(result[3])
  email=str(result[4])
  salary=str(result[5])
  print('|| '+ id+ ((2-len(id))*' ')+' || '+title[:5]+((5-len(title))*' ')+' || '+forename[:8]+((8-len(forename))*' ')+' ||   '+surname[:11]+((11-len(surname))*' ')+'   ||        '+email[:19]+((19-len(email))*' ')+'        ||  '+salary[:8]+((8-len(salary))*' ')+'  || ')
  print("===================================================================================================")

def printHeaderMultiple(results):
  os.system('cls' if os.name == 'nt' else 'clear')
  print("===================================================================================================")
  print("|| ID || TITLE || FORENAME ||     SURNAME     ||               EMAIL               ||   SALARY   ||")
  print("===================================================================================================")
  for result in results:
    id = str(result[0])
    title = str(result[1])
    forename=str(result[2])
    surname=str(result[3])
    email=str(result[4])
    salary=str(result[5])
    print('|| '+ id+ ((2-len(id))*' ')+' || '+title[:5]+((5-len(title))*' ')+' || '+forename[:8]+((8-len(forename))*' ')+' ||   '+surname[:11]+((11-len(surname))*' ')+'   ||        '+email[:19]+((19-len(email))*' ')+'        ||  '+salary[:8]+((8-len(salary))*' ')+'  || ')
    print("===================================================================================================")
# The main function will parse arguments. 
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.
  
while True:

  os.system('cls' if os.name == 'nt' else 'clear')
  print ("\n Menu:")
  print ("*****************************************************************\n")
  print (" 1. Create new table")
  print (" 2. Change table")
  print (" 3. Add new employee")
  print (" 4. Show all employees")
  print (" 5. Search employees")
  print (" 6. Update data")
  print (" 7. Delete data")
  print (" 8. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.create_table()
  elif __choose_menu == 2:
    db_ops.select_table()
  elif __choose_menu == 3:
    db_ops.insert_data()
  elif __choose_menu == 4:
    db_ops.select_all()
  elif __choose_menu == 5:
    db_ops.search_data()
  elif __choose_menu == 6:
    db_ops.update_data()
  elif __choose_menu == 7:
    db_ops.delete_data()
  elif __choose_menu == 8:
    exit(0)
  else:
    print ("Invalid Choice")



