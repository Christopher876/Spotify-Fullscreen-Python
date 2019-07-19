import sys
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt5.QtGui import QIcon, QPixmap, QIcon
import spotipy
from spotify_account import Spotify
import threading
import time

class Login_Dialog(QDialog):
    def __init__(self):
        super(Login_Dialog,self).__init__()
        loadUi('spotify-dialog.ui',self)
        self.setWindowTitle("Spotify Account")
        
        self.options_button.accepted.connect(self.save_login_info)
    
    #TODO NOT WORKING ATM
    @pyqtSlot()    
    def save_login_info(self):
        '''with open("config.ini","w") as outfile:
            outfile.write(self.username.toPlainText() + '\n')
            outfile.write(self.client_id.toPlainText() + '\n')
            outfile.write(self.client_secret.toPlainText())
'''
class Fullscreen_Spotify(QMainWindow):
    def __init__(self):
        super(Fullscreen_Spotify,self).__init__()
        loadUi('spotify-fullscreen.ui',self)
        self.setWindowTitle("Full Screen Spotify")
        self.setWindowIcon(QIcon('icon.png'))
        self.showFullScreen()
        #self.test1.clicked.connect(self.on_click)

        self.menu_account.triggered.connect(self.account_login)

        self.spotify = Spotify()
        self.set_widgets_song_info()
        self.menubar.setVisible(False)

        self.need_to_exit = False
        self.check_thread = threading.Thread(target=self.check_song_update)
        self.check_thread.start()
    
    #Check if the song has changed and then change it
    def check_song_update(self):
        while(self.need_to_exit != True):
            time.sleep(2)
            self.set_widgets_song_info()
    
    #Set all the information from the now playing song to the QT interface
    def set_widgets_song_info(self):
        song_info = self.spotify.get_song_info()
        
        if song_info is not None and song_info['song_name'] != self.song_name.text(): 
            #Set new album info
            pixmap = QPixmap()
            pixmap.loadFromData(self.spotify.get_album_art(song_info['album_art']))
            self.image1.setPixmap(pixmap)
            self.image1.resize(1920,1080)

            self.album_name.setText(song_info['album_name'])
            self.artist_name.setText(song_info['artist_name'])
            self.release_date.setText(song_info['release_date'])
            self.song_length.setText(song_info['song_length'])
            self.song_name.setText(song_info['song_name'])

    #Setup for getting key events
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.need_to_exit = True
            time.sleep(1)
            QApplication.exit()
        
        if key == Qt.Key_Right:
            self.spotify.next_track()
            self.set_widgets_song_info()
        
        if key == Qt.Key_Left:
            self.spotify.previous_track()
            self.set_widgets_song_info()
        
        if key == Qt.Key_Space:
            if self.spotify.is_playing_music is True:
                try:
                    self.spotify.pause_track()
                except Exception:
                    self.spotify.play_track()

            else:
                self.spotify.play_track()

        if key == Qt.Key_M:
            if self.menubar.isVisible():
                self.menubar.setVisible(False)
            else:
                self.menubar.setVisible(True)
        
        if key == Qt.Key_R:
            self.set_widgets_song_info()
        
        if key == Qt.Key_I:
            if self.isFullScreen():
                self.showMaximized()
            else:
                self.showFullScreen()

    @pyqtSlot()
    def on_click(self):
        pass
    
    @pyqtSlot()
    #Show the dialog box for the account info
    def account_login(self):
        spotify_account = Login_Dialog()
        spotify_account.exec_()

def main():
    app = QApplication(sys.argv)
    widget = Fullscreen_Spotify()
    widget.show()
    sys.exit(app.exec_())
    print("Exited Successfully!")

if __name__ == "__main__":
    main()