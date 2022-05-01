import api from '../../api';
import guy_star_img from '../../assets/img/guy-star.svg'
import logo from "../../assets/img/logo.svg"
import style from "./Login.scss"

export default function Login(props){


    function handleSubmit(e){
        e.preventDefault();

        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);
        api.login(formProps.email, formProps.password, u=>props.onLogin(u));
    }
    return <div className='content login'>
        <main>
            <img src={logo} alt="logo"></img>
            <section className="login-section">
                <h2>Login to your account</h2>
                <form onSubmit={handleSubmit}>
                    <input type={"email"} name={"email"} placeholder={"Email"} required></input>
                    <input type={"password"} name={"password"} placeholder={"Password"} required></input>
                    <input type={"submit"} value="Log in"/>
                </form>
            </section>

            <section className="signup-section">
                <h2>New to our site? </h2>
                <div>
                    <button onClick = {()=>window.location = "/signup/seeker" }>

                        Join as a Seeker
                    </button>
                    <button onClick = {()=>window.location = "/signup/mentor" }>
                        Join as a Mentor
                    </button>
                </div>
            </section>
        </main>
        <img className="background-img" src={guy_star_img}></img>
    </div>
}