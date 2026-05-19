"""
Purpose: Custom exception classes for specific error handling
Lab: General Utils
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

class MathDomainError(Exception):
    
    def __init__(self, message="Mathematical domain error occurred."):
        self.message = message
        super().__init__(self.message)


class InvalidDimensionError(Exception):
    
    def __init__(self, message="Invalid dimensions provided."):
        self.message = message
        super().__init__(self.message)
        

