import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Layout from './components/Layout';
import PrivateRoute from './components/PrivateRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CreateWordCloud from './pages/CreateWordCloud';
import EditWordCloud from './pages/EditWordCloud';
import ViewWordCloud from './pages/ViewWordCloud';
import Profile from './pages/Profile';
import MfaSetup from './pages/MfaSetup';
import NotFound from './pages/NotFound';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* Public routes */}
          <Route index element={<Home />} />
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          
          {/* Protected routes */}
          <Route path="dashboard" element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } />
          <Route path="create" element={
            <PrivateRoute>
              <CreateWordCloud />
            </PrivateRoute>
          } />
          <Route path="edit/:id" element={
            <PrivateRoute>
              <EditWordCloud />
            </PrivateRoute>
          } />
          <Route path="view/:id" element={
            <PrivateRoute>
              <ViewWordCloud />
            </PrivateRoute>
          } />
          <Route path="profile" element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          } />
          <Route path="mfa-setup" element={
            <PrivateRoute>
              <MfaSetup />
            </PrivateRoute>
          } />
          
          {/* Fallback routes */}
          <Route path="404" element={<NotFound />} />
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Route>
      </Routes>
      
      <ToastContainer position="bottom-right" />
    </>
  );
}

export default App;
