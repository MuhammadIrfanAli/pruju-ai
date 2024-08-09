import React, { useEffect, useState } from 'react';
// import { Box, Button, TextField, Typography, Container } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../constants';

// src/Dashboard.js
// import React from 'react';
import { Box, Stack, Card, AppBar, Toolbar, Typography, CssBaseline, Drawer, List, ListItem, ListItemText, Divider } from '@mui/material';
import { Outlet } from 'react-router-dom'; // If using react-router
// import AppBar from '@mui/material';


const drawerWidth = 240;

const Dashboard = () => {
  // const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const apiToken = localStorage.getItem('token');

  const getInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/users/me/`,  {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiToken}`

        }});
        setUsername(response.data.username)
    } catch (error) {
    }
  };


  useEffect(()=>{
    getInfo()
  }, [])

  return (
    <AppBar sx={{background: 'none', padding: '16px', boxShadow: 'none', color: 'primary'}}>
      <Typography variant="h6" >
       Pruju
      </Typography>
      <Stack direction="row"  sx={{width: '100%' }}>
        <Stack direction="column" >
          <Card variant="outlined">Vector</Card>
        </Stack>
        <Stack direction="column" sx={{width: '70%' }}>
          <Card variant="outlined">Details</Card>
        </Stack>

      </Stack>
    </AppBar>

  );
};

export default Dashboard;



// const Dashboard = () => {
//   const navigate = useNavigate();
//   const [username, setUsername] = useState('');
//   const apiToken = localStorage.getItem('token');

//   const getInfo = async () => {
//     try {
//       const response = await axios.get(`${API_URL}/users/me/`,  {
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': `Bearer ${apiToken}`

//         }});
//         setUsername(response.data.username)
//     } catch (error) {
//     }
//   };


//   useEffect(()=>{
//     if(!apiToken) navigate('/login')
//     getInfo()
//   }, [])

//   return (
//     <Container maxWidth="xs">
//       Username: {username}
//     </Container>
//   );
// };

// export default Dashboard;
