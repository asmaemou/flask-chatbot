from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from llama_index.core import StorageContext, load_index_from_storage
import requests
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core import Prompt
import json
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.llms.replicate import Replicate
from llama_index.core import Settings
from llama_index.core.base.llms.types import ChatMessage,MessageRole


import os

os.environ["REPLICATE_API_TOKEN"] ="r8_bcABLvl5BKBeHKJVjL4lmEAblqbZuhx13mcZf"

Settings.embed_model= JinaEmbedding(
    api_key="jina_a706cf657cb44a228b0171965f49bf83PK6_1iMw-bARcrTjZdeWbmEejpq6",
    model="jina-embeddings-v2-base-en",
    embed_batch_size=16,
    )

Settings.llm = Replicate(
        model="mistralai/mistral-7b-instruct-v0.1:5fe0a3d7ac2852264a25279d1dfb798acbc4d49711d126646594e212cb821749",
        additional_kwargs={"top_p": 1, "max_new_tokens": 100},
    )



app = Flask(__name__)
CORS(app)


# Define the URLs of your website pages
# PAGE_URLS = {
#     'home': 'http://localhost:3000/',
#     'about': 'http://localhost:3000/about',
#     'service': 'http://localhost:3000/services',
#     'contact': 'http://localhost:3000/contact',
# }
def create_llama_index():
        
    index_dir = 'index'  # Specify the directory your index will be stored
    os.makedirs(index_dir, exist_ok=True)

    from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader
    embed_model = JinaEmbedding(
    api_key="jina_a706cf657cb44a228b0171965f49bf83PK6_1iMw-bARcrTjZdeWbmEejpq6",
    model="jina-embeddings-v2-base-en",
    embed_batch_size=16,
    )
    documents = SimpleDirectoryReader("raw_document").load_data()
    index = VectorStoreIndex.from_documents(
        documents=documents, embed_model=embed_model
    )
    index.storage_context.persist(persist_dir=index_dir)
    if not os.path.exists(index_dir) or not os.listdir(index_dir):
        print({'error':  "Error: in indexing document"})
    print({'result': 'File indexed successfully'})


def extract_page_content(url):
    # Function to extract relevant content from a webpage
    # You may need to customize this function based on your website's structure
    # Example: extract text from specific elements on the page
    # Here, I'm just returning the whole page content for simplicity
    response = requests.get(url)
    return response.text

def get_custom_prompt():
    # Function to create a custom prompt for querying the index
    try:
        return Prompt("""\
Rephrase the conversation and subsequent message into 
a self-contained question while including all relevant details. 
Conclude the question with: Only refer to this document.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
""")
    except Exception as e:
        return jsonify({'error':  f"An error occurred: {e}"})




def getChatHistory(history='[]'):

        history = json.loads(history)

        # initialize chart history
        custom_chat_history = []
        roles = {"left_bubble": "ASSISTANT", "right_bubble": "USER"}
        for chat in history:
            position = chat['position']
            role = MessageRole[roles[position]]
            content = chat['message']
            custom_chat_history.append(
                ChatMessage(
                    # can be USER or ASSISTANT
                    role=role,
                    content=content
                )
            )
        return custom_chat_history



def query_index(prompt, chat_history):
    # Function to query the llama index and generate a response

    storage_context = StorageContext.from_defaults(persist_dir="index")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    
    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        condense_question_prompt=get_custom_prompt(),
        chat_history=getChatHistory(chat_history),
        verbose=True,
        llm=Settings.llm,
    )

    response_node = chat_engine.chat(prompt)  # chat here
    return response_node.response
@app.route('/')
def hello_world():
    return jsonify({'result': "Hello world"})

@app.route('/ask_asmae', methods=['POST'])
def query_endpoint():

    data = request.get_json()
    prompt = data.get('prompt')
    chat_history = data.get('chatHistory', [])
    print( chat_history)
    print(data)
    response = query_index(prompt, chat_history)
    # print(response.get_json())
    print(jsonify({'result': response}))
    return jsonify({'result': response})

if __name__ == '__main__':
    # create_llama_index()
    app.run(debug=True,host="localhost",port=1234)


