import {
    Box,
    Typography,
    useMediaQuery,
    Button,
    Grid
} from "@material-ui/core";
import { Link } from "react-router-dom";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import AnalyticsSharpIcon from '@mui/icons-material/AnalyticsSharp';


import ApartmentsTable from "../Table"
  
const Apartments = () => {
    const isMobile = useMediaQuery((theme) => theme.breakpoints.down("sm"));
  
    return (
      <div>
        <Box py={20} textAlign="center">
          <Typography variant="h2">Apartments</Typography>
          <p></p>
          <ApartmentsTable/>
        </Box>
        {isMobile ? (
          <Grid container justify="space-between">
            <Grid item>
              <Button
                variant="contained"
                color="primary"
                component={Link}
                to="/Analytics"
              >
                <AnalyticsSharpIcon style={{ marginRight: 15 }} />
                <Typography variant="button">Analytics</Typography>
                <ChevronRightIcon />
              </Button>
            </Grid>
          </Grid>
        ) : (
          <></>
        )}
      </div>
    );
};
export default Apartments;  