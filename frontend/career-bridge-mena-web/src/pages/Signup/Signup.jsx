import logo_sm from "../../assets/img/logo_sm.svg"
import bg_img from "../../assets/img/ppl-flag.png"
import "./Signup.scss"

export default function Signup(props){

    return <div className="signup">

        <img src={logo_sm} class="logo" ></img>
        <img src={bg_img} class="bg-img"></img>

        <main>
            <h1>Create your Account</h1>
            
            <form>
            <section >
                <h2>Credentials</h2>
                    <input type={"email"} name={"email"} placeholder={"Email"} required></input>
                    <input type={"password"} name={"password"} placeholder={"Password"} required></input>
                    
            </section>
            <section >
                <h2>Basic Info</h2>
                    <input type={"text"} name={"first_name"} placeholder={"First Name"} required></input>
                    <input type={"text"} name={"last_name"} placeholder={"Last Name"} required></input>
                    <label for="birth_date">Birth-date</label>
                    <input type={"date"} id="birth_date" name={"birth_date"} placeholder={"Birth date"} required></input>
                    <div className="gender">
                        <input type="radio" id = "gender-m" name="gender" value="M"></input>
                        <label for="gender-m">Male</label>
                        <input type="radio" id = "gender-f" name="gender" value="F"></input>
                        <label for="gender-m">Female</label>
                    </div>
            </section>
            <section >
                <h2>Additional Info</h2>
                    <input type={"url"} name={"linkedin"} placeholder={"LinkedIn URL"} ></input>
                    <input type={"url"} name={"website"} placeholder={"Website"} ></input>
                    <input type={"tel"} name="phone" placeholder="Phone Number" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"></input>
                    
            </section>
            <input type={"submit"} value="Create Account"/>
            </form>
        </main>

    </div>

}