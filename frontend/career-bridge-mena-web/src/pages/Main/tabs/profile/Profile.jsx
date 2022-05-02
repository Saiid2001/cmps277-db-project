import React, { useEffect, useState, useContext } from "react";
import api from "../../../../api";
import { UserContext, TypeContext } from "../../../../Context";
import Select from 'react-select';
import CreatableSelect from 'react-select/creatable';
import { InlineListItems } from "../../../../components/InlineListItems";
import { UserDataContext, OrganizationsContext } from "../../Main";

import { Card } from "../../../../components/Card"
import { ListContent } from "../../../../components/ListContent"
import { type } from "@testing-library/user-event/dist/type";


export default function Profile(props){

    const userType = useContext(TypeContext);
    console.log(props.other)
    
    return <div id="profile-tab" className="tab">

        <Card title="Profile" editButton={!props.other}>
                
                <ProfileInfoContent/>
                {userType==api.USER_TYPES.Mentor? <MentorPositionContent/>:<SeekerInfoContent/>}
                
            </Card>

            <Card title="Education" editButton={false}>
                <ListContent 
                className={"education-info"}
                api_request={api.getEducations}
                new_record= {{"type":"new", "accomplishments":[]}}
                RecordType= {EducationRecord}
                noEdit = {props.other}
                />
                <div></div>
            </Card>

            {userType==api.USER_TYPES.Mentor?<Card title="Experience" editButton={false}>
                <ListContent 
                className={"experience-info"}
                api_request={api.getExperiences}
                new_record= {{"type":"new", "accomplishments":[]}}
                RecordType= {ExperienceRecord}
                noEdit = {props.other}
                />
                <div></div>
            </Card>:null}

            {userType==api.USER_TYPES.Seeker?<Card title="Projects" editButton={false}>
                <ListContent 
                className={"projects-info"}
                api_request={api.getProjects}
                new_record= {{"type":"new"}}
                RecordType= {ProjectRecord}
                noEdit = {props.other}
                />
                <div></div>
            </Card>:null}

            {userType==api.USER_TYPES.Seeker?<Card title="Certifications" editButton={false}>
                <ListContent 
                className={"certifications-info"}
                api_request={api.getCertifications}
                new_record= {{"type":"new"}}
                RecordType= {CertificationRecord}
                noEdit = {props.other}
                />
                <div></div>
            </Card>:null}

            {userType==api.USER_TYPES.Seeker?<Card title="Skills" editButton={!props.other}>
                <SkillsContent></SkillsContent>
                <div></div>
            </Card>:null}
    </div>

}

export function ProfileInfoContent(props) {

    const contextUser = useContext(UserContext);
    const user = useContext(UserDataContext);


    if (props.save && !props.edit) {
        document.querySelector("#profile-info-form button").click();
    }

    function handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        let formProps = Object.fromEntries(formData);

        formProps.email = contextUser;

        api.setUser( formProps);
    }

     

    return <div className="info">
        <form id="profile-info-form" onSubmit={handleSubmit}>
            <section>
                <h2>Basic Info</h2>
                <input type={"text"} name={"first_name"} placeholder={"First Name"} required {...!props.edit ? { "disabled": true } : ""} defaultValue={user.first_name}></input>
                <input type={"text"} name={"last_name"} placeholder={"Last Name"} required {...!props.edit ? { "disabled": true } : ""} defaultValue={user.last_name}></input>
                <label htmlFor="birth_date">Birth-date</label>
                <input type={"date"} id="birth_date" name={"birth_date"} placeholder={"Birth date"} required {...!props.edit ? { "disabled": true } : ""} defaultValue={user.birth_date}></input>
                {user.gender?<div className="gender">
                    <input type="radio" id="gender-m" name="gender" value="M" {...!props.edit ? { "disabled": true } : ""} defaultChecked={user.gender == "Male"}></input>
                    <label htmlFor="gender-m">Male</label>
                    <input type="radio" id="gender-f" name="gender" value="F" {...!props.edit ? { "disabled": true } : ""} defaultChecked={user.gender == "Female"}></input>
                    <label htmlFor="gender-f">Female</label>
                </div>:null}
            </section>
            <section>
                <h2>Additional Info</h2>
                <input type={"url"} name={"linkedin"} placeholder={"LinkedIn URL"} {...!props.edit ? { "disabled": true } : ""} defaultValue={user.linkedin}></input>
                <input type={"url"} name={"website"} placeholder={"Website"} {...!props.edit ? { "disabled": true } : ""} defaultValue={user.website}></input>
                <input type={"tel"} name="phone" placeholder="Phone Number" {...!props.edit ? { "disabled": true } : ""} defaultValue={user.phone}></input>

            </section>
            <button type={"submit"} hidden></button>
        </form>
    </div>;
}
export function MentorPositionContent(props) {

    const contextUser = useContext(UserContext);


    const [data, setData] = useState({});
    const orgs = useContext(OrganizationsContext);
    const [selectedOrg, setSelectedOrg] = useState("");



    useEffect(() => {
        if (!("position" in data)) {
            api.getCurrentPosition(contextUser, setData);
        }
    });

    if (props.save && !props.edit) {
        document.querySelector("#mentor-info-form button").click();
    }

    function handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);


        if (selectedOrg != "")
            formProps.org_id = selectedOrg;
        else
            formProps.org_id = data.org_id;

        api.setCurrentPosition(contextUser, formProps);
    }

    function onSelectChange(val, act) {

        if (act.action == "select-option")
            setSelectedOrg(val.value.toString());
    }

    let url = null;
    let opts = [];

    if (orgs.length && typeof(orgs) == typeof([1,2])){
    if ("position" in data) {
        url = <a href={"/organizations?id=" + (selectedOrg != "" ? orgs.find(x => x.org_id == selectedOrg).org_id : orgs.find(x => x.org_id == data.org_id).org_id)}>{selectedOrg != "" ? orgs.find(x => x.org_id == selectedOrg).org_name : orgs.find(x => x.org_id == data.org_id).org_name}</a>;
    }

     opts = orgs.map(org => { return { 'value': org.org_id, "label": org.org_name }; });
    }
    return <section className="mentor-info">
        <h1>Mentor</h1>
        <div>
            <form id="mentor-info-form" onSubmit={handleSubmit}>
                <h3>Current Position</h3>
                <input type={"text"} name={"position"} placeholder={"Position"} {...!props.edit ? { "disabled": true } : ""} defaultValue={data.position}></input>
                <p>at</p>
                {props.edit ? (
                    <Select
                        options={opts}
                        onChange={onSelectChange}
                        defaultValue={opts.find(x => x.value == data.org_id)} />) : url}


                <button type={"submit"} hidden></button>
            </form>
        </div>

    </section>;

}
export function SeekerInfoContent(props) {

    const contextUser = useContext(UserContext);

    const [data, setData] = useState({});

    useEffect(() => {

        if (!("sop" in data)) {

            api.getSeekerData(contextUser, setData);
        }
    });

    if (props.save && !props.edit) {
        document.querySelector("#seeker-info-form button").click();
    }

    function handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);
        formProps.open_to_work = (formProps.open_to_work == "true");
        api.setSeekerData(contextUser, formProps);
    }

    return <section className="seeker-info">
        <h1>Seeker</h1>
        <div>
            <form id="seeker-info-form" onSubmit={handleSubmit}>
                {data.open_to_work != null?<div><input type={"checkbox"} name={"open_to_work"} id="open_to_work_bx" {...!props.edit ? { "disabled": true } : ""} defaultChecked={data.open_to_work} value="true"></input>
                    <label htmlFor="open_to_work_bx">Open to work</label>
                </div>:null}

                <textarea name="sop" id="sop" placeholder="statment of purpose" {...!props.edit ? { "disabled": true } : ""} defaultValue={data.sop}>

                </textarea>

                <button type={"submit"} hidden></button>
            </form>
        </div>

    </section>;
}
export function EducationRecord(props) {

    const contextUser = useContext(UserContext);
    const [selectedOrg, setSelectedOrg] = useState("");
    const orgs = useContext(OrganizationsContext);
    const [accomplishments, setAccomplishments] = useState(props.data.accomplishments);

    function handleSubmit(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);

        if (selectedOrg != "")
            formProps.org_id = selectedOrg;
        else
            formProps.org_id = props.data.org_id;

        let accomplishments = [];
        document.querySelectorAll(`#education-info-${props.id}-form li input`).forEach(x => {
            accomplishments.push(x.value);
        });

        formProps.accomplishments = accomplishments;

        formProps.id = props.data.id? props.data.id: 0;

        api.setEducation(contextUser, formProps);

    }

    let url = null;

    let opts = [];

    if(orgs.length){

    if ("org_id" in props.data) {
        url = <a className="university" href={"/organizations?id=" + (selectedOrg != "" ? orgs.find(x => x.org_id == selectedOrg).org_id : orgs.find(x => x.org_id == props.data.org_id).org_id)}>{selectedOrg != "" ? orgs.find(x => x.org_id == selectedOrg).org_name : orgs.find(x => x.org_id == props.data.org_id).org_name}</a>;
    }

    opts = orgs.map(org => { return { 'value': org.org_id, "label": org.org_name }; });
    }

    function onSelectChange(val, act) {

        if (act.action == "select-option")
            setSelectedOrg(val.value.toString());
    }

    function addOption() {
        let d = [...accomplishments];
        d.push("");
        setAccomplishments(d);
    }

    function removeOption(i) {
        let d = [...accomplishments];
        d.splice(i, 1);
        setAccomplishments(d);
    }

    const [isEditing, setIsEditing] = useState(props.isNew);
    const [shouldSave, setShouldSave] = useState(false);

    function editChildren() {

        setShouldSave(false);
        setIsEditing(true);
    }

    function cancelChildren() {
        setShouldSave(false);
        setIsEditing(false);
    }

    function saveChildren() {
        document.querySelector(`#education-info-${props.id}-form .submit`).click();
        setShouldSave(true);
        setIsEditing(false);
    }

    function deleteChildren() {
        api.deleteEducation(contextUser, props.data);
        props.onDelete();
    }


    return <div className="education_records">

        <form id={`education-info-${props.id}-form`} onSubmit={handleSubmit}>
            <div className="flexer">
                <input type={"text"} name={"major"} className={"major"} placeholder={"Major"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.major}></input>

                <p className="date">from <input type={"date"} name={"start_at"} placeholder={"start date"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.start_at}></input>
                    to <input type={"date"} name={"end_at"} placeholder={"end date"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.end_at}></input></p>
            </div>
            {isEditing ? (
                <Select
                    options={opts}
                    onChange={onSelectChange}
                    defaultValue={opts.find(x => x.value == props.data.org_id)} />) : url}
            <div className="spacer">
                <p className="score">Score</p>
                <input className="score" type={"text"} name={"score"} placeholder={"Score"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.score}></input>
            </div>
            <p htmlFor="" className="score">Accomplishments</p>
            <ul>
                {accomplishments.map((x, i) => <li><input key={i} type={"text"} placeholder={"Accomplishment description"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={x}></input>{isEditing ? <button onClick={() => removeOption(i)}>Remove</button> : null}</li>)}
                {isEditing ? <li><button onClick={addOption}>Add accomplishment</button></li> : null}
            </ul>
            <button type="submit" className="submit" hidden />
        </form>
        {props.noEdit?null:<div className="buttons">
            {!props.no_edit && !isEditing ? <button onClick={editChildren}>Edit</button> : null}
            {!props.no_edit && isEditing ? <button onClick={saveChildren}>Save</button> : null}
            {!props.no_edit && isEditing ? <button onClick={cancelChildren}>Cancel</button> : null}
            {!props.no_edit && isEditing ? <button onClick={deleteChildren}>Delete</button> : null}
        </div>}
    </div>;
}
export function ExperienceRecord(props) {

    const contextUser = useContext(UserContext);
    const [selectedOrg, setSelectedOrg] = useState("");
    const orgs = useContext(OrganizationsContext);

    function handleSubmit(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);

        if (selectedOrg != "")
            formProps.org_id = selectedOrg;
        else
            formProps.org_id = props.data.org_id;

        let accomplishments = [];
        document.querySelectorAll(`#experience-info-${props.id}-form .accomplishments-list li textarea`).forEach(x => {
            accomplishments.push(x.value);
        });

        formProps.accomplishments = accomplishments;

        formProps.id = props.data.id? props.data.id: 0;

        api.setExperience(contextUser, formProps);

        if(formProps.id == 0) window.location.reload();

    }


    //url part
    let url = null;
    let opts = [];

    if(orgs.length){
    if ("org_id" in props.data || props.data.type == "new") {
        url = <a className="university" href={"/organizations?id=" + (selectedOrg != "" ? orgs.find(x => x.org_id == selectedOrg).org_id : orgs.find(x => x.org_id == props.data.org_id).org_id)}>{selectedOrg != "" ? orgs.find(x => x.org_id == selectedOrg).org_name : orgs.find(x => x.org_id == props.data.org_id).org_name}</a>;
        console.log(selectedOrg)
    }
    //select
     opts = orgs.map(org => { return { 'value': org.org_id, "label": org.org_name }; });

    }

    function onSelectChange(val, act) {
        if (act.action == "select-option")
            setSelectedOrg(val.value.toString());
    }

    const [isEditing, setIsEditing] = useState(props.isNew);
    const [shouldSave, setShouldSave] = useState(false);

    function editChildren() {
        setShouldSave(false);
        setIsEditing(true);
    }

    function cancelChildren() {
        setShouldSave(false);
        setIsEditing(false);
    }

    function saveChildren() {
        document.querySelector(`#experience-info-${props.id}-form .submit`).click();
        setShouldSave(true);
        setIsEditing(false);
    }

    function deleteChildren() {
        api.deleteExperience(contextUser, props.data);
        props.onDelete();
    }

    return <div className="education_records">

        <form id={`experience-info-${props.id}-form`} onSubmit={handleSubmit}>
            <div className="flexer">
                <input type={"text"} name={"position"} className={"major"} placeholder={"Position"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.position}></input>

                <p className="date">from <input type={"date"} name={"start_at"} placeholder={"start date"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.start_at}></input>
                    to <input type={"date"} name={"end_at"} placeholder={"end date"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.end_at}></input></p>
            </div>
            {isEditing ? (
                <Select
                    options={opts}
                    onChange={onSelectChange}
                    defaultValue={opts.find(x => x.value == props.data.org_id)} />) : url}
            <p htmlFor="" className="score">Accomplishments</p>
            <InlineListItems className={"accomplishments-list"} items={props.data.accomplishments} edit={isEditing} />
            <button type="submit" className="submit" hidden />
        </form>
        {props.noEdit?null:<div className="buttons">
            {!props.no_edit && !isEditing ? <button onClick={editChildren}>Edit</button> : null}
            {!props.no_edit && isEditing ? <button onClick={saveChildren}>Save</button> : null}
            {!props.no_edit && isEditing ? <button onClick={cancelChildren}>Cancel</button> : null}
            {!props.no_edit && isEditing ? <button onClick={deleteChildren}>Delete</button> : null}
        </div>}
    </div>;
}
export function ProjectRecord(props) {

    const contextUser = useContext(UserContext);

    function handleSubmit(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);

        if( props.data.type != "new" && props.data.date != formProps.date)
            api.deleteProject(contextUser, props.data)

        api.setProject(contextUser, formProps);
    }

    const [isEditing, setIsEditing] = useState(props.isNew);
    const [shouldSave, setShouldSave] = useState(false);

    function editChildren() {
        setShouldSave(false);
        setIsEditing(true);
    }

    function cancelChildren() {
        setShouldSave(false);
        setIsEditing(false);
    }

    function saveChildren() {
        document.querySelector(`#project-info-${props.id}-form .submit`).click();
        setShouldSave(true);
        setIsEditing(false);
    }

    function deleteChildren() {
        api.deleteProject(contextUser, props.data);
        props.onDelete();
    }

    return <div className="education_records">

        <form id={`project-info-${props.id}-form`} onSubmit={handleSubmit}>
            <div className="flexer">
                <input type={"text"} name={"name"} className={"major"} placeholder={"Project Name"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.name}></input>
                <p className="date"><input type={"date"} name={"date"} placeholder={"date"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.date}></input></p>
            </div>
            <textarea type={"text"} name={"description"} className={"major"} placeholder={"Project Description"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.description}></textarea>
            <button type="submit" className="submit" hidden />
        </form>
        {props.noEdit?null:<div className="buttons">
            {!props.no_edit && !isEditing ? <button onClick={editChildren}>Edit</button> : null}
            {!props.no_edit && isEditing ? <button onClick={saveChildren}>Save</button> : null}
            {!props.no_edit && isEditing ? <button onClick={cancelChildren}>Cancel</button> : null}
            {!props.no_edit && isEditing ? <button onClick={deleteChildren}>Delete</button> : null}
        </div>}
    </div>;
}
export function CertificationRecord(props) {

    const contextUser = useContext(UserContext);

    function handleSubmit(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);

        if( props.data.type != "new" && props.data.url != formProps.url)
            api.deleteCertification(contextUser, props.data)

        api.setCertification(contextUser, formProps);
    }

    const [isEditing, setIsEditing] = useState(props.isNew);
    const [shouldSave, setShouldSave] = useState(false);

    function editChildren() {
        setShouldSave(false);
        setIsEditing(true);
    }

    function cancelChildren() {
        setShouldSave(false);
        setIsEditing(false);
    }

    function saveChildren() {
        document.querySelector(`#project-info-${props.id}-form .submit`).click();
        setShouldSave(true);
        setIsEditing(false);
    }

    function deleteChildren() {
        api.deleteCertification(contextUser, props.data);
        props.onDelete();
    }

    return <div className="education_records">

        <form id={`project-info-${props.id}-form`} onSubmit={handleSubmit}>
            <div className="flexer">
                <input type={"text"} name={"name"} className={"major"} placeholder={"Certification Name"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.name}></input>
                <p className="date"><input type={"date"} name={"date"} placeholder={"date"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.date}></input></p>
            </div>
            {isEditing ? <input type={"url"} name={"url"} className={"major"} placeholder={"Certification URL"} required {...!isEditing ? { "disabled": true } : ""} defaultValue={props.data.url}></input> : (
                <a href={props.data.url}>Link to certification</a>
            )}
            <button type="submit" className="submit" hidden />
        </form>
        {props.noEdit?null:<div className="buttons">
            {!props.no_edit && !isEditing ? <button onClick={editChildren}>Edit</button> : null}
            {!props.no_edit && isEditing ? <button onClick={saveChildren}>Save</button> : null}
            {!props.no_edit && isEditing ? <button onClick={cancelChildren}>Cancel</button> : null}
            {!props.no_edit && isEditing ? <button onClick={deleteChildren}>Delete</button> : null}
        </div>}
    </div>;
}
export function SkillsContent(props) {

    const contextUser = useContext(UserContext);

    const [skills, setSkills] = useState([]);
    const [loaded, setLoaded] = useState(false);

    useEffect(() => {
        if (!loaded) {
            api.getSkills(contextUser, setSkills);
            setLoaded(true);
        }
    }, [loaded]);

    if (props.save && !props.edit) {
        api.setSkills(contextUser, skills);
    }

    function handleChange(
        newValue,
        actionMeta
    ) {
        console.group('Value Changed');
         
         
        console.groupEnd();

        setSkills(newValue.map(x => x.value));
    }

    let opts = skills.map(x => { return { label: x, value: x }; });

    return <div className="education_records">

        <form>

            {skills.length > 0 ? <CreatableSelect
                isMulti
                onChange={handleChange}
                isDisabled={!props.edit}
                value={skills.map(x => { return { label: x, value: x }; })}
                options={skills.map(x => { return { label: x, value: x }; })} /> : <CreatableSelect
                isMulti
                onChange={handleChange}
                isDisabled={!props.edit}
                options={opts} />}

            <button type="submit" className="submit" hidden />
        </form>
    </div>;
}
