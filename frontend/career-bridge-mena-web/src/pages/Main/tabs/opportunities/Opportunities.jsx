import { useContext, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import api from "../../../../api";
import { Card } from "../../../../components/Card";
import { ListView } from "../../../../components/ListView";
import { TypeContext, UserContext } from "../../../../Context";


import search_icn from "../../../../assets/img/search.svg";
import Select from 'react-select';


let query = {}

export default function Opportunities(props){

    const userType = useContext(TypeContext)
    const userContext = useContext(UserContext)
    
    const [searchParams, setSearchParams] = useSearchParams();
    const [allFields, setAllFields] = useState([]);
    const [allOrgs, setAllOrgs] = useState([]);

    const [data, setData] = useState([])
    const [loaded, setLoaded] = useState(false)
    useEffect(()=>{
        if(!loaded){

            query = {
                name: searchParams.get('query'),
                org_id: searchParams.get('org'),
                field_id: searchParams.get('field'),
                start_after: searchParams.get('s'),
                end_before: searchParams.get('e'),
                open: searchParams.has('open'),
                sort_by: searchParams.get('sort_by')
            }

             
            api.getOpportunities(userContext, query, setData)
            api.getFields({}, (data)=>{ data.push({id:-1,name:"No Field Filter"}); setAllFields(data)})
            api.getAllOrganizationNames((data)=>{ data.push({org_id:-1,org_name:"No Organization Filter"}); setAllOrgs(data)})
            setLoaded(true)
        }
    },[loaded])

    function search(){

         
        api.getOpportunities(userContext, query, setData)
    }

    function handleSearchSubmit(e){

        e.preventDefault();
        const searchP = e.target.querySelector("[type='text']").value;

        query.name=searchP;

        if(selectedField != -1)
            query.field_id = selectedField;
        else
            query.field_id = null;

        if(selectedOrg != -1)
            query.org_id = selectedOrg;
        else
            query.org_id = null;

        query.start_after = document.querySelector("[name='start_after']").value;
        query.end_before = document.querySelector("[name='end_before']").value;

        search();

    }

    const [selectedField, setSelectedField] = useState(null);
    const [selectedOrg, setSelectedOrg] = useState(null);

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

    return <section className="tab" id="opportunities">

        <div className="floating-header">
            {userType==api.USER_TYPES.Mentor?<button onClick={()=>window.location="/opportunities/add"}>Add Opportunity</button>:null}
            <form onSubmit={handleSearchSubmit}>
                <input type="text" placeholder="Search fields..."></input>
                <button type="submit"><img src={search_icn} height="12px"/></button>
            </form>
        </div>

        <div className="floating-header">

            <div>
            <label>Starts before</label>
            <input type={"date"}  name="start_after"/>
            </div>

            <div>
            <label>Ends after</label>
            <input type={"date"}  name="end_before"/>
            </div>

            <Select
                    options={allFields.map(x=>{return {value: x.id, label:x.name}})}
                    onChange={onFieldsSelectChange}
                    placeholder={"Fields"} />
            <Select
                    options={allOrgs.map(x=>{return {value: x.org_id, label:x.org_name}})}
                    onChange={onOrgsSelectChange}
                    placeholder={"Organizations"} />

        </div>
        <Card title = "Your Opportunities" className={"summary"} editButton={false}>
        {userType == api.USER_TYPES.Mentor?<PostedOpportunities/>:<AppliedOpportunities/>}
        {userType == api.USER_TYPES.Mentor?<AssociatedOpportunities/>:<MatchedMentorOpportunities/>}
        {userType == api.USER_TYPES.Mentor?<MatchedSeekerOpportunities/>:<div></div>}
        </Card>

        <Card title = "All Opportunities" editButton={false}>
        <ListView 
            data={data}
            sort_fields = {
                [
                    {label: "Compensation", value: "compensation" },
                    {label: "Seekers", value: "seekers" },
                    {label: "Mentors", value: "mentors" },
                    {label: "Deadline", value: "deadline" },
                ]
            }
            query = {query}
            search={search}
            ListItemTemplate = {OpportunityListItem}
            ></ListView>
        </Card>
    </section>
}

function PostedOpportunities(props){

    const [data, setData] = useState([])
    const [loaded, setLoaded] = useState(false)

    const userContext = useContext(UserContext);
     

    useEffect(() => {
        if (!loaded) {
            api.getPostedOpportunities(userContext, setData);
            setLoaded(true);
        }
    });


    return <div class="list-group">
        <h3>Posted</h3>
        <ListView 
            data={data.map(x=> {return {...x, type:"posted"}})}
            sort_fields = {
                []
            }
            ListItemTemplate = {SummaryOpportunityListItem}
            ></ListView>
    </div>

}

function AssociatedOpportunities(props){
    
    const [data, setData] = useState([])
    const [loaded, setLoaded] = useState(false)

    const userContext = useContext(UserContext);
     

    useEffect(() => {
        if (!loaded) {
            api.getAssociatedOpportunities(userContext, setData);
            setLoaded(true);
        }
    });


    return <div class="list-group">
        <h3>Associated</h3>
        <ListView 
            data={data.map(x=> {return {...x, type:"associated"}})}
            sort_fields = {
                []
            }
            ListItemTemplate = {SummaryOpportunityListItem}
            ></ListView>
    </div>


}

function MatchedSeekerOpportunities(props){
    
    const [data, setData] = useState([])
    const [loaded, setLoaded] = useState(false)

    const userContext = useContext(UserContext);
     

    useEffect(() => {
        if (!loaded) {
            api.getMatchedSeekerOpportunities(userContext, setData);
            setLoaded(true);
        }
    });


    return <div class="list-group">
        <h3>Matched</h3>
        <ListView 
            data={data.map(x=> {return {...x, type:"matched"}})}
            sort_fields = {
                []
            }
            ListItemTemplate = {SummaryOpportunityListItem}
            ></ListView>
    </div>



}

function AppliedOpportunities(props){
    
    const [data, setData] = useState([])
    const [loaded, setLoaded] = useState(false)

    const userContext = useContext(UserContext);
    useEffect(() => {
        if (!loaded) {
            api.getAppliedOpportunities(userContext, setData);
            setLoaded(true);
        }
    });


    return <div class="list-group">
        <h3>Pending</h3>
        <ListView 
            data={data.map(x=> {return {...x, type:"applied"}})}
            sort_fields = {
                []
            }
            ListItemTemplate = {SummaryOpportunityListItem}
            ></ListView>
    </div>

}

function MatchedMentorOpportunities(props){

    const [data, setData] = useState([])
    const [loaded, setLoaded] = useState(false)

    const userContext = useContext(UserContext);
     

    useEffect(() => {
        if (!loaded) {
            api.getMatchedMentorOpportunities(userContext, setData);
            setLoaded(true);
        }
    });


    return <div class="list-group">
        <h3>Matched</h3>
        <ListView 
            data={data.map(x=> {return {...x, type:"matched"}})}
            sort_fields = {
                []
            }
            ListItemTemplate = {SummaryOpportunityListItem}
            ></ListView>
    </div>

}


function SummaryOpportunityListItem(props){

    const userContext = useContext(UserContext);
    const userType = useContext(TypeContext);
    function _delete(){

        api.deleteOpportunity(props.data.id, ()=>{window.location.reload()})

    }

    function _edit(){
        window.location = "/opportunities/edit?id="+props.data.id;
    }

    function _cancel(){
        api.cancelApplyToOpportunity(useContext, props.data.id, ()=>window.location.reload())
    }

    function _dessociate(){
        api.dessociateOpportunity(useContext, props.data.id, ()=>window.location.reload())
    
    }

    function _unmatch(){

        let mentor, seeker;
        if(userType == api.USER_TYPES.Mentor){
            mentor = userContext;
            seeker = props.data.seeker_id;
        }
        else{
            mentor = props.data.mentor_id;
            seeker = userContext;
        }
        api.unmatchMentoring(mentor, seeker, props.data.id, ()=>window.location.reload())
    
    }

    function _message(){

        const other = props.data.seeker_id? props.data.seeker_id: props.data.mentor_id;
        window.dispatchEvent(new CustomEvent("open-messages", {detail:{other: other}}))
    }

    return <div className="list-item">

        <div className="upper">

        <div>
        <h3 onMouseUp={()=>window.location = "/opportunities/details/"+props.data.id}>{props.data.name}</h3>
        {props.data.type=="posted"?<button onClick={_delete}>Remove</button>:null}
        {props.data.type=="posted"?<button onClick={_edit}>Edit</button>:null}
        {props.data.type=="associated"?<button onClick={_dessociate}>Unlink</button>:null}
        {props.data.type=="matched"?<button onClick={_unmatch}>Unmatch</button>:null}
        {props.data.type=="applied"?<button onClick={_cancel}>Cancel</button>:null}
        </div>
        <div className="info">
            <a href={"/organizations/details/"+props.data.org_id}>{props.data.org_name}</a>
            <a href={"/users/details/"+props.data.poster_id}>{props.data.poster_name}</a>
            <small>closes in {props.data.deadline_date}</small>
        </div>
        {props.data.n_mentors?<div className="stats">
            <div className="card-count">
            <p>{props.data.n_mentors}</p>
            <label>Mentors</label>
            </div>
            <div className="card-count">
            <p>{props.data.n_seekers}</p>
            <label>Seekers</label>
            </div>
        </div>:null}

        {props.data.seeker_name?(
            <div className="contact">
            <small>Seeker</small>
            <a href={"/seekers/details/"+props.data.seeker_id}>{props.data.seeker_name}</a>
            <button onClick={_message}>Message</button>
            </div>
            
        ):null}

        {props.data.mentor_name?(
            <div className="contact">
            <small>Mentor</small>
            <a href={"/users/details/"+props.data.mentor_id}>{props.data.mentor_name}</a>
            <button onClick={_message}>Message</button>
            </div>
        ):null}
        
        </div >
            
        <div className="extra">
            {props.children}
        </div>

    </div>
}


export function OpportunityListItem(props){

    
    const userType = useContext(TypeContext);
    const userContext = useContext(UserContext);

    function _apply(){
        api.applyToOpportunity(useContext, props.data.id, ()=>window.location.reload())
   
    }

    function _associate(){
        api.associateOpportunity(useContext, props.data.id, ()=>window.location.reload())

    }


    return <SummaryOpportunityListItem data={props.data}>
        <div>
            <label>Starts</label>
            <small>{props.data.start_date}</small>
        </div>
        <div>
            <label>Ends</label>
            <small>{props.data.end_date}</small>
        </div>
        <div>
            <label>Deadline</label>
            <small>{props.data.deadline_date}</small>
        </div>
        <div>
            <label>Compensation</label>
            <small>{props.data.compensation + "$ "+ props.data.compensation_type}</small>
        </div>
        {userType == api.USER_TYPES.Seeker?<button onClick={_apply}>Request Mentor</button>:<button onClick={_associate}>Associate</button>}
    </SummaryOpportunityListItem>
}