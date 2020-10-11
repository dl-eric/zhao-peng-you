import React from 'react';

export default function({placeholder, onChange}) {
    return (
        <div className="text-input">
            <input placeholder={placeholder} onChange={onChange}></input>
        </div>
    )
}