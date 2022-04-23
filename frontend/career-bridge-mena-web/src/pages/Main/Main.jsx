import React, { useEffect, useState, useContext } from "react"
import logo from "../../assets/img/logo_sm.svg"
import avatar from "../../assets/img/avatar.svg"
import api from "../../api"
import { TypeContext, UserContext } from "../../Context"
import "./Main.scss"
import {useParams, useSearchParams} from "react-router-dom";

import Profile from "./tabs/profile/Profile"
import Fields from "./tabs/fields/Fields"
import NewField from "./tabs/fields/NewField"
import Organizations from "./tabs/organizations/Organizations"
import NewOrganization from "./tabs/organizations/NewOrganization"
import DetailsOrganization from "./tabs/organizations/DetailsOrganization"
import Opportunities from "./tabs/opportunities/Opportunities"
import NewOpportunity from "./tabs/opportunities/NewOpportunity"
import DetailsOpportunity from "./tabs/opportunities/DetailsOpportunity"
import Users from "./tabs/profile/Users"
import Select from "react-select"

export const UserDataContext = React.createContext("user-data")
export const OrganizationsContext = React.createContext('orgs')

export default function Main(props){

    const contextUser = useContext(UserContext)

    const [user, setUser] = useState({})
    const [userType, setUserType] = useState(null)
    const [orgs, setOrgs] = useState([])

    const [searchParams, setSearchParams] = useSearchParams()
    const {orgID, oppID, uid} = useParams();
    
    const contextType = useContext(TypeContext)

    //get username on load
    useEffect(()=>{
        if(!("first_name" in user)){
        
        if(props.tab != "profile-other"){
            api.getUser(contextUser, setUser)
            api.getUserType(props.user, setUserType)
        }else{
            api.getUser(uid, setUser)
            api.getUserType(uid, setUserType)
        }
        api.getAllOrganizationNames(setOrgs)
        }
    })

    var tab = null;

    switch (props.tab) {
        case "profile":
            tab = <Profile></Profile>;
            break;

        case "profile-other":
            tab = <Profile></Profile>;
            break;
    
        case "users":
            tab = <Users></Users>;
            break;
    

        case "fields":
            tab = <Fields></Fields>;
            break;

        case "new-field":
            tab = <NewField></NewField>;
            break;

        case "edit-field":
            tab = <NewField edit={true} id={searchParams.get("id")}></NewField>;
            break;

        case "organizations":
            tab = <Organizations></Organizations>;
            break;   
            
        case "new-organization":
            tab = <NewOrganization></NewOrganization>;
            break; 

        case "edit-organization":
            tab = <NewOrganization edit={true} id={searchParams.get("id")}></NewOrganization>;
            break; 

        case "details-organization":
            tab = <DetailsOrganization id={orgID}></DetailsOrganization>;
            break;
            
        case "opportunities":
            tab = <Opportunities></Opportunities>;
            break; 
        
        case "new-opportunity":
            tab = <NewOpportunity></NewOpportunity>;
            break; 

        case "edit-opportunity":
            tab = <NewOpportunity edit={true} id={searchParams.get("id")}></NewOpportunity>;
            break; 
    
        case "details-opportunity":
            tab = <DetailsOpportunity edit={true} id={oppID}></DetailsOpportunity>;
            break; 
    
        default:
            tab = <Profile></Profile>
            break;
    }

    
    return <div className="main">
    
        <header>

            <img src={logo}></img>

            <div className="username">
                <h3>{user.first_name} {user.last_name}</h3>
                <img src={avatar}></img>
            </div>

        </header>
        <nav>
            <a href={"/"}  {...props.tab=="profile"? {"className":"selected"}:null}>Profile</a>
            <a href={"/organizations"}  {...props.tab=="organizations"? {"className":"selected"}:null}>Organizations</a>
            <a href={"/opportunities"}  {...props.tab=="opportunities"? {"className":"selected"}:null}>Opportunities</a>
            
            {userType == api.USER_TYPES.Mentor?<a href={"/users?type=S"}  {...props.tab=="seekers"? {"className":"selected"}:null}>Seekers</a>:(
                <a href={"/users?type=M"}>Mentors</a>
            )}
            <a href={"/fields"} {...props.tab=="fields"? {"className":"selected"}:null}>Fields</a>
        </nav>

        <UserContext.Provider value = {props.tab=="profile-other"?uid: contextUser}>
        <OrganizationsContext.Provider value={orgs}>
        <TypeContext.Provider value={userType}>
        <UserDataContext.Provider value={user}>
        <main>

            {tab}

        </main>

        <MessageView></MessageView>

        </UserDataContext.Provider>
        </TypeContext.Provider>
        </OrganizationsContext.Provider>
        </UserContext.Provider>
    </div>

}

function MessageView(props){

    const [open, setOpen] = useState(false);



    return <div id = "message-view">
        <h1 onClick={()=>setOpen(!open)}>Messages</h1>

        {open?
        <div className="main">
            <Select></Select>
            <div className="messages-container">
                <p className="sent" data-time="2020-03-04 12:00"><b>Hello</b></p>
                <p className="received" data-time="2020-03-04 12:00"><b>By</b></p>
            </div>
            <form>
                <input type="text" name="message"></input>
                <button type="submit">Send</button>
            </form>
        </div>
        :null}
    </div>
}

