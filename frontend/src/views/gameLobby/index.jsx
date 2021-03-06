import React, {useEffect, useState} from 'react';
import Cleave from 'cleave.js/react';
import {Link, useParams, withRouter} from 'react-router-dom';
import queryString from 'query-string';
import io from 'socket.io-client';

import Button from 'components/button';

function GameLobby(props) {
    let {gamecode} = useParams();
    let {name} = queryString.parse(props.location.search);

    const [inputName, setName] = useState('');
    const [socket, setSocket] = useState(null);
    const [players, setPlayers] = useState([]);

    const initializeSocket = (name) => {
        // ws://localhost:8000/lobby/%s <- %s = lobby_code
        const socket = io("http://localhost:8000");
        setSocket(socket)
        socket.emit('join_lobby', gamecode, name);
        socket.on("name", (msg) => setName(msg));
        socket.on("players", (players_json) => setPlayers(JSON.parse(players_json)));
    }

    useEffect(() => {
        if(name) {
            initializeSocket(name);
        }
    }, [])

    const onNameChange = (e) => {
        setName(e.target.value);
    }

    return (
        <div className="main-menu">
            <h1><Link to="/">← </Link>GAME LOBBY {gamecode}</h1> 
            {(!name && !socket) ? 
            [
                <h1>ENTER A NAME TO JOIN</h1>,
                <Cleave className="name-input" placeholder="NAME" onChange={onNameChange}/>,
                <Button onClick={() => initializeSocket(inputName)}>JOIN LOBBY</Button>
            ] : 
                <div>
                    <h1>YOUR NAME IS {inputName}</h1>
                    <div>Players: </div>
                    <ul>
                        {players.map(playerName => (
                            <li>{playerName}</li>
                        ))}
                    </ul>
                </div>
            
            }
        </div>
    )
}

export default withRouter(GameLobby);