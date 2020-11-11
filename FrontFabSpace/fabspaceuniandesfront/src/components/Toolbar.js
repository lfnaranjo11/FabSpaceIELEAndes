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
import Slide from '@material-ui/core/Slide';
import Tooly from '@material-ui/core/Toolbar';
import AppBar from '@material-ui/core/AppBar';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction='up' ref={ref} {...props} />;
});
const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
}));

const Toolbar = (props) => {
  const classes = useStyles();
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
    <>
      <div className={classes.root}>
        <AppBar position='static' color='secondary'>
          <Tooly variant='dense'>
            <IconButton
              edge='start'
              className={classes.menuButton}
              color='inherit'
              aria-label='menu'
            >
              <MenuIcon />
            </IconButton>
            <Typography variant='h6' color='inherit'>
              FabSpace Uniandes
            </Typography>
          </Tooly>
        </AppBar>
      </div>
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
    </>
  );
};
export default Toolbar;
