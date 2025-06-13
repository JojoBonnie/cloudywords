import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { HexColorPicker } from 'react-colorful';
import { wordCloudApi, aiApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import WordCloudPreview from '../components/WordCloudPreview';

const CreateWordCloud = () => {
  const navigate = useNavigate();
  const { userCredits, updateCredits } = useAuth();
  
  const [formData, setFormData] = useState({
    title: '',
    input_text: '',
    is_ai_generated: false,
    width: 800,
    height: 400,
    font: 'arial',
    color_scheme: 'default',
    background_color: 'white',
    max_words: 200,
    word_density: 80,
    orientation: 'random'
  });
  
  const [aiTopic, setAiTopic] = useState('');
  const [aiCount, setAiCount] = useState(100);
  const [showColorPicker, setShowColorPicker] = useState(false);
  const [generatedWordCloud, setGeneratedWordCloud] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleColorChange = (color) => {
    setFormData({
      ...formData,
      background_color: color
    });
  };

  const handleAiGenerate = async (e) => {
    e.preventDefault();
    
    if (!aiTopic) {
      toast.error('Please enter a topic for AI generation');
      return;
    }
    
    if (userCredits <= 0) {
      toast.error('You have no AI credits remaining. Please purchase more credits.');
      return;
    }
    
    try {
      setAiLoading(true);
      setError(null);
      
      const response = await aiApi.getWordSuggestions(aiTopic, aiCount);
      console.log('AI response:', response.data);
      setFormData({
        ...formData,
        input_text: response.data.words.join(', '),
        is_ai_generated: true
      });
      
      await updateCredits();
      toast.success('AI words generated successfully');
      
    } catch (err) {
      console.error('Error generating AI words:', err);
      setError('Failed to generate AI words. Please try again.');
      toast.error(err.response?.data?.error || 'Failed to generate AI words');
    } finally {
      setAiLoading(false);
    }
  };

  const handleGenerateWordCloud = async (e) => {
    e.preventDefault();
    
    if (!formData.title) {
      toast.error('Please enter a title for your word cloud');
      return;
    }
    
    if (!formData.input_text) {
      toast.error('Please enter text or generate words with AI');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await wordCloudApi.generate(formData);
      setGeneratedWordCloud(response.data);
      
      toast.success('Word cloud generated successfully');
      
    } catch (err) {
      console.error('Error generating word cloud:', err);
      setError('Failed to generate word cloud. Please try again.');
      toast.error(err.response?.data?.error || 'Failed to generate word cloud');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = () => {
    navigate(`/view/${generatedWordCloud.id}`);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="md:grid md:grid-cols-3 md:gap-6">
        <div className="md:col-span-1">
          <div className="px-4 sm:px-0">
            <h3 className="text-lg font-medium leading-6 text-gray-900">Create Word Cloud</h3>
            <p className="mt-1 text-sm text-gray-600">
              Enter text manually or generate words with AI to create your word cloud.
            </p>
            
            {/* AI Credits Section */}
            <div className="mt-6 rounded-md bg-blue-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-blue-800">AI Credits Available</h3>
                  <div className="mt-2 text-sm text-blue-700">
                    <p>You have {userCredits} AI credits remaining.</p>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Word Cloud Preview */}
            <div className="mt-6">
              <WordCloudPreview 
                imageUrl={generatedWordCloud?.image_url} 
                title={formData.title || 'Preview'} 
                isLoading={loading}
              />
            </div>
          </div>
        </div>
        
        <div className="mt-5 md:col-span-2 md:mt-0">
          <div className="shadow sm:overflow-hidden sm:rounded-md">
            <div className="space-y-6 bg-white px-4 py-5 sm:p-6">
              {/* Basic Info */}
              <div>
                <h3 className="text-lg font-medium leading-6 text-gray-900">Basic Information</h3>
                <div className="mt-2 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                  <div className="sm:col-span-4">
                    <label htmlFor="title" className="block text-sm font-medium leading-6 text-gray-900">
                      Title
                    </label>
                    <div className="mt-2">
                      <input
                        type="text"
                        name="title"
                        id="title"
                        value={formData.title}
                        onChange={handleInputChange}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      />
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Word Input */}
              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-lg font-medium leading-6 text-gray-900">Word Input</h3>
                
                {/* AI Generation */}
                <div className="mt-4 rounded-md bg-gray-50 p-4">
                  <h4 className="text-sm font-medium text-gray-900">AI-Generated Words</h4>
                  <div className="mt-2 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                    <div className="sm:col-span-3">
                      <label htmlFor="aiTopic" className="block text-sm font-medium leading-6 text-gray-900">
                        Topic
                      </label>
                      <div className="mt-2">
                        <input
                          type="text"
                          id="aiTopic"
                          value={aiTopic}
                          onChange={(e) => setAiTopic(e.target.value)}
                          disabled={aiLoading}
                          placeholder="e.g., Climate Change, Space Exploration"
                          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                        />
                      </div>
                    </div>
                    <div className="sm:col-span-2">
                      <label htmlFor="aiCount" className="block text-sm font-medium leading-6 text-gray-900">
                        Word Count
                      </label>
                      <div className="mt-2">
                        <input
                          type="number"
                          id="aiCount"
                          value={aiCount}
                          onChange={(e) => setAiCount(Math.max(10, Math.min(500, parseInt(e.target.value) || 100)))}
                          disabled={aiLoading}
                          min="10"
                          max="500"
                          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                        />
                      </div>
                    </div>
                    <div className="sm:col-span-1">
                      <label htmlFor="aiGenerate" className="block text-sm font-medium leading-6 text-gray-900">
                        &nbsp;
                      </label>
                      <button
                        type="button"
                        id="aiGenerate"
                        onClick={handleAiGenerate}
                        disabled={aiLoading || !aiTopic || userCredits <= 0}
                        className="mt-2 inline-flex items-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
                      >
                        {aiLoading ? (
                          <>
                            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Generating...
                          </>
                        ) : (
                          'Generate'
                        )}
                      </button>
                    </div>
                  </div>
                </div>
                
                {/* Manual Text Input */}
                <div className="mt-4">
                  <label htmlFor="input_text" className="block text-sm font-medium leading-6 text-gray-900">
                    Text Input
                  </label>
                  <div className="mt-2">
                    <textarea
                      id="input_text"
                      name="input_text"
                      rows={5}
                      value={formData.input_text}
                      onChange={handleInputChange}
                      className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      placeholder="Enter text or use AI generation above"
                    />
                  </div>
                  <p className="mt-2 text-sm text-gray-500">
                    Enter text from which to generate the word cloud. Words that appear more frequently will be larger.
                  </p>
                </div>
              </div>
              
              {/* Customization Options */}
              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-lg font-medium leading-6 text-gray-900">Customization Options</h3>
                
                <div className="mt-2 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                  {/* Dimensions */}
                  <div className="sm:col-span-3">
                    <label htmlFor="width" className="block text-sm font-medium leading-6 text-gray-900">
                      Width (pixels)
                    </label>
                    <div className="mt-2">
                      <input
                        type="number"
                        name="width"
                        id="width"
                        min="100"
                        max="2000"
                        value={formData.width}
                        onChange={handleInputChange}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      />
                    </div>
                  </div>
                  
                  <div className="sm:col-span-3">
                    <label htmlFor="height" className="block text-sm font-medium leading-6 text-gray-900">
                      Height (pixels)
                    </label>
                    <div className="mt-2">
                      <input
                        type="number"
                        name="height"
                        id="height"
                        min="100"
                        max="2000"
                        value={formData.height}
                        onChange={handleInputChange}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      />
                    </div>
                  </div>
                  
                  {/* Font and Color */}
                  <div className="sm:col-span-3">
                    <label htmlFor="font" className="block text-sm font-medium leading-6 text-gray-900">
                      Font
                    </label>
                    <div className="mt-2">
                      <select
                        id="font"
                        name="font"
                        value={formData.font}
                        onChange={handleInputChange}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      >
                        <option value="arial">Arial</option>
                        <option value="times">Times New Roman</option>
                        <option value="courier">Courier New</option>
                        <option value="verdana">Verdana</option>
                        <option value="georgia">Georgia</option>
                        <option value="trebuchet">Trebuchet MS</option>
                        <option value="comic">Comic Sans MS</option>
                      </select>
                    </div>
                  </div>
                  
                  <div className="sm:col-span-3">
                    <label htmlFor="color_scheme" className="block text-sm font-medium leading-6 text-gray-900">
                      Color Scheme
                    </label>
                    <div className="mt-2">
                      <select
                        id="color_scheme"
                        name="color_scheme"
                        value={formData.color_scheme}
                        onChange={handleInputChange}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      >
                        <option value="Default">Default</option>
                        <option value="Blues">Blues</option>
                        <option value="Reds">Reds</option>
                        <option value="Greens">Greens</option>
                        <option value="Purples">Purples</option>
                        <option value="Oranges">Oranges</option>
                        <option value="Greys">Greys</option>
                        <option value="Rainbow">Rainbow</option>
                      </select>
                    </div>
                  </div>
                  
                  {/* Background Color */}
                  <div className="sm:col-span-3">
                    <label htmlFor="background_color" className="block text-sm font-medium leading-6 text-gray-900">
                      Background Color
                    </label>
                    <div className="mt-2 relative">
                      <input
                        type="text"
                        name="background_color"
                        id="background_color"
                        value={formData.background_color}
                        onChange={handleInputChange}
                        onClick={() => setShowColorPicker(!showColorPicker)}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      />
                      <div 
                        className="w-6 h-6 absolute right-2 top-1.5 rounded border border-gray-300 cursor-pointer"
                        style={{ backgroundColor: formData.background_color }}
                        onClick={() => setShowColorPicker(!showColorPicker)}
                      ></div>
                      {showColorPicker && (
                        <div className="absolute z-10 mt-2">
                          <div 
                            className="fixed inset-0" 
                            onClick={() => setShowColorPicker(false)}
                          ></div>
                          <HexColorPicker
                            color={formData.background_color}
                            onChange={handleColorChange}
                          />
                        </div>
                      )}
                    </div>
                  </div>
                  
                  {/* Word Options */}
                  <div className="sm:col-span-3">
                    <label htmlFor="max_words" className="block text-sm font-medium leading-6 text-gray-900">
                      Maximum Words
                    </label>
                    <div className="mt-2">
                      <input
                        type="number"
                        name="max_words"
                        id="max_words"
                        min="10"
                        max="1000"
                        value={formData.max_words}
                        onChange={handleInputChange}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      />
                    </div>
                  </div>
                  
                  <div className="sm:col-span-3">
                    <label htmlFor="word_density" className="block text-sm font-medium leading-6 text-gray-900">
                      Word Density (%)
                    </label>
                    <div className="mt-2">
                      <input
                        type="range"
                        name="word_density"
                        id="word_density"
                        min="10"
                        max="100"
                        value={formData.word_density}
                        onChange={handleInputChange}
                        className="block w-full"
                      />
                      <div className="mt-1 text-center text-sm text-gray-500">
                        {formData.word_density}%
                      </div>
                    </div>
                  </div>
                  
                  <div className="sm:col-span-3">
                    <label htmlFor="orientation" className="block text-sm font-medium leading-6 text-gray-900">
                      Word Orientation
                    </label>
                    <div className="mt-2">
                      <select
                        id="orientation"
                        name="orientation"
                        value={formData.orientation}
                        onChange={handleInputChange}
                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-primary-600 sm:text-sm sm:leading-6"
                      >
                        <option value="horizontal">Horizontal</option>
                        <option value="vertical">Vertical</option>
                        <option value="random">Random</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {error && (
              <div className="bg-red-50 px-4 py-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}
            
            <div className="bg-gray-50 px-4 py-3 text-right sm:px-6">
              {generatedWordCloud ? (
                <button
                  type="button"
                  onClick={handleSave}
                  className="inline-flex justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
                >
                  View Word Cloud
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleGenerateWordCloud}
                  disabled={loading || !formData.title || !formData.input_text}
                  className="inline-flex justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Generating...
                    </>
                  ) : (
                    'Generate Word Cloud'
                  )}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateWordCloud;
