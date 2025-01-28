
<img src="https://github.com/user-attachments/assets/cc657c7a-5513-4cbe-b032-5d1e80dc6e41" width="400">


# AI-Bookshelf
Put your books here and chat with AI about it

# Main goal
While we don't usaly have a privelege of having a free time to read to the book we want I came up with this simple solution.
Just put your books on AI Bookshelf and ask all the questions about them! 
It will help you save a lot of time and give all the answers. 

# How to use?
Simple: 
1) Go to @ai_bookshelf_bot in Telegram and hit /start
2) Send all the books you need answers from in PDF
3) Start chatting with /chat (Dev in progress... You can help too!)
<img width="1424" alt="Screenshot 2025-01-28 at 13 44 21" src="https://github.com/user-attachments/assets/71908eca-97cb-40a1-aab6-2200c6a1064a" />



# Technologies 
* Python for Telegram bot & communication with my local AI server
* GPT4All to run AI models on my local server
* MySQL for database
* RTX3060 12GB overclocked to run AI models on
* Reasoner and Llama AI models using books in PDF


# Project structure
                  ai_bookshelf/
                  ├── config/
                  │   └── config.py         # Database and bot configuration
                  ├── models/
                  │   ├── __init__.py
                  │   ├── user.py          # User model
                  │   ├── book.py          # Book model
                  │   └── category.py      # Category model
                  ├── handlers/
                  │   ├── __init__.py
                  │   ├── start.py         # Start command handler
                  │   ├── book.py          # Book-related commands
                  │   └── category.py      # Category-related commands
                  ├── utils/
                  │   ├── __init__.py
                  │   └── db.py           # Database connection utilities
                  ├── requirements.txt
                  └── main.py             # Main bot file

