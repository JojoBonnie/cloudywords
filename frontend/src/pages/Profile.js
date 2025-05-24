import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';

const Profile = () => {
  const { currentUser, userCredits } = useAuth();
  const [loading, setLoading] = useState(false);
  
  if (!currentUser) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Profile</h1>
          <p className="mt-2 text-sm text-gray-700">
            Your account information and preferences
          </p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-x-8 gap-y-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-base font-semibold leading-6 text-gray-900">Account Information</h3>
              
              <dl className="mt-4 space-y-4">
                <div className="flex items-center">
                  <dt className="w-1/4 flex-shrink-0 text-sm font-medium text-gray-500">Username:</dt>
                  <dd className="text-sm text-gray-900">{currentUser.username}</dd>
                </div>
                
                <div className="flex items-center">
                  <dt className="w-1/4 flex-shrink-0 text-sm font-medium text-gray-500">Email:</dt>
                  <dd className="text-sm text-gray-900">{currentUser.email}</dd>
                </div>
                
                <div className="flex items-center">
                  <dt className="w-1/4 flex-shrink-0 text-sm font-medium text-gray-500">Joined:</dt>
                  <dd className="text-sm text-gray-900">
                    {new Date(currentUser.date_joined).toLocaleDateString(undefined, {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </dd>
                </div>
              </dl>
            </div>
          </div>
          
          <div className="mt-6 overflow-hidden rounded-lg bg-white shadow">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-base font-semibold leading-6 text-gray-900">Multi-Factor Authentication</h3>
              
              <div className="mt-4">
                <p className="text-sm text-gray-500">
                  Multi-factor authentication adds an extra layer of security to your account by requiring
                  a verification code in addition to your password when you sign in.
                </p>
                
                <div className="mt-4">
                  {currentUser.profile?.mfa_enabled ? (
                    <div className="flex items-center">
                      <svg className="h-5 w-5 text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      <span className="ml-2 text-sm text-gray-900">MFA is enabled for your account</span>
                    </div>
                  ) : (
                    <div className="flex items-center">
                      <svg className="h-5 w-5 text-yellow-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                      <span className="ml-2 text-sm text-gray-900">MFA is not enabled for your account</span>
                    </div>
                  )}
                  
                  <div className="mt-4">
                    <Link
                      to="/mfa-setup"
                      className="inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
                    >
                      {currentUser.profile?.mfa_enabled ? 'Manage MFA Settings' : 'Set Up MFA'}
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-base font-semibold leading-6 text-gray-900">AI Credits</h3>
              
              <div className="mt-4">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="relative h-16 w-16 overflow-hidden rounded-full bg-primary-100">
                      <svg className="h-10 w-10 absolute inset-3 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-5">
                    <h4 className="text-lg font-bold text-gray-900">{userCredits}</h4>
                    <p className="text-sm text-gray-500">Credits Remaining</p>
                  </div>
                </div>
                
                <div className="mt-6">
                  <p className="text-sm text-gray-500">
                    AI credits are used when generating word suggestions with AI.
                    Each AI generation costs 1 credit.
                  </p>
                  
                  <button
                    type="button"
                    onClick={() => toast.info('Purchase functionality coming soon!')}
                    className="mt-4 inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  >
                    Purchase More Credits
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-6 overflow-hidden rounded-lg bg-white shadow">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-base font-semibold leading-6 text-gray-900">Account Actions</h3>
              
              <div className="mt-4 space-y-4">
                <button
                  type="button"
                  onClick={() => toast.info('This feature is coming soon!')}
                  className="inline-flex w-full justify-center items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                >
                  Change Password
                </button>
                
                <button
                  type="button"
                  onClick={() => toast.info('This feature is coming soon!')}
                  className="inline-flex w-full justify-center items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                >
                  Export My Data
                </button>
                
                <button
                  type="button"
                  onClick={() => toast.info('This feature is coming soon!')}
                  className="inline-flex w-full justify-center items-center rounded-md bg-red-50 px-3 py-2 text-sm font-semibold text-red-700 shadow-sm ring-1 ring-inset ring-red-200 hover:bg-red-100"
                >
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
