import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useEffect, useState } from 'react';
import Button from '@material-ui/core/Button';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';


const styles = theme => ({
    margin: {
      margin: theme.spacing.unit,
    },
    extendedIcon: {
      marginRight: theme.spacing.unit,
    },
});


function ApartmentsTable(props) {
    const [apartments, setApartment] = useState([]);
    const { classes } = props;

    useEffect(() => {
            fetch("http://127.0.0.1:8000/apartments/page/1/", {
                'method': 'GET',
            })
            .then(resp => resp.json())
            .then(resp => setApartment(resp))
            .catch(error => console.log(error))
        }, [])

    const loadAll = () => {
        fetch("http://127.0.0.1:8000/apartments/", {
                'method': 'GET',
            })
            .then(resp => resp.json())
            .then(resp => setApartment(resp))
            .catch(error => console.log(error))
    }
    console.log(apartments);
    return (
<div>
    <Button variant="contained"
    size="large"
    fontSize="30px"
    color="primary"
    className={classes.margin}
    onClick={loadAll}>
        Load All
    </Button>
    <p/>
    <Paper>
        <Table>
          <TableHead>
            <TableRow>
                <TableCell align="right">Price</TableCell>
                <TableCell align="right">Address</TableCell>
                <TableCell align="right">Rooms</TableCell>
                <TableCell align="right">Owner</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>{
          apartments.map((row) => (
                    <TableRow
                    key={row.ID}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                        <TableCell align="right">{row.PRICE}</TableCell>
                        <TableCell align="right">{row.LOCATION_ADDRESS}</TableCell>
                        <TableCell align="right">{row.ROOMS}</TableCell>
                        <TableCell align="right">{row.OWNER}</TableCell>
                    </TableRow>))
                    }
          </TableBody>
        </Table>
    </Paper>
    </div>
    )
}

ApartmentsTable.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ApartmentsTable);