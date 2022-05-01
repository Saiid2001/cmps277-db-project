import sort_icn from "../assets/img/sort.svg";

export function ListView(props) {


    function toggleSortBy(key) {
        props.query.sort_by != key ? props.query.sort_by = key : props.query.sort_by = null;
        props.search(props.query);
    }

     
    return (
        <div className="list-view">
            <header>
                {props.sort_fields.map(field => {
                    return <button key={"button-sort-" + field.value} onClick={() => toggleSortBy(field.value)}><img src={sort_icn} width="12px"></img> {field.label}</button>;
                })}
            </header>
            <div className="list-container">
                {props.data ? props.data.map(x => <props.ListItemTemplate data={x}></props.ListItemTemplate>) : null}
            </div>
        </div>
    );
}
