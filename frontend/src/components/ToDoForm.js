import React from 'react';
import {Button} from "react-bootstrap";


class TodoForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            text: '',
            isActive: 1,
            userId: props.users[0]?.id,
            projectId: props.projects[0]?.id

        }
    }

    handlerOnChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
    }


    handlerOnSubmit(event) {
        console.log(this.state)
        this.props.createTodo(this.state.name, this.state.text, this.state.isActive, this.state.userId, this.state.projectId);
        event.preventDefault();
    }

    render() {
        return (
            <div className='d-flex justify-content-center'>
                <form onSubmit={(event) => this.handlerOnSubmit(event)}>
                    <div className='form-group'>
                        <label htmlFor="name">Name:</label>
                        <input type="text" className='form-control' name='name' value={this.state.name}
                               onChange={(event) => this.handlerOnChange(event)}/>
                    </div>
                    <div className='form-group'>
                        <label htmlFor="text">Text:</label>
                        <textarea className='form-control' name='text' value={this.state.text}
                                  onChange={(event) => this.handlerOnChange(event)}/>
                    </div>
                    <div className='form-group'>
                        <label htmlFor="userId">User:</label>
                        <select name="userId" className="form-control"
                                onChange={(event) => this.handlerOnChange(event)}> {this.props.users.map((user) =>
                            <option key={user.uid} value={user.url}>{user.username}</option>)}
                        </select>
                        <label htmlFor="projectId">Project:</label>
                        <select name="projectId" className="form-control"
                                onChange={(event) => this.handlerOnChange(event)}> {this.props.projects.map((project) =>
                            <option key={project.id} value={project.url}>{project.name}</option>)}
                        </select>
                    </div>
                    <Button type="submit" className='btn btn-primary'>Create</Button>
                </form>
            </div>
        );
    }
}

export default TodoForm;