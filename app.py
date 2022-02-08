from flask import Flask
from flask_restx import Api, Resource
from todo import Todo
from auth import Auth

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title='Simple Api Server',
    description='연습용 Api 서버',
    terms_url='/',
    contact='kimsh4265@korea.ac.kr',
    license='KSH'
)

# api.add_namespace(Todo, '/todos')     #todo 기능
api.add_namespace(Auth, '/auth')        #login 기능




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)