import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { useToken, useUpdateToken } from '../store/TokenContext';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Slide from '@material-ui/core/Slide';
const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction='up' ref={ref} {...props} />;
});
const Toolbar = (props) => {
  const token = useToken();
  const setToken = useUpdateToken();
  const [open, setOpen] = React.useState(false);
  const handleClickOpen = () => {
    setOpen(true);
  };
  const [enterprise_name, setEnterprise_name] = useState('');

  const handleClose = () => {
    setOpen(false);
  };
  const logOut = () => {
    setToken('');
  };
  return (
    <header>
      <nav class='navbar navbar-expand navbar-dark bg-dark'>
        <a class='navbar-brand ' href='/'>
          DesignMatch ©
        </a>
        <div class='collapse navbar-collapse' id='navbarNav'>
          <ul class='navbar-nav'>
            {token === '' ? (
              <li class='nav-item'>
                <a class='nav-link' href='/'>
                  Home
                </a>
              </li>
            ) : (
              <li class='nav-item'>
                <a class='nav-link' href='/myEnterprise'>
                  Mi empresa
                </a>
              </li>
            )}
          </ul>

          {token === '' ? (
            <ul class='navbar-nav ml-auto'>
              <li class='nav-item ml-auto'>
                <Link class='nav-link' to='/login'>
                  Log in
                </Link>
              </li>
              <li class='nav-item ml-auto'>
                <Link class='nav-link' to='/register'>
                  Sign up
                </Link>
              </li>
            </ul>
          ) : (
            <ul class='navbar-nav ml-auto'>
              <li class='nav-item ml-auto'>
                <Link class='nav-link' to='/' onClick={() => logOut()}>
                  Log out
                </Link>
              </li>
            </ul>
          )}
        </div>
      </nav>
      <div class='conteiner p-3'></div>
    </header>
  );
};
export default Toolbar;
