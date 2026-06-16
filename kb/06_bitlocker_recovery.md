# BitLocker Recovery Key Retrieval

## Overview
BitLocker encrypts your Windows device's hard drive. If Windows prompts for a 48-digit recovery key (usually after a hardware change, BIOS update, or multiple failed login attempts), you can retrieve it yourself from Microsoft Entra ID — no IT call required in most cases.

## Retrieving Your Recovery Key (Self-Service)

### Method 1 – Via Microsoft Account Portal (Recommended)
1. On any device (phone, another computer), go to: https://account.microsoft.com/devices/recoverykey
2. Sign in with your **corporate** Microsoft account (not personal)
3. Find your device by name or serial number
4. Copy the 48-digit recovery key
5. Enter it on the BitLocker prompt screen — use the on-screen keyboard if possible

### Method 2 – Via Entra ID Portal (For IT Admins)
IT admins can retrieve keys at: https://entra.microsoft.com → Devices → All Devices → [Device Name] → Recovery Keys

## Entering the Recovery Key
At the BitLocker recovery screen:
1. Press **Esc** if the screen only shows a PIN field — this reveals the recovery key option
2. Select "Enter recovery key"
3. Type the 48-digit key exactly as shown (hyphens are optional)
4. Press **Enter** — Windows will boot normally

## After Recovery
Once logged in, BitLocker will automatically re-seal to your current system state. No further action is needed. If BitLocker continues to prompt on every boot, submit a ticket — a hardware component may have changed and needs to be cleared in TPM.

## Recovery Key Not Found
If no key appears in the portal:
- The device may have been enrolled before Entra ID key backup was configured
- Contact the IT Help Desk — we may have the key in Jamf (Mac) or a legacy backup system

## Preventing Future Lockouts
Do not update BIOS or change hardware (RAM, SSD) without notifying IT, as these changes can trigger BitLocker. If you plan hardware upgrades, IT can temporarily suspend BitLocker first.
