import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';

const MfaSetup = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  
  const [qrCode, setQrCode] = useState('');
  const [secretKey, setSecretKey] = useState('');
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [disabling, setDisabling] = useState(false);
  const [error, setError] = useState('');
  const [isMfaEnabled, setIsMfaEnabled] = useState(false);

  useEffect(() => {
    if (currentUser?.profile?.mfa_enabled) {
      setIsMfaEnabled(true);
    } else {
      fetchMfaSetup();
    }
  }, [currentUser]);

  const fetchMfaSetup = async () => {
    try {
      setLoading(true);
      const response = await authApi.setupMFA();
      setQrCode(response.data.qr_code);
      setSecretKey(response.data.secret_key);
      setError('');
    } catch (err) {
      console.error('Error setting up MFA:', err);
      setError('Failed to set up MFA. Please try again.');
      toast.error('Failed to set up MFA');
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (e) => {
    e.preventDefault();
    
    if (!token || token.length !== 6) {
      toast.error('Please enter a valid 6-digit token');
      return;
    }
    
    try {
      setLoading(true);
      await authApi.verifyMFA(token);
      setIsMfaEnabled(true);
      toast.success('MFA has been successfully enabled');
    } catch (err) {
      console.error('Error verifying MFA token:', err);
      setError('Invalid token. Please try again.');
      toast.error('Invalid token');
    } finally {
      setLoading(false);
    }
  };

  const handleDisableMfa = async () => {
    if (!window.confirm('Are you sure you want to disable MFA? This will make your account less secure.')) {
      return;
    }
    
    try {
      setDisabling(true);
      await authApi.disableMFA();
      setIsMfaEnabled(false);
      toast.success('MFA has been disabled');
      navigate('/profile');
    } catch (err) {
      console.error('Error disabling MFA:', err);
      toast.error('Failed to disable MFA');
    } finally {
      setDisabling(false);
    }
  };

  const handleCancel = () => {
    navigate('/profile');
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
          Multi-Factor Authentication
        </h1>
        <p className="mt-2 text-sm text-gray-700">
          {isMfaEnabled 
            ? 'Manage your multi-factor authentication settings' 
            : 'Set up multi-factor authentication to add an extra layer of security to your account'}
        </p>
      </div>

      <div className="mt-6 overflow-hidden rounded-lg bg-white shadow">
        {isMfaEnabled ? (
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center">
              <svg className="h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <h3 className="ml-2 text-lg font-medium leading-6 text-gray-900">MFA is Enabled</h3>
            </div>
            
            <div className="mt-4">
              <p className="text-sm text-gray-500">
                Your account is secured with multi-factor authentication. When you sign in,
                you'll be asked to provide a verification code from your authenticator app.
              </p>
              
              <div className="mt-6">
                <button
                  type="button"
                  onClick={handleDisableMfa}
                  disabled={disabling}
                  className="inline-flex items-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600 disabled:bg-red-400"
                >
                  {disabling ? 'Disabling...' : 'Disable MFA'}
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="ml-3 inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                >
                  Back to Profile
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-base font-semibold leading-6 text-gray-900">Set Up MFA</h3>
            
            {loading && !qrCode ? (
              <div className="mt-4 flex justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
              </div>
            ) : (
              <div className="mt-4">
                <p className="text-sm text-gray-500">
                  1. Scan the QR code below with an authenticator app like Google Authenticator or Authy.
                </p>
                
                <div className="mt-4 flex justify-center">
                  {qrCode && (
                    <img
                      src={`data:image/png;base64,${qrCode}`}
                      alt="QR Code for MFA setup"
                      className="h-48 w-48 rounded-md border border-gray-300"
                    />
                  )}
                </div>
                
                <p className="mt-4 text-sm text-gray-500">
                  2. If you can't scan the QR code, enter this key manually in your authenticator app:
                </p>
                
                <div className="mt-2 rounded-md bg-gray-50 px-3 py-2 text-center">
                  <code className="text-sm font-mono text-gray-900">{secretKey}</code>
                </div>
                
                <p className="mt-4 text-sm text-gray-500">
                  3. Enter the verification code from your authenticator app:
                </p>
                
                <form className="mt-2" onSubmit={handleVerify}>
                  <div className="flex items-center">
                    <input
                      type="text"
                      inputMode="numeric"
                      pattern="[0-9]*"
                      maxLength="6"
                      value={token}
                      onChange={(e) => setToken(e.target.value.replace(/[^0-9]/g, ''))}
                      className="block rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      placeholder="6-digit code"
                    />
                    
                    <button
                      type="submit"
                      disabled={loading || token.length !== 6}
                      className="ml-3 inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:bg-primary-400"
                    >
                      {loading ? 'Verifying...' : 'Verify'}
                    </button>
                  </div>
                  
                  {error && (
                    <p className="mt-2 text-sm text-red-600">{error}</p>
                  )}
                </form>
                
                <div className="mt-6">
                  <button
                    type="button"
                    onClick={handleCancel}
                    className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default MfaSetup;
