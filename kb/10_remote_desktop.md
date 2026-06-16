# Remote Desktop & Remote Access Setup

## Overview
There are two ways to access your work computer or corporate resources remotely:
1. **VPN** — connects your device to the corporate network (required for on-premises resources)
2. **Windows Remote Desktop (RDP)** — connects to your physical work PC from home

## Option 1 — VPN Access (Most Common)
For most remote work (email, Teams, SharePoint, cloud apps), VPN alone is sufficient. See the Cisco AnyConnect VPN article for setup instructions.

## Option 2 — Remote Desktop (RDP) to Your Work PC

### Prerequisites
- Your work PC must be powered on and not sleeping
- Your work PC must be enrolled in Intune and compliant
- You must be connected to VPN first
- Remote Desktop must be enabled on your work PC (IT can enable this remotely via Intune)

### Enabling Remote Desktop (Request)
Submit a ServiceNow request for "Remote Desktop Access Enablement." IT will configure your work PC via Intune policy within one business day.

### Connecting via Remote Desktop on Windows
1. Connect to VPN (Cisco AnyConnect)
2. Press Win+R → type `mstsc` → Enter
3. In the "Computer" field, enter your work PC's hostname (e.g., `WZOLL-JF01`) — find this in: Settings → System → About → Device name
4. Click **Connect** and sign in with your corporate credentials
5. Approve the MFA prompt if prompted

### Connecting via Remote Desktop on Mac
1. Install **Microsoft Remote Desktop** from the Mac App Store (free)
2. Connect to VPN first
3. Open Microsoft Remote Desktop → Add PC → enter your work PC hostname
4. Double-click the PC to connect and sign in with your corporate credentials

## Option 3 — Microsoft Entra App Proxy (Browser-Based Internal Apps)
Some internal web applications are published via Entra App Proxy and accessible without VPN at: https://myapps.microsoft.com. Sign in with your corporate account to see available apps.

## Troubleshooting Remote Desktop

### "Remote Desktop can't connect to the remote computer"
1. Confirm VPN is connected and showing a lock icon
2. Verify your work PC is powered on (ask a colleague to check, or check the Intune device status in Company Portal)
3. Confirm the hostname is correct — try the device's IP address instead
4. Ensure Remote Desktop is enabled on the target machine (submit a ticket if unsure)

### "Your credentials did not work"
Use your full corporate email (user@company.com) not just your username. For domain login, try: COMPANY\yourusername

### "The remote session was disconnected because there are no Remote Desktop License Servers"
Contact IT — this is a server-side licensing issue that requires admin intervention.

## Best Practices
- Always disconnect properly (Start → Power icon → Disconnect) rather than just closing the window
- Lock your home PC when done to prevent unauthorized access to the RDP session
- Do not leave sensitive files on your home desktop while RDP is active
