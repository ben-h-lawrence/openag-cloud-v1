import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import {Link} from "react-router-dom";

class login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: ''
        };
        // This binding is necessary to make `this` work in the callback
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
        event.preventDefault();
    }

    handleSubmit(event) {

        alert('A login form was submitted: ' + this.state);
        event.preventDefault();
    }


    render() {

        return (
            <div className="login-page">
                <div className="form">
                    <div className="image-section">
                        <img className="logo" src={logo}></img>
                    </div>
                    <form className="login-form" onSubmit={this.handleSubmit}>
                        <input type="text" placeholder="username" name="username" value={this.state.username}
                               onChange={this.handleChange}/>
                        <input type="password" placeholder="password" name="password" value={this.state.password}
                               onChange={this.handleChange}/>
                        <button>login</button>

                        <p className="message">Not registered? <Link to="signup"> Create an account </Link> </p>
                </form>
            </div>

    </div>

    )
        ;
    }
}

export default login;
