from azure.durable_functions import DurableOrchestrationClient

def fire_orchestrator(starter, function_name, data):
    client = DurableOrchestrationClient(starter)
    instance_id = client.start_new(function_name, None, data)
    return instance_id