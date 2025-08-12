# Discord Bots Collection

This repository contains several Discord bots with different functionalities:

- **Custom Embed Bot** — create custom embed messages.  
- **Clear Bot** — clear messages in a channel.  
- **Ticket Bot** — open and manage support tickets.  
- **Verify Bot** — user verification with role assignment.  
- **Command List Bot** — display or set a global channel for command info.

---

## 1. Custom Embed Bot

### Description  
This bot allows users with specific roles to create rich embed messages using the `/customembed` command. It also provides a help command to explain how to use it.

### Commands  
- `/helpembed` — shows a guide on how to use the embed command.  
- `/customembed <title> <description> <color> <image_url> <thumbnail_url> <footer_text> <field>` — creates a custom embed message. Most parameters are optional except title and description.

### Roles allowed to use the commands  
MOD, FLEXX DEVELOPER, OWNER, SUPPORT, DEV

### How to run  
- Set your bot token in the TOKEN variable.  
- Run the bot with Python 3.11+.  
- Use the commands in your Discord server.

---

## 2. Clear Bot

### Description  
This bot clears messages from a channel. It supports clearing a specified number of messages or deleting and recreating the channel entirely.

### Commands  
- `/clear <number|all>` — clears messages or the entire channel.

### Permissions  
Requires `manage_messages` permission and one of the roles: MOD, FLEXX DEVELOPER, OWNER, SUPPORT, DEV.

### How to run  
- Set your bot token in the TOKEN variable.  
- Run the bot with Python 3.11+.  
- Use the slash command `/clear` in your Discord server.

---

## 3. Ticket Bot

### Description  
Users can open support tickets by reacting to a message. Tickets open in separate channels with appropriate permissions.

### Commands  
- `/ticket <channel_id>` — sends a message in a specified channel where users can react to open tickets.

### How it works  
- React with 🎟️ on the bot's message to open a ticket.  
- Ticket channels are created automatically with limited access.  
- React with ❌ inside your ticket to close it (only owner or mods).

### How to run  
- Set your bot token in the TOKEN variable.  
- Run the bot with Python 3.11+.

---

## 4. Verify Bot

### Description  
This bot sends a verification message where users react to gain a role (default: MEMBER).

### Commands  
- `/verify <channel_id>` — sends the verification message.

### How it works  
- React with ✅ to get the MEMBER role.

### How to run  
- Set your bot token in the TOKEN variable.  
- Run the bot with Python 3.11+.

---

## 5. Command List Bot

### Description  
This bot provides a `/commandlist` slash command that either displays a list of all available commands or sets a global channel where the bot sends messages.

### Commands  
- `/commandlist` — shows an embed with all available bot commands and descriptions.  
- `/commandlist <channel_id>` — sets the specified channel as a global channel for bot messages.

### How it works  
- Running `/commandlist` without arguments sends an embed listing key commands.  
- Running `/commandlist <channel_id>` sets that channel for bot notifications. If the channel ID is invalid, the bot notifies you.

### How to run  
- Set your bot token in the TOKEN variable.  
- Run the bot with Python 3.11+.

---

## Requirements

- Python 3.11 or higher  
- `discord.py` library (`pip install discord.py`)

---
