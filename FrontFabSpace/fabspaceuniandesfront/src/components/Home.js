import React, { useRef, useEffect, useState } from 'react';
export default function Home() {
  return (
    <>
      <h1>FabSpace Uniandes</h1>
      <p>Es una plataforma que permite </p>
      <p>Esta pagina esta conectada a la siguente ip </p>
      {process.env.REACT_APP_BACK_END}
    </>
  );
}
