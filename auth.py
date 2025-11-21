"""
Authentication module for Suno Music Player
Handles token management, validation, and automatic token retrieval
"""

import json
import requests
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime
import jwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time


class AuthManager:
    """Manages authentication with Suno API"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".suno_player"
        self.config_dir.mkdir(exist_ok=True)
        self.token_file = self.config_dir / "token.json"
        self.api_base = "https://studio-api.prod.suno.com"
        self.device_id = "8f955be9-40b8-496e-9a05-c12b86abd5f8"
    
    def get_valid_token(self) -> Optional[str]:
        """Get a valid token, either from cache or by re-authenticating"""
        # Try to load from cache
        token = self._load_cached_token()
        
        if token and self._validate_token(token):
            print("✓ Using cached token")
            return token
        
        # Token expired or missing, need new one
        print("Token expired or missing, need to authenticate...")
        return None
    
    def authenticate(self) -> Optional[str]:
        """Authenticate with Suno and get a new token"""
        print("\n=== SUNO AUTHENTICATION ===\n")
        
        # Try automatic authentication first
        token = self._auto_authenticate()
        
        if token:
            self._save_token(token)
            return token
        
        # Fallback to manual token entry
        print("\nFallback: Manual token entry")
        token = self._manual_token_entry()
        
        if token and self._validate_token(token):
            self._save_token(token)
            return token
        
        return None
    
    def _auto_authenticate(self) -> Optional[str]:
        """Automatically retrieve token by launching browser and capturing from localStorage"""
        try:
            print("1. Opening Suno.com in browser...")
            print("2. Please login with your Suno account...")
            print("3. Waiting for authentication...")
            
            # Setup Chrome options
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Launch browser
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://suno.com/create")
            
            # Wait for user to login (max 5 minutes)
            print("\n(Waiting max 5 minutes for login...)")
            wait = WebDriverWait(driver, 300)
            
            # Wait for the app to fully load after login
            # We'll check for the presence of the project list or just wait for a token in localStorage
            
            for attempt in range(60):  # Check every 5 seconds for 5 minutes
                try:
                    # Try to get token from localStorage
                    script = """
                    try {
                        const token = localStorage.getItem('__clerk_db_jwt');
                        if (token) {
                            return token;
                        }
                        return null;
                    } catch(e) {
                        return null;
                    }
                    """
                    
                    token = driver.execute_script(script)
                    
                    if token:
                        print("✓ Token captured from browser!")
                        driver.quit()
                        return token
                    
                    if attempt > 0 and attempt % 6 == 0:
                        print(f"Still waiting... ({attempt * 5} seconds)")
                    
                    time.sleep(5)
                    
                except Exception as e:
                    time.sleep(5)
                    continue
            
            driver.quit()
            print("✗ Timeout: Could not capture token")
            return None
            
        except Exception as e:
            print(f"✗ Auto-authentication failed: {e}")
            try:
                driver.quit()
            except:
                pass
            return None
    
    def _manual_token_entry(self) -> Optional[str]:
        """Prompt user to manually enter their token"""
        print("\nHow to get your token:")
        print("  1. Go to https://suno.com/create")
        print("  2. Press F12 (Developer Tools)")
        print("  3. Go to Network tab")
        print("  4. Refresh the page")
        print("  5. Look for a request to 'api/project/me'")
        print("  6. Click on it -> Headers tab")
        print("  7. Find 'Authorization: Bearer XXX'")
        print("  8. Copy the string after 'Bearer '")
        print()
        
        token = input("Paste your Bearer Token: ").strip()
        return token if token else None
    
    def _validate_token(self, token: str) -> bool:
        """Validate that the token is still valid"""
        try:
            # Check token format
            if not token or len(token) < 100:
                return False
            
            # Decode JWT to check expiration
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp = decoded.get('exp')
            
            if exp and datetime.fromtimestamp(exp) < datetime.now():
                print("✗ Token expired")
                return False
            
            # Verify with API
            headers = {
                "Authorization": f"Bearer {token}",
                "Device-Id": self.device_id,
            }
            
            response = requests.get(
                f"{self.api_base}/api/session/",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                print("✓ Token is valid")
                return True
            else:
                print("✗ Token invalid (API rejected)")
                return False
                
        except Exception as e:
            print(f"✗ Token validation error: {e}")
            return False
    
    def _load_cached_token(self) -> Optional[str]:
        """Load token from cache file"""
        try:
            if self.token_file.exists():
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
                    return data.get('token')
        except:
            pass
        return None
    
    def _save_token(self, token: str):
        """Save token to cache file"""
        try:
            data = {
                'token': token,
                'saved_at': datetime.now().isoformat()
            }
            with open(self.token_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Token saved to {self.token_file}")
        except Exception as e:
            print(f"Warning: Could not save token: {e}")
    
    def clear_token(self):
        """Clear cached token"""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
            print("✓ Token cleared")
        except:
            pass
