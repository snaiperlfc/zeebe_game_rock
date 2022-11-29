from pyzeebe import ZeebeClient, create_insecure_channel

# Create a zeebe client
channel = create_insecure_channel(hostname="localhost", port=26500)
zeebe_client = ZeebeClient(channel)
