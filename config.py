from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

KEYVAULT_NAME = "pockeyvaultkittu01"

KV_URI = f"https://{KEYVAULT_NAME}.vault.azure.net"

credential = DefaultAzureCredential()

client = SecretClient(
    vault_url=KV_URI,
    credential=credential
)

def get_secret(secret_name):
    return client.get_secret(secret_name).value