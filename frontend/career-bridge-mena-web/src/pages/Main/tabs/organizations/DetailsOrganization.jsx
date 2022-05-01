import { useEffect, useState } from "react";
import api from "../../../../api";
import { Card } from "../../../../components/Card";
import { ListView } from "../../../../components/ListView";
import { OpportunityListItem } from "../opportunities/Opportunities";

export default function DetailsOrganization(props){

    const [data, setData] = useState({})
    const [opps, setOpps] = useState([])
    useEffect(()=>{
        if(!("id" in data)){
            api.getOrganization(props.id, setData);
            api.getOpportunities({
                org_id: data.id
            }, setOpps)
        }
    }, [data])

    return <section className="tab" id="org-detail">
    
    <Card title={data.name} editButton={false}>
        {data.is_educational?<small className="badge">Educational Institution</small>:<div></div>}
        <table>
            <tbody>
            <tr>
                <th>Organization email</th><td><a href={"mailto:"+data.email}>{data.email}</a></td>
            </tr>
            <tr>
                <th>Organization website</th><td><a href={data.website}>{data.website}</a></td>
            </tr>
            <tr>
                <th>Location</th><td>{data.location}</td>
            </tr>
            </tbody>
        </table>

        <div className="stats">
            <div>
            <div className="card-count">
            <p>{data.n_mentors}</p>
            <label>Mentors</label>
            </div>
            <div className="card-count">
            <p>{data.n_opportunities}</p>
            <label>Opportunities</label>
            </div>
            </div>

            <div>
            <div className="card-count">
            <p>{Math.floor(data.min_compensation)+"$"}</p>
            <label>Min $</label>
            </div>
            <div className="card-count">
            <p>{Math.floor(data.avg_compensation)+"$"}</p>
            <label>Av. $</label>
            </div>
            <div className="card-count">
            <p>{Math.floor(data.max_compensation)+"$"}</p>
            <label>Max $</label>
            </div>
            </div>
        </div>
    </Card>

    <Card title={"Related Opportunities"} editButton={false}>
    <ListView 
            data={opps}
            sort_fields = {
                [
                    {label: "Compensation", value: "compensation" },
                    {label: "Seekers", value: "seekers" },
                    {label: "Mentors", value: "mentors" },
                    {label: "Deadline", value: "deadline" },
                ]
            }
            query = {{}}
            search={()=>{}}
            ListItemTemplate = {OpportunityListItem}
            >
            </ListView>
        
    </Card>

    </section>

}