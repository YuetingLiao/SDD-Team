import unittest, requests, pymysql, random

#Help Function: make a request to database with an sql query as input
def search_db(sql):
    try:
        conn = pymysql.connect("localhost", "root", "123456", "sdd")        
        curs = conn.cursor()         
        curs.execute(sql)
        conn.commit()
        result = curs.fetchall()
    except EOFError:
        conn.rollback()
    finally:
        conn.close()
        return result


#Unit Tests for AddToMenu method
class AddToMenuTest(unittest.TestCase): 
    
    #Purpose: Test an appropriate addition to the menu
    #Input: valid user id, valid meal type, valid recipe id
    #Expected output: new recipe should be inserted in menu, menu_ins, and menu_ingr table in the database
    def test_add_menu(self):
        before = search_db("SELECT count(*) FROM menu")
        before1 = search_db("SELECT count(*) FROM menu_ins")
        before2 = search_db("SELECT count(*) FROM menu_ingr")
        cookies = {
            'id': 'jianr'
        }        
        data = {
          'type': 'b',
          'name': '64d3724048'
        }
        response = requests.post('http://localhost:1880/addToMenu', cookies=cookies, data=data).json()
        after = search_db("SELECT count(*) FROM menu")
        after1 = search_db("SELECT count(*) FROM menu_ins")
        after2 = search_db("SELECT count(*) FROM menu_ingr")
        diff1 = search_db("SELECT count(*) FROM (SELECT DISTINCT * FROM instructions WHERE id = '{}') as x".format(data["name"]))
        diff2 = search_db("SELECT count(*) FROM (SELECT DISTINCT * FROM ingredient WHERE id = '{}') as x".format(data["name"]))
        self.assertTrue(before[0][0]+1 == after[0][0])
        self.assertTrue(before1[0][0]+diff1[0][0] == after1[0][0])
        self.assertTrue(before2[0][0]+diff2[0][0] == after2[0][0])
        search_db("DELETE FROM menu WHERE recipe = '{}' and username = '{}' and type = '{}'".format(data["name"], cookies["id"], data["type"]))
        search_db("DELETE FROM menu_ins WHERE recipe = '{}' and username = '{}' and type = '{}'".format(data["name"], cookies["id"], data["type"]))
        search_db("DELETE FROM menu_ingr WHERE recipe = '{}' and username = '{}' and type = '{}'".format(data["name"], cookies["id"], data["type"]))
    
    #Purpose: Test an addition to the menu with an invalid user id
    #Input: invalid user id, valid meal type, valid recipe id
    #Expected output: menu, menu_ins, and menu_ingr table in the database should remain unchanged
    def test_add_menu_invalid_cookie(self):
        before = search_db("SELECT count(*) FROM menu")
        before1 = search_db("SELECT count(*) FROM menu_ins")
        before2 = search_db("SELECT count(*) FROM menu_ingr")
        cookies = {
            'id': 'rjian'
        }        
        data = {
          'type': 'b',
          'name': '64d3724048'
        }
        response = requests.post('http://localhost:1880/addToMenu', cookies=cookies, data=data).json()
        after = search_db("SELECT count(*) FROM menu")
        after1 = search_db("SELECT count(*) FROM menu_ins")
        after2 = search_db("SELECT count(*) FROM menu_ingr")
        self.assertTrue(before[0][0] == after[0][0])
        self.assertTrue(before1[0][0] == after1[0][0])
        self.assertTrue(before2[0][0] == after2[0][0])

    #Purpose: Test an addition to the menu with an invalid recipe id
    #Input: valid user id, valid meal type, invalid recipe id
    #Expected output: menu, menu_ins, and menu_ingr table in the database should remain unchanged
    def test_add_menu_invalid_recipe(self):
        before = search_db("SELECT count(*) FROM menu")
        before1 = search_db("SELECT count(*) FROM menu_ins")
        before2 = search_db("SELECT count(*) FROM menu_ingr")
        cookies = {
            'id': 'jianr'
        }        
        data = {
          'type': 'b',
          'name': '666666666'
        }
        response = requests.post('http://localhost:1880/addToMenu', cookies=cookies, data=data).json()
        after = search_db("SELECT count(*) FROM menu")
        after1 = search_db("SELECT count(*) FROM menu_ins")
        after2 = search_db("SELECT count(*) FROM menu_ingr")
        self.assertTrue(before[0][0] == after[0][0])
        self.assertTrue(before1[0][0] == after1[0][0])
        self.assertTrue(before2[0][0] == after2[0][0])
    
    #Purpose: Test an addition to the menu with an invalid meal type
    #Input: valid user id, invalid meal type, valid recipe id
    #Expected output: menu, menu_ins, and menu_ingr table in the database should remain unchanged
    def test_add_menu_invalid_meal_type(self):
        before = search_db("SELECT count(*) FROM menu")
        before1 = search_db("SELECT count(*) FROM menu_ins")
        before2 = search_db("SELECT count(*) FROM menu_ingr")
        cookies = {
            'id': 'jianr'
        }        
        data = {
          'type': 'a',
          'name': '64d3724048'
        }
        response = requests.post('http://localhost:1880/addToMenu', cookies=cookies, data=data).json()
        after = search_db("SELECT count(*) FROM menu")
        after1 = search_db("SELECT count(*) FROM menu_ins")
        after2 = search_db("SELECT count(*) FROM menu_ingr")
        self.assertTrue(before[0][0] == after[0][0])
        self.assertTrue(before1[0][0] == after1[0][0])
        self.assertTrue(before2[0][0] == after2[0][0])


#Unit Tests for GetMacro method
class GetMacroTest(unittest.TestCase):   

    #Purpose: Test for getting all values of 5 macronutrients for a valid user id and meal type
    #Input: valid user id, valid meal type
    #Expected output: if menu is empty for given type, return a list of null values. Otherwise, the values are not null
    def test_get_macro(self):
        cookies = {
            'id': 'jianr'
        }
        data = {
          'type': 'b'
        }        
        response = requests.post('http://localhost:1880/get_macro', cookies=cookies, data=data).json()
        self.assertTrue(len(response["nutrients"]) == 5)
        count = search_db("SELECT count(*) FROM menu WHERE type = '{}'".format(data["type"]))
        if count[0][0] == 0:
            for i in response["key"]:
                self.assertTrue(response[i] == None)
        else:
            for i in response["key"]:
                self.assertTrue(response[i] != None)    
        
    #Purpose: Test for getting all values of 5 macronutrients for empty inputs
    #Input: empty user id, empty meal type
    #Expected output: get a list of null values
    def test_get_macro_empty(self):
        cookies = {
            'id': ''
        }
        data = {
          'type': ''
        }        
        response = requests.post('http://localhost:1880/get_macro', cookies=cookies, data=data).json()
        self.assertTrue(list(response[0].keys())[0] == "username")
    
    #Purpose: Test for getting all values of 5 macronutrients for invalid user id
    #Input: invalid user id, valid meal type
    #Expected output: get a list of null values
    def test_get_macro_invalid_cookies(self):
        count = search_db("SELECT count(*) FROM users")
        cookies = {
            'id': 'rjian'
        }
        data = {
          'type': 'b'
        }        
        response = requests.post('http://localhost:1880/get_macro', cookies=cookies, data=data).json()
        self.assertTrue(list(response[0].keys())[0] == "username")
        
    #Purpose: Test for getting all values of 5 macronutrients for invalid meal type
    #Input: valid user id, invalid meal type
    #Expected output: get a list of null values
    def test_get_macro_invalid_meal_type(self):
        count = search_db("SELECT count(*) FROM users")
        cookies = {
            'id': 'jianr'
        }
        data = {
          'type': 'a'
        }        
        response = requests.post('http://localhost:1880/get_macro', cookies=cookies, data=data).json()
        self.assertTrue(len(response["nutrients"]) == 5)
        for i in response["key"]:
            self.assertTrue(response[i] == None)


#Unit Tests for CreateAccount method
class CreateAccountTest(unittest.TestCase):   

    #Purpose: Test an appropriate registration to the website
    #Input: valid user id, valid password
    #Expected output: users table in database should be updated with the new user info
    def test_create_account(self):
        before = search_db("SELECT count(*) FROM users")      
        data = {
          'firstname': str(int(random.random()*100)),
          'lastname': '123456'
        }        
        response = requests.post('http://localhost:1880/create_account', data=data)
        after = search_db("SELECT count(*) FROM users")
        self.assertTrue(before[0][0]+1 == after[0][0])
        search_db("DELETE FROM users WHERE username = '{}'".format(data["firstname"]))
    
    #Purpose: Test a registration with empty user id and empty password
    #Input: empty user id, empty password
    #Expected output: users table in database is unchanged
    def test_create_account_empty(self):
        before = search_db("SELECT count(*) FROM users")
        data = {
          'firstname': '',
          'lastname': ''
        }        
        response = requests.post('http://localhost:1880/create_account', data=data)
        after = search_db("SELECT count(*) FROM users")
        self.assertTrue(before[0][0] == after[0][0])

    #Purpose: Test a registration with user id already registered and valid password
    #Input: duplicate user id, valid password
    #Expected output: users table in database is unchanged
    def test_create_account_duplicate_username(self):
        before = search_db("SELECT count(*) FROM users")
        data = {
          'firstname': 'jianr',
          'lastname': '132435'
        }        
        response = requests.post('http://localhost:1880/create_account', data=data)
        after = search_db("SELECT count(*) FROM users")
        #print(after)
        self.assertTrue(before[0][0] == after[0][0])
    
    #Purpose: Test a registration with user id with length 25, 26 and valid password
    #Input: long user id, valid password
    #Expected output: if user id length is below 25, users table updated with new account. Otherwise, table is unchaged
    def test_create_account_username_limit_25(self):
        before = search_db("SELECT count(*) FROM users")
        data = {
          'firstname': 'jianrjianrjianrjianrjianr1',
          'lastname': '132435'
        }        
        response = requests.post('http://localhost:1880/create_account', data=data)
        after = search_db("SELECT count(*) FROM users")
        self.assertTrue(before[0][0] == after[0][0])
        before = search_db("SELECT count(*) FROM users")
        data = {
          'firstname': 'jianrjianrjianrjianrjianr',
          'lastname': '132435'
        }        
        response = requests.post('http://localhost:1880/create_account', data=data)
        after = search_db("SELECT count(*) FROM users")
        self.assertTrue(before[0][0]+1 == after[0][0])
        search_db("DELETE FROM users WHERE username = '{}'".format(data["firstname"]))

    #Purpose: Test a registration with valid user id  and pasword with length 16, 17
    #Input: valid user id, long password
    #Expected output: if password length is below 16, users table updated with new account. Otherwise, table is unchanged
    def test_create_account_pwd_limit_16(self):
        before = search_db("SELECT count(*) FROM users")
        data = {
          'firstname': 'new',
          'lastname': '12345678901234567'
        }        
        response = requests.post('http://localhost:1880/create_account', data=data)
        after = search_db("SELECT count(*) FROM users")
        self.assertTrue(before[0][0] == after[0][0])
        
        before = search_db("SELECT count(*) FROM users")
        data = {
          'firstname': 'new',
          'lastname': '1234567890123456'
        }        
        response = requests.post('http://localhost:1880/create_account', data=data)
        after = search_db("SELECT count(*) FROM users")
        self.assertTrue(before[0][0]+1 == after[0][0])
        search_db("DELETE FROM users WHERE username = '{}'".format(data["firstname"]))
        

#Unit Tests for DeleteMenu method
class DeleteMenuTest(unittest.TestCase): 
    
    #Purpose: Test a appropriate deletion from the menu
    #Input: valid user id, valid meal type, valid recipe id
    #Expected output: specified recipe should be removed in menu, menu_ins, and menu_ingr table in the database
    def test_delete_menu(self):
        cookies = {
            'id': 'jianr'
        }        
        data = {
          'type': 'b',
          'name': '64d3724048'
        }
        response = requests.post('http://localhost:1880/addToMenu', cookies=cookies, data=data).json()
        before = search_db("SELECT count(*) FROM menu")
        before1 = search_db("SELECT count(*) FROM menu_ins")
        before2 = search_db("SELECT count(*) FROM menu_ingr")
        response = requests.post('http://localhost:1880/delete_menu', cookies=cookies, data=data)
        after = search_db("SELECT count(*) FROM menu")
        after1 = search_db("SELECT count(*) FROM menu_ins")
        after2 = search_db("SELECT count(*) FROM menu_ingr")
        diff1 = search_db("SELECT count(*) FROM (SELECT DISTINCT * FROM instructions WHERE id = '{}') as x".format(data["name"]))
        diff2 = search_db("SELECT count(*) FROM (SELECT DISTINCT * FROM ingredient WHERE id = '{}') as x".format(data["name"]))
        self.assertTrue(before[0][0]-1 == after[0][0])
        self.assertTrue(before1[0][0]-diff1[0][0] == after1[0][0])
        self.assertTrue(before2[0][0]-diff2[0][0] == after2[0][0])

    #Purpose: Test a deletion to the menu with an invalid user id
    #Input: invalid user id, valid meal type, valid recipe id
    #Expected output: menu, menu_ins, and menu_ingr table in the database should remain unchanged
    def test_delete_menu_invalid_cookie(self):
        cookies = {
            'id': 'rjian'
        }        
        data = {
          'type': 'b',
          'name': '64d3724048'
        }
        response = requests.post('http://localhost:1880/addToMenu', cookies=cookies, data=data).json()
        before = search_db("SELECT count(*) FROM menu")
        before1 = search_db("SELECT count(*) FROM menu_ins")
        before2 = search_db("SELECT count(*) FROM menu_ingr")
        response = requests.post('http://localhost:1880/delete_menu', cookies=cookies, data=data)
        after = search_db("SELECT count(*) FROM menu")
        after1 = search_db("SELECT count(*) FROM menu_ins")
        after2 = search_db("SELECT count(*) FROM menu_ingr")
        self.assertTrue(before[0][0] == after[0][0])
    
    #Purpose: Test a deletion to the menu with an invalid recipe id
    #Input: valid user id, valid meal type, invalid recipe id
    #Expected output: menu, menu_ins, and menu_ingr table in the database should remain unchanged
    def test_delete_menu_invalid_recipe(self):
        cookies = {
            'id': 'jianr'
        }        
        data = {
          'type': 'b',
          'name': '666666666'
        }
        response = requests.post('http://localhost:1880/addToMenu', cookies=cookies, data=data).json()
        before = search_db("SELECT count(*) FROM menu")
        before1 = search_db("SELECT count(*) FROM menu_ins")
        before2 = search_db("SELECT count(*) FROM menu_ingr")
        response = requests.post('http://localhost:1880/delete_menu', cookies=cookies, data=data)
        after = search_db("SELECT count(*) FROM menu")
        after1 = search_db("SELECT count(*) FROM menu_ins")
        after2 = search_db("SELECT count(*) FROM menu_ingr")
        self.assertTrue(before[0][0] == after[0][0])
    
    #Purpose: Test a deletion to the menu with an invalid meal type
    #Input: valid user id, invalid meal type, valid recipe id
    #Expected output: menu, menu_ins, and menu_ingr table in the database should remain unchanged
    def test_delete_menu_invalid_meal_type(self):
        cookies = {
            'id': 'jianr'
        }        
        data = {
          'type': 'a',
          'name': '64d3724048'
        }
        response = requests.post('http://localhost:1880/addToMenu', cookies=cookies, data=data).json()
        before = search_db("SELECT count(*) FROM menu")
        before1 = search_db("SELECT count(*) FROM menu_ins")
        before2 = search_db("SELECT count(*) FROM menu_ingr")
        response = requests.post('http://localhost:1880/delete_menu', cookies=cookies, data=data)
        after = search_db("SELECT count(*) FROM menu")
        after1 = search_db("SELECT count(*) FROM menu_ins")
        after2 = search_db("SELECT count(*) FROM menu_ingr")
        self.assertTrue(before[0][0] == after[0][0])

if __name__ == '__main__': 
    unittest.main(verbosity=2, exit=False)