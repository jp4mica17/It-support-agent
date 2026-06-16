# Windows Device Enrollment in Microsoft Intune

## Overview
All company-owned Windows devices must be enrolled in Microsoft Intune (MDM) to access corporate resources. Enrollment enables IT to push security policies, deploy software, and ensure compliance.

## Prerequisites
- Windows 10 (version 1909 or later) or Windows 11
- Your corporate email and password
- Active internet connection

## Enrollment Steps

### Method 1 – Enroll During Windows Setup (New Devices)
On the "How would you like to set up?" screen, choose "Set up for an organization." Sign in with your corporate email address. Windows will automatically join Azure AD and enroll in Intune.

### Method 2 – Enroll an Existing Windows Device
1. Open **Settings** → **Accounts** → **Access work or school**
2. Click **Connect**
3. Enter your corporate email address
4. Sign in with your password and approve the MFA prompt
5. When prompted, allow the device to be managed by your organization
6. Windows will download and apply Intune policies in the background (5–15 minutes)

## Verifying Enrollment
Open Settings → Accounts → Access work or school. You should see your account listed with a briefcase icon and the label "Connected to [Company] Azure AD." To confirm compliance, open the **Company Portal** app and check that your device shows "Compliant."

## What Happens After Enrollment
- Company Wi-Fi and VPN certificates are pushed automatically
- Required software is installed via Company Portal
- BitLocker encryption is enabled (your recovery key is backed up to Entra ID)
- Security policies (screen lock, password requirements) are applied

## Troubleshooting

### "I can't connect — enrollment fails with an error"
Ensure you are using your corporate email, not a personal Microsoft account. If you see "Your organization doesn't allow personal accounts," contact IT — your account may need a license assigned.

### "Company Portal says my device is 'Not compliant'"
Common causes: pending Windows Updates, BitLocker not yet activated, or antivirus out of date. Allow 30 minutes after enrollment for policies to apply, then open Company Portal and tap "Check access."
