# Discord Bots Collection

This repository contains several Discord bots with different functionalities:

- **Custom Embed Bot** — create custom embed messages.
- **Clear Bot** — clear messages in a channel.
- **Ticket Bot** — open and manage support tickets.
- **Verify Bot** — user verification with role assignment.

---

## 1. Custom Embed Bot

### Description
This bot allows users with specific roles to create rich embed messages using the `/customembed` command. It also provides a help command to explain how to use it.

### Commands
- `/helpembed`  
  Shows a guide on how to use the embed command.

- `/customembed <title> <description> <color> <image_url> <thumbnail_url> <footer_text> <field>`  
  Creates a custom embed message. Most parameters are optional except **title** and **description**.

### Roles Allowed to Use the Commands
- MOD  
- FLEXX DEVELOPER  
- OWNER  
- SUPPORT  
- DEV

### How to Run
1. Set your bot token in the `TOKEN` variable.  
2. Run the bot with Python 3.11+  
3. Use the commands in your Discord server.

---

## 2. Clear Bot

### Description
This bot clears messages from a channel. It supports clearing a specified number of messages or deleting and recreating the channel entirely.

### Commands
- `/clear <number|all>`  
  Clears messages or the entire channel.

### Permissions
- Requires **manage_messages** permission.  
- User must have one of these roles: MOD, FLEXX DEVELOPER, OWNER, SUPPORT, DEV.

### How to Run
1. Set your bot token in the `TOKEN` variable.  
2. Run the bot with Python 3.11+  
3. Use slash command `/clear` in your Discord server.

---

## 3. Ticket Bot

### Description
Users can open support tickets by reacting to a message. Tickets open in separate channels with appropriate permissions.

### Commands
- `/ticket <channel_id>`  
  Sends a message in a specified channel where users can react to open tickets.

### How it Works
- React with 🎟️ on the bot's message to open a ticket.  
- Ticket channels are created automatically with limited access.  
- React with ❌ inside your ticket to close it (only owner or mods can close).

### How to Run
1. Set your bot token in the `TOKEN` variable.  
2. Run the bot with Python 3.11+.

---

## 4. Verify Bot

### Description
This bot sends a verification message where users react to gain a role (default: MEMBER).

### Commands
- `/verify <channel_id>`  
  Sends the verification message.

### How it Works
- React with ✅ to get the MEMBER role.

### How to Run
1. Set your bot token in the `TOKEN` variable.  
2. Run the bot with Python 3.11+.

---

## Requirements
- Python 3.11 or higher  
- `discord.py` library installed (`pip install discord.py`)

---

Feel free to open issues or pull requests if you want to improve the bots or the documentation!
