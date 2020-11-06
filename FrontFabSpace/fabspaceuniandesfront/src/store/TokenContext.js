import React, { useContext, useState, useEffect } from 'react';

const TokenContext = React.createContext();
const TokenUpdateContext = React.createContext();
export function useToken() {
  return useContext(TokenContext);
}
export function useUpdateToken() {
  return useContext(TokenUpdateContext);
}

export function TokenProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token1') || '');

  useEffect(() => {
    localStorage.setItem('token1', token);
  }, [token]);

  return (
    <TokenContext.Provider value={token}>
      <TokenUpdateContext.Provider value={setToken}>
        {children}
      </TokenUpdateContext.Provider>
    </TokenContext.Provider>
  );
}
