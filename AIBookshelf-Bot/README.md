# AI-Bookshelf
Put your books here and chat with AI about it


## Project structure

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

