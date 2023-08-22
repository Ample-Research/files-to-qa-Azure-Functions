import json

def build_ping_req():
    config_data = json.dumps({
            "user_id": "PING",
            "title": "Ping Request",
            "custom_prompt_q":"THIS IS JUST A TEST. PLEASE GENERATE 3 VERY SHORT QUESTIONS.",
            "custom_prompt_a":"THIS IS JUST A TEST. PLEASE GENERATE SHORT ANSWERS TO THE GIVEN QUESTIONS.",
            "model_name":"qa-gpt-35-4k-context",
            "start_sequence":"\n\n###\n\n",
            "stop_sequence":"###"
        })
    payload = {'data': config_data}

    file_id = "PING_FILE"
    file_data = """
ping is a computer network administration software utility used to test the reachability of a host on an Internet Protocol (IP) network. It is available for virtually all operating systems that have networking capability, including most embedded network administration software.
Ping measures the round-trip time for messages sent from the originating host to a destination computer that are echoed back to the source. The name comes from active sonar terminology that sends a pulse of sound and listens for the echo to detect objects under water.[1]
Ping operates by means of Internet Control Message Protocol (ICMP) packets. Pinging involves sending an ICMP echo request to the target host and waiting for an ICMP echo reply. The program reports errors, packet loss, and a statistical summary of the results, typically including the minimum, maximum, the mean round-trip times, and standard deviation of the mean.
"""
    files_payload = [
        ('file', (file_id + ".txt", file_data, 'application/octet-stream'))
    ]

    return payload, files_payload