import logging
import json
import azure.functions as func

def create_error_msg(e, status_code=500, note = ""):
    logging.error(f"Error--{note}: {str(e)}")
  
    error_response = {
            "status": "error",
            "message": f"Failed to process the request. Error: {str(e)}\n\n\nNote:{note}"
        }
  
    return func.HttpResponse(json.dumps(error_response), status_code, mimetype="application/json")