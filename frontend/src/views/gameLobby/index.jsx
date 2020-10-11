import React from 'react';
import {Link, useParams} from 'react-router-dom';

export default function() {
    let {gamecode} = useParams();
    return (
        <div className="main-menu">
            <h1><Link to="/">← </Link>GAME LOBBY {gamecode}</h1>
        </div>
    )
}