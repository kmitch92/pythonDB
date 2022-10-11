import sqlite3
import os
from prints import printHeaderMultiple, printHeaderSingle

#############-GLOBAL VARIABLE FOR TARGETING TABLES WITHIN DB#########################################################
target_table = 0
#####################################################################################################################

class DBOperations:  
  current_tables=[]
  sql_create_table1 = "CREATE TABLE IF NOT EXISTS "     
  sql_create_table2 = """ (
     EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT, Title VARCHAR(5), Forename VARCHAR(30), Surname VARCHAR(30), Email VARCHAR(80), SALARY INTEGER
  );"""     
 
  def __init__(self):
    try:
      self.conn = sqlite3.connect("DBEmployees.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table1+'Employees'+self.sql_create_table2)
      self.current_tables = self.get_current_tables()
      self.conn.commit()

    except Exception as e:
      return

    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("DBEmployees.db")
    self.cur = self.conn.cursor()

  def get_current_tables(self):
    try:
      self.get_connection()
      self.cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
      results = self.cur.fetchall()
      cleaned = []
      for result in results:
        cleaned.append(str(result).strip("('',)"))
      self.current_tables = cleaned
      return cleaned

    except Exception as e:
      print(e)

    finally: 
      self.conn.close()

  def create_table(self):
    try:
      os.system('cls' if os.name == 'nt' else 'clear')
      print ("*"*30+"\n")
      print("Current existing tables: ")
      count = 0
      for table in self.current_tables:
        print(str(count) + ': ' +str(table))
        count +=1
      new_table = input("Please enter the name of the table that you would like to CREATE: ")
      
      self.get_connection()
      self.cur.execute(self.sql_create_table1+ new_table+ self.sql_create_table2)
      self.current_tables.append(new_table)
      self.conn.commit()
      print("Table created successfully")
      print(str(self.get_current_tables()))
      input("Press 'ENTER' to exit: ")

    except Exception as e:
      print(e)
      input("Press 'ENTER' to exit: ")
    
    finally: 
      self.conn.close()

  def select_table(self):
    global target_table
    try:
      os.system('cls' if os.name == 'nt' else 'clear')
      print("Existing Tables: ")
      print ("*"*30)
      count = 0
      for table in self.current_tables:
        print(str(count) + ': ' +str(table))
        count +=1
      print ("*"*30 + "\n" + "Current table: " + str(self.current_tables[target_table]) + "\n" + "*"*30 + "\n")
      table_select = 999
      while table_select not in range(len(self.current_tables)):
        table_select=int(input('Select target table number: '))
      target_table=int(table_select)
      print("Changed target table to: " + str(target_table) +": "+ str(self.current_tables[target_table]))
      input("Press 'ENTER' to exit: ")

    except Exception as e:
      print(e)
      input("Press 'ENTER' to exit: ")

  def insert_data(self):
    global target_table
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      title = (str(input("Enter employee title: ")))
      forename = (str(input("Enter employee forename: ")))
      surname = (str(input("Enter employee surname: ")))
      email = (str(input("Enter employee email: ")))
      salary = (str(input("Enter employee salary: ")))
      employee_list = [title,forename,surname,email,salary]    
      table = self.current_tables[target_table]
      self.cur.execute("INSERT INTO "+table+" (Title,Forename,Surname,Email,Salary) VALUES(" + ' "'+'" ,"'.join(employee_list) + '");')
      self.conn.commit()
      print("Inserted data successfully")
      input("Press 'ENTER' to exit: ")

    except Exception as e:
      print(e)
      input("Press 'ENTER' to exit: ")
    
    finally:
      self.conn.close()

  def select_all(self):
    global target_table
    try:
      self.get_connection()
      res1 = self.current_tables[int(target_table)]
      print(res1)
      res = str(res1).strip("('',)")
      print(res)
      self.cur.execute("SELECT * FROM "+res+';')
      results = self.cur.fetchall()
      printHeaderMultiple(results)

    except Exception as e:
      print(e)
    
    finally:
      input("Press 'ENTER' to exit: ")
      self.conn.close()
    
  def search_data(self):
    global target_table
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      terms = {1: "EmployeeID", 2: "Title", 3:"Forename",4:"Surname",5:"Email",6:"Salary"}
      print ("*"*30 + "\n")
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
      table = self.current_tables[target_table]
      os.system('cls' if os.name == 'nt' else 'clear')
      if int(key) == 6:
        mods = {1: " > ", 2: " >= ", 3: " = ", 4:" < ", 5:" <= "}
        print ("*"*30 + "\n")
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
      self.cur.execute("SELECT * FROM "+table+" WHERE " + sqlSearchStringEnd)
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
    global target_table
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      print ("*"*30 + "\n")
      print("Please enter the employee ID for the record that you would like to UPDATE : ")
      empID = int(input("Employee ID: "))
      table = self.current_tables[target_table]     
      self.cur.execute("SELECT * FROM "+table+" WHERE EmployeeID="+str(empID)+";")
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
    

        sqlStatement = "UPDATE "+str(table)+" SET "
        for key in terms:
          if terms[key]:
            sqlStatement += (str(key)+"='"+str(terms[key])+"', ")
        sqlStatement = sqlStatement[:-2]
        sqlStatement += (" WHERE EmployeeID = '" + str(empID)+"';")  
        self.cur.execute(sqlStatement)
        self.cur.execute("SELECT * FROM "+table+" WHERE EmployeeID="+str(empID)+";")
        check = self.cur.fetchone()
        print(result)
        if result != check:
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
 
  def delete_data(self):
    global target_table
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      print ("*"*30 + "\n")
      print("Please enter the employee ID for the record that you would like to DELETE : ")
      empID = int(input("Employee ID: "))
      table = self.current_tables[target_table]     
      self.cur.execute("SELECT * FROM "+str(table)+" WHERE EmployeeID="+str(empID)+";")
      result = self.cur.fetchone()
      if type(result)==type(tuple()):
        print ("Employee found")
        printHeaderSingle(result)
        answer=''
        while answer not in ['y','n']:
          answer =input("Do you want to DELETE this record? (y/n): ")
        if answer == 'y':
          self.cur.execute("DELETE FROM "+table+' WHERE EmployeeID='+ str(empID)+';')
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

  def delete_tables(self):
    try:
      self.get_connection()
      os.system('cls' if os.name == 'nt' else 'clear')
      print ("*"*30 + "\n")
      self.current_tables = self.get_current_tables()
      print('1. Delete a single table')
      print('2. Delete all tables (reset the Database)')
      print('3. Exit')
      select = ''
      while select not in ['1','2','3']:
        select = input("Choose which action you would like to take.")
      if select == '3':
        return
      elif select == '1':
        count = 0
        for table in self.current_tables:
          print(str(count)+': '+ str(table).strip("('',)"))
          count+=1
        select = 999
        while int(select) not in range(len(self.current_tables)):
          select = input("Choose which table you would like to delete: ")
        res1 = self.current_tables[int(select)]
        res = str(res1).strip("('',)")
        self.get_connection()
        self.cur.execute("DROP TABLE IF EXISTS "+res+';')
        self.conn.commit()
        print('Table: ' + res + " has been deleted.")
      elif select =='2':
 
        count = 0
        answer=''
        while answer not in ['y','n']:
         answer =input("Do you wish to DELETE ALL TABLES? (Employees table will be re-initialised) (y/n): ")
        if answer == 'y':
          for table in self.current_tables:
            self.get_connection()  
            self.cur.execute("DROP TABLE IF EXISTS "+ str(table).strip("('',)")+';')
            self.conn.commit()  

    except Exception as e:
      print(e)
      
    finally:
      input("press 'ENTER' to exit." )
      self.conn.close()

while True:
  os.system('cls' if os.name == 'nt' else 'clear')
  db_ops = DBOperations()
  result = db_ops.get_current_tables()
  print("Current Table: " + str(result[target_table]))

  print ("\n Menu:")
  print ("*"*30 + "\n")
  print (" 1. Create New Table")
  print (" 2. Change Table")
  print (" 3. Add New Employee")
  print (" 4. Show All Employees")
  print (" 5. Search Employees")
  print (" 6. Update Data")
  print (" 7. Delete Data")
  print (" 8. Delete Tables")
  print (" 9. Exit\n")

  __choose_menu = int(input("Enter your choice: "))

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
    db_ops.delete_tables()
  elif __choose_menu == 9:
    exit(0)
  else:
    print ("Invalid Choice")



