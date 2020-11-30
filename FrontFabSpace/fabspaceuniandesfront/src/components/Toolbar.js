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
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import PopupState, { bindTrigger, bindMenu } from 'material-ui-popup-state';

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
            <PopupState variant='popover' popupId='demo-popup-menu'>
              {(popupState) => (
                <React.Fragment>
                  <IconButton
                    edge='start'
                    className={classes.menuButton}
                    color='inherit'
                    aria-label='menu'
                    {...bindTrigger(popupState)}
                  >
                    <MenuIcon />
                  </IconButton>

                  <Menu {...bindMenu(popupState)}>
                    <MenuItem onClick={popupState.close}>
                      <Link class='nav-link' to='/'>
                        hOme{' '}
                      </Link>
                    </MenuItem>
                    <MenuItem onClick={popupState.close}>
                      <Link class='nav-link' to='/register'>
                        Registrar{' '}
                      </Link>
                    </MenuItem>
                    <MenuItem onClick={popupState.close}>
                      <Link class='nav-link' to='/index'>
                        IndexDeImagenes{' '}
                      </Link>
                    </MenuItem>
                    <MenuItem onClick={popupState.close}>
                      <Link class='nav-link' to='/BigZoneCreateReq'>
                        <Typography variant='h12' color='inherit'>
                          Registrar zona amplia{' '}
                        </Typography>
                      </Link>
                    </MenuItem>
                  </Menu>
                </React.Fragment>
              )}
            </PopupState>
          </Tooly>
        </AppBar>
      </div>
    </>
  );
};
export default Toolbar;
