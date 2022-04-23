import React, { useEffect, useState } from "react";

export function InlineListItems(props) {
    //accomplishments -> props.items
    //isEditing -> props.edit
    //className

    const [items, setItems] = useState(props.items);

    useEffect(()=>{
        setItems(props.items)
    },[props.items])

    function removeOption(i) {
        let d = [...items];
        d.splice(i, 1);
        setItems(d);
    }
    function addOption() {
        let d = [...items];
        d.push("");
        setItems(d);
    }

    return <ul className={props.className}>
        {items.map((x, i) => <li><textarea key={i} type={"text"} placeholder={"New entry"} required {...!props.edit ? { "disabled": true } : ""} defaultValue={x}></textarea>{props.edit ? <button onClick={() => removeOption(i)}>Remove</button> : null}</li>)}
        {props.edit ? <li><button onClick={addOption}>Add item</button></li> : null}
    </ul>;

}
