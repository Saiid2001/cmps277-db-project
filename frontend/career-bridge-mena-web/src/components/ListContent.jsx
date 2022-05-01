import React, { useEffect, useState, useContext } from "react";
import { UserContext } from "../Context";

export function ListContent(props) {
    //api_request
    //new record
    // className
    // child record type RecordType

    const contextUser = useContext(UserContext);

    const [data, setData] = useState([]);

    const [loaded, setLoaded] = useState(false);

    useEffect(() => {

        if (!loaded) {
            props.api_request(contextUser, setData);
            setLoaded(true);
        }
    });

    function deleteRecord(i) {
        let d = [...data];
         
        d.splice(i, 1);
        setData(d);
    }

    function addRecord() {
        let d = [...data];
        d.push(props.new_record);
        setData(d);
    }

    return <section className={props.className}>
        <div>
            {data.map((x, i) => <props.RecordType key={i} id={i} data={x} isNew={x.type == "new"} onDelete={() => deleteRecord(i)}></props.RecordType>)}

            <button className="button" onClick={addRecord}>Add</button>
        </div>

    </section>;
}
