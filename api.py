"""
Suno API Client
Handles all API calls to Suno backend
"""

import requests
from typing import List, Dict, Optional


class SunoAPI:
    """Client for Suno Music API"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://studio-api.prod.suno.com"
        self.device_id = "8f955be9-40b8-496e-9a05-c12b86abd5f8"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Device-Id": self.device_id,
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0"
        }
    
    def get_workspaces(self, page: int = 1, limit: int = 50) -> List[Dict]:
        """Get all user workspaces/projects"""
        try:
            url = f"{self.base_url}/api/project/me?page={page}&limit={limit}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('projects', [])
        except Exception as e:
            print(f"Error fetching workspaces: {e}")
            return []
    
    def get_clips(self, project_id: str, page: int = 1, limit: int = 100) -> List[Dict]:
        """Get clips/songs from a specific workspace"""
        try:
            url = f"{self.base_url}/api/project/{project_id}/clips?page={page}&limit={limit}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('clips', [])
        except Exception as e:
            print(f"Error fetching clips: {e}")
            return []
    
    def get_clip_details(self, clip_id: str) -> Dict:
        """Get detailed information about a clip including audio URL"""
        try:
            url = f"{self.base_url}/api/clip/{clip_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching clip details: {e}")
            return {}
    
    def get_session_info(self) -> Dict:
        """Get current session information"""
        try:
            url = f"{self.base_url}/api/session/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching session: {e}")
            return {}
