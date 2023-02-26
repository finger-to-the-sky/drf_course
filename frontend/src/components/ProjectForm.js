import React from 'react';
import {Button} from "react-bootstrap";


class ProjectForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            repo: '',
            users: [],
        }
    }

    handlerOnChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    handlerOnChangeMultipleSelect(event) {
        let options = event.target.childNodes
        let checkedValues = []
        options.forEach((option) => {
            if (option.selected) {
                checkedValues.push(option.value)
            }
        })

        this.setState({
            [event.target.name]: checkedValues
        })
    }

    handlerOnSubmit(event) {
        this.props.createProject(this.state.name, this.state.repo, this.state.users);
        event.preventDefault();
    }

    render() {
        return (
            <div className='d-flex justify-content-center'>
                <form onSubmit={(event) => this.handlerOnSubmit(event)}>
                    <div className='form-group'>
                        <label htmlFor="name">Name</label>
                        <input type="text" className='form-control' name='name' value={this.state.name}
                               onChange={(event) => this.handlerOnChange(event)}/>
                    </div>
                    <div className='form-group'>
                        <label htmlFor="repo">Repo URL</label>
                        <input type="text" className='form-control' name='repo' value={this.state.repo}
                               onChange={(event) => this.handlerOnChange(event)}/>
                    </div>
                    <div className='form-group'>
                        <label htmlFor="users">Users
                            <select name="users" multiple={true} className="form-control"
                                    onChange={(event) => this.handlerOnChangeMultipleSelect(event)}> {this.props.users.map((user) =>
                                <option key={user.uuid} value={user.uuid}>{user.username}</option>)}
                            </select>
                        </label>
                    </div>
                    <Button type="submit" className='btn btn-primary'>Create</Button>
                </form>
            </div>
        );
    }
}

export default ProjectForm