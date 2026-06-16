# Software Installation via Company Portal & Jamf Self Service

## Overview
All software on company devices must be installed through approved channels. Installing unauthorized software violates company security policy and may trigger endpoint alerts.

## Installing Approved Software

### Windows — Company Portal
1. Open the **Company Portal** app (search in Start menu)
2. Browse or search for the application you need
3. Click **Install**
4. The software installs silently in the background — no admin password required
5. Check status under "Installed" once complete (typically 5–20 minutes)

### macOS — Jamf Self Service
1. Open **Self Service** from your Applications folder or Dock
2. Search for the application by name
3. Click **Install**
4. The app installs automatically — some apps may request your Mac login password
5. Larger apps (e.g., Adobe Creative Cloud) may take 15–30 minutes

## Requesting Software Not in the Portal

If the software you need is not available in Company Portal or Self Service, submit a software request through ServiceNow:
1. Go to https://company.service-now.com
2. Select "Software Request" from the catalog
3. Provide: software name, version, business justification, and your manager's name
4. IT will review for security/licensing compatibility within 3 business days
5. Approved software is added to the portal and you receive a notification to install

## Common Applications and Where to Find Them

| Application | Platform | Location |
|---|---|---|
| Microsoft 365 (Office) | Win / Mac | Company Portal / Self Service |
| Zoom | Win / Mac | Company Portal / Self Service |
| Slack | Win / Mac | Company Portal / Self Service |
| Adobe Acrobat Reader | Win / Mac | Company Portal / Self Service |
| GitHub Desktop | Win / Mac | Company Portal / Self Service |
| Python / VS Code | Win / Mac | Company Portal / Self Service |
| Adobe Creative Cloud | Mac | Jamf Self Service (license required) |

## Troubleshooting

### "Company Portal shows 0 apps / blank screen"
Your device may not be compliant. Check Settings → Accounts → Access Work or School to ensure your account is connected. If the issue persists, restart the Intune Management Extension service: open Services, find "Microsoft Intune Management Extension," and click Restart.

### "Install button is grayed out"
You may already have a version of this app installed. Uninstall the existing version through Add/Remove Programs first, then retry. If the button remains grayed out, contact the Help Desk.

### "Software installed but not launching"
Try restarting your computer. Some applications require a full reboot after installation to complete configuration.
