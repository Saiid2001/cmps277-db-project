import React, { useState, cloneElement } from "react";

export function Card(props) {


    const [isEditing, setIsEditing] = useState(false);
    const [shouldSave, setShouldSave] = useState(false);

    function editChildren() {

        setShouldSave(false);
        setIsEditing(true);
    }

    function cancelChildren() {
        setShouldSave(false);
        setIsEditing(false);
    }

    function saveChildren() {
        setShouldSave(true);
        setIsEditing(false);
    }
    return <section className={props.className}>
        <h2>{props.title}</h2>
        <div className="content">
            {props.children?(
                props.children.length?(
                    props.children.map(
                        (child, i) => cloneElement(
                            child, { key: i, edit: isEditing, save: shouldSave }
                            )
                        )
                        ):cloneElement(
                            props.children, { key: 0, edit: isEditing, save: shouldSave }
                            )
                        ):null}
        </div>
        {props.editButton != false ? <div className="buttons">
            {!props.no_edit && !isEditing ? <button onClick={editChildren}>Edit</button> : null}
            {!props.no_edit && isEditing ? <button onClick={saveChildren}>Save</button> : null}
            {!props.no_edit && isEditing ? <button onClick={cancelChildren}>Cancel</button> : null}
        </div> : null}

    </section>;
}
