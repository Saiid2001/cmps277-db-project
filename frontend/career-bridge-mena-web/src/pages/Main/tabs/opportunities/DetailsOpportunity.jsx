import { useContext, useEffect, useState } from "react";
import api from "../../../../api";
import { Card } from "../../../../components/Card";
import { ListView } from "../../../../components/ListView";
import { TypeContext, UserContext } from "../../../../Context";
import { UserListItem, UserListItemBuilder } from "../profile/Users";
import Rating from "react-rating";

const comp_type_label = {
    monthly: "/mo",
    task: "per task",
    final: "total sum",
    hourly: "/hr"
}
export default function DetailsOpportunity(props){

    const [data, setData] = useState({})
    const [rel, setRel] = useState({})
    const [mentors, setMentors] = useState(null)
    const [rating, setRating] = useState(null)
    
    const userType = useContext(TypeContext);
    const userContext = useContext(UserContext);

    useEffect(()=>{
        if(!("id" in data)){
            api.getOpportunity(props.id, setData);
            api.getOpportunityRelation(userContext, props.id,setRel)
            api.getMentors(props.id, setMentors)

            window.addEventListener('finish-mentoring', e=>{
                setRating(e.detail.mentor)
            })
        }
    }, [data])

    function _delete(){

        api.deleteOpportunity(data.id, ()=>{window.location="/opportunities/"})

    }

    function _edit(){
        window.location = "/opportunities/edit?id="+data.id;
    }

    function _cancel(){
        api.cancelApplyToOpportunity(useContext, data.id, ()=>window.location.reload())
    }

    function _dessociate(){
        api.dessociateOpportunity(useContext, data.id, ()=>window.location.reload())
    
    }

    function _unmatch(){

        let mentor, seeker;
        if(userType == api.USER_TYPES.Mentor){
            mentor = userContext;
            seeker = rel.uid;
        }
        else{
            mentor = data.mentor_id;
            seeker = userContext;
        }
        api.unmatchMentoring(mentor, seeker, data.id, ()=>window.location.reload())
    
    }

    function _message(){

        const other = props.data.seeker_id? props.data.seeker_id: props.data.mentor_id;
        window.dispatchEvent(new CustomEvent("open-messages", {detail:{other: other}}))
    }

    function _apply(){
        api.applyToOpportunity(useContext,data.id, ()=>window.location.reload())
   
    }

    function _associate(){
        api.associateOpportunity(useContext, data.id, ()=>window.location.reload())

    }

    return <section className="tab" id="opp-detail">
    
    <Card title={data.name} editButton={false}>

        <div className="post-date">
            {data.deadline_date}
        </div>
        
        <div className="buttons">
        <div className="card-count seekers">
        <p>{data.n_seekers}</p>
        <label>Seekers</label>
        </div>
        {rel.rel=="poster"?<button onClick={_delete}>Remove</button>:null}
        {rel.rel=="poster"?<button onClick={_edit}>Edit</button>:null}
        {rel.rel=="associated"?<button onClick={_dessociate}>Unlink</button>:null}
        {rel.rel=="applied"?<button onClick={_cancel}>Cancel</button>:null}
        {rel.rel=="no_rel" && userType == api.USER_TYPES.Mentor?<button onClick={_associate}>Associate</button>:null}
        {rel.rel=="no_rel" && userType == api.USER_TYPES.Seeker?<button onClick={_apply}>Request Mentor</button>:null}
        </div>
        
        
        

        <div className="links">
            <a href={"/organizations/details/"+data.org_id}>{data.org_name}</a>
            <a href={"/fields?query="+data.field_name}>{data.field_name}</a>
            <a href={"/users/details/"+data.poster_id}>Posted by {data.poster_name}</a>
        </div>


        <div className="middle">
        <p className="description">
            {data.description}
        </p>

        <div className="mentor-group">
            <div className="card-count">
            
            <label>Mentors</label>
            <p>{data.n_mentors}</p>
            </div>

            <div className="mentor-list">
                <ul>
                {mentors?mentors.map(x=><li><a href={"/users/details/"+x.id}>{x.name}</a></li>):null}
                </ul>
            </div>
        </div>

        </div>

        <div className="stats">
            <div className="card-count">
            <label>Start date</label>
            <p>{data.start_date}</p>
            </div>
            <div className="card-count">
            <label>End date</label>
            <p>{data.end_date}</p>
            </div>
            <div className="card-count">
            <label>Deadline</label>
            <p>{data.deadline_date}</p>
            </div>
            <div className="card-count">
            <label>Location</label>
            <p>{data.location}</p>
            </div>
        </div>
        <div className="stats">
            <div className="card-count">
            <label>Compensation</label>
            <p>{data.compensation+"$ "+comp_type_label[data.compensation_type]}</p>
            </div>
            <div className="card-count">
            <label>Application Portal</label>
            <p><button onClick={()=>window.location= data.portal}>Click here to go to portal</button></p>
            </div>
        </div>

        <div className="stats">
            <div className="card-count">
            <label>Additional Benifits</label>
            <ul>
                {data.benifits?data.benifits.map(x=><li>{x}</li>):null}
            </ul>
            </div>
        </div>
    </Card>



    {userType == api.USER_TYPES.Mentor?
    <Card title={"Applicants"} editButton={false}>
        <MentoringStudents></MentoringStudents>
        <AllStudents></AllStudents>
    </Card>:null}

    {userType == api.USER_TYPES.Seeker?
    <Card title={"Mentors"} editButton={false}>
        <MentoringMentors></MentoringMentors>
        <AllMentors></AllMentors>
    </Card>:null}


    {rating? <RatingPopup data = {{m_id: rating, oppid: data.id, s_id: userContext}}></RatingPopup>:null}

    </section>


}

function RatingPopup(props){

    const [data, setData] = useState({});

    useEffect(()=>{
        if(!("first_name" in data)){
            api.getUser(props.data.m_id, setData);
        }
    }, [data])

    function _finish(rating){

        api.finishMentoring(props.data.m_id, props.data.s_id, props.data.oppid , rating, ()=>window.location.reload())
    }

    return <section id="rating-popup">
        <h2>Rate {data.first_name+" "+data.last_name} Before finishing</h2>
        <Rating onChange={_finish} ></Rating>
    </section>
}

function MentoringStudents(props){

    const [data, setData] = useState(null)
    
    const userType = useContext(TypeContext);
    const userContext = useContext(UserContext);

    useEffect(()=>{
        if(!(data)){
            api.getMentoredSeekers(userContext, props.id, setData);
        }
    }, [data])


    function _remove(id){
        api.unmatchMentoring(userContext, id, props.id, ()=>window.location.reload());
    }

    function _message(id){
        window.dispatchEvent(new CustomEvent("open-messages", {detail:{other: id}}))
    }

    

    const userActions = [
        {
            label: "Message",
            callback: _message
        },
        {
            label: "Remove",
            callback: _remove
        }
    ]


    if(data && data.length){
    return <section>
        <h3>Your Applicants</h3>
    {data? <ListView 
        data={data}
        sort_fields = {
            []
        }
        ListItemTemplate = {(props)=>UserListItem(props, userActions)}
            ></ListView>:null}
        </section>

    }
    return null
}


function AllStudents(props){

    const [data, setData] = useState(null)
    
    const userType = useContext(TypeContext);
    const userContext = useContext(UserContext);

    useEffect(()=>{
        if(!(data)){
            api.getSeekers(props.id, {pending: true},  setData);
        }
    }, [data])


    function _mentor(id){
        api.matchMentoring(userContext, id, props.id, ()=>window.location.reload());
    }

    

    

    const userActions = [
        {
            label: "Mentor",
            callback: _mentor
        }
    ]

    
    if(data && data.length){
    return <section>
        <h3>All Applicants</h3>
    {data? <ListView 
        data={data}
        sort_fields = {
            []
        }
        ListItemTemplate = {(props)=>UserListItem(props, userActions)}
            ></ListView>:null}
        </section>

    }
    return null
}

function MentoringMentors(props){

    const [data, setData] = useState(null)
    
    const userType = useContext(TypeContext);
    const userContext = useContext(UserContext);

    useEffect(()=>{
        if(!(data)){
            api.getMentoringMentors(props.id, {pending: true},  setData);
        }
    }, [data])

    function _message(){

        const other = props.data.seeker_id? props.data.seeker_id: props.data.mentor_id;
        window.dispatchEvent(new CustomEvent("open-messages", {detail:{other: other}}))
    }

    function _finish(id){
        window.dispatchEvent(new CustomEvent('finish-mentoring', {detail:{mentor: id}}))
    }

    const userActions = [
        {
            label: "Message",
            callback: _message,
            
        },
        {
            label:"Finish",
            callback: _finish
        }
    ]

    if(data && data.length){
    return <section>
        <h3>Your Mentor</h3>
    {data? <ListView 
        data={data}
        sort_fields = {
            []
        }
        ListItemTemplate = {(props)=>UserListItem(props, userActions)}
            ></ListView>:null}
        </section>

    }
    return null
}


function AllMentors(props){

    const [data, setData] = useState(null)
    
    const userType = useContext(TypeContext);
    const userContext = useContext(UserContext);

    useEffect(()=>{
        if(!(data)){
            api.getMentors(props.id,  setData);
        }
    }, [data])

    function _message(){

        const other = props.data.seeker_id? props.data.seeker_id: props.data.mentor_id;
        window.dispatchEvent(new CustomEvent("open-messages", {detail:{other: other}}))
    }

    const userActions = [
        {
            label: "Message",
            callback: _message,
            
        }
    ]

    if(data && data.length){
    return <section>
        <h3>All Mentors</h3>
    {data? <ListView 
        data={data}
        sort_fields = {
            []
        }
        ListItemTemplate = {(props)=>UserListItem(props, userActions)}
            ></ListView>:null}
        </section>

    }
    return null
}



