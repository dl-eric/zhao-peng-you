import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom';
import MainMenu from 'views/mainMenu';
import './App.css';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/">
          <MainMenu />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
