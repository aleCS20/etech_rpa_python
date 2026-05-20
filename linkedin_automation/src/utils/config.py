import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LINKEDIN_URL = "https://www.linkedin.com/login"
    TERMO_PESQUISA = "RPA Automation"
    
    EMAIL = os.getenv("LINKEDIN_EMAIL")
    PASSWORD = os.getenv("LINKEDIN_PASSWORD")
