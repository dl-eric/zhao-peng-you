import React, {useState} from 'react';
import {Link} from 'react-router-dom';
import Cleave from 'cleave.js/react';

import Button from 'components/button';
import {createLobby} from 'utils/api';

export default function() {
    const [name, setName] = useState('');

    const onNameChange = (e) => {
        setName(e.target.value)
    };

    const handleCreateLobby = async () => {
        const lobbyCode = await createLobby(name);
        if(lobbyCode) {
            console.log("created lobby with code ", lobbyCode);
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