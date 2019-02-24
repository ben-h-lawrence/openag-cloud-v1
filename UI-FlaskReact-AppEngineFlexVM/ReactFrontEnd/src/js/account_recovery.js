import React, {Component} from 'react';
import logo from '../images/logo.svg';
import {Link} from "react-router-dom";

export class AccountRecovery extends Component {
    constructor(props) {
        super(props);
        var qs = require('url').parse(window.location.href, true).query;

        if( typeof qs['vcode'] != 'undefined') {
            console.log(qs['vcode'])
            this.vcode = qs['vcode'];
        }
        var url = window.location.protocol+'//'+window.location.hostname+(window.location.port ? ':'+window.location.port: '');
        this.state = {
            name: '',
            email_address: '',
            error_message: '',
            success_message: '',
            loading: false,
            url: url,
            vcode:this.vcode,
        };
        // This binding is necessary to make `this` work in the callback
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.goToSignIn = this.goToSignIn.bind(this)
    }
    goToSignIn()
    {

        if(this.state.vcode != "" && this.state.vcode != undefined && this.state.vcode != "undefined") {
                        window.location.href = "/login?vcode=" + this.state.vcode
                    }
                    else {
             window.location.href = "/login"
        }
    }
    componentDidMount() {

    }
    //
    handleChange(event) {
        this.setState({[event.target.name]: event.target.value});
        event.preventDefault();
    }

    handleSubmit(event) {

        console.log('Account recovery requested: ' + this.state);
        this.setState({
          success_message: '',
          error_message: '',
          loading: true
        });
        this.recoverAccount();
        event.preventDefault();
    }

    recoverAccount() {
        return fetch( process.env.REACT_APP_FLASK_URL + '/api/account_recovery/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'username': this.state.name,
                'email_address': this.state.email_address,
                'url': this.state.url
            })
        })
            .then((response) => response.json())
            .then((responseJson) => {
                console.log(responseJson)
                if (responseJson["response_code"]== 200){
                    console.log("Succesfully sent account recovery link")
                    let success_message = responseJson['message']
                    this.setState({
                      success_message: success_message,
                      error_message: '',
                      loading: false
                    })

                } else {
                    let error_message = responseJson['message']
                    this.setState({
                      error_message: error_message,
                      loading: false
                    })
                }
            })
            .catch((error) => {
                console.error(error);
            });
    }

    render() {
        return (
            <div className="login-page">
                <div className="form">
                    {this.state.error_message &&
                        <p style={{color: 'red'}}>
                            {this.state.error_message}
                        </p>
                    }
                    {this.state.success_message &&
                        <p>
                            {this.state.success_message}
                        </p>
                    }
                    {this.state.loading &&
                        <p>Sending account recovery link...</p>
                    }
                    <div className="image-section">
                        <img className="logo" src={logo}></img>
                    </div>
                    <p className="message-bold">Please enter your username OR email address</p>
                    <p className="message-bold">We will send an account recovery link to the email address associated with your account</p>
                    <form className="account-recovery-form" onSubmit={this.handleSubmit}>
                        <input type="text" placeholder="username" name="name" value={this.state.name}
                               onChange={this.handleChange} />
                        <input type="email" placeholder="email address" name="email_address"
                               value={this.state.email_address}
                               onChange={this.handleChange} />
                        <button>send recovery link</button>
                        <p className="message"><a onClick={this.goToSignIn}> Back to Login </a></p>
                    </form>
                </div>

            </div>
        );
    }
}
