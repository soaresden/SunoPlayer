#!/usr/bin/env python3
"""
Suno Music Player
A beautiful PyQt5 application to browse, play and download Suno music

Usage:
    python main.py
"""

import sys
import os
import json
import requests
from pathlib import Path
from datetime import datetime
import pygame
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QSlider,
    QComboBox, QFileDialog, QMessageBox, QProgressBar,
    QSystemTrayIcon, QMenu, QHeaderView, QDialog, QSpinBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QObject, QSize
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import QApplication
import requests
from auth import AuthManager
from api import SunoAPI


class DownloadWorker(QObject):
    """Worker thread for downloading files"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, url: str, output_path: str):
        super().__init__()
        self.url = url
        self.output_path = output_path
    
    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(self.output_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            self.progress.emit(int(percent))
            
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))


class MusicPlayer(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Suno Music Player")
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1000, 600)
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
        except:
            print("Warning: Could not initialize audio mixer")
        
        # State variables
        self.auth_manager = AuthManager()
        self.api = None
        self.token = None
        self.workspaces = []
        self.current_clips = []
        self.current_clip = None
        self.is_playing = False
        self.current_file_path = None
        
        # Setup UI
        self.setup_ui()
        self.setup_tray()
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_player_state)
        self.timer.start(100)
        
        # Authenticate and load data
        self.authenticate()
    
    def setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Top bar with workspace selector
        top_layout = QHBoxLayout()
        
        label = QLabel("Workspace:")
        label.setStyleSheet("font-weight: bold;")
        top_layout.addWidget(label)
        
        self.workspace_combo = QComboBox()
        self.workspace_combo.currentIndexChanged.connect(self.on_workspace_changed)
        self.workspace_combo.setMinimumWidth(300)
        top_layout.addWidget(self.workspace_combo)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_workspaces)
        top_layout.addWidget(refresh_btn)
        
        logout_btn = QPushButton("🔐 Re-login")
        logout_btn.clicked.connect(self.relogin)
        top_layout.addWidget(logout_btn)
        
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        
        # Songs table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["#", "Title", "Status", "Created", "Duration"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
        """)
        self.table.itemSelectionChanged.connect(self.on_track_selected)
        main_layout.addWidget(self.table)
        
        # Player section
        player_layout = QVBoxLayout()
        
        # Now playing
        self.now_playing_label = QLabel("No track selected")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.now_playing_label.setFont(font)
        player_layout.addWidget(self.now_playing_label)
        
        # Progress bar
        progress_layout = QHBoxLayout()
        self.time_label_start = QLabel("0:00")
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.sliderMoved.connect(self.seek_player)
        self.time_label_end = QLabel("0:00")
        progress_layout.addWidget(self.time_label_start)
        progress_layout.addWidget(self.progress_slider, 1)
        progress_layout.addWidget(self.time_label_end)
        player_layout.addLayout(progress_layout)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.clicked.connect(self.play_current)
        self.play_btn.setMinimumWidth(100)
        control_layout.addWidget(self.play_btn)
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.clicked.connect(self.pause_player)
        self.pause_btn.setMinimumWidth(100)
        control_layout.addWidget(self.pause_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(self.stop_player)
        self.stop_btn.setMinimumWidth(100)
        control_layout.addWidget(self.stop_btn)
        
        # Volume control
        control_layout.addSpacing(20)
        control_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximumWidth(150)
        self.volume_slider.valueChanged.connect(self.set_volume)
        control_layout.addWidget(self.volume_slider)
        
        # Download button
        download_btn = QPushButton("⬇ Download")
        download_btn.clicked.connect(self.download_current)
        download_btn.setMinimumWidth(100)
        control_layout.addWidget(download_btn)
        
        control_layout.addStretch()
        player_layout.addLayout(control_layout)
        
        main_layout.addLayout(player_layout)
        
        central_widget.setLayout(main_layout)
    
    def setup_tray(self):
        """Setup system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show_window)
        
        play_action = tray_menu.addAction("Play")
        play_action.triggered.connect(self.play_current)
        
        pause_action = tray_menu.addAction("Pause")
        pause_action.triggered.connect(self.pause_player)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction("Exit")
        quit_action.triggered.connect(QApplication.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Simple icon
        self.set_tray_icon()
        self.tray_icon.activated.connect(self.tray_activated)
    
    def set_tray_icon(self):
        """Set tray icon"""
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (64, 64), color='#0078d4')
        draw = ImageDraw.Draw(img)
        draw.text((18, 20), "SUNO", fill='white')
        
        icon_path = Path.home() / ".suno_player" / "icon.png"
        icon_path.parent.mkdir(exist_ok=True)
        img.save(icon_path)
        
        self.tray_icon.setIcon(QIcon(str(icon_path)))
        self.setWindowIcon(QIcon(str(icon_path)))
    
    def authenticate(self):
        """Handle authentication"""
        # Try to get cached token
        token = self.auth_manager.get_valid_token()
        
        if not token:
            # Need new authentication
            token = self.auth_manager.authenticate()
        
        if not token:
            QMessageBox.critical(self, "Authentication Error", "Failed to authenticate with Suno")
            sys.exit(1)
        
        self.token = token
        self.api = SunoAPI(token)
        
        # Verify and load data
        session_info = self.api.get_session_info()
        if session_info and 'user' in session_info:
            user_name = session_info['user'].get('name', 'Unknown')
            self.setWindowTitle(f"Suno Music Player - {user_name}")
        
        self.refresh_workspaces()
    
    def relogin(self):
        """Clear token and re-authenticate"""
        self.auth_manager.clear_token()
        self.authenticate()
    
    def refresh_workspaces(self):
        """Refresh list of workspaces"""
        if not self.api:
            return
        
        self.workspaces = self.api.get_workspaces()
        
        self.workspace_combo.blockSignals(True)
        self.workspace_combo.clear()
        
        for ws in self.workspaces:
            display_text = f"{ws['name']} ({ws.get('clip_count', 0)} clips)"
            self.workspace_combo.addItem(display_text, ws['id'])
        
        self.workspace_combo.blockSignals(False)
        
        if self.workspace_combo.count() > 0:
            self.on_workspace_changed()
    
    def on_workspace_changed(self):
        """Handle workspace selection change"""
        if self.workspace_combo.currentIndex() < 0:
            return
        
        project_id = self.workspace_combo.currentData()
        self.current_clips = self.api.get_clips(project_id)
        self.load_clips_table()
    
    def load_clips_table(self):
        """Load clips into table"""
        self.table.setRowCount(len(self.current_clips))
        
        for idx, clip in enumerate(self.current_clips):
            # Number
            item = QTableWidgetItem(str(idx + 1))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(idx, 0, item)
            
            # Title
            item = QTableWidgetItem(clip.get('title', 'N/A'))
            self.table.setItem(idx, 1, item)
            
            # Status
            status = clip.get('status', 'unknown')
            item = QTableWidgetItem(status)
            item.setTextAlignment(Qt.AlignCenter)
            if status == 'success':
                item.setBackground(QColor(144, 238, 144))
            elif status == 'queued':
                item.setBackground(QColor(255, 200, 124))
            else:
                item.setBackground(QColor(200, 200, 200))
            self.table.setItem(idx, 2, item)
            
            # Created date
            created = clip.get('created_at', '').split('T')[0]
            item = QTableWidgetItem(created)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(idx, 3, item)
            
            # Duration
            duration = clip.get('duration', 0)
            duration_str = f"{duration}s" if duration else "N/A"
            item = QTableWidgetItem(duration_str)
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(idx, 4, item)
    
    def on_track_selected(self):
        """Handle track selection"""
        selected = self.table.selectedIndexes()
        if not selected:
            return
        
        row = selected[0].row()
        self.current_clip = self.current_clips[row]
        
        title = self.current_clip.get('title', 'Unknown')
        status = self.current_clip.get('status', 'unknown')
        
        self.now_playing_label.setText(f"Selected: {title} ({status})")
    
    def play_current(self):
        """Play the selected track"""
        if not self.current_clip:
            QMessageBox.warning(self, "Error", "Please select a track!")
            return
        
        if self.current_clip.get('status') != 'success':
            QMessageBox.warning(self, "Error", "This track is not ready yet!")
            return
        
        clip_details = self.api.get_clip_details(self.current_clip['id'])
        audio_url = clip_details.get('audio_url')
        
        if not audio_url:
            QMessageBox.warning(self, "Error", "No audio URL found!")
            return
        
        try:
            # Download to temp file
            response = requests.get(audio_url, timeout=30)
            temp_file = Path.home() / ".suno_player" / "temp_play.mp3"
            temp_file.parent.mkdir(exist_ok=True)
            
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            
            # Play with pygame
            pygame.mixer.music.load(str(temp_file))
            pygame.mixer.music.play()
            self.is_playing = True
            self.current_file_path = str(temp_file)
            self.play_btn.setText("⏸ Playing...")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Playback error: {e}")
    
    def pause_player(self):
        """Pause/unpause playback"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_btn.setText("▶ Paused")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_btn.setText("⏸ Playing...")
    
    def stop_player(self):
        """Stop playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_btn.setText("▶ Play")
        self.progress_slider.setValue(0)
    
    def seek_player(self, position):
        """Seek in track (limited by pygame capabilities)"""
        pass
    
    def set_volume(self, value):
        """Set player volume"""
        pygame.mixer.music.set_volume(value / 100.0)
    
    def update_player_state(self):
        """Update player state"""
        if pygame.mixer.music.get_busy() and self.is_playing:
            pass
    
    def download_current(self):
        """Download the selected track"""
        if not self.current_clip:
            QMessageBox.warning(self, "Error", "Please select a track!")
            return
        
        if self.current_clip.get('status') != 'success':
            QMessageBox.warning(self, "Error", "This track is not ready yet!")
            return
        
        save_dir = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if not save_dir:
            return
        
        clip_details = self.api.get_clip_details(self.current_clip['id'])
        audio_url = clip_details.get('audio_url')
        
        if not audio_url:
            QMessageBox.warning(self, "Error", "No audio URL found!")
            return
        
        try:
            title = self.current_clip['title']
            # Clean filename
            title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            file_path = Path(save_dir) / f"{title}.mp3"
            
            # Show download progress
            progress = QProgressBar()
            progress.setWindowTitle("Downloading...")
            progress.show()
            
            response = requests.get(audio_url, stream=True, timeout=30)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(file_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = int((downloaded / total_size) * 100)
                            progress.setValue(percent)
            
            progress.close()
            QMessageBox.information(self, "Success", f"Downloaded to:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Download error: {e}")
    
    def show_window(self):
        """Show/restore window"""
        self.show()
        self.activateWindow()
    
    def tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
    
    def changeEvent(self, event):
        """Handle window state changes"""
        if event.type() == event.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self.hide()
                event.ignore()
        super().changeEvent(event)
    
    def closeEvent(self, event):
        """Handle close event"""
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            pygame.mixer.stop()
            event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Suno Music Player")
    app.setApplicationVersion("1.0.0")
    
    player = MusicPlayer()
    player.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
