import requests

from lightning_custom import LndNode
from L402 import L402APIChain

from langchain.llms import OpenAI

API_DOCS = '''BASE URL: https://localhost:8081

API Documentation
The API endpoint /v1/models HTTP endpoint can be used to fetch the set of supported models. The response is text, the list of models separated by a comma

Request:
There are no query params for the API

Response:
A JSON object of the set of supported models, which looks similar to:
{
  "models": [
    {
      "id": "gpt9",
      "name": "GPT-9",
      "version": "1.0"
    },
    {
      "id": "gpt10",
      "name": "GPT-10",
      "version": "1.0"
    },
    {
      "id": "gptalphabeta",
      "name": "GPT-Alpha-Beta",
      "version": "1.0"
    }
  ]
}
'''

url = 'https://localhost:8081/v1'

lnd_node = LndNode(
    cert_path='.lnd/tls.cert',
    macaroon_path='.lnd/data/chain/bitcoin/simnet/admin.macaroon',
    # host='172.23.0.3',
    host='127.0.0.1',
    # port=8080,
    port=10009,
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
curl -k -v -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" https://localhost:8081/v1
"""
print("url:", url)
resp = requests.get(url)
print("Response:", resp)
print("Headers:", resp.headers)

output = chain_new.run('how many total models are supported?')
print(output)

output = chain_new.run('which models are supported?')
print(output)
