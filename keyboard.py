from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def lang_kb(langs, page=0):
    kb = []
    
    items_per_page = 6
    start = page * items_per_page
    end = start + items_per_page
    current_langs = langs[start:end]
    
    row1 = []
    row2 = []
    
    for i, (name, code) in enumerate(current_langs):
        if i < 3:
            row1.append(InlineKeyboardButton(text=name, callback_data=f"lang_{code}"))
        else:
            row2.append(InlineKeyboardButton(text=name, callback_data=f"lang_{code}"))
    
    if row1:
        kb.append(row1)
    if row2:
        kb.append(row2)
    
    nav_buttons = []
    
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page-1}"))
    
    total_pages = (len(langs) + items_per_page - 1) // items_per_page
    if total_pages > 1:
        nav_buttons.append(InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="page_info"))
    
    if end < len(langs):
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page+1}"))
    
    if nav_buttons:
        kb.append(nav_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=kb)