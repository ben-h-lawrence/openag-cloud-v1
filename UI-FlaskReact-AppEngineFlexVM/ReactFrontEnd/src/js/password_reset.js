import React, {Component} from 'react';
import logo from '../images/logo.svg';
import {Link} from "react-router-dom";

export class PasswordReset extends Component {
    constructor(props) {
        super(props);
        var qs = require('url').parse(window.location.href, true).query;

        if( typeof qs['rt'] != 'undefined') {
            console.log(qs['rt'])
            this.recovery_token = qs['rt'];
        }
        this.state = {
            name: '',
            password: '',
            error_message: '',
            success_message: '',
            hide_form: true,
            recovery_token:this.recovery_token
        };
        // This binding is necessary to make `this` work in the callback
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.goToSignIn = this.goToSignIn.bind(this)
    }
    goToSignIn()
    {
      window.location.href = "/login";
    }
    componentDidMount() {
      this.fetchRecoveryRequest();
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
        });
        this.changePassword();
        event.preventDefault();
    }
    fetchRecoveryRequest() {
      return fetch( process.env.REACT_APP_FLASK_URL + '/api/fetch_recovery_request/', {
          method: 'POST',
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              'recovery_token': this.state.recovery_token,
          })
      })
          .then((response) => response.json())
          .then((responseJson) => {
              console.log(responseJson)
              if (responseJson["response_code"]== 200){
                  console.log("Account Recovery Request Found")
                  let success_message = responseJson['message']
                  let username = responseJson['username']
                  this.setState({
                    success_message: success_message,
                    name: username,
                    error_message: '',
                    hide_form: false
                  })

              } else {
                  let error_message = responseJson['message']
                  this.setState({
                    error_message: error_message
                  })
              }
          })
          .catch((error) => {
              console.error(error);
          });
    }
    changePassword() {
        return fetch( process.env.REACT_APP_FLASK_URL + '/api/change_password/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'username': this.state.name,
                'password': this.state.password,
                'recovery_token': this.state.recovery_token
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
                      hide_form: true
                    })

                } else {
                    let error_message = responseJson['message']
                    this.setState({
                      error_message: error_message
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
                    {!this.state.hide_form &&
                      <form className="account-recovery-form" onSubmit={this.handleSubmit}>
                      <input type="text" placeholder="username" id="username" name="name" value={"username: " + this.state.name}
                                 onChange={this.handleChange} readOnly />
                          <input type="password" placeholder="password" name="password"
                                 value={this.state.password}
                                 onChange={this.handleChange} />
                          <button >reset password</button>
                      </form>
                    }
                      <p className="message"><a onClick={this.goToSignIn}> Back to Login </a></p>
                </div>

            </div>
        );
    }
}
