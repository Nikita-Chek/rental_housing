import {
    Box,
    Typography,
    useMediaQuery,
    Button,
    Grid,
} from "@material-ui/core";
import { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import TableRowsIcon from '@mui/icons-material/TableRows';
import Plot from 'react-plotly.js';
  
const Analytics = () => {
    const isMobile = useMediaQuery((theme) => theme.breakpoints.down("sm"));
    const [meanByYear, setMeanByYear] = useState([]);
    const [countRooms, setCountRooms] = useState([]);
    const [medianByYear, setMedianByYear] = useState([]);

    useEffect(() => {
            fetch("http://0.0.0.0:8000/mean_by/year/", {
                'method': 'GET',
            })
            .then(resp => resp.json())
            .then(resp => setMeanByYear(resp))
            .catch(error => console.log(error))
        }, [])

    useEffect(() => {
          fetch("http://0.0.0.0:8000/median_by_year/", {
              'method': 'GET',
          })
          .then(resp => resp.json())
          .then(resp => setMedianByYear(resp))
          .catch(error => console.log(error))
      }, [])

      useEffect(() => {
        fetch("http://0.0.0.0:8000/count_rooms/", {
            'method': 'GET',
        })
        .then(resp => resp.json())
        .then(resp => setCountRooms(resp))
        .catch(error => console.log(error))
    }, [])

    return (
      <div>
        <Box py={20} textAlign="center">
          <Typography variant="h2">Analytics</Typography>
          <p/>


          <Plot data={[{
              y: meanByYear.map(row => row.MEAN),
              x: meanByYear.map(row => row.YEAR.toString()),
              type: 'bar',
              marker: {color: 'cornflowerblue'},
            }
          ]}
          layout={ {width: 720, height: 540, title: 'Mean price by year'} }/>

          <Plot data={[{
              y: medianByYear.map(row => row.MEDIAN),
              x: medianByYear.map(row => row.YEAR.toString()),
              type: 'scatter',
              marker: {color: 'cornflowerblue'},
            }
          ]}
          layout={ {width: 720, height: 540, title: 'Median price by year'} }/>


          <Plot data={[{
              y: countRooms.map(row => row.TOTAL),
              x: countRooms.map(row => row.ROOMS),
              type: 'bar',
              marker: {color: 'cornflowerblue'},
            }
          ]}
          layout={ {width: 720, height: 540, title: 'Number of apartments'} }/>


        </Box>
        {isMobile ? (
          <Grid container justify="space-between">
            <Grid item>
              <Button
                variant="contained"
                color="primary"
                component={Link}
                to="/"
              >
                <ChevronLeftIcon />
                <Typography variant="button">Apartments</Typography>
                <TableRowsIcon style={{ marginLeft: 15 }} />
              </Button>
            </Grid>
          </Grid>
        ) : (
          <></>
        )}
      </div>
    );
  };
export default Analytics;  