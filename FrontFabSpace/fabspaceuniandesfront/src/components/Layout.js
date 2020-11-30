import React from 'react';
//import Route from 'react-router-dom';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from 'react-router-dom';

import { useToken } from '../store/TokenContext';
import CreateRequeriment from './CreateRequeriment';
import IndexingImages from './IndexingImages';
import Home from './Home';
import BigZoneCreateReq from './BigZoneCreateReq';

//withMyHook(MyDiv);
const Layout = (props) => {
  const token = useToken();
  return (
    <>
      {token === '' ? (
        <Switch name='sin sesion iniciada'></Switch>
      ) : (
        <Switch name='con sesion iniciada'></Switch>
      )}
      <Switch name='con o sin sesion'>
        <Route path='/register' exact component={CreateRequeriment} />
        <Route path='/index' exact component={IndexingImages} />
        <Route path='/' exact component={Home} />
        <Route path='/BigZoneCreateReq' exact component={BigZoneCreateReq} />
      </Switch>
    </>
  );
};

export default Layout;
