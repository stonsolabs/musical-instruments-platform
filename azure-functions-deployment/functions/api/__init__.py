# Azure Functions API Module
# This module contains all the HTTP-triggered functions for the Musical Instruments Platform

import azure.functions as func
import logging
from . import products, search, compare, health, categories, brands

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main function to handle all routes
def main(req: func.HttpRequest) -> func.HttpResponse:
    """Main function that routes requests to appropriate handlers"""
    
    try:
        # Get the route from the URL
        route = req.route_params.get('route', '')
        
        # Route to appropriate function
        if route.startswith('products'):
            return products.main(req)
        elif route.startswith('search'):
            return search.main(req)
        elif route.startswith('compare'):
            return compare.main(req)
        elif route.startswith('categories'):
            return categories.main(req)
        elif route.startswith('brands'):
            return brands.main(req)
        elif route == 'health':
            return health.main(req)
        else:
            return func.HttpResponse(
                "Route not found",
                status_code=404
            )
            
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        return func.HttpResponse(
            f"Internal server error: {str(e)}",
            status_code=500
        )
