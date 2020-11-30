import React, { useRef, useEffect, useState } from 'react';
import instance from '../helpers/axios-requests';

import { useHistory } from 'react-router-dom';
import { useToken, useUpdateToken } from '../store/TokenContext';
//material-ui

import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import { Button } from '@material-ui/core';
import DialogActions from '@material-ui/core/DialogActions';

import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import ListSubheader from '@material-ui/core/ListSubheader';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

//open layers imports
import 'ol/ol.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import GeoJSON from 'ol/format/GeoJSON';
import { OSM, Vector as VectorSource } from 'ol/source';
import { Vector as VectorLayer } from 'ol/layer';
import { DragBox, Select as OLSelect } from 'ol/interaction';
import { platformModifierKeyOnly } from 'ol/events/condition';
import { fromLonLat } from 'ol/proj';
const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  textfroot: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
}));

export default function CreateRequeriment() {
  const classes = useStyles();
  const token = useToken();
  const setToken = useUpdateToken();
  const [dragBoxy, setBox] = useState();
  const [deptos, setDeptos] = useState([]);
  const [selectedDepto, setSelectedDepto] = useState('');
  const [mpios, setMpios] = useState([]);
  const [selectedMpio, setSelectedMpio] = useState('');
  const [vdas, setVdas] = useState([]);
  const [selectedVda, setSelectedVda] = useState();
  const [mapu, setMap] = useState();
  const [selectedFeaturesu, setselectedFeaturesu] = useState();
  const nombreRef = useRef('');

  useEffect(() => {
    instance
      .get('/listdeptos/')
      .then((res) => {
        setDeptos(res.data);
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);
  useEffect(() => {
    const map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
      ],
      view: new View({
        maxZoom: 25,
        center: fromLonLat([-73.103194, 4.631602]),
        zoom: 5,
      }),
    });
    setMap(map);
  }, []);
  const handleSelectVereda = (event) => {
    setSelectedVda(event.target.value);
    console.log(event.target.value);
    //enviar la solicitud con esa geometria
  };
  const handleSelectMpio = (event) => {
    instance
      .get(`/listvdas/${event.target.value}`)
      .then((res) => {
        setVdas(res.data);
        //console.log(res);
      })
      .catch((err) => {
        // console.log(err);
      });
    var sourceMpios = new VectorSource({
      url: `http://${process.env.REACT_APP_BACK_END}/restapi/veredasgeojson/${event.target.value}`,
      format: new GeoJSON(),
    });
    var vectorLayerMpios = new VectorLayer({
      source: sourceMpios,
      visible: true,
      title: 'ColombiaMpiosGEOJSON',
    });
    mapu.addLayer(vectorLayerMpios);

    var infoBox = document.getElementById('info2');

    selectedFeaturesu.on(['add', 'remove'], function () {
      var names = selectedFeaturesu.getArray().map(function (feature) {
        return feature.get('nombre_ver');
      });
      if (names.length > 0) {
        infoBox.innerHTML = names.join(', ');
      } else {
        infoBox.innerHTML = 'No vereda selected';
      }
    });
  };
  const handleSelectDepto = (event) => {
    instance
      .get(`/listmpios/${event.target.value}`)
      .then((res) => {
        setMpios(res.data);
        //console.log(res);
      })
      .catch((err) => {
        // console.log(err);
      });
    setSelectedDepto(event.target.value);
    //console.log(event.target.value);
    var sourceDepto = new VectorSource({
      url: `http://${process.env.REACT_APP_BACK_END}/restapi/deptogeojson/${event.target.value}`,
      format: new GeoJSON(),
    });
    var vectorLayerDepto = new VectorLayer({
      source: sourceDepto,
      visible: true,
      title: 'ColombiaDeptoGEOJSON',
    });
    var sourceMpios = new VectorSource({
      url: `http://${process.env.REACT_APP_BACK_END}/restapi/mpiosgeojson/${event.target.value}`,
      format: new GeoJSON(),
    });
    var vectorLayerMpios = new VectorLayer({
      source: sourceMpios,
      visible: true,
      title: 'ColombiaMpiosGEOJSON',
    });
    mapu.addLayer(vectorLayerMpios);
    var select = new OLSelect();
    mapu.addInteraction(select);
    var selectedFeatures = select.getFeatures();
    setselectedFeaturesu(selectedFeatures);
    // a DragBox interaction used to select features by drawing boxes
    var dragBox = new DragBox({
      condition: platformModifierKeyOnly,
    });
    mapu.addInteraction(dragBox);
    setBox(dragBox);
    dragBox.on('boxend', function () {
      var rotation = mapu.getView().getRotation();
      var oblique = rotation % (Math.PI / 2) !== 0;
      var candidateFeatures = oblique ? [] : selectedFeatures;
      var extent = dragBox.getGeometry().getExtent();
      sourceMpios.forEachFeatureIntersectingExtent(extent, function (feature) {
        candidateFeatures.push(feature);
      });
    });

    // clear selection when drawing a new box and when clicking on the map
    dragBox.on('boxstart', function () {
      selectedFeatures.clear();
    });

    var infoBox = document.getElementById('info');

    selectedFeatures.on(['add', 'remove'], function () {
      var names = selectedFeatures.getArray().map(function (feature) {
        return feature.get('mpio_cnmbr');
      });
      if (names.length > 0) {
        infoBox.innerHTML = names.join(', ');
      } else {
        infoBox.innerHTML = 'No municipios selected';
      }
    });
  };

  const handleSubmit = (state) => {
    const options = {
      headers: { 'Content-Type': 'multipart/form-data' },
    };
    var bodyFormData = new FormData();
    bodyFormData.append(
      'title',
      nombreRef.current.children[1].children[0].value
    );
    bodyFormData.append('vereda', selectedVda);
    bodyFormData.append('state', state);
    bodyFormData.append('mission', 'Sentinel-2');
    instance
      .post(`/now/`, bodyFormData, options)
      .then((resp) => {
        console.log(resp.data);
      })
      .catch((error) => {
        //console.log(error.resp.original_design);
        // console.log(error);
      });
  };

  return (
    <>
      {' '}
      <style></style>
      <div
        id='map'
        style={{ color: 'red', width: '800px', height: '650px' }}
      ></div>
      <div id='info'>No countries selected</div>
      <div id='info2'>No countries selected</div>
      <FormControl className={classes.formControl}>
        <InputLabel htmlFor='grouped-native-select'>Departamento</InputLabel>
        <Select
          native
          defaultValue=''
          id='grouped-native-select'
          onChange={handleSelectDepto}
        >
          <option aria-label='None' value='' />
          <option value={1}>Option 1</option>
          <option value={2}>Option 2</option>
          {deptos.map((option) => (
            <option value={option.cod_dpto}>{option.nom_dep}</option>
          ))}
        </Select>
      </FormControl>
      <FormControl className={classes.formControl}>
        <InputLabel htmlFor='grouped-native-select'>Municipio</InputLabel>
        <Select
          native
          defaultValue=''
          id='grouped-native-select'
          onChange={handleSelectMpio}
        >
          <option aria-label='None' value='' />
          {mpios.map((option) => (
            <option value={option.mpio_ccnct}>{option.mpio_cnmbr}</option>
          ))}
        </Select>
      </FormControl>
      <FormControl className={classes.formControl}>
        <InputLabel htmlFor='grouped-native-select'>Vereda</InputLabel>
        <Select
          native
          defaultValue=''
          id='grouped-native-select'
          onChange={handleSelectVereda}
        >
          <option aria-label='None' value='' />
          {vdas.map((option) => (
            <option value={option.codigo_ver}>{option.nombre_ver}</option>
          ))}
        </Select>
      </FormControl>
      <form className={classes.textfroot} noValidate autoComplete='off'>
        <TextField
          id='outlined-basic'
          ref={nombreRef}
          label='titulo'
          variant='outlined'
        />
      </form>
      <Button
        variant='outlined'
        color='primary'
        onClick={(e) => handleSubmit('NOW')}
      >
        Enviar Ahora
      </Button>
      <Button
        variant='outlined'
        color='primary'
        onClick={(e) => handleSubmit('WATCHLIST')}
      >
        Monitorear
      </Button>
    </>
  );
}
