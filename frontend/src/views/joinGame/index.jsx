import React, { useState } from 'react';
import {Link} from 'react-router-dom';
import Cleave from 'cleave.js/react';

import Button from 'components/button';

export default function() {
    const [code, setCode] = useState('');

    const onCodeChange = (e) => {
        const code = e.target.value.replace(/\s+/g, '').toUpperCase();
        setCode(code)
    };

    return (
        <div className="main-menu">
            <h1><Link to="/">← </Link>JOIN GAME</h1>
            <Cleave className="input code-input" placeholder="CODE" options={{blocks: [1,1,1,1]}} onChange={onCodeChange}/>
            <Link to={`/join/${code}`}><Button>JOIN</Button></Link>
        </div>
    )
}