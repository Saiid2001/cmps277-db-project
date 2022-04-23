import { useContext, useEffect, useState } from "react";
import Select from "react-select";
import api from "../../../../api";
import { InlineListItems } from "../../../../components/InlineListItems";
import { UserContext } from "../../../../Context";

export default function NewOpportunity(props){

    const [data, setData] = useState({})
    const [allFields, setAllFields] = useState([]);
    const [allOrgs, setAllOrgs] = useState([]);

    const contextUser = useContext(UserContext)

    useEffect(()=>{
        if(!("id" in data) && props.edit){
            api.getOpportunity(props.id, setData);
        }

        if(allFields.length==0){
        api.getFields({}, setAllFields)
        api.getAllOrganizationNames(setAllOrgs)
        }
    }, [data])

    function handleSubmit(e){
        e.preventDefault();

        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);
        
        let benifits = [];
        document.querySelectorAll(` .benifits-list li textarea`).forEach(x => {
            benifits.push(x.value);
        });

        formProps.benifits = benifits;
        formProps.field_id = selectedField;
        formProps.org_id = selectedOrg;
        
        console.log(formProps)
        props.edit?api.editOpportunity(props.id, formProps, ()=>{window.location="/opportunities"}):api.addOpportunity(contextUser, formProps, ()=>{window.location="/opportunities"});
    
    
    }

    const [selectedField, setSelectedField] = useState(data.field_id);
    const [selectedOrg, setSelectedOrg] = useState(data.org_id);

    useEffect(()=>{
        setSelectedField(data.field_id)
        setSelectedOrg(data.org_id)
    }, [data])

    function onFieldsSelectChange(val, type){
        if(type.action == 'select-option'){
            setSelectedField(val.value);
        }
    }

    function onOrgsSelectChange(val, type){

        if(type.action == 'select-option'){
            setSelectedOrg(val.value);
        }
    }


    console.log(allOrgs.filter(x=> x.org_id == data.org_id))
    return (
        <form id="new-field" className="add-entity-form" onSubmit={handleSubmit}>
            {props.edit?<h1>Edit Opportunity</h1>:<h1>New Opportunity</h1>}
            <label>Name</label>
            <input type="text" name='name' placeholder="Opportunity Name" required defaultValue={data.name}></input>
            <label>Description</label>
            <textarea name="description"  placeholder="Opportunity description ... " defaultValue={data.description}>
            </textarea>
            <label>Field</label>
            {!props.edit || data.field_id ?<Select
                    options={allFields.map(x=>{return {value: x.id, label:x.name}})}
                    onChange={onFieldsSelectChange}
                    defaultValue={allFields.filter(x=> x.id == data.field_id).map(x=>{return {value: x.id, label:x.name}})[0]}
                    required
                    placeholder={"Fields"} />:null}
            <label>Organization</label>
            {!props.edit || data.org_id?<Select
                    options={allOrgs.map(x=>{return {value: x.org_id, label:x.org_name}})}
                    onChange={onOrgsSelectChange}
                    defaultValue={allOrgs.filter(x=> x.org_id == data.org_id).map(x=>{return {value: x.org_id, label:x.org_name}})[0]}
                    required
                    placeholder={"Organizations"} />:null}
            <label>Location</label>
            <input type="text" name='location' required placeholder="Opportunity Location"  defaultValue={data.location}></input>
            <label>Application portal</label>
            <input type="url" name='portal' placeholder="Opportunity Portal" required defaultValue={data.portal}></input>
            
            <label>Start Date</label>
            <input type="date" name='start_date' required  placeholder="Start Date" defaultValue={data.start_date}></input >
            <label>End Date</label>
            <input type="date" name='end_date' required placeholder="End Date" defaultValue={data.end_date}></input >
            <label>Application Deadline</label>
            <input type="date" name='deadline_date' required placeholder="Deadline Date" defaultValue={data.deadline_date}></input >
            
            <label>Compensation ($)</label>
            <input type="number" name='compensation' required placeholder="Compensation" defaultValue={data.compensation}></input >
            <label>Compensation type</label>
            {data.compensation_type || !props.edit?<select name="compensation_type" required defaultValue={data.compensation_type}>
                <option value='monthly' >
                    Monthly
                </option>
                <option value='final'>
                    One time Payement
                </option>
                <option value='hourly'>
                    Hourly
                </option>
                <option value='task'>
                    Per task
                </option>
            </select>:null}
            <label>Additional Benifits</label>
            <InlineListItems className={"benifits-list"} items={data.benifits?data.benifits: []} edit={true} />
            {props.edit?<button type="submit">Save</button>:<button type="submit">Add Opportunity</button>}
        </form>
    )
}