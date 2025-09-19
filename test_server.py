import unittest
import bcrypt
from server import authenticate, add_user_hashed,manage_private_message,users_list

class TestServerFunctions(unittest.TestCase):
    def setUp(self):
        
        #clears the in-memory storage
        users_list.clear()
        #creates a test users file
        self.test_file = 'test_users.txt'
        #add test users
        add_user_hashed('James', 'password1', self.test_file)
        add_user_hashed('Jake','password2', self.test_file)

    def test_add_user_hashed(self):
            #Ensures add_user_hashed stores a bcrypt hash, not a plaint-text.
            hashed_pswd = users_list['James']
            self.assertTrue(hashed_pswd.startswith('$2'))
            self.assertNotEqual(hashed_pswd, 'password1')

    def test_aunthenticate_correct_password(self):
           '''Users should authenticate with correct password.'''
           self.assertTrue(authenticate('James', 'password1'))
    
    def test_authenticate_wrong_password(self):
           #wrong password should fail authentication
           self.assertFalse(authenticate('James', 'wrongpassword'))

    def test_authenticate_nonexistent_user(self):
           #authentication should fail for non-existent user
           self.assertFalse(authenticate('Alice', 'password1'))

if __name__ == '__main__':
            unittest.main()
