import logo from './logo.svg';
import './App.css';
import Login from "./pages/Login/Login";
import Signup from './pages/Signup/Signup';
import React, {useEffect, useState} from "react";
import Main from "./pages/Main/Main";

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import { UserContext } from './Context';


import { ReactSession } from 'react-client-session';

function App() {

  const [user, setUser] = useState(ReactSession.get('user'));

  useEffect(
    ()=>{

      if(user)
        ReactSession.set('user', user)
    }
    ,[user]
  )

  return (
    <div className="App">
      <Router>
      <div>
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Routes>
          <Route path="/signup/mentor" element={<Signup type={"mentor"} onLogin={setUser}></Signup>}>
            
          </Route>
          <Route path="/signup/seeker" element={
            <Signup type={"seeker"} onLogin={setUser}></Signup>}>
          </Route>
          <Route path={"/"}>

          <Route path=""  element={
user?<UserContext.Provider  value={user}><Main tab={"profile"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }>
            </Route>

            <Route path="/users"  element={
user?<UserContext.Provider  value={user}><Main tab={"users"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }>
            </Route>

            <Route path="/users/details/:uid"  element={
user?<UserContext.Provider  value={user}><Main tab={"profile-other"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>

            </Route>
            <Route path={"/fields"} >
            <Route path="" element={
user?<UserContext.Provider value={user}><Main tab={"fields"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }>
            </Route>
            <Route path="add" element={
user?<UserContext.Provider value={user}><Main tab={"new-field"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>

            <Route path="edit" element={
user?<UserContext.Provider value={user}><Main tab={"edit-field"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>

            </Route>

            <Route path={"/organizations"} >
            <Route path="" element={
user?<UserContext.Provider value={user}><Main tab={"organizations"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }>
            </Route>
            <Route path="add" element={
user?<UserContext.Provider value={user}><Main tab={"new-organization"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>

<Route path="edit" element={
user?<UserContext.Provider value={user}><Main tab={"edit-organization"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>
          <Route path="details/:orgID" element={
user?<UserContext.Provider value={user}><Main tab={"details-organization"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>
          </Route>


<Route path={"/opportunities"} >
            <Route path="" element={
user?<UserContext.Provider value={user}><Main tab={"opportunities"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }>
            </Route>
            <Route path="add" element={
user?<UserContext.Provider value={user}><Main tab={"new-opportunity"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>

<Route path="edit" element={
user?<UserContext.Provider value={user}><Main tab={"edit-opportunity"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>

<Route path="details/:oppID" element={
user?<UserContext.Provider value={user}><Main tab={"details-opportunity"} user={user}></Main></UserContext.Provider>:<Login onLogin={setUser}></Login>
          }></Route>

            </Route>
        </Routes>
      </div>
    </Router>
    </div>
  );
}

export default App;
