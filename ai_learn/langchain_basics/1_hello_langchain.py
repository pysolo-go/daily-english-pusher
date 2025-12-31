from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_utils import init_langchain_env

def main():
    # 1. Initialize Environment
    api_key, base_url = init_langchain_env()

    # 2. Initialize LLM (Chat Model)
    # LangChain allows easy swapping of models.
    llm = ChatOpenAI(
        model="Qwen/Qwen2.5-7B-Instruct", # Using the model from your previous context/env
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0.7
    )

    # 3. Define a Prompt Template
    # This is where LangChain shines: flexible prompt management.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
        ("user", "{text}")
    ])

    # 4. Define Output Parser
    # Converts the raw AI message to a string
    parser = StrOutputParser()

    # 5. Create a Chain using LCEL (LangChain Expression Language)
    # The pipe '|' operator connects components: Prompt -> LLM -> Parser
    chain = prompt | llm | parser

    # 6. Invoke the Chain
    input_text = "Hello, how are you today?"
    print(f"Input: {input_text}")
    
    response = chain.invoke({
        "input_language": "English",
        "output_language": "French",
        "text": input_text
    })

    print(f"Output: {response}")

if __name__ == "__main__":
    main()
