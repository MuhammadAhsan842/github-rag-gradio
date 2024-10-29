# from flask import Flask, jsonify, request
# from llama_index.readers.github import GithubRepositoryReader, GithubClient
# from llama_index.core import VectorStoreIndex
# import os


# app = Flask(__name__)


# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# if not OPENAI_API_KEY or not GITHUB_TOKEN:
#     raise ValueError("Please set the OPENAI_API_KEY and GITHUB_TOKEN as environment variables.")


# github_client = GithubClient(github_token=GITHUB_TOKEN, verbose=True)


# @app.route('/query', methods=['POST'])
# def query_repository():
    
#     data = request.get_json()
#     prompt = data.get('prompt')
#     owner=data.get('owner')
#     repo=data.get('repo')
#     branch=data.get('branch')
#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400
#     if not owner:
#         return jsonify({"error": "Prompt is required"}), 400
#     if not repo:
#         return jsonify({"error": "Prompt is required"}), 400
#     if not branch:
#         return jsonify({"error": "Prompt is required"}), 400
    
#     github_client = GithubClient(github_token=GITHUB_TOKEN, verbose=True)

#     loader = GithubRepositoryReader(github_client=github_client, owner=owner, repo=repo, verbose=True)
    
#     documents = loader.load_data(branch=branch)
    
#     index = VectorStoreIndex.from_documents(documents)
#     query_engine = index.as_query_engine()


#     response = query_engine.query(prompt)


#     return jsonify({"response": str(response),"owner": str(owner),"repo": str(repo),"branch": str(branch)})


# if __name__ == '__main__':
#     app.run(debug=True)


import os
import gradio as gr
import os
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.core import VectorStoreIndex
from llama_index.readers.github import GithubRepositoryReader, GithubClient



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


github_token = os.environ.get("GITHUB_TOKEN")
github_client = GithubClient(github_token=github_token, verbose=True)

def query_github_repo(owner, repo, branch, prompt):

    loader = GithubRepositoryReader(github_client=github_client, owner=owner, repo=repo, verbose=True)


    documents = loader.load_data(branch=branch)


    index = VectorStoreIndex.from_documents(documents)


    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)

    return f"**Query Result:**\n\n{response}"


interface = gr.Interface(
    fn=query_github_repo,
    inputs=[
        gr.Textbox(label="Repository Owner", placeholder="e.g., colinhacks"),
        gr.Textbox(label="Repository Name", placeholder="e.g., zod"),
        gr.Textbox(label="Branch", placeholder="e.g., main"),
        gr.Textbox(label="Prompt", placeholder="e.g., please give me the code of release.yml")
    ],
    outputs=gr.Markdown(label="Response"),
    title="GitHub Repository Query",
    description="Input the GitHub repository details and a prompt to query specific information,(Please wait for 20 to 30 secs (after pressing submit) \n while answer is being processed and outputed)."
)


interface.launch()
