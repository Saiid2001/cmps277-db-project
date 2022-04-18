import { useEffect, useState, cloneElement, useContext } from "react"
import logo from "../../assets/img/logo_sm.svg"
import avatar from "../../assets/img/avatar.svg"
import api from "../../api"
import { UserContext } from "../../Context"
import "./Main.scss"


export default function Main(props){


    const contextUser = useContext(UserContext)

    const [tab, setTab] = useState(0)
    const [user, setUser] = useState({})
    const [userType, setUserType] = useState(null)

    //get username on load
    useEffect(()=>{
        if(!("first_name" in user)){
        api.getUser(contextUser, setUser)
        api.getUserType(props.user, setUserType)
        }
    })

    
    return <div className="main">
    
        <header>

            <img src={logo}></img>

            <div className="username">
                <h3>{user.first_name} {user.last_name}</h3>
                <img src={avatar}></img>
            </div>

        </header>
        <nav>
            <a href={"/"} className={"selected"}>Profile</a>
            <a href={"/organizations"}>Organizations</a>
            <a href={"/opportunities"}>Opportunities</a>
            
            {userType == api.USER_TYPES.Mentor?<a href={"/seekers"}>Seekers</a>:(
                <a href={"/mentors"}>Mentors</a>
            )}
            {userType == api.USER_TYPES.Seeker?<a href={"/fields"}>Fields</a>:null}
        </nav>
        <main>

            <Card title="Profile">
                
                <ProfileInfoContent data={user}/>
                
            </Card>

        </main>
    </div>
}

function Card(props){


    const [isEditing, setIsEditing] = useState(false);
    const [shouldSave, setShouldSave] = useState(false);

    function editChildren(){

        setShouldSave(false);
        setIsEditing(true);
    }

    function cancelChildren(){
        setShouldSave(false);
        setIsEditing(false);
    }

    function saveChildren(){
        setShouldSave(true);
        setIsEditing(false);
    }
    return <section>
        <h2>{props.title}</h2>
        <div className="content">
            <>{cloneElement(props.children, {edit: isEditing, save: shouldSave})}</>
        </div>
        <div className="buttons">
        {!props.no_edit && ! isEditing ?<button onClick={editChildren}>Edit</button>:null}
        {!props.no_edit && isEditing ?<button onClick={saveChildren}>Save</button>:null}
        {!props.no_edit && isEditing ?<button onClick={cancelChildren}>Cancel</button>:null}
        </div>
    
    </section>
}

function ProfileInfoContent(props){

    const contextUser = useContext(UserContext)


    if(props.save && !props.edit){
        document.querySelector("#profile-info-form button").click()
    }

    function handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);

        api.setUser(contextUser, formProps)
      }

    return <div className="info">
        <form id="profile-info-form" onSubmit={handleSubmit}>
            <section >
                <h2>Basic Info</h2>
                    <input type={"text"} name={"first_name"} placeholder={"First Name"} required {... !props.edit? {"disabled":true}: ""} defaultValue={props.data.first_name}></input>
                    <input type={"text"} name={"last_name"} placeholder={"Last Name"} required {... !props.edit? {"disabled":true}: ""}defaultValue={props.data.last_name}></input>
                    <label htmlFor="birth_date">Birth-date</label>
                    <input type={"date"} id="birth_date" name={"birth_date"} placeholder={"Birth date"} required {... !props.edit? {"disabled":true}: ""} defaultValue={props.data.birth_date}></input>
                    <div className="gender">
                        <input type="radio" id = "gender-m" name="gender" value="M" {... !props.edit? {"disabled":true}: ""} defaultChecked={props.data.gender == "M"}></input>
                        <label htmlFor="gender-m">Male</label>
                        <input type="radio" id = "gender-f" name="gender" value="F" {... !props.edit? {"disabled":true}: ""} defaultChecked={props.data.gender == "F"}></input>
                        <label htmlFor="gender-f">Female</label>
                    </div>
            </section>
            <section >
                <h2>Additional Info</h2>
                    <input type={"url"} name={"linkedin"} placeholder={"LinkedIn URL"} {... !props.edit? {"disabled":true}: ""} defaultValue={props.data.linkedin}></input>
                    <input type={"url"} name={"website"} placeholder={"Website"} {... !props.edit? {"disabled":true}: ""} defaultValue={props.data.website}></input>
                    <input type={"tel"} name="phone" placeholder="Phone Number" {... !props.edit? {"disabled":true}: ""} defaultValue={props.data.phone}></input>
                    
            </section>
            <button type={"submit"} hidden></button>
            </form>
    </div>
}