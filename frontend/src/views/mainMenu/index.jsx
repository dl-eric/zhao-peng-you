import React from 'react';
import {Link} from 'react-router-dom';

import Button from 'components/button';

export default function() {
    return (
        <div className="main-menu">
            <h1>ZHAO PENG YOU / 找朋友</h1>
            <Link to="/create">
                <Button>CREATE GAME</Button>
            </Link>
            <Link to="/join">
                <Button>JOIN GAME</Button>
            </Link>
        </div>
    )
}