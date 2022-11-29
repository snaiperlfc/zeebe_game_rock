from pyzeebe import ZeebeClient, create_insecure_channel
import os

# Create a zeebe client
channel = create_insecure_channel(hostname=os.environ["ZEEBE_HOST"], port=26500)
zeebe_client = ZeebeClient(channel)
