import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { wordCloudApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';

const Dashboard = () => {
  const [wordClouds, setWordClouds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { userCredits } = useAuth();

  useEffect(() => {
    fetchWordClouds();
  }, []);

  const fetchWordClouds = async () => {
    try {
      setLoading(true);
      const response = await wordCloudApi.getAll();
      setWordClouds(response.data.results || response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching word clouds:', err);
      setError('Failed to load your word clouds. Please try again.');
      toast.error('Failed to load your word clouds');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this word cloud?')) {
      return;
    }

    try {
      await wordCloudApi.delete(id);
      setWordClouds(wordClouds.filter(cloud => cloud.id !== id));
      toast.success('Word cloud deleted successfully');
    } catch (err) {
      console.error('Error deleting word cloud:', err);
      toast.error('Failed to delete word cloud');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
  };

  return (
    <div>
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Dashboard</h1>
          <p className="mt-2 text-sm text-gray-700">
            Your word cloud creations and AI credits
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:flex sm:items-center">
          <div className="mr-4 rounded-md bg-white px-3 py-2 text-sm font-medium text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300">
            <span className="text-gray-500">AI Credits:</span> {userCredits}
          </div>
          <Link
            to="/create"
            className="block rounded-md bg-primary-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
          >
            Create New
          </Link>
        </div>
      </div>

      {loading ? (
        <div className="mt-6 flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
        </div>
      ) : error ? (
        <div className="mt-6 rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      ) : wordClouds.length === 0 ? (
        <div className="mt-6 text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-semibold text-gray-900">No word clouds</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new word cloud.</p>
          <div className="mt-6">
            <Link
              to="/create"
              className="inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
            >
              <svg className="-ml-0.5 mr-1.5 h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path d="M10.75 4.75a.75.75 0 00-1.5 0v4.5h-4.5a.75.75 0 000 1.5h4.5v4.5a.75.75 0 001.5 0v-4.5h4.5a.75.75 0 000-1.5h-4.5v-4.5z" />
              </svg>
              Create Word Cloud
            </Link>
          </div>
        </div>
      ) : (
        <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {wordClouds.map((wordCloud) => (
            <div
              key={wordCloud.id}
              className="overflow-hidden rounded-lg bg-white shadow"
            >
              <div className="p-5">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium leading-6 text-gray-900">{wordCloud.title}</h3>
                  {wordCloud.is_ai_generated && (
                    <span className="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700">
                      AI Generated
                    </span>
                  )}
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  Created: {formatDate(wordCloud.created_at)}
                </p>
              </div>
              <div className="px-5 pb-3">
                <div className="aspect-w-16 aspect-h-9 overflow-hidden rounded bg-gray-50">
                  {wordCloud.image_url ? (
                    <img
                      src={wordCloud.image_url}
                      alt={wordCloud.title}
                      className="h-full w-full object-contain"
                    />
                  ) : (
                    <div className="flex h-full items-center justify-center">
                      <p className="text-sm text-gray-500">No preview available</p>
                    </div>
                  )}
                </div>
              </div>
              <div className="bg-gray-50 px-5 py-3">
                <div className="flex justify-between">
                  <div className="flex space-x-3">
                    <Link
                      to={`/view/${wordCloud.id}`}
                      className="text-sm font-medium text-primary-600 hover:text-primary-500"
                    >
                      View
                    </Link>
                    <Link
                      to={`/edit/${wordCloud.id}`}
                      className="text-sm font-medium text-primary-600 hover:text-primary-500"
                    >
                      Edit
                    </Link>
                  </div>
                  <button
                    onClick={() => handleDelete(wordCloud.id)}
                    className="text-sm font-medium text-red-600 hover:text-red-500"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
