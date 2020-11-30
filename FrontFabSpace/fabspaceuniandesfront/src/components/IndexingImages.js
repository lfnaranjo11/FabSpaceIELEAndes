import React, { useRef, useEffect, useState } from 'react';
//OL IMPORTS
import 'ol/ol.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import GeoJSON from 'ol/format/GeoJSON';
import { OSM, Vector as VectorSource } from 'ol/source';
import { Vector as VectorLayer } from 'ol/layer';
import { DragBox, Select as OLSelect } from 'ol/interaction';
import { platformModifierKeyOnly } from 'ol/events/condition';
import { fromLonLat } from 'ol/proj';
import { all } from 'ol/loadingstrategy'; //MATERIAL-UI IMPORTS
import { tile } from 'ol/loadingstrategy';
import * as olLoadingstrategy from 'ol/loadingstrategy';
import { bbox } from 'ol/loadingstrategy';

//MATERIAL-UI IMPORTS
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import InputBase from '@material-ui/core/InputBase';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import SearchIcon from '@material-ui/icons/Search';
import DirectionsIcon from '@material-ui/icons/Directions';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import 'date-fns';
import Grid from '@material-ui/core/Grid';
import DateFnsUtils from '@date-io/date-fns';
import Button from '@material-ui/core/Button';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
  KeyboardDatePicker,
  DatePicker,
} from '@material-ui/pickers';

import instance from '../helpers/axios-requests';
import { DataGrid } from '@material-ui/data-grid';
import { set } from 'date-fns';

const useStyles = makeStyles((theme) => ({
  rootGrid: {
    flexGrow: 2,
  },
  root: {
    padding: '2px 4px',
    display: 'flex',
    alignItems: 'center',
    width: 1000,
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
  input: {
    marginLeft: theme.spacing(1),
    flex: 1,
  },
  iconButton: {
    padding: 10,
  },
  divider: {
    height: 28,
    margin: 4,
  },
  slider: {
    width: 300,
  },
}));

export default function IndexingImages() {
  const [mapu, setMap] = useState();
  const reqRef = useRef();
  const [requeriments, setRequirements] = useState([]);
  const [requerimentSelected, setRequirementSelected] = useState();
  const [imagenes, setImagenes] = useState([]);

  //////////////INITIAL CONFIGURATION////////////////
  useEffect(() => {
    instance
      .get('/listreq/')
      .then((res) => {
        setRequirements(res.data);
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
    var sourceMpios = new VectorSource({
      url: 'http://127.0.0.1:8000/restapi/imgsjson/',
      format: new GeoJSON(),
    });
    var vectorLayerMpios = new VectorLayer({
      source: sourceMpios,
      visible: true,
      title: 'ColombiaMpiosGEOJSON',
    });
    setMap(map);
    setCurrentLayer(vectorLayerMpios);
    map.addLayer(vectorLayerMpios);
    var select = new OLSelect();
    map.addInteraction(select);
    // a DragBox interaction used to select features by drawing boxes
    var selectedFeatures = select.getFeatures();
    // a DragBox interaction used to select features by drawing boxes
    var dragBox = new DragBox({
      condition: platformModifierKeyOnly,
    });

    map.addInteraction(dragBox);

    dragBox.on('boxend', function () {
      var rotation = map.getView().getRotation();
      var oblique = rotation % (Math.PI / 2) !== 0;
      var candidateFeatures = oblique ? [] : selectedFeatures;
      var extent = dragBox.getGeometry().getExtent();
      sourceMpios.forEachFeatureIntersectingExtent(extent, function (feature) {
        candidateFeatures.push(feature);
      });
      if (oblique) {
        var anchor = [0, 0];
        var geometry = dragBox.getGeometry().clone();
        geometry.rotate(-rotation, anchor);
        var extent$1 = geometry.getExtent();
        candidateFeatures.forEach(function (feature) {
          var geometry = feature.getGeometry().clone();
          geometry.rotate(-rotation, anchor);
          if (geometry.intersectsExtent(extent$1)) {
            selectedFeatures.push(feature);
          }
        });
      }
    });

    // clear selection when drawing a new box and when clicking on the map
    dragBox.on('boxstart', function () {
      selectedFeatures.clear();
      setImagenes([]);
    });
    selectedFeatures.on(['add', 'remove'], function () {
      console.log(selectedFeatures.getArray());
      var arreglo = selectedFeatures.getArray().map(function (feature) {
        return {
          title: feature.get('title'),
          id: feature.get('id'),
          esa: feature.get('esa_uiid'),
          ingestion_date: feature.get('ingestion_date'),
          filedir: feature.get('filedir'),
          thumbnail_location: feature.get('thumbnail_location'),
        };
      });
      console.log(arreglo);

      if (arreglo.length > 0) {
        setImagenes(arreglo);
      } else {
        setImagenes([]);
      }
    });
  }, []);

  ////////////////////////////////

  /////DATE MANAGEMEET/////////////////////////////////
  /////////////////////////////////////////////////////
  //////////////////needs its own component
  const [fechaInicio, setFechaInicio] = useState(new Date('01/01/2020'));
  const [fechaFin, setFechaFin] = useState(new Date('2020/12/31'));
  const [currentLayer, setCurrentLayer] = useState();
  const [valueSliderFechas, setValueSliderFechas] = React.useState([1, 365]);
  const handleChangeSlider = (event, newValue) => {
    setValueSliderFechas(newValue);
    var [nuinicio, nunfin] = newValue;
    const inicio = getDateFromDayNum(nuinicio, 2020);
    const fin = getDateFromDayNum(nunfin, 2020);
    setFechaInicio(inicio);
    setFechaFin(fin);
    console.log(inicio);
  };

  ///from date to number
  const calculateDay = (now) => {
    var start = new Date(now.getFullYear(), 0, 0);
    var diff = now - start;
    var oneDay = 1000 * 60 * 60 * 24;
    var day = Math.floor(diff / oneDay);
    console.log('Day of year: ' + day);
    return day;
  };
  var getDateFromDayNum = (dayNum, year) => {
    var date = new Date();
    if (year) {
      date.setFullYear(year);
    }
    date.setMonth(0);
    date.setDate(0);
    var timeOfFirst = date.getTime(); // this is the time in milliseconds of 1/1/YYYY
    var dayMilli = 1000 * 60 * 60 * 24;
    var dayNumMilli = dayNum * dayMilli;
    date.setTime(timeOfFirst + dayNumMilli);
    return date;
  };
  //from
  var getDateFromDayNumStr = (dayNum, year) => {
    var date = new Date();
    if (year) {
      date.setFullYear(year);
    }
    date.setMonth(0);
    date.setDate(0);
    var timeOfFirst = date.getTime(); // this is the time in milliseconds of 1/1/YYYY
    var dayMilli = 1000 * 60 * 60 * 24;
    var dayNumMilli = dayNum * dayMilli;
    date.setTime(timeOfFirst + dayNumMilli);
    return date.toDateString();
  };

  const handleDateChangeInit = (date) => {
    setFechaInicio(date);
    var [inicio, fin] = valueSliderFechas;
    setValueSliderFechas([calculateDay(date), fin]);
    console.log(date);
  };
  const handleDateChangeEnd = (date) => {
    var [inicio, fin] = valueSliderFechas;
    setValueSliderFechas([inicio, calculateDay(date)]);
    setFechaFin(date);
    console.log(date);
    filter_date();
  };
  /////DATE MANAGEMEET END
  ///////////////////////////

  ///////BEHAVIOR///////////////////
  const handleSelectReq = (event) => {
    setRequirementSelected(event.target.value);
    mapu.removeLayer(currentLayer);
    var sourceReq = new VectorSource({
      url: `http://${process.env.REACT_APP_BACK_END}/restapi/imgsjson/${event.target.value}`,
      format: new GeoJSON(),
    });
    var vectorLayerImg = new VectorLayer({
      source: sourceReq,
      visible: true,
      title: 'ImgsbyReqGEOJSON',
    });
    setCurrentLayer(vectorLayerImg);
    mapu.addLayer(vectorLayerImg);
    console.log(vectorLayerImg);
  };

  const classes = useStyles();
  const filter_date = (e) => {
    e.preventDefault();

    mapu.removeLayer(currentLayer);
    var sourceReq = new VectorSource({
      format: new GeoJSON(),
      url: `http://${
        process.env.REACT_APP_BACK_END
      }/restapi/imgsjson/from=${fechaInicio.toISOString()}to=${fechaFin.toISOString()}`,

      /*
        instance
          .post(
            `/imgsjson/`,
            {
              ingestion_date_init: fechaInicio,
              ingestion_date_end: fechaFin,
            },
            {
              headers: {
                'Content-Type': `application/json`,
              },
            }
          )
          .then((res) => {
            sourceReq.addFeatures(
              sourceReq.getFormat().readFeatures(JSON.stringify(res.data))
            );
            console.log(JSON.stringify(res.data));
          })
          .catch((err) => {
            sourceReq.removeLoadedExtent(extent);
            console.log(err);
          });*/
    });
    var vectorLayerImg = new VectorLayer({
      source: sourceReq,
      visible: true,
      title: 'newImgas',
    });
    setCurrentLayer(vectorLayerImg);
    mapu.addLayer(vectorLayerImg);
  };

  const handleSearchReq = (event) => {
    event.preventDefault();
  };
  ///////BEHAVIOR END/////////////////

  return (
    <>
      <Paper component='form' className={classes.root}>
        <IconButton className={classes.iconButton} aria-label='menu'>
          <MenuIcon />
        </IconButton>
        <InputBase
          className={classes.input}
          placeholder='Buscar imagenes '
          inputProps={{ 'aria-label': 'search google maps' }}
        />
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor='grouped-native-select'>Requerimiento</InputLabel>
          <Select
            native
            defaultValue=''
            id='grouped-native-select'
            onChange={(e) => handleSelectReq(e)}
          >
            <option aria-label='None' value='' />
            {requeriments.map((option) => (
              <option value={option.id}>{option.title}</option>
            ))}
          </Select>
        </FormControl>
        <IconButton
          type='submit'
          className={classes.iconButton}
          aria-label='search'
          onClick={(e) => filter_date(e)}
        >
          <SearchIcon />
        </IconButton>
      </Paper>
      <div
        id='map'
        style={{ color: 'red', width: '600px', height: '450px' }}
      ></div>
      <div>
        <div className={classes.slider}>
          <Typography id='range-slider' gutterBottom>
            Rango de fechas
          </Typography>
          <Slider
            value={valueSliderFechas}
            onChange={handleChangeSlider}
            min={0}
            max={365}
            valueLabelDisplay='auto'
            valueLabelFormat={(x) => getDateFromDayNumStr(x, 2020)}
            aria-labelledby='range-slider'
          />
        </div>
        <MuiPickersUtilsProvider utils={DateFnsUtils}>
          <Grid container justify='space-around'>
            <KeyboardDatePicker
              variant='inline'
              format='dd/MM/yyyy'
              margin='normal'
              id='date-picker-inline'
              label='Fecha inicial'
              value={fechaInicio}
              onChange={(x) => handleDateChangeInit(x)}
            />
          </Grid>
        </MuiPickersUtilsProvider>
        <MuiPickersUtilsProvider utils={DateFnsUtils}>
          <Grid container justify='space-around'>
            <KeyboardDatePicker
              disableToolbar
              variant='inline'
              format='dd/MM/yyyy'
              margin='normal'
              id='date-picker-inline'
              label='Fecha Final'
              value={fechaFin}
              onChange={(x) => handleDateChangeEnd(x)}
            />
          </Grid>
        </MuiPickersUtilsProvider>
      </div>

      <Grid
        style={{ marginTop: '5px' }}
        container
        className={classes.rootGrid}
        spacing={2}
      >
        <Grid container justify='center' alignItems='center' spacing={2}>
          {imagenes.map((imagen, i) => (
            <Card className={classes.root}>
              <CardHeader title={imagen.title} />
              <CardContent>
                <Typography variant='body2' color='textSecondary' component='p'>
                  {imagen.filedir}
                </Typography>
                <Typography variant='body2' color='textSecondary' component='p'>
                  {imagen.ingestion_date}
                </Typography>
                <Typography variant='body2' color='textSecondary' component='p'>
                  {imagen.id}
                </Typography>

                <picture>
                  <source
                    srcset={`${imagen.thumbnail_location}.jp2`}
                    type='image/jp2'
                  />
                </picture>
                <img
                  src={`${imagen.thumbnail_location}.png`}
                  alt={`${imagen.thumbnail_location}.png`}
                ></img>
              </CardContent>
            </Card>
          ))}
        </Grid>
      </Grid>
    </>
  );
}
