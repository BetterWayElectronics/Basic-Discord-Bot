# Basic-Discord-Bot

**Description**  
A simple Discord bot that deletes messages in a specified category if they lack an attachment or a URL. Repeated violations result in a temporary "Timeout" role.

**Key Features**  
- Monitors a specified category for messages without attachments/URLs  
- Deletes offending messages  
- Sends warnings and temporarily applies a "Timeout" role after repeated violations  

**Setup**  
1. Install Python 3.8+ and `discord.py aiohttp`.  
2. Insert your Discord bot token in the script.  
3. Enable Message Content Intent in your bot settings.  
4. Run the script with `python your_bot_script.py`.

**License**  
MIT License
