import { useContext, useEffect, useState } from "react";
import api from "../../../../api";
import { Card } from "../../../../components/Card";
import { TypeContext, UserContext } from "../../../../Context";
import sort_icn from "../../../../assets/img/sort.svg";
import search_icn from "../../../../assets/img/search.svg";
import { useSearchParams } from "react-router-dom";
import { ListView } from "../../../../components/ListView";

export let query = {}

export default function Fields(props){

    const contextUser = useContext(UserContext);
    const userType = useContext(TypeContext);

    const [data, setData] = useState([]);
    const [loaded, setLoaded] = useState(false);

    const [searchParams, setSearchParams] = useSearchParams();

    

    function search(){
        console.log(query)
        api.getFields(query, setData);
    }

    useEffect(() => {
        if (!loaded) {

            query = {
                name: searchParams.get("query"), 
                sort_by: searchParams.get("sort")
            }

            api.getFields(query, setData);
            setLoaded(true);
        }
    });

    function handleSearchSubmit(e){

        e.preventDefault();
        const searchP = e.target.querySelector("[type='text']").value;

        query.name=searchP;
        search();

    }


    return <div id="fields-tab" className="tab">

        <div className="floating-header">
            {userType==api.USER_TYPES.Mentor?<button onClick={()=>window.location="/fields/add"}>Add Field</button>:null}
            <form onSubmit={handleSearchSubmit}>
                <input type="text" placeholder="Search fields..."></input>
                <button type="submit"><img src={search_icn} height="12px"/></button>
            </form>
        </div>

    {userType==api.USER_TYPES.Seeker?<Card title="Your Followed Fields" editButton={false}>
            <FollowedFieldsContent></FollowedFieldsContent>
            <div></div>
        </Card>:null}

        <Card title="All Fields" editButton={false}>
            <ListView 
            data={data} 
            search = {search}
            query = {query}
            sort_fields = {
                [
                    {label: "name", value: "name"},
                    {label: "seekers", value: "seekers"},
                    {label: "opportunities", value: "opp"},
                ]
            }
            ListItemTemplate = {FieldListItem}
            ></ListView>
            <div></div>
        </Card>
</div>

}


function FollowedFieldsContent(props){


    const contextUser = useContext(UserContext);
    const [data, setData] = useState([]);

    useEffect(() => {
        if (!("n_fields" in data)) {
            api.getFollowedFields(contextUser, setData);
        }
    });


    return (
        <div className='followed-fields'>

            <div className="card-count">
            <label>Fields</label>
            <p>{data.length}</p>
            </div>

        <div className="cards-view">
            {data? data.map(x=><FieldCard key={"field-"+x.id} data={x}></FieldCard>):null}
        </div>
        </div>

    )

}

function FieldCard(props){

    const contextUser = useContext(UserContext);

    function unfollow(){
        api.unfollowField(contextUser,props.data.id, ()=>{window.location.reload(false);});
        
    }

    return (
        <div className="field-card" id={"field-"+props.id}>
            <h3>{props.data.name}</h3>
            <button className="unfollow" onClick={unfollow}>unfollow</button>
            <div className="card-count">
            <p>{props.data.n_seekers}</p>
            <label>Seekers</label>
            </div>
            <div className="card-count">
            <p>{props.data.n_opportunities}</p>
            <label>Opportunities</label>
            </div>
        </div>
    )
}

function FieldListItem(props){

    const contextUser = useContext(UserContext);
    const userType = useContext(TypeContext);

    function unfollow(){
        api.unfollowField(contextUser,props.data.id, ()=>{window.location.reload(false);});
        
    }

    function follow(){
        api.followField(contextUser,props.data.id, ()=>{window.location.reload(false);});
        
    }

    function editField(){

        window.location = "/fields/edit?id="+props.data.id;
    }

    function deleteField(){
        api.deleteField(props.data.id, ()=>{window.location.reload(false);});
        
    }

    return (
        <div className="list-item">
        <div className="text-content">
        <h3>{props.data.name}</h3>
        {userType==api.USER_TYPES.Seeker? props.data.followed?<button className="unfollow" onClick={unfollow}>unfollow</button>:<button className="unfollow" onClick={follow}>follow</button>:null}
        {userType==api.USER_TYPES.Mentor? <button className="delete" onClick={deleteField}>delete</button>:null}
        {userType==api.USER_TYPES.Mentor? <button className="delete" onClick={editField}>edit</button>:null}
        <p>{props.data.description}</p>
        </div>
        <div className="counts">
        <div className="card-count">
            <p>{props.data.n_opportunities}</p>
            <label>Opportunities</label>
            </div>
            <div className="card-count">
            <p>{props.data.n_seekers}</p>
            <label>Seekers</label>
            </div>
            </div>
        </div>
    )

}