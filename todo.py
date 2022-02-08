from flask import request
from flask_restx import Resource, Api, Namespace, fields

todos = {}
count = 1

Todo = Namespace(
    name='Todo',
    description='Todo 리스트를 만들기 위한 api'
)

todo_fields = Todo.model('Todo', {
    'data': fields.String(description='a Todo', required=True, example='what todo')
})

todo_fields_with_id = Todo.inherit('Todo With Id', todo_fields, {
    'todo_id' : fields.Integer(description='a Todo ID')
})

@Todo.route('')
class TodoPost(Resource):
    @Todo.expect(todo_fields)
    @Todo.response(201, 'Success', todo_fields_with_id)
    def post(self):
        """Todo 리스트에 할일을 추가"""
        global todos
        global count

        idx = count
        count += 1
        todos[idx] = request.json.get('data')

        return {
            'todo_id' : idx,
            'data' : todos[idx]
        },201

@Todo.route('/<int:todo_id>')
@Todo.doc(params={'todo_id': 'An ID'})
class TodoSimple(Resource):
    @Todo.response(200,'Success', todo_fields_with_id)
    @Todo.response(500, 'Failed')
    def get(self, todo_id):
        """id에 해당하는 할일 출력"""
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }
    
    @Todo.response(202, 'Success', todo_fields_with_id)
    @Todo.response(500, 'Failed')
    def put(self, todo_id):
        """id에 해당하는 할일 수정"""
        todos[todo_id] = request.json.get('data')
        return {
            'todo_id': todo_id,
            'data' : todos[todo_id]
        }, 202
    

    @Todo.doc(responses={202: 'Success'})
    @Todo.doc(responses={500: 'Failed'})
    def delete(self, todo_id):
        """id에 해당하는 할일 삭제"""
        del todos[todo_id]
        return {
            'delete' : 'success'
        }, 202