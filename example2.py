from bitcoin_tools import LndTools
from lightning_custom import LndNode
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

lnd_node = LndNode(
    cert_path='.lnd/tls.cert',
    macaroon_path='.lnd/data/chain/bitcoin/simnet/admin.macaroon',
    # host='172.23.0.3',
    host='127.0.0.1',
    # port=8080,
    port=8081,
)

lnd_tools = LndTools.from_lnd_node(lnd_node=lnd_node)

llm_model = ChatOpenAI(model="gpt-3.5-turbo-0613")

bitcoin_agent = initialize_agent(
    lnd_tools.get_tools(),
    llm_model,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

print("\n\n==== Current Balance ====")
print(bitcoin_agent.run('What is my current channel balance in satoshis?'))

print("\n\n==== Invoice ====")
invoice = "lnsb100u1pjfz83lpp55h08akqscecxejh5jfecdx7hxf693tsv7c3lyp207fjqwmx9a8fsdqqcqzzsxqyz5vqsp5xhdak7n7h2dtl0gky9xzffnwel67h94jawkn0skpkj4xmcvtyphq9qyyssqrk86elwl2wctg6pw4uxjh4a3swrpljfvefy3xcxxk90tu484wxrpyu5pcwdfk65yjgw4fash3dsyuyxdyalengm4pwwj8t083cgqyhcphvaj27"
prompt = "How many satoshis is this invoice requesting: {invoice}".format(invoice=invoice)
print(bitcoin_agent.run(prompt))