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
    # 10009 is LND node for Aperture
    # 10010 is LND node for client
    port=10010,
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
invoice = "lnsb100n1pjhru52pp5pfrzzgwmt7mj4kq37utugcacryj2elulupkddry8yefgkyxny88sdq8f3f5z4qcqzzsxqyz5vqsp5ek3l8p88duqcqpdx0m6w2mlpsfkg7au87hcde245esuc6zs0vm9q9qyyssqg22mp266jnwz8jhc04kfmc7rmhsd6admhsqdrpua0tj9s4vm0ng85lpj9kx8vp7xj77n2tp6w2jzch5r9q8wp39qfuws6h2mvqdt4vqprx4hnn"
prompt = "How many satoshis is this invoice requesting: {invoice}".format(invoice=invoice)
print(bitcoin_agent.run(prompt))