import React from 'react';

export default function({onClick, children}) {
    return (
        <div className="btn" onClick={onClick}>
            {children}
        </div>
    )
}