# MFA Setup with Microsoft Authenticator

## Overview
Multi-Factor Authentication (MFA) is required for all corporate accounts. The Microsoft Authenticator app is the preferred method. This article covers initial setup and common troubleshooting steps.

## Initial Setup

### Step 1 – Download the app
Install Microsoft Authenticator from the App Store (iOS) or Google Play (Android).

### Step 2 – Navigate to the MFA setup portal
On your computer, go to: https://aka.ms/mfasetup
Sign in with your corporate email and current password.

### Step 3 – Add your account in the app
In the Authenticator app, tap the "+" icon → Work or school account → Scan QR code.
Scan the QR code displayed on the setup portal.

### Step 4 – Test the setup
The portal will send a test notification to your phone. Approve it to confirm setup is complete.

## Troubleshooting Common MFA Issues

### "I'm not receiving push notifications"
1. Check that notifications are enabled for Microsoft Authenticator in your phone's Settings.
2. Ensure your phone has an active internet connection (Wi-Fi or cellular).
3. Open the Authenticator app and tap "Refresh" to manually fetch pending notifications.
4. If notifications still don't arrive, use the 6-digit code shown in the app instead of a push notification.

### "My codes keep saying 'incorrect'"
Time drift can cause TOTP codes to fail. On Android: open Authenticator → Menu → Settings → Time Correction for Codes → Sync Now. On iPhone, ensure "Set Automatically" is enabled under Settings → General → Date & Time.

### "I got a new phone and lost access to Authenticator"
Contact the IT Help Desk immediately. An IT analyst will verify your identity through alternate means and re-register your MFA device. Do not delay — you will be locked out of all corporate systems until this is resolved.

### "I'm being prompted for MFA every time I log in"
This is expected on new or unregistered devices. Once your device is enrolled in Intune and marked as compliant, you will experience fewer MFA prompts on trusted devices.

## Adding a Backup MFA Method
Always register a backup method (phone number for SMS) in case your primary device is unavailable. Go to https://aka.ms/mfasetup → Add method → Phone.
