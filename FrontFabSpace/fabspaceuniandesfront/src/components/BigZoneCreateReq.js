import React, { useRef, useEffect, useState } from 'react';
import instance from '../helpers/axios-requests';

import Button from '@material-ui/core/Button';

//OL IMPORTS
import 'ol/ol.css';
import { Map, View } from 'ol';
import GeoJSON from 'ol/format/GeoJSON';
import { OSM, Vector as VectorSource } from 'ol/source';
import { DragBox, Select as OLSelect } from 'ol/interaction';
import { platformModifierKeyOnly } from 'ol/events/condition';
import { fromLonLat } from 'ol/proj';
import { all } from 'ol/loadingstrategy';
import { tile } from 'ol/loadingstrategy';
import * as olLoadingstrategy from 'ol/loadingstrategy';
import { bbox } from 'ol/loadingstrategy';
import 'ol/ol.css';
import Draw, { createBox, createRegularPolygon } from 'ol/interaction/Draw';
import Polygon from 'ol/geom/Polygon';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
import Projection from 'ol/proj/Projection';
import * as olProj from 'ol/proj';
import { toLonLat } from 'ol/proj';
export default function BigZoneCreateReq() {
  const [mapu, setMap] = useState();
  const [coordinatesSelected, setCoordinatesSelected] = useState([]);
  const [source2, setsource] = useState();
  useEffect(() => {
    var raster = new TileLayer({
      source: new OSM(),
    });

    var source = new VectorSource({ wrapX: false });

    var vector = new VectorLayer({
      source: source,
    });
    //console.log(vector.getProjection());
    var map = new Map({
      layers: [raster, vector],
      target: 'map',
      view: new View({
        center: [-11000000, 4600000],
        zoom: 4,
      }),
    });

    var typeSelect = document.getElementById('type');

    var draw; // global so we can remove it later
    function addInteraction() {
      var value = typeSelect.value;
      if (value !== 'None') {
        var geometryFunction;

        draw = new Draw({
          source: source,
          type: value,
          geometryFunction: geometryFunction,
        });
        map.addInteraction(draw);
      }
      draw.on('drawend', function (evt) {
        console.log(evt.feature);
        console.log(evt.feature.getGeometry());
        setCoordinatesSelected(evt.feature.getGeometry().getCoordinates());
        console.log(evt.feature.getGeometry().getCoordinates());
        var geometry = evt.feature.getGeometry().clone();
        var arreglito = [];
        for (var i = 0; i < geometry.getCoordinates()[0].length; i++) {
          arreglito[i] = toLonLat(
            geometry.getCoordinates()[0][i],
            new Projection('EPSG:4326')
          );
        }
        console.log(
          toLonLat(geometry.getCoordinates()[0][0]),
          new Projection('EPSG:4326')
        );
      });
    }

    /**
     * Handle change event.
     */
    typeSelect.onchange = function () {
      map.removeInteraction(draw);
      addInteraction();
    };

    addInteraction();
  }, []);

  //////////////////////////////////BEHAVIOR///////////
  const handleSubmit = (state) => {
    const options = {
      headers: { 'Content-Type': 'multipart/form-data' },
    };
    var data = {};
    data.type = 'MultiPolygon';
    data.coordinates = [[coordinatesSelected]];
    var bodyFormData = new FormData();
    /*
    instance
      .post(`/now/`, bodyFormData, options)
      .then((resp) => {
        console.log(resp.data);
      })
      .catch((error) => {
        //console.log(error.resp.original_design);
        // console.log(error);
      });
      */
  };
  return (
    <>
      <div
        id='map'
        style={{ color: 'red', width: '600px', height: '450px' }}
      ></div>
      <p>Hola</p>
      <form class='form-inline'>
        <label>Shape type &nbsp;</label>
        <select id='type'>
          <option value='Polygon'>Polygon</option>
        </select>
      </form>
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
