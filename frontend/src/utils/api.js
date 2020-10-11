async function postURL(url, body, verb='POST') {
    const response = await fetch(url, {
        method: verb,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
    return response.json();
}

export async function createLobby(name) {
    return await postURL('/createLobby', {name}, 'PUT');
}