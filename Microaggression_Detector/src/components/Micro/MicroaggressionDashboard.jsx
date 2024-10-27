import React, { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  TextField,
  Card,
  CardContent,
} from "@mui/material";
import { makeStyles } from "@mui/styles";

const useStyles = makeStyles((theme) => ({
  container: {
    padding: theme.spacing(3),
    backgroundColor: theme.palette.background.default,
  },
  card: {
    marginBottom: theme.spacing(3),
    borderRadius: theme.shape.borderRadius,
    boxShadow: theme.shadows[5],
    transition: "transform 0.2s, box-shadow 0.2s",
    "&:hover": {
      transform: "translateY(-2px)",
      boxShadow: theme.shadows[10],
    },
  },
  title: {
    marginBottom: theme.spacing(2),
    color: theme.palette.primary.main,
    fontWeight: 700,
  },
  header: {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.common.white,
  },
  cell: {
    fontWeight: 500,
  },
  filter: {
    marginBottom: theme.spacing(2),
  },
  emptyMessage: {
    padding: theme.spacing(2),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },
  stripedRow: {
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover,
    },
    "&:hover": {
      backgroundColor: theme.palette.grey[200],
      cursor: "pointer",
    },
  },
  tableContainer: {
    maxHeight: 500,
    overflowY: "auto",
  },
}));

const initialData = [
  {
    userId: 1,
    email: "user1@example.com",
    nonMicroAggression: 5,
    moderateMicroAggression: 2,
    highMicroAggression: 1,
  },
  {
    userId: 2,
    email: "user2@example.com",
    nonMicroAggression: 3,
    moderateMicroAggression: 4,
    highMicroAggression: 0,
  },
  {
    userId: 3,
    email: "user3@example.com",
    nonMicroAggression: 8,
    moderateMicroAggression: 1,
    highMicroAggression: 3,
  },
  {
    userId: 4,
    email: "user4@example.com",
    nonMicroAggression: 2,
    moderateMicroAggression: 3,
    highMicroAggression: 1,
  },
  {
    userId: 5,
    email: "user5@example.com",
    nonMicroAggression: 6,
    moderateMicroAggression: 1,
    highMicroAggression: 4,
  },
  {
    userId: 6,
    email: "user6@example.com",
    nonMicroAggression: 4,
    moderateMicroAggression: 5,
    highMicroAggression: 2,
  },
  {
    userId: 7,
    email: "user7@example.com",
    nonMicroAggression: 7,
    moderateMicroAggression: 2,
    highMicroAggression: 1,
  },
  {
    userId: 8,
    email: "user8@example.com",
    nonMicroAggression: 1,
    moderateMicroAggression: 3,
    highMicroAggression: 0,
  },
  {
    userId: 9,
    email: "user9@example.com",
    nonMicroAggression: 5,
    moderateMicroAggression: 0,
    highMicroAggression: 5,
  },
  {
    userId: 10,
    email: "user10@example.com",
    nonMicroAggression: 9,
    moderateMicroAggression: 1,
    highMicroAggression: 2,
  },
];

const MessageDashboard = () => {
  const classes = useStyles();
  const [filter, setFilter] = useState("");

  const filteredData = initialData.filter((row) =>
    row.email.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className={classes.container}>
      <Typography variant="h4" className={classes.title}>
        User Message Dashboard
      </Typography>
      <Card className={classes.card}>
        <CardContent>
          <TextField
            variant="outlined"
            placeholder="Filter by email..."
            fullWidth
            className={classes.filter}
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
          <TableContainer component={Paper} className={classes.tableContainer}>
            <Table stickyHeader>
              <TableHead>
                <TableRow className={classes.header}>
                  <TableCell>User ID</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Non-Micro-Aggression</TableCell>
                  <TableCell>Moderate Micro-Aggression</TableCell>
                  <TableCell>High Micro-Aggression</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredData.length > 0 ? (
                  filteredData.map((row) => (
                    <TableRow key={row.userId} className={classes.stripedRow}>
                      <TableCell className={classes.cell}>
                        {row.userId}
                      </TableCell>
                      <TableCell className={classes.cell}>
                        {row.email}
                      </TableCell>
                      <TableCell className={classes.cell}>
                        {row.nonMicroAggression}
                      </TableCell>
                      <TableCell className={classes.cell}>
                        {row.moderateMicroAggression}
                      </TableCell>
                      <TableCell className={classes.cell}>
                        {row.highMicroAggression}
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={5} className={classes.emptyMessage}>
                      No results found.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </div>
  );
};

export default MessageDashboard;
