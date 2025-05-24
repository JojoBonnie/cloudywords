import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { wordCloudApi } from '../services/api';
import { toast } from 'react-toastify';

const ViewWordCloud = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [wordCloud, setWordCloud] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [exporting, setExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState('png');
  const [exportResolution, setExportResolution] = useState('medium');

  useEffect(() => {
    fetchWordCloud();
  }, [id]);

  const fetchWordCloud = async () => {
    try {
      setLoading(true);
      const response = await wordCloudApi.getById(id);
      setWordCloud(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching word cloud:', err);
      setError('Failed to load word cloud. It may have been deleted or you may not have permission to view it.');
      toast.error('Failed to load word cloud');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      setExporting(true);
      const response = await wordCloudApi.export(id, exportFormat, exportResolution);
      
      // Create a download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${wordCloud.title}.${exportFormat}`);
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast.success(`Word cloud exported as ${exportFormat.toUpperCase()}`);
    } catch (err) {
      console.error('Error exporting word cloud:', err);
      toast.error('Failed to export word cloud');
    } finally {
      setExporting(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this word cloud?')) {
      return;
    }

    try {
      await wordCloudApi.delete(id);
      toast.success('Word cloud deleted successfully');
      navigate('/dashboard');
    } catch (err) {
      console.error('Error deleting word cloud:', err);
      toast.error('Failed to delete word cloud');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{error}</p>
            </div>
            <div className="mt-4">
              <Link
                to="/dashboard"
                className="rounded-md bg-red-50 px-2 py-1.5 text-sm font-medium text-red-800 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2"
              >
                Go back to dashboard
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!wordCloud) {
    return null;
  }

  return (
    <div>
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">{wordCloud.title}</h1>
          <p className="mt-2 text-sm text-gray-500">
            Created: {formatDate(wordCloud.created_at)}
            {wordCloud.updated_at !== wordCloud.created_at && (
              <> • Updated: {formatDate(wordCloud.updated_at)}</>
            )}
          </p>
        </div>
        <div className="mt-4 flex sm:mt-0 sm:ml-4">
          <Link
            to={`/edit/${wordCloud.id}`}
            className="mr-3 inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            Edit
          </Link>
          <button
            type="button"
            onClick={handleDelete}
            className="inline-flex items-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600"
          >
            Delete
          </button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-x-8 gap-y-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="px-4 py-5 sm:p-6">
              {wordCloud.image_url ? (
                <img
                  src={wordCloud.image_url}
                  alt={wordCloud.title}
                  className="w-full rounded-md"
                />
              ) : (
                <div className="flex h-48 items-center justify-center rounded-md bg-gray-100">
                  <p className="text-gray-500">No image available</p>
                </div>
              )}
            </div>
          </div>
        </div>

        <div>
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-base font-semibold leading-6 text-gray-900">Word Cloud Details</h3>
              
              {/* Details List */}
              <dl className="mt-4 space-y-3">
                <div className="flex items-start">
                  <dt className="w-1/3 flex-shrink-0 text-sm font-medium text-gray-500">Type:</dt>
                  <dd className="text-sm text-gray-900">
                    {wordCloud.is_ai_generated ? (
                      <span className="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700">
                        AI Generated
                      </span>
                    ) : (
                      <span className="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600">
                        Manual
                      </span>
                    )}
                  </dd>
                </div>
                
                <div className="flex items-start">
                  <dt className="w-1/3 flex-shrink-0 text-sm font-medium text-gray-500">Dimensions:</dt>
                  <dd className="text-sm text-gray-900">{wordCloud.width} × {wordCloud.height} px</dd>
                </div>
                
                <div className="flex items-start">
                  <dt className="w-1/3 flex-shrink-0 text-sm font-medium text-gray-500">Font:</dt>
                  <dd className="text-sm text-gray-900">
                    {wordCloud.font.charAt(0).toUpperCase() + wordCloud.font.slice(1)}
                  </dd>
                </div>
                
                <div className="flex items-start">
                  <dt className="w-1/3 flex-shrink-0 text-sm font-medium text-gray-500">Color Scheme:</dt>
                  <dd className="text-sm text-gray-900">
                    {wordCloud.color_scheme.charAt(0).toUpperCase() + wordCloud.color_scheme.slice(1)}
                  </dd>
                </div>
                
                <div className="flex items-start">
                  <dt className="w-1/3 flex-shrink-0 text-sm font-medium text-gray-500">Background:</dt>
                  <dd className="flex items-center text-sm text-gray-900">
                    <div 
                      className="mr-2 h-4 w-4 rounded border border-gray-300"
                      style={{ backgroundColor: wordCloud.background_color }}
                    ></div>
                    {wordCloud.background_color}
                  </dd>
                </div>
                
                <div className="flex items-start">
                  <dt className="w-1/3 flex-shrink-0 text-sm font-medium text-gray-500">Max Words:</dt>
                  <dd className="text-sm text-gray-900">{wordCloud.max_words}</dd>
                </div>
                
                <div className="flex items-start">
                  <dt className="w-1/3 flex-shrink-0 text-sm font-medium text-gray-500">Density:</dt>
                  <dd className="text-sm text-gray-900">{wordCloud.word_density}%</dd>
                </div>
                
                <div className="flex items-start">
                  <dt className="w-1/3 flex-shrink-0 text-sm font-medium text-gray-500">Orientation:</dt>
                  <dd className="text-sm text-gray-900">
                    {wordCloud.orientation.charAt(0).toUpperCase() + wordCloud.orientation.slice(1)}
                  </dd>
                </div>
              </dl>
              
              {/* Export Section */}
              <div className="mt-6 border-t border-gray-100 pt-4">
                <h4 className="text-sm font-medium text-gray-900">Export Word Cloud</h4>
                
                <div className="mt-3 grid grid-cols-2 gap-3">
                  <div>
                    <label htmlFor="exportFormat" className="block text-xs font-medium text-gray-700">
                      Format
                    </label>
                    <select
                      id="exportFormat"
                      name="exportFormat"
                      value={exportFormat}
                      onChange={(e) => setExportFormat(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 py-1.5 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    >
                      <option value="png">PNG Image</option>
                      <option value="svg">SVG Vector</option>
                    </select>
                  </div>
                  
                  <div>
                    <label htmlFor="exportResolution" className="block text-xs font-medium text-gray-700">
                      Resolution
                    </label>
                    <select
                      id="exportResolution"
                      name="exportResolution"
                      value={exportResolution}
                      onChange={(e) => setExportResolution(e.target.value)}
                      className="mt-1 block w-full rounded-md border-gray-300 py-1.5 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>
                </div>
                
                <button
                  type="button"
                  onClick={handleExport}
                  disabled={exporting}
                  className="mt-3 w-full rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:bg-primary-400"
                >
                  {exporting ? 'Exporting...' : `Export as ${exportFormat.toUpperCase()}`}
                </button>
              </div>
            </div>
          </div>
          
          <div className="mt-4 overflow-hidden rounded-lg bg-white shadow">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-base font-semibold leading-6 text-gray-900">Input Text</h3>
              <div className="mt-2">
                <div className="max-h-60 overflow-y-auto rounded-md bg-gray-50 p-2 text-sm text-gray-700">
                  {wordCloud.input_text.split('\n').map((line, i) => (
                    <p key={i} className="mb-1">
                      {line || <br />}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewWordCloud;
