import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import Toolbar from './components/Toolbar';
import Layout from './components/Layout';

function App() {
  return (
    <>
      <BrowserRouter>
        <Toolbar></Toolbar>
        <Layout></Layout>
      </BrowserRouter>
    </>
  );
}

export default App;
