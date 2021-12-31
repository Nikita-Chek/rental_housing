// IMPORTING APIS
import React from "react";
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  useMediaQuery,
  Button,
  useScrollTrigger,
  Slide,
  Menu,
  MenuItem,
  ListItemIcon
} from "@material-ui/core";

import { makeStyles, useTheme } from "@material-ui/core/styles";
import { BrowserRouter, Route, Switch, Link } from "react-router-dom";

// IMPORTING ICONS
import MenuIcon from "@material-ui/icons/Menu";
import TableRowsIcon from '@mui/icons-material/TableRows';
import AnalyticsSharpIcon from '@mui/icons-material/AnalyticsSharp';

// REACT APP IMPORTS
import Apartments from "./pages/Apartments";
import Analytics from "./pages/Analytics";

// LOCAL-STYLING
const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1
  }
}));

function HideOnScroll(props) {
  const { children } = props;
  const trigger = useScrollTrigger();

  return (
    <Slide appear={false} direction={"down"} in={!trigger}>
      {children}
    </Slide>
  );
}

const Header = (props) => {
  const classes = useStyles();
  const [anchor, setAnchor] = React.useState(null);
  const open = Boolean(anchor);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const handleMenu = (event) => {
    setAnchor(event.currentTarget);
  };
  return (
    <div className={classes.root}>
      <HideOnScroll {...props}>
        <BrowserRouter>
          <AppBar>
            <Toolbar>
              <Typography
                variant="h5"
                component="p"
                color="textSecondary"
                className={classes.title}
              >
                Apartments Analitycs
              </Typography>
              {isMobile ? (
                <>
                  <IconButton
                    color="textPrimary"
                    className={classes.menuButton}
                    edge="start"
                    aria-label="menu"
                    onClick={handleMenu}
                  >
                    <MenuIcon />
                  </IconButton>
                  <Menu
                    id="menu-appbar"
                    anchorEl={anchor}
                    anchorOrigin={{
                      vertical: "top",
                      horizontal: "right"
                    }}
                    KeepMounted
                    transformOrigin={{
                      vertical: "top",
                      horizontal: "right"
                    }}
                    open={open}
                  >
                    <MenuItem
                      onClick={() => setAnchor(null)}
                      component={Link}
                      to="/"
                    >
                      <ListItemIcon>
                        <TableRowsIcon/>
                      </ListItemIcon>
                      <Typography variant="h6"> Table </Typography>
                    </MenuItem>

                    <MenuItem
                      onClick={() => setAnchor(null)}
                      component={Link}
                      to="/Analytics"
                    >
                      <ListItemIcon>
                        <AnalyticsSharpIcon/>
                      </ListItemIcon>
                      <Typography variant="h6"> Analytics</Typography>
                    </MenuItem>

                  </Menu>
                </>
              ) : (
                <div style={{ marginRight: "2rem" }}>
                  <Button
                    variant="text"
                    component={Link}
                    to="/"
                    color="default"
                  >
                    <TableRowsIcon/>
                    Table
                  </Button>

                  <Button
                    variant="text"
                    component={Link}
                    to="/Analytics"
                    color="default"
                  >
                    <AnalyticsSharpIcon/>
                    Analytics
                  </Button>
                </div>
              )}
            </Toolbar>
          </AppBar>
          <Switch>
            <Route exact path="/" component={Apartments} />
            <Route exact path="/Analytics" component={Analytics} />
          </Switch>
        </BrowserRouter>
      </HideOnScroll>
    </div>
  );
};
export default Header;