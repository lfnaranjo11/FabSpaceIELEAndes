import React, { useRef, useEffect } from 'react';
import axios from '../helpers/axios-requests';
import { useHistory } from 'react-router-dom';
import { useToken, useUpdateToken } from '../store/TokenContext';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import { Button } from '@material-ui/core';
import DialogActions from '@material-ui/core/DialogActions';

import Container from '@material-ui/core/Container';

//open layers imports
import 'ol/ol.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import GeoJSON from 'ol/format/GeoJSON';
import { OSM, Vector as VectorSource } from 'ol/source';
import { Vector as VectorLayer } from 'ol/layer';
export default function CreateRequeriment() {
  const token = useToken();
  const setToken = useUpdateToken();
  const namedRef = useRef();
  const passwordRef = useRef();
  const mailRef = useRef();
  const history = useHistory();
  useEffect(() => {
    const map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
      ],
      view: new View({
        center: [0, 0],
        zoom: 0,
      }),
    });
    var source = new VectorSource({
      url: 'http://127.0.0.1:8000/restapi/veredasgeojson/',
      format: new GeoJSON(),
    });
    var vectorLayer = new VectorLayer({
      source: source,
      visible: true,
      title: 'ColombiaRegionsGEOJSON',
    });
    map.addLayer(vectorLayer);
  }, []);

  return (
    <>
      {' '}
      <style></style>
      <div
        id='map'
        style={{ color: 'red', width: '800px', height: '650px' }}
      ></div>
    </>
  );
}
