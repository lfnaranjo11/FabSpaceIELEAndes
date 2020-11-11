import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import Toolbar from './components/Toolbar';
import Layout from './components/Layout';
import { TokenProvider } from './store/TokenContext';

function App() {
  return (
    <>
      <TokenProvider>
        <BrowserRouter>
          <Toolbar></Toolbar>
          <Layout></Layout>
        </BrowserRouter>
      </TokenProvider>
    </>
  );
}

export default App;
