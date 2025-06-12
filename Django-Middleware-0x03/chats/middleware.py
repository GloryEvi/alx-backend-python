import logging
import os
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseForbidden

# Configure logger for request logging
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Create file handler for logging to requests.log
log_file = os.path.join(settings.BASE_DIR, 'requests.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger if not already added
if not logger.handlers:
    logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file,
    including the timestamp, user, and request path.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Process the request and log the information.
        
        Args:
            request: The HTTP request object
            
        Returns:
            The response from the next middleware/view
        """
        # Get user information
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        
        # Log the request information in the specified format
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Continue processing the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours.
    Access is only allowed between 6PM and 9PM.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Check the current server time and deny access if outside allowed hours.
        
        Args:
            request: The HTTP request object
            
        Returns:
            403 Forbidden response if outside allowed hours, otherwise normal response
        """
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour
        
        # Check if current time is outside allowed hours (6PM to 9PM = 18 to 21)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to the messaging app is restricted. Please try again between 6PM and 9PM.")
        
        # Continue processing the request if within allowed hours
        response = self.get_response(request)
        
        return response