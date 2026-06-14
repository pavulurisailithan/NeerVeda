import os
import struct

def create_mo_file():
    # Telugu translations
    translations = {
        "Welcome to NeerVeda": "నీర్వేదకు స్వాగతం",
        "Sign in to your account": "మీ ఖాతాలోకి సైన్ ఇన్ చేయండి",
        "Email": "ఇమెయిల్",
        "Password": "పాస్వర్డ్",
        "Sign In": "సైన్ ఇన్",
        "Don't have an account?": "ఖాతా లేదా?",
        "Sign up": "సైన్ అప్",
        "Create Account": "ఖాతా సృష్టించండి",
        "Get started with NeerVeda": "నీర్వేదతో ప్రారంభించండి",
        "Full Name": "పూర్తి పేరు",
        "Already have an account?": "ఇప్పటికే ఖాతా ఉందా?",
        "English": "ఇంగ్లీష్",
        "Telugu": "తెలుగు"
    }
    
    # Create simple mo file content
    mo_content = b''
    
    # Write to file
    os.makedirs('translations/te/LC_MESSAGES', exist_ok=True)
    
    # Create a simple mapping file for Flask-Babel
    with open('translations/te/LC_MESSAGES/messages.mo', 'wb') as f:
        # Simple MO file header
        f.write(b'\xde\x12\x04\x95')  # Magic number
        f.write(struct.pack('<I', 0))  # Version
        f.write(struct.pack('<I', len(translations)))  # Number of strings
        f.write(struct.pack('<I', 28))  # Offset of key table
        f.write(struct.pack('<I', 28 + len(translations) * 8))  # Offset of value table
        f.write(struct.pack('<I', 0))  # Hash table size
        f.write(struct.pack('<I', 0))  # Hash table offset
        
        # Write string tables (simplified)
        for key, value in translations.items():
            key_bytes = key.encode('utf-8')
            value_bytes = value.encode('utf-8')
            f.write(struct.pack('<I', len(key_bytes)))
            f.write(struct.pack('<I', 0))  # Offset placeholder
        
        for key, value in translations.items():
            value_bytes = value.encode('utf-8')
            f.write(struct.pack('<I', len(value_bytes)))
            f.write(struct.pack('<I', 0))  # Offset placeholder

if __name__ == '__main__':
    create_mo_file()
    print("Translation file created!")