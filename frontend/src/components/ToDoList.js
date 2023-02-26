import React from 'react'
import {Button} from "react-bootstrap";
import {Link} from "react-router-dom";

const ToDoItem = ({todo, deleteTodo}) => {
    return (
        <tr>
            <td>
                {todo.name}
            </td>
            <td>
                {todo.text}
            </td>
            <td>
                {todo.updateAt}
            </td>
            <td>
                {todo.isActive ?
                    <Button className='btn-success' onClick={() => deleteTodo(todo.id)} type='button'
                            onMouseOver={(event) => event.target.textContent = 'Close'}
                            onMouseOut={(event) => event.target.textContent = 'Active'}>Active</Button> :
                    <p style={{color: "red"}}>Closed</p>}
            </td>
        </tr>
    )
}


const ToDosList = ({todos, deleteTodo}) => {
    return (
        <div>
            <div>
                <Button>
                    <Link className="text-white" to='create/'>Create new todos</Link>
                </Button>
            </div>
            <div className="table-responsive">
                <table className="table table-striped table-sm">
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Text</th>
                        <th>Last update</th>
                        <th>Status</th>
                    </tr>
                    </thead>
                    <tbody>
                    {todos?.map((todo) => <ToDoItem key={todo.url} todo={todo}
                                                    deleteTodo={deleteTodo}/>)}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default ToDosList