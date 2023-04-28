from PyQt5 import QtWidgets,uic
import sys,sqlite3
from PyQt5.QtWidgets import QMessageBox,QApplication

is_logged_in = False
username=''

class Login(QtWidgets.QMainWindow):

    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Login.ui', self)
        self.show()
        self.login.clicked.connect(self.loginUser)

    def loginUser(self):
        global username
        username=self.emailfield.text()
        password=self.passwordfield.text()
        if len(username)==0 or len(password)==0:
            self.error.setText("Please input all fields.")
        else:
            conn = sqlite3.connect(r'D:\Databases\users.db')
            c=conn.cursor()
            query = 'SELECT password FROM users_list WHERE username =\''+username+"\'"
            c.execute(query)
            result_pass = c.fetchone()[0]
            if result_pass == password:
                print("Successfully logged in.")
                self.error.setText("")
                global is_logged_in
                is_logged_in=True
                self.close()
            else:
                self.error.setText("Invalid username or password")
        


app = QtWidgets.QApplication(sys.argv)
window = Login()
app.exec_()