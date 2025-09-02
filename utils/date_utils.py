"""
Date Utilities
Functions to convert posted dates from various job platforms
"""

from datetime import datetime, timedelta

def convert_posted_date_indeed(text):
    """Convert Indeed posted date format to YYYY-MM-DD"""
    now = datetime.now()
    text = text.lower()
    if "today" in text or "just posted" in text: 
        return now.strftime("%Y-%m-%d")
    if "day" in text: 
        return (now - timedelta(days=int(text.split()[0]))).strftime("%Y-%m-%d")
    if "week" in text: 
        return (now - timedelta(weeks=int(text.split()[0]))).strftime("%Y-%m-%d")
    if "month" in text: 
        return (now - timedelta(days=30 * int(text.split()[0]))).strftime("%Y-%m-%d")
    return now.strftime("%Y-%m-%d")

def convert_posted_date_jobstreet(text):
    """Convert JobStreet posted date format to YYYY-MM-DD"""
    now = datetime.now()
    if "day" in text or "d" in text:
        days = int(''.join(filter(str.isdigit, text)))
        return (now - timedelta(days=days)).strftime("%Y-%m-%d")
    return now.strftime("%Y-%m-%d")

def linkedin_format_posted_date(text):
    """Convert LinkedIn posted date format to YYYY-MM-DD"""
    now = datetime.now()
    if "today" in text or "just now" in text: 
        return now.strftime("%Y-%m-%d")
    if "yesterday" in text: 
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    if "day" in text: 
        return (now - timedelta(days=int(text.split()[0]))).strftime("%Y-%m-%d")
    if "week" in text: 
        return (now - timedelta(weeks=int(text.split()[0]))).strftime("%Y-%m-%d")
    if "month" in text: 
        return (now - timedelta(days=30 * int(text.split()[0]))).strftime("%Y-%m-%d")
    return now.strftime("%Y-%m-%d")

def convert_posted_date_kalibrr(text):
    """Convert Kalibrr posted date format to YYYY-MM-DD"""
    now = datetime.now()
    text = text.lower()
    
    if "today" in text or "just posted" in text:
        return now.strftime("%Y-%m-%d")
    elif "yesterday" in text:
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    elif "day" in text:
        days = int(''.join(filter(str.isdigit, text)))
        return (now - timedelta(days=days)).strftime("%Y-%m-%d")
    elif "week" in text:
        weeks = int(''.join(filter(str.isdigit, text)))
        return (now - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
    elif "month" in text:
        months = int(''.join(filter(str.isdigit, text)))
        return (now - timedelta(days=30 * months)).strftime("%Y-%m-%d")
    
    return now.strftime("%Y-%m-%d")

def convert_posted_date_foundit(text):
    """Convert Foundit posted date format to YYYY-MM-DD"""
    from datetime import datetime, timedelta
    import re
    
    now = datetime.now()
    text_lower = text.lower().strip()
    
    # Handle "today"
    if "today" in text_lower:
        return now.strftime("%Y-%m-%d")
    
    # Handle "yesterday"
    if "yesterday" in text_lower:
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Handle "X days ago"
    days_match = re.search(r'(\d+)\s+days?\s+ago', text_lower)
    if days_match:
        days_ago = int(days_match.group(1))
        return (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    
    # Handle "X hours ago"
    hours_match = re.search(r'(\d+)\s+hours?\s+ago', text_lower)
    if hours_match:
        hours_ago = int(hours_match.group(1))
        return (now - timedelta(hours=hours_ago)).strftime("%Y-%m-%d")
    
    # Handle "X weeks ago"
    weeks_match = re.search(r'(\d+)\s+weeks?\s+ago', text_lower)
    if weeks_match:
        weeks_ago = int(weeks_match.group(1))
        return (now - timedelta(weeks=weeks_ago)).strftime("%Y-%m-%d")
    
    # Handle "X months ago"
    months_match = re.search(r'(\d+)\s+months?\s+ago', text_lower)
    if months_match:
        months_ago = int(months_match.group(1))
        return (now - timedelta(days=30 * months_ago)).strftime("%Y-%m-%d")
    
    # Fallback to today if no pattern matches
    return now.strftime("%Y-%m-%d")