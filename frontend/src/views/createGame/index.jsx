import React, {useState} from 'react';
import {Link} from 'react-router-dom';
import {withRouter} from 'react-router';
import Cleave from 'cleave.js/react';

import Button from 'components/button';
import {createLobby} from 'utils/api';

function CreateGame(props) {
    const [name, setName] = useState('');

    const onNameChange = (e) => {
        setName(e.target.value)
    };

    const handleCreateLobby = async () => {
        const lobbyCode = await createLobby(name);
        console.log(props);
        if(lobbyCode) {
            // navigate to the newly created lobby
            props.history.push({
                pathname: `/join/${lobbyCode}`,
                search: `?name=${name}`
            });
        }
    }

    return (
        <div className="main-menu">
            <h1><Link to="/">← </Link>CREATE GAME</h1>
            <Cleave className="name-input" placeholder="NAME" onChange={onNameChange}/>
            <Button onClick={handleCreateLobby}>CREATE GAME</Button>
        </div>
    )
}

export default withRouter(CreateGame);