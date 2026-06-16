# macOS Device Enrollment — Intune & Jamf Pro

## Overview
Mac devices are managed through Jamf Pro and optionally co-managed with Microsoft Intune. Enrollment is required before you can access corporate Wi-Fi, email, or VPN.

## Automated Device Enrollment (ADE) — IT-Provisioned Macs
Company-purchased Macs are enrolled automatically via Apple Business Manager. When you power on a new Mac and sign in with your corporate Apple ID, Jamf enrollment begins automatically. Follow the on-screen prompts — no manual steps required.

## Manual Enrollment (Personal Mac or Reassigned Device)

### Step 1 – Download the enrollment profile
Go to your company's Jamf Self Service URL (provided by IT) or download the MDM profile from the IT portal.

### Step 2 – Install the profile
Open System Settings → Privacy & Security → Profiles → Install the downloaded profile. Enter your Mac password when prompted.

### Step 3 – Install Company Portal (for Intune compliance)
Download Microsoft Intune Company Portal from the Mac App Store. Sign in with your corporate Microsoft account and register your device.

### Step 4 – Verify compliance
Open Company Portal → Devices. Your Mac should show as "Compliant" within 15–30 minutes.

## Key Software Deployed via Jamf

| Software | Purpose |
|---|---|
| Cisco AnyConnect | Corporate VPN |
| Microsoft 365 (Office) | Productivity suite |
| CrowdStrike Falcon | Endpoint protection |
| Slack | Team communication |
| FileVault (policy) | Full-disk encryption |
| Kerberos SSO Extension | Single sign-on for internal apps |

## FileVault Encryption
All Macs must have FileVault enabled. Jamf pushes this policy automatically. If prompted, enable FileVault and your recovery key will be escrowed to Jamf — you never need to manage it manually.

## Troubleshooting

### "Jamf Self Service is empty / shows no apps"
Ensure your device successfully enrolled and appears in Jamf. Open Terminal and run: `sudo profiles show -type enrollment`. If no MDM profile appears, re-install the enrollment profile and reboot.

### "My Mac keeps prompting for Kerberos credentials"
Open the Kerberos SSO Extension (found in System Settings → Users & Groups → Network Account Server or via the menu bar). Sign in with your corporate credentials to refresh your Kerberos ticket.
