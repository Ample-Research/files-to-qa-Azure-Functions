import logging
import json
import azure.functions as func
from utils.timeit import timeit

@timeit
def create_error_msg(e, status_code=500, note = ""):
    logging.error(f"Error--{note}: {str(e)}")
  
    error_response = {
            "status": "error",
            "message": f"Failed to process the request. Error: {str(e)} -- Note:{note}"
        }
  
    return func.HttpResponse(json.dumps(error_response), status_code=status_code, mimetype="application/json")