from PyQt5 import QtWidgets,uic
import sys,sqlite3,datetime
from PyQt5.QtWidgets import QMessageBox,QApplication
from num2words import num2words

is_logged_in = False
username=''
class_room=''

class Login(QtWidgets.QMainWindow):

    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('Login.ui', self)
        self.show()
        self.login.clicked.connect(self.loginUser)

    def loginUser(self):
        global username
        global class_room
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
                current_time=datetime.datetime.now()
                formatted_time=current_time.strftime("%H:%M:%S")[:2]
                current_day=datetime.datetime.now().strftime("%A").lower()
                if int(formatted_time)>16:
                    is_logged_in=False
                    QMessageBox.warning(self,"TIME UP","ITS LATE. GET HOME SOON")
                #elif int(formatted_time)<9:
                    #is_logged_in=False
                    #QMessageBox.warning(self,"TOO SOON","YOU ARE A TOO SOON FOR THE CLASS")
                #elif current_day=="sunday":
                    #is_logged_in=False
                    #MessageBox.warning(self,"SUNDAY","TODAY IS A SUNDAY. TAKE A BREAK")
                else:
                    if formatted_time[0]=='0':
                        formatted_time=formatted_time[1:]
                    formatted_time=int(formatted_time)
                    number_in_words = num2words(formatted_time)
                    time_query='SELECT '+number_in_words+' FROM timetable WHERE teacher_name =\''+username+"\'"+' AND day =\''+current_day+"\'"
                    c.execute(time_query)
                    rows=c.fetchone()[0]
                    print(rows)
                    if rows==None:
                        msg_box = QMessageBox()
                        msg_box.setWindowTitle("EXTRA CLASS")
                        msg_box.setText("Are you sure you want to take an extra class?")
                        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                        #msg_box.setDefaultButton(QMessageBox.Cancel)
                        response = msg_box.exec_()
                        if response == QMessageBox.Ok:
                            is_logged_in=True
                        else:
                            is_logged_in=False
                    class_room=rows
                self.close()
            else:
                self.error.setText("Invalid username or password")
        


app = QtWidgets.QApplication(sys.argv)
window = Login()
app.exec_()