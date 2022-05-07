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
import { type } from "@testing-library/user-event/dist/type"

import { ReactSession } from 'react-client-session';

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

        api.getAllOrganizationNames(x=>{setOrgs(x)})
        
    }
    }, [userType])

    var tab = null;

    useEffect(()=>{

        if(orgs.length && typeof(orgs) == typeof("")){
            setOrgs(JSON.parse(orgs))
        }

    }, [orgs])

    switch (props.tab) {
        case "profile":
            tab = <Profile ></Profile>;
            break;

        case "profile-other":
            tab = <Profile other={true}></Profile>;
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

    function handleLogout(){
        ReactSession.remove('user')
        window.location = "";
    }

    if (orgs.length)
    return <div className="main">
    
        <header>

            <img src={logo}></img>

            <div className="username">
                <h3>{user.first_name} {user.last_name}</h3>
                <img src={avatar}></img>
                <button onClick={handleLogout}>Logout</button>
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


    return null

}



function MessageView(props){

    const [open, setOpen] = useState(false);
    const [loaded, setLoaded] = useState(false);
    const [refresh ,setRefresh] = useState(true); 
    const [messages, setMessages] = useState([]);
    const [other, setOther] = useState(null);
    const userContext = useContext(UserContext)

    console.log(messages)

    useEffect(()=>{
        if(!loaded){

            window.addEventListener('open-messages', 
            (e)=>{
               
                let other_id = e.detail.other
                setOther(other_id)
                api.getMessage(userContext, other_id, setMessages)
                setOpen(true)
            })
            setLoaded(true)
        }

        if(refresh){
            console.log('h')
            api.getMessage(userContext, other, setMessages)
            setRefresh(false)
        }
    },[loaded,refresh])

    

    function handleSubmit(e){
        e.preventDefault();
        const formData = new FormData(e.target);
        let formProps = Object.fromEntries(formData);
        api.sendMessage(userContext, other, formProps.message, ()=>{
            setRefresh(true)
            e.target.reset()
        })
    }
    
    return <div id = "message-view">
        <h1 onClick={()=>setOpen(false)}>Messages</h1>

        {open?
        <div className="main">
            <h3>{other}</h3>
            <div className="messages-container">

                {messages.map(x =>{
                    return x.type=="sent"?<p className="sent" data-time={x.timestamp}><b>{x.message}</b></p>:<p className="received" data-time={x.timestamp}><b>{x.message}</b></p>
            })}
            </div>
            <form onSubmit={handleSubmit}>
                <input type="text" name="message"></input>
                <button type="submit">Send</button>
            </form>
        </div>
        :null}
    </div>
}

