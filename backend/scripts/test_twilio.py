#!/usr/bin/env python3
"""
Test script for Twilio SMS functionality
"""

import os
from twilio.rest import Client

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")
TEST_PHONE_NUMBER = os.getenv("TEST_PHONE_NUMBER", "+1234567890")

def test_twilio_sms():
    """
    Test sending SMS via Twilio
    """
    if not TWILIO_AVAILABLE:
        print("Cannot test Twilio SMS - library not available")
        return False
        
    try:
        if Client is not None:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body="This is a test message from Acoustic Guardian simulation.",
                from_=TWILIO_PHONE_NUMBER,
                to=TEST_PHONE_NUMBER
            )
            print(f"SUCCESS: SMS sent. Message SID: {message.sid}")
            return True
        else:
            print("Twilio Client not available")
            return False
    except Exception as e:
        print(f"ERROR: Failed to send SMS: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Twilio SMS functionality...")
    test_twilio_sms()