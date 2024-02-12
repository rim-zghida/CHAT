from flask import Flask ,request ,jsonify
from flask_cors import CORS
import os 
from datetime import datetime
import json
app= Flask(__name__)
CORS(app)
app.debug=True
os.environ["OPENAI_API_KEY"]="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"





# @app.route('/ask_ai', methods=['POST'])
# def query_endpoint():
#     response = query_index()
#     return response


def create_llama_index():
    try:
        print("debut llama")
        index_dir = 'index'  # Specify the directory your index will be stored
        os.makedirs(index_dir, exist_ok=True)

        from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
        documents = SimpleDirectoryReader("uploads").load_data()
        index = GPTVectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=index_dir)
        if not os.path.exists(index_dir) or not os.listdir(index_dir):
            return "Error: in indexing document",400
        return jsonify({'result': 'File indexed successfully'})
    except Exception as e:
        return f"An error occurred:{e}",400
# this creates a custom prompt to be used in quering the index



@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        upload_dir = 'uploads'  # Specify the directory where you want to save uploaded files
        os.makedirs(upload_dir, exist_ok=True)

        file.save(os.path.join(upload_dir, "data.txt"))
        create_llama_index()
        
        return jsonify({'msg':'true'})
      


# @app.route('/')
# def hello_world():
#     return jsonify({'r':'home page hiya ili yhezni lina default route il houwa /'})
  
  
  
# @app.route('/<int:yearOfBirth>') 
# def age(yearOfBirth):
#     print (datetime.now().year)
#     age=datetime.now().year-yearOfBirth
#     return jsonify({'resultat': age})



 
# @app.route('/<prenom>')
# def bonjour(prenom):
#     return jsonify({'message':f'bonjour {prenom}'})


 

if __name__ == '__main__':
    app.run()