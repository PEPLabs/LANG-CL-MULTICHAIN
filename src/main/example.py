from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.schema.runnable import RunnablePassthrough

model = AzureChatOpenAI(
    model_name="gpt-35-turbo"
)

# In this script, we will create a multi-chain using 2 chains:
# 1. A chain that prompts the LLM for an essay on a certain topic
# 2. A chain that extract the most difficult word from the essay

essay_prompt = """
    Generate an essay of 100 words on the following topic:
    {topic}
    The essay should contain vocabulary that a college student can understand.
"""

# In this first chain, we specify the prompt, the output parser, 
# and the output key. The output key is important because it allows the
# next part of the chain to access the output of this chain
chain1 = (
    ChatPromptTemplate.from_template(essay_prompt)
    | model
    | StrOutputParser()
    | {"essay": RunnablePassthrough()}
)

vocab_prompt = """
    What is the most difficult word in the following essay:
    {essay}
"""

# In this second chain, we use the .from_messages() method to emulate
# a conversation between a human and the LLM. The first message is the
# prompt, the second message is the output of the previous chain, and the
# third message is the question that the human asks the LLM
chain2 = (
    ChatPromptTemplate.from_messages(
        [
            ("human", "Generate an essay of 100 words on the following topic"),
            ("ai","{essay}"),
            ("system", vocab_prompt)
        ]
    )
    | model
    | StrOutputParser()
)

# Combining multiple chains is fairly straightforward:
final_chain = chain1 | chain2

# Can change this topic to see different results.
# Just don't change any of the other code or it might not 
# run properly:
topic = "The Water Cycle"

print(final_chain.invoke({"topic": topic}))