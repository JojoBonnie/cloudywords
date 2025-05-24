import React, { useState, useEffect } from 'react';

const WordCloudPreview = ({ imageUrl, title, isLoading }) => {
  const [error, setError] = useState(false);

  useEffect(() => {
    setError(false);
  }, [imageUrl]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg bg-gray-50 min-h-[300px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500 mb-4"></div>
        <p className="text-gray-500">Generating word cloud...</p>
      </div>
    );
  }

  if (!imageUrl) {
    return (
      <div className="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg bg-gray-50 min-h-[300px]">
        <p className="text-gray-500">Preview will appear here</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg bg-white shadow">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">
          {title || 'Word Cloud Preview'}
        </h3>
        <div className="word-cloud-container">
          {error ? (
            <div className="flex flex-col items-center justify-center p-4 border border-gray-200 rounded-lg bg-gray-50 min-h-[300px]">
              <p className="text-red-500">Failed to load image</p>
            </div>
          ) : (
            <img
              src={imageUrl}
              alt="Word Cloud"
              className="max-w-full rounded-md"
              onError={() => setError(true)}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default WordCloudPreview;
