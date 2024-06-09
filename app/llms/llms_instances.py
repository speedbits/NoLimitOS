from langchain_openai import ChatOpenAI

llm_repo = {}
chatOpenAI_V35=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
llm_repo["chatOpenAI_V35"] = chatOpenAI_V35

def get_llm(llm_name):
    my_llm = None
    if (llm_name in llm_repo.keys()):
        my_llm = llm_repo[llm_name]
    return my_llm