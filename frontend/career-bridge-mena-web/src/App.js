import logo from './logo.svg';
import './App.css';
import Login from "./pages/Login/Login";
import Signup from './pages/Signup/Signup';
import React, {useState} from "react";
import Main from "./pages/Main/Main";

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import { UserContext } from './Context';



function App() {

  const [user, setUser] = useState('1');
  return (
    <div className="App">
      <Router>
      <div>
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Routes>
          <Route path="/signup/mentor" element={<Signup type={"mentor"}></Signup>}>
            
          </Route>
          <Route path="/signup/seeker" element={
            <Signup type={"seeker"}></Signup>}>
          </Route>
          <Route path="/" element={
user?<UserContext.Provider value={user}><Main user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>

          }>
            </Route>
        </Routes>
      </div>
    </Router>
    </div>
  );
}

export default App;
