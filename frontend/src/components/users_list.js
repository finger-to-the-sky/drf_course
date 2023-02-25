const UserItem = ({user}) => {

    return (
        <tr>
            <td>
                {user.username}
            </td>
            <td>
                {user.firstName}
            </td>
            <td>
                {user.lastName}
            </td>
        </tr>
    )
}

const UserList = ({users}) => {
    return (
        <div className="table-responsive">
            <table className="table table-striped table-sm">
                <thead>
                    <th>Username</th>
                    <th>First name</th>
                    <th>Last name</th>
                    {users.map((user) => <UserItem user={user}/>)}
                </thead>
            </table>
        </div>
    )
}

export default UserList