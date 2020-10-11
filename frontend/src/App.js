import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom';

import MainMenu from 'views/mainMenu';
import CreateGame from 'views/createGame';
import JoinGame from 'views/joinGame';
import GameLobby from 'views/gameLobby';

import './App.css';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/create">
          <CreateGame />
        </Route>
        <Route path="/join/:gamecode">
          <GameLobby />
        </Route>
        <Route path="/join">
          <JoinGame />
        </Route>
        <Route path="/">
          <MainMenu />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
