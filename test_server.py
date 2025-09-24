import unittest
import bcrypt
from server import authenticate, add_user_hashed,manage_private_message,users_list, clients, clients_name

'''
Dummy socket class to simulate sending/receiving 
without real network.
'''
class DummySocket:
    #a fake socket to capture sent messages in memory instead of sending over network.
    def __init__(self):
         self.sent_messages = []
             
    def send(self, data):
       #Simulate sending by storing messages in a list.
       self.sent_messages.append(data.decode())

    def close(self):
          pass

class TestServerFunctions(unittest.TestCase):
    def setUp(self):
        
        #clears the in-memory storage.Runs before each test.
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

    def test_manage_private_message_success(self):
          
        sender = 'James'
        recipient = 'John'
        message = 'Hello John!'

        fake_sender_socket = DummySocket()
        fake_recipient_socket = DummySocket()

        #setup server state
        clients.clear()
        clients_name.clear()
        clients.append(fake_recipient_socket)
        clients_name.append(recipient)

        #call the function under test
        manage_private_message(sender, recipient, message,fake_sender_socket)

        #verify recipient got the Direct Message (DM)
        self.assertTrue(any('Hello John!' in msg for msg in fake_recipient_socket.sent_messages))
          #verifies sender got confirmation
        self.assertTrue(any('DM to John' in msg for msg in fake_sender_socket.sent_messages))

    def test_manage_private_message_user_not_found(self):
        sender = 'James'
        recipient = 'John'
        message = 'Hi!'
        fake_sender_socket = DummySocket()

        clients.clear()
        clients_name.clear()

        manage_private_message(sender, recipient,message,fake_sender_socket)

        self.assertTrue(any('not found' in msg for msg in fake_sender_socket.sent_messages))
if __name__ == '__main__':
            unittest.main()