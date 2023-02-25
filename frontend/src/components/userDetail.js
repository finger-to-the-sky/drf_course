import React from "react";
import {useParams} from 'react-router-dom'


const UserDetail = ({items}) => {
    let {uid} = useParams();
    let user = items.find(item => item.uid === uid);
    return (
        <div className="justify-content-center">
            <h4 className="d-flex justify-content-between text-center mb-3">
                <span className="text-primary">
                    {user.username}
                </span>
            </h4>
            <ul className="list-group mb-3">
                <li className="list-group-item d-flex justify-content-between lh-sm">
                    <div>
                        <h6 className="my-0">First name</h6>
                        <small className="text-muted">{user.firstName}</small>
                    </div>
                </li>
                <li className="list-group-item d-flex justify-content-between lh-sm">
                    <div>
                        <h6 className="my-0">Last name</h6>
                        <small className="text-muted">{user.lastName}</small>
                    </div>
                </li>
                <li className="list-group-item d-flex justify-content-between lh-sm">
                    <div>
                        <h6 className="my-0">Email</h6>
                        <small className="text-muted">{user.email}</small>
                    </div>
                </li>
            </ul>
        </div>
    )
}

export default UserDetail