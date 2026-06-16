# Microsoft Outlook Troubleshooting

## Overview
This article covers the most common Outlook issues and how to resolve them without contacting IT. Try these steps in order before submitting a ticket.

## Email Not Loading / Outlook Stuck on "Loading"

### Step 1 – Force quit and restart
Close Outlook completely (right-click the taskbar icon → Close window, then check Task Manager for any remaining Outlook.exe processes). Reopen Outlook.

### Step 2 – Check for "Offline" mode
Look at the bottom status bar in Outlook. If it says "Working Offline," go to the **Send/Receive** tab → click **Work Offline** to toggle it off. This is the most common cause of email not loading.

### Step 3 – Check your internet connection
If you are working remotely, ensure you have internet access. Some internal features require VPN — however, Microsoft 365 email does not require VPN.

### Step 4 – Clear the Outlook cache
Close Outlook → navigate to `%localappdata%\Microsoft\Outlook\` → move (do not delete) the .ost file to your Desktop as a backup → reopen Outlook. Outlook will rebuild the cache (30–60 minutes for large mailboxes).

## Outlook Calendar Not Syncing

1. Close and reopen Outlook
2. Go to File → Account Settings → Account Settings → select your account → Repair
3. Wait for the repair to complete and restart Outlook
4. If calendar entries are still missing, check if you are looking at the correct calendar (some users have multiple Exchange calendars)

## "Cannot Connect to Server" Error

1. Verify your internet is working (open a browser and load a website)
2. Confirm your password has not expired — try signing in to https://outlook.office.com
3. If the web version works but the desktop app does not, try removing and re-adding your account: File → Account Settings → Remove your account → Add Account again

## Outlook Running Slowly or Freezing

1. Reduce the local email cache: File → Account Settings → select account → Change → drag the "Mail to keep offline" slider to 3 months
2. Disable add-ins that are slowing startup: File → Options → Add-ins → Manage COM Add-ins → Go → uncheck non-essential add-ins
3. Run Outlook in Safe Mode to test: press Win+R → type `outlook.exe /safe` → OK

## I Accidentally Deleted an Email

Deleted items are kept for 30 days. Check the **Deleted Items** folder. If not there, look in the **Recoverable Items** folder: Folder tab → Recover Deleted Items. IT admins can also perform litigation hold recoveries for compliance purposes — submit a ticket if needed.

## When to Submit a Ticket
Submit a ServiceNow ticket if:
- You cannot access Outlook after trying all steps above
- You received a security warning or phishing email with suspicious attachments you may have opened
- You need an email recovered older than 30 days
