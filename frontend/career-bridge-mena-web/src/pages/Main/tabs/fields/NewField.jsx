import { useEffect, useState } from "react";
import api from "../../../../api";

export default function NewField(props){


    const [data, setData] = useState({})

    useEffect(()=>{
        if(!("id" in data) && props.edit){
            api.getField(props.id, setData);
        }
    }, [data])

    function handleSubmit(e){
        e.preventDefault();

        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);

        props.edit?api.editField(props.id, formProps, ()=>{window.location = "/fields"}):api.addField(formProps, ()=>{window.location="/fields"});
    }

    return (
        <form id="new-field" className="add-entity-form" onSubmit={handleSubmit}>
            {props.edit?<h1>Edit Field</h1>:<h1>New Field</h1>}
            <label>Name</label>
            <input type="text" name='name' placeholder="Field Name" defaultValue={data.name}></input>
            <label>Description</label>
            <textarea name="description" placeholder="Write few lines about this field..." defaultValue={data.description}></textarea>
            <button type="submit">{props.edit?"Save":"Add Field"}</button>
        </form>
    )
}