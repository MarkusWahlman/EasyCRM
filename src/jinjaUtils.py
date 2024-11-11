"""
Jinja utility processor for adding utility functions to Flask templates.
"""

from flask import request, url_for

def utilityProcessor():
    """
    Utility functions for the Jinja context.
    """

    def isActive(endpoint):
        return 'active' if request.path == url_for(endpoint) else ''
    return {"isActive": isActive}
