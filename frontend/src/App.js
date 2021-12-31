import Header from "./components/Header";
import { ThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import "fontsource-roboto";
import { Paper, Container } from "@material-ui/core";
import { lightBlue, orange } from "@material-ui/core/colors";


const theme = createMuiTheme({
  typography: {
    h1: {
      fontSize: "3rem"
    }
  },
  palette: {
    type: "dark",
    primary: {
      main: lightBlue[600]
    },
    secondary: {
      main: orange[400]
    }
  }
});


function App() {
  return (
    <ThemeProvider theme={theme}>
      <Paper > 
        {/* style={{ height: "500vh" }} */}
        <Container>
          <Header />
        </Container>
      </Paper>
    </ThemeProvider>
  );
}

export default App;