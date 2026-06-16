# Password Reset via Microsoft Entra ID (Azure AD)

## Overview
This article explains how to reset your Windows or Microsoft 365 password using Microsoft Entra ID Self-Service Password Reset (SSPR). Most employees can reset their own password without contacting IT.

## Self-Service Password Reset (Recommended)

### Step 1 – Go to the reset portal
Open a browser and navigate to: https://aka.ms/sspr

### Step 2 – Enter your corporate email
Type your full corporate email address (e.g., jsmith@company.com) and complete the CAPTCHA.

### Step 3 – Verify your identity
You will be prompted to verify via one of the methods you registered:
- Microsoft Authenticator app notification
- Text message to your registered mobile number
- Email to your personal/backup email address

### Step 4 – Set your new password
Enter and confirm a new password that meets the complexity requirements:
- Minimum 12 characters
- At least one uppercase letter, one lowercase letter, one number, and one special character
- Cannot reuse any of your last 10 passwords

### Step 5 – Sign back in
Your new password is effective immediately across all Microsoft 365 apps, Windows login, and VPN.

## If SSPR Is Not Working

SSPR may be unavailable if:
- You have not registered your SSPR methods (common for new hires)
- Your account is locked out due to too many failed attempts

In these cases, contact the IT Help Desk:
- Submit a ticket via ServiceNow
- Call the help desk at ext. 5000

## Registering for SSPR (First-Time Setup)
Go to https://aka.ms/ssprsetup while signed into your corporate account. Register at least two verification methods to ensure you can always recover access.

## Related Articles
- MFA Setup with Microsoft Authenticator
- Account Lockout and Entra ID
