"""
Configuration file with security issues
"""

# Security Issue: Hardcoded credentials
DATABASE_URL = "postgresql://admin:password123@localhost/mydb"

# Security Issue: Hardcoded API keys
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Security Issue: Weak encryption
ENCRYPTION_KEY = "1234567890123456"

# Security Issue: Insecure settings
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
SSL_VERIFY = False
