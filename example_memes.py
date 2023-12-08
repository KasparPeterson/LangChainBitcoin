import requests

from lightning_custom import LndNode
from L402 import L402APIChain

from langchain.llms import OpenAI

API_DOCS = '''BASE URL: https://memes.innovativecommercegroup.com/quote/1

API Documentation
The API endpoint /quote/1 can be used to get a quote

Request:
There are no query params for the API

Response:
Any
'''

url = 'https://memes.innovativecommercegroup.com/quote/1'

lnd_node = LndNode(
    cert_path='.lnd_testnet/tls.cert',
    macaroon_path='.lnd_testnet/admin.macaroon',
    # host='172.23.0.3',
    host='kaspartest.t.voltageapp.io',
    # port=8080,
    # port=443,
)

print("get_info:", lnd_node.get_info())
print("channel_balance:", lnd_node.channel_balance())
print("wallet_balance:", lnd_node.wallet_balance())

llm = OpenAI(temperature=0)

chain_new = L402APIChain.from_llm_and_api_docs(
    llm, API_DOCS, lightning_node=lnd_node, verbose=True,
)

print("\n\n==== Trying with simple requests ====")
"""
curl -v https://memes.innovativecommercegroup.com/quote/1
"""
print("url:", url)
resp = requests.get(url)
print("Response:", resp)
print("Headers:", resp.headers)

output = chain_new.run('how many total models are supported?')
print(output)

output = chain_new.run('which models are supported?')
print(output)

"""
curl --location \
  --request GET 'https://memes.innovativecommercegroup.com/meme/show/2' \
  --header 'Authorization: L402 AgEEbHNhdAJCAACVNTtHKQd4CrPqgmA5J3BeLoBbPe2wKr4M7P5KZT2gijaYUAcGMPHJ9SSEEAmbfuiEPJ5WeAvvaib3vZymaixJAAIRc2VydmljZXM9cXVvdGVzOjAAAiBxdW90ZXNfY2FwYWJpbGl0aWVzPWFkZCxzdWJ0cmFjdAACFnZhbGlkX3VudGlsPTIwMjUtMDEtMDEAAAYgGBdIKAPYfo6/xR2ii7/7wumG6eDJE/yBwQ6d2YH1vBE=:'
"""