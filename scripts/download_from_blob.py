from azure.storage.blob import BlobServiceClient
from pathlib import Path

# CONFIGURATION
account_name = "retailstorage12345"
account_key = "BS3/VXtkwIt5D5s9nETgwuHWcOGytXpT0kVwmTMDWv25tAuswNAazdXftVDAU+MjNrHnD6GQt21R+AStu9Ui9A=="
container_name = "staging"
blob_name = "sales_data_copy.csv"
local_file_path = f"{str(Path.home())}/retail_pipeline_project/clean_data/sales_data_clean.csv"

# CONNECT AND DOWNLOAD
blob_service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# Save file locally
with open(local_file_path, "wb") as f:
    f.write(blob_client.download_blob().readall())

print("✅ File downloaded to:", local_file_path)
