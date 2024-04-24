from django.contrib.auth.models import User
from .models import *

def is_listing_in_watchlist(user, listing_id):
    try:
        # Retrieve the user and listing objects based on their IDs
        
        listing = Listing.objects.get(pk=listing_id)
        
        # Check if there is a Watchlist entry for the user and listing
        watchlist_entry = Watchlist.objects.filter(user=user, listing=listing).exists()
        
        return watchlist_entry
    except (User.DoesNotExist, Listing.DoesNotExist):
        # Handle cases where user or listing does not exist
        return False
    
def generate_message(code, message_text):
    
    class Message:
        def __init__(self, bg_class, text):
            self.bg_class = bg_class
            self.text = text
    
    message_obj = Message(bg_class=code, text=message_text)
    
    return message_obj