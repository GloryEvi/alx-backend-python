import logging
import os
from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from collections import defaultdict

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


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of chat messages a user can send 
    within a certain time window, based on their IP address.
    Allows 5 messages per minute per IP address.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response
        # Dictionary to store IP addresses and their request timestamps
        self.ip_requests = defaultdict(list)
        # Rate limit settings
        self.max_requests = 5  # Maximum requests per time window
        self.time_window = 60  # Time window in seconds (1 minute)
    
    def __call__(self, request):
        """
        Count the number of POST requests (messages) from each IP address
        and implement rate limiting.
        
        Args:
            request: The HTTP request object
            
        Returns:
            429 Too Many Requests if limit exceeded, otherwise normal response
        """
        # Only apply rate limiting to POST requests (messages)
        if request.method == 'POST':
            # Get client IP address
            ip_address = self.get_client_ip(request)
            current_time = datetime.now()
            
            # Clean old requests outside the time window
            self.cleanup_old_requests(ip_address, current_time)
            
            # Check if IP has exceeded the rate limit
            if len(self.ip_requests[ip_address]) >= self.max_requests:
                response = HttpResponse(
                    f"Rate limit exceeded. You can only send {self.max_requests} messages per minute. Please try again later.",
                    status=429
                )
                return response
            
            # Add current request timestamp
            self.ip_requests[ip_address].append(current_time)
        
        # Continue processing the request
        response = self.get_response(request)
        
        return response
    
    def get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        
        Args:
            request: The HTTP request object
            
        Returns:
            str: Client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def cleanup_old_requests(self, ip_address, current_time):
        """
        Remove requests that are outside the time window.
        
        Args:
            ip_address: The IP address to clean up
            current_time: Current datetime
        """
        cutoff_time = current_time - timedelta(seconds=self.time_window)
        self.ip_requests[ip_address] = [
            timestamp for timestamp in self.ip_requests[ip_address]
            if timestamp > cutoff_time
        ]


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
        if current_hour < 3 or current_hour >= 6:
            return HttpResponseForbidden("Access to the messaging app is restricted. Please try again between 6PM and 9PM.")
        
        # Continue processing the request if within allowed hours
        response = self.get_response(request)
        
        return response