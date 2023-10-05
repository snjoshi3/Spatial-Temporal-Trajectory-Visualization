import {load_data} from "./api.js";
const {DeckGL, TripsLayer} = deck;

// mapboxgl = require('mapbox-gl@^1.5.1/dist/mapbox-gl.js');


  


// import {TripsLayer} from '@deck.gl/geo-layers';

document.addEventListener("DOMContentLoaded",function(){
    console.log("Hello"); 

    // document.querySelector("WrapperOne").setAttribute("display","block")

    document.querySelector("#dropDown").addEventListener("change",function(){
        changeDisplay();
    })
})

function changeDisplay(){
    const dropdown= document.querySelector("#dropDown").value;
    const w1 = document.querySelector("#wrapperOne")
    const w2= document.querySelector("#wrapperTwo")
    const w3= document.querySelector("#wrapperThree")
    const w4= document.querySelector("#wrapperFour")
    const w5= document.querySelector("#wrapperFive")
    const wr= document.querySelector("#wrapperResult")

    switch(dropdown){
        case 'one':
            doFirst();
            w1.style.display = "block"
            w2.style.display = "none"
            w3.style.display = "none"
            w4.style.display = "none"
            w5.style.display = "none"
            wr.style.display = "none"
            break;
        case 'two':
            w1.style.display = "none"
            w2.style.display = "block"
            w3.style.display = "none"
            w4.style.display = "none"
            w5.style.display = "none"
            wr.style.display = "none"
            break;
        case 'three':
            w1.style.display = "none"
            w2.style.display = "none"
            w3.style.display = "block"
            w4.style.display = "none"
            w5.style.display = "none"
            wr.style.display = "none"
            break;
        case 'four':
            w1.style.display = "none"
            w2.style.display = "none"
            w3.style.display = "none"
            w4.style.display = "block"
            w5.style.display = "none"
            wr.style.display = "none"
            break;
        case 'five':
            w1.style.display = "none"
            w2.style.display = "none"
            w3.style.display = "none"
            w4.style.display = "none"
            w5.style.display = "block"
            wr.style.display = "none"
            break;
    }
}

function doFirst(){
    let data;
    console.log("doFirst");
    load_data().then((response)=>{
        console.log(response);
        data = response.data;
    })

    // // const trips = new deck.TripsLayer({
    // //     id: 'trips-layer',
    // //     data,
    // //     getPath: d => d.waypoints.map(p => p.coordinates),
    // //     // deduct start timestamp from each data point to avoid overflow
    // //     getTimestamps: d => d.waypoints.map(p => p.timestamp - 1554772579000),
    // //     getColor: [253, 128, 93],
    // //     opacity: 0.8,
    // //     widthMinPixels: 5,
    // //     rounded: true,
    // //     fadeTrail: true,
    // //     trailLength: 200,
    // //     currentTime: 100
    // //   });
    // // console.log(trips);


    // const wr = document.querySelector("#wrapperResult");

    // // console.log(wr)




    // const layer = new TripsLayer({
    //     id: 'TripsLayer',
    //     data: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf.trips.json',
        
    //     /* props from TripsLayer class */
        
    //     currentTime: 500,
    //     // fadeTrail: true,
    //     getTimestamps: d => d.waypoints.map(p => p.timestamp - 1554772579000),
    //     trailLength: 600,
        
    //     /* props inherited from PathLayer class */
        
    //     // billboard: false,
    //     capRounded: true,
    //     getColor: [253, 128, 93],
    //     getPath: d => d.waypoints.map(p => p.coordinates),
    //     // getWidth: 1,
    //     jointRounded: true,
    //     // miterLimit: 4,
    //     // rounded: true,
    //     // widthMaxPixels: Number.MAX_SAFE_INTEGER,
    //     widthMinPixels: 8,
    //     // widthScale: 1,
    //     // widthUnits: 'meters',
        
    //     /* props inherited from Layer class */
        
    //     // autoHighlight: false,
    //     // coordinateOrigin: [0, 0, 0],
    //     // coordinateSystem: COORDINATE_SYSTEM.LNGLAT,
    //     // highlightColor: [0, 0, 128, 128],
    //     // modelMatrix: null,
    //     opacity: 0.8,
    //     // pickable: false,
    //     visible: true,
    //     // wrapLongitude: false,
    //   });
      
    //   new DeckGL({
    //     mapStyle: maplibregl,
    //     initialViewState: {
    //       longitude: -122.4,
    //       latitude: 37.74,
    //       zoom: 11,
    //       maxZoom: 20,
    //       pitch: 30,
    //       bearing: 0
    //     },
    //     controller: true,
    //     container:'wrapperResult',
    //     map: mapboxgl,
    //     mapboxApiAccessToken:'pk.eyJ1IjoiYW1yaXRiaGFza2FyIiwiYSI6ImNsYXl1Y2treTEzNHYzcHA1aXJxanlhNWcifQ._C2XJ0KSPB2WTGKICzeSeg',
    //     mapStyle: 'mapbox://styles/mapbox/dark-v10',
    //     layers: [layer],
    //   });

    plotTripsLayer(data);
}

function plotTripsLayer(data){
    require(["esri/Map", "esri/views/MapView"], function(Map, MapView) {
        const TripsLayer = deck.TripsLayer;

        deck.loadArcGISModules().then(function({ DeckLayer }) {
          const layer = new DeckLayer({
            "deck.layers": []
          });

          setInterval(() => {
            layer.deck.layers = [
              new TripsLayer({
                id: 'trips',
                data: [{"trajectory_id":0,"vehicle_id":0,"timestamp":[1664515076,1664515106],"location":[[-111.92518390436581, 33.414237578989216],[-111.92518384063071, 33.414183655342725]]}
,{"trajectory_id":1,"vehicle_id":1,"timestamp":[1664514836,1664514851,1664514866,1664514881,1664514896],"location":[[-111.92285145187222,33.41427909937204],[-111.92282161935306,33.414252073168285],[-111.92285157742808,33.41422517574458],[-111.92282153563072,33.41419819611907],[-111.92282149374189,33.414171205538906]]}
,{"trajectory_id":0,"vehicle_id":0,"timestamp":[1664511371,1664511386,1664511401,1664511416,1664511431,1664511446,1664512181,1664512196,1664512211,1664512226,1664512241,1664515751,1664515766,1664515781,1664515796,1664515811,1664516546,1664516561,1664516591,1664516606],"location":[[-111.92518382004077,33.414291502635706],[-111.92518396810091,33.414264523000654],[-111.9251839362123,33.414237578989216],[-111.92518390436581,33.41421059935417],[-111.9251838724772,33.414183655342725],[-111.92518384063071,33.41415667570768],[-111.9251838087421,33.41427408234834],[-111.92518394751099,33.4142471027133],[-111.92518391562238,33.41422015870185],[-111.92518388377589,33.41419317906681],[-111.92518385188728,33.41416623505537],[-111.92518382004077,33.414264523000654],[-111.9251839362123,33.414237578989216],[-111.92518390436581,33.41421059935417],[-111.9251838724772,33.414183655342725],[-111.92518384063071,33.41415667570768],[-111.9251838087421,33.41427408234834],[-111.92518394751099,33.4142471027133],[-111.92518391562238,33.41419317906681],[-111.92518385188728,33.41416623505537]]}
],
                getPath: d => d.location,
                getTimestamps: d => d.timestamp-1664511371,
                getColor: d => (d.trajectory_id === 0 ? [253, 128, 93] : [23, 184, 190]),
                opacity: 1.0,
                widthMinPixels: 4,
                rounded: true,
                trailLength: 5,
                currentTime: (performance.now() % 1500) / 10,
                shadowEnabled: false
              })
            ];
          }, 50);

          // In the ArcGIS API for JavaScript the MapView is responsible
          // for displaying a Map, which usually contains at least a basemap.
          const mapView = new MapView({
            container: "viewDiv",
            map: new Map({
              basemap: "dark-gray-vector",
              layers: [layer]
            }),
            center: [-111.92518390436581, 33.414237578989216],
            zoom: 18
          });
        });
      });
    }