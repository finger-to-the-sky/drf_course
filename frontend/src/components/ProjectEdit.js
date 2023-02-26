import React, {useContext} from "react";
import {Button} from "react-bootstrap";
import {useParams} from "react-router-dom";


const ProjectEdit = ({users, projects, editProject}) => {
    let {id} = useParams();
    let project = projects.find(item => item.id === +id);
    let projectState = {name: project?.name, repoUrl: project?.repoUrl, users: project?.users
    };

    function handlerOnChange(event) {
        console.log(event.target.value);
        projectState[event.target.name] = event.target.value
    }

    function handlerOnChangeMultipleSelect(event){
        let options = event.target.childNodes
        let checkedValues = []
        options.forEach((option) => {
            if (option.selected){
                checkedValues.push(option.value)
            }
        })
        projectState[event.target.name] = checkedValues

    }

     function handlerOnSubmit(event) {
        editProject(id, projectState.name, projectState.repoUrl, projectState.users);
        console.log(id, projectState.name, projectState.repoUrl, projectState.users)
        event.preventDefault();
    }
    return (
        <div className='d-flex justify-content-center'>
            <form onSubmit={(event) => handlerOnSubmit(event)}>
                <div className='form-group'>
                    <label htmlFor="name">Name</label>
                    <input type="text" className='form-control' name='name' defaultValue={project?.name}
                           onChange={(event) => handlerOnChange(event)}/>
                </div>
                <div className='form-group'>
                    <label htmlFor="repoUrl">Repo URL</label>
                    <input type="text" className='form-control' name='repoUrl' defaultValue={project?.repoUrl}
                           onChange={(event) => handlerOnChange(event)}/>
                </div>
                <div className='form-group'>
                    <label htmlFor="users">Users
                        <select name="users" multiple={true} className="form-control"
                                onChange={(event) => handlerOnChangeMultipleSelect(event)}> {users.map((user) =>
                            <option key={user.uuid} value={user.uuid}>{user.username}</option>)}
                        </select>
                    </label>
                </div>
                <Button type="submit" className='btn btn-primary'>Edit</Button>
            </form>
        </div>
    )
}

export default ProjectEdit