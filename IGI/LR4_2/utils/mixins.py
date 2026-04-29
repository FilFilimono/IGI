"""
Purpose: Mixin classes for logging and identification
Lab: #X (General Utils)
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

class InfoMixin:
    """
    A mixin to provide common information about objects.
    """
    def get_class_info(self):
        """Returns the name of the class."""
        return f"Object of type: {self.__class__.__name__}"

    def log_action(self, action):
        """Simple action logger."""
        print(f"[LOG]: {self.__class__.__name__} performed '{action}'")
    
# Для соблюдения требования №4 (примеси).