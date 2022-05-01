import { useEffect, useState } from "react";
import api from "../../../../api";

export default function NewOrganization(props){

    const [data, setData] = useState({})
     

    useEffect(()=>{
        if(!("id" in data) && props.edit){
            api.getOrganization(props.id, setData);
        }
    }, [data])

    function handleSubmit(e){
        e.preventDefault();

        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);

        props.edit?api.editOrganization(props.id, formProps, ()=>{window.location="/organizations"}):api.addOrganization(formProps, ()=>{window.location="/organizations"});
    }


    return (
        <form id="new-field" className="add-entity-form" onSubmit={handleSubmit}>
            {props.edit?<h1>Edit Organization</h1>:<h1>New Organization</h1>}
            <label>Name</label>
            <input type="text" name='name' placeholder="Organization Name" required defaultValue={data.name}></input>
            <label>Email</label>
            <input type="email" name='email' placeholder="Organization Contact Email" required defaultValue={data.email}></input>
            <label>Website</label>
            <input type="url" name='website' placeholder="Organization Website" defaultValue={data.website}></input >
            <label>Location</label>
            <input type="text" name='location' placeholder="Organization Location" defaultValue={data.location}></input>
            <label>It is an educational organization</label>
            <input type="checkbox" name='educational' label="yes" value="true" defaultChecked={data.is_educational}></input>
            {props.edit?<button type="submit">Save</button>:<button type="submit">Add Organization</button>}
        </form>
    )
}