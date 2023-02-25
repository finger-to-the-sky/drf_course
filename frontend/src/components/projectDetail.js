import React from "react";
import {useParams} from 'react-router-dom'

const ProjectNotes= ({item}) => {
    return (
        <div className="col-md-6">
            <div
                className="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative">
                <div className="col p-4 d-flex flex-column position-static">
                    <strong className="d-inline-block mb-2 text-success">{item.isActive}</strong>
                    <h3 className="mb-0">{item.name}</h3>
                    <p className="mb-auto">{item.text}</p>
                    <div className="mb-1 text-muted">Last update: {item.updateAt}</div>
                </div>

            </div>
        </div>
    )
}


const ProjectDetail = ({items}) => {
    let {id} = useParams();
    let project = items.filter((item) => item.id === +id)[0];
    return (
        <div>
            <div className="p-4 p-md-5 mb-4 text-white rounded bg-dark">
                <div className="col-md-6 px-0">
                    <h1 className="display-4 fst-italic">Project: {project.name}</h1>
                    <p className="lead mb-0">Repo: <a href="#" className="text-white fw-bold">{project.repoUrl}</a></p>
                    <p className="lead mb-0">Created at: {project.createdAt}</p>
                </div>
            </div>
            <h3 className="pb-4 mb-4 fst-italic border-bottom">
                Notes
            </h3>
            {project.todoList.map((item) => <ProjectNotes item={item}/>)}
        </div>
    )
}

export default ProjectDetail