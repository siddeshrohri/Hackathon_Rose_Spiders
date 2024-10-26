import React from "react";
import MessageDashboard from "./components/MicroaggressionDashboard";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3f51b5", // Customize the primary color
    },
  },
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div style={{ padding: "20px" }}>
        <MessageDashboard />
      </div>
    </ThemeProvider>
  );
};

export default App;
