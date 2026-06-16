# VPN Access — Cisco AnyConnect Setup & Troubleshooting

## Overview
Remote access to corporate resources (internal servers, shared drives, on-premises apps) requires the Cisco AnyConnect VPN client. VPN is available on Windows, macOS, iOS, and Android.

## Installation

### Windows
Cisco AnyConnect is deployed automatically via Intune Company Portal. If it is missing, open Company Portal, search for "Cisco AnyConnect," and click Install.

### macOS
Jamf deploys AnyConnect automatically after device enrollment. If missing, open Jamf Self Service and click "Install" next to Cisco AnyConnect. An admin password prompt may appear during installation — use your Mac login password.

## Connecting to VPN

1. Open the Cisco AnyConnect Secure Mobility Client
2. In the server field, enter: `vpn.company.com`
3. Click **Connect**
4. Enter your corporate username (your email) and password
5. Complete the MFA prompt on your Microsoft Authenticator app
6. You are connected when the icon shows a lock

## Disconnecting
Click the AnyConnect icon in the system tray (Windows) or menu bar (Mac) → Disconnect. Always disconnect when you do not need VPN to conserve bandwidth and battery.

## Troubleshooting

### "VPN connects but disconnects every few minutes"
This is usually a split-tunnel or DNS timeout issue. Try:
1. Quit and reopen AnyConnect completely
2. Restart your router/modem
3. Try a wired (Ethernet) connection instead of Wi-Fi
4. If the problem persists across different networks, submit a ticket — your VPN profile may need to be reissued

### "VPN says 'Authentication failed'"
- Confirm your password is correct (try logging into https://portal.office.com first)
- Ensure your MFA device is functioning (see MFA Setup article)
- Your account may be locked — check with the Help Desk

### "AnyConnect is blocking my home internet"
Full-tunnel mode routes all traffic through VPN. If approved by your manager, IT can configure split-tunnel access. Submit a ticket with your manager's approval.

### "I can't install AnyConnect — 'Installation failed'"
On Mac, go to System Settings → Privacy & Security and look for a blocked kernel extension from Cisco. Click "Allow" and retry the installation.

## VPN Not Required For
- Microsoft 365 (Outlook, Teams, SharePoint Online)
- Azure-hosted applications
- Company intranet sites published via Microsoft Entra App Proxy
