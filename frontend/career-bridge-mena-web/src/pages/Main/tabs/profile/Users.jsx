import { useContext, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import api from "../../../../api";
import { TypeContext, UserContext } from "../../../../Context";

import search_icn from "../../../../assets/img/search.svg";
import { Card } from "../../../../components/Card";
import { ListView } from "../../../../components/ListView";

export function UserListItem(props, actions){
    return <div className="list-item">
        {props.data?<a href={"/users/details/"+props.data.id}>{props.data.name}</a>:null}
        <div>{actions.map(act=><button onClick={()=>act.callback(props.data.id)}>{act.label}</button>)}</div>
    </div>
}

let query = {}

export default function Users(props){

    const contextUser = useContext(UserContext);
    const userType = useContext(TypeContext);

    const [data, setData] = useState([]);
    const [loaded, setLoaded] = useState(false);

    const [searchParams, setSearchParams] = useSearchParams();

    

    function search(){
         
        api.getUsers(query, setData);
    }

    useEffect(() => {
        if (!loaded) {

            query = {
                name: searchParams.get("query"), 
                type: searchParams.get("type")
            }

            api.getUsers(query, setData);
            setLoaded(true);
        }
    });

    function handleSearchSubmit(e){

        e.preventDefault();
        const searchP = e.target.querySelector("[type='text']").value;

        query.name=searchP;
        search();

    }

    function _message(id){
        window.dispatchEvent(new CustomEvent("open-messages", {detail:{other: id}}))
    }

    let userActions = [
        {
            label: "Message",
            callback: _message
        }
    ]

    if(userType == api.USER_TYPES.Mentor){

    }

    return <div id="users-tab" className="tab">

        <div className="floating-header">
            <form onSubmit={handleSearchSubmit}>
                <input type="text" placeholder="Search Users..."></input>
                <button type="submit"><img src={search_icn} height="12px"/></button>
            </form>
        </div>

        <Card title="Users" editButton={false}>
            <ListView
            
            data={data}
            search= {search}
            query = {query}
            sort_fields = {
                [
                ]
            }
            ListItemTemplate = {(props)=>UserListItem(props, userActions)}
            >

            </ListView>
            <div></div>
        </Card>
</div>


}

