import { useContext, useEffect, useState } from "react";
import api from "../../../../api";
import { Card } from "../../../../components/Card";
import { TypeContext, UserContext } from "../../../../Context";
import sort_icn from "../../../../assets/img/sort.svg";
import search_icn from "../../../../assets/img/search.svg";
import { useSearchParams } from "react-router-dom";
import { ListView } from "../../../../components/ListView";


let query = {};

export default function Organizations(props){
    const contextUser = useContext(UserContext);
    const userType = useContext(TypeContext);

    const [data, setData] = useState([]);
    const [loaded, setLoaded] = useState(false);

    const [searchParams, setSearchParams] = useSearchParams();

    

    function search(){
        console.log(query)
        api.getOrganizations(query, setData);
    }

    useEffect(() => {
        if (!loaded) {

            query = {
                name: searchParams.get("query"), 
            }

            api.getOrganizations(query, setData);
            setLoaded(true);
        }
    });

    function handleSearchSubmit(e){

        e.preventDefault();
        const searchP = e.target.querySelector("[type='text']").value;

        query.name=searchP;
        search();

    }

    return <div id="organizations-tab" className="tab">

        <div className="floating-header">
            {userType==api.USER_TYPES.Mentor?<button onClick={()=>window.location="/organizations/add"}>Add Organization</button>:null}
            <form onSubmit={handleSearchSubmit}>
                <input type="text" placeholder="Search organizations..."></input>
                <button type="submit"><img src={search_icn} height="12px"/></button>
            </form>
        </div>

        <Card title="Organizations" editButton={false}>
            <ListView
            
            data={data}
            search= {search}
            query = {query}
            sort_fields = {
                [
                    {label: "name", value: "name"},
                    {label: "seekers", value: "seekers"},
                    {label: "opportunities", value: "opp"},
                ]
            }
            ListItemTemplate = {OrganizationListItem}
            >

            </ListView>
            <div></div>
        </Card>
</div>
}

function OrganizationListItem(props){

    const contextUser = useContext(UserContext);
    const userType = useContext(TypeContext);

    function _edit(){

        window.location = "/organizations/edit?id="+props.data.id;
    }

    function _delete(){
        api.deleteOrganization(props.data.id, ()=>{window.location.reload(false);});
        
    }

    return <div className="list-item">
        <div>
        <h1><a href={"/organizations/details/"+props.data.id}>{props.data.name}</a></h1>
        {userType==api.USER_TYPES.Mentor? <button className="delete" onClick={_delete}>delete</button>:null}
        {userType==api.USER_TYPES.Mentor? <button className="delete" onClick={_edit}>edit</button>:null}
        </div>
        <div className="counts">
        <div className="card-count">
            <p>{props.data.n_opportunities}</p>
            <label>Opportunities</label>
            </div>
            <div className="card-count">
            <p>{props.data.n_opportunities}</p>
            <label>Mentors</label>
            </div>
        </div>
    </div>
}


