from azure.storage.blob import BlobServiceClient
import os

# Your connection string from Azure portal
connection_string = "DefaultEndpointsProtocol=https;AccountName=retailstorage12345;AccountKey=BS3/VXtkwIt5D5s9nETgwuHWcOGytXpT0kVwmTMDWv25tAuswNAazdXftVDAU+MjNrHnD6GQt21R+AStu9Ui9A==;EndpointSuffix=core.windows.net"

# Blob container name
container_name = "raw"

# Local file path
local_file_path = os.path.join(os.path.expanduser("~"), "retail_pipeline_project", "raw_data", "sales_data.csv")

# Blob name in Azure (filename in container)
blob_name = "sales_data.csv"

def upload_file_to_blob():
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {blob_name} to container {container_name}")

if __name__ == "__main__":
    upload_file_to_blob()
