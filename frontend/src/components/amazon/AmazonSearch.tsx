'use client';

import { useState } from 'react';
import { searchAmazonProducts, syncProductFromAmazon } from '@/lib/api';

interface AmazonProduct {
  asin: string;
  title: string;
  price: number;
  currency: string;
  rating: number;
  review_count: number;
  category: string;
  brand: string;
  availability: boolean;
  image_url?: string;
  product_url?: string;
  description: string;
}

interface SearchResult {
  query: string;
  total_results: number;
  products: AmazonProduct[];
}

export default function AmazonSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult | null>(null);
  const [searching, setSearching] = useState(false);
  const [syncing, setSyncing] = useState<string | null>(null);
  const [message, setMessage] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setSearching(true);
    setMessage('');
    
    try {
      const results = await searchAmazonProducts(searchQuery);
      setSearchResults(results);
      
      if (results.total_results === 0) {
        setMessage('No products found. Make sure Amazon API key is configured.');
      }
    } catch (error) {
      console.error('Search failed:', error);
      setMessage('Search failed. Please check if Amazon API is properly configured.');
      setSearchResults(null);
    } finally {
      setSearching(false);
    }
  };

  const handleSync = async (asin: string) => {
    setSyncing(asin);
    setMessage('');
    
    try {
      await syncProductFromAmazon(asin);
      setMessage(`Product ${asin} synced successfully!`);
    } catch (error) {
      console.error('Sync failed:', error);
      setMessage(`Failed to sync product ${asin}. Please check if Amazon API is configured.`);
    } finally {
      setSyncing(null);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-8">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-2">Amazon Product Search</h2>
        <p className="text-gray-600">Search and sync products from Amazon</p>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-4">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for products on Amazon..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={searching}
          />
          <button
            type="submit"
            disabled={searching || !searchQuery.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {searching ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {/* Message */}
      {message && (
        <div className={`p-4 rounded-md mb-4 ${
          message.includes('failed') || message.includes('No products') 
            ? 'bg-red-50 text-red-700 border border-red-200'
            : 'bg-green-50 text-green-700 border border-green-200'
        }`}>
          {message}
        </div>
      )}

      {/* Search Results */}
      {searchResults && searchResults.total_results > 0 && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Found {searchResults.total_results} products for "{searchResults.query}"
          </h3>
          
          <div className="space-y-4">
            {searchResults.products.map((product) => (
              <div key={product.asin} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-1">{product.title}</h4>
                    <div className="text-sm text-gray-600 mb-2">
                      <span className="mr-4">ASIN: {product.asin}</span>
                      <span className="mr-4">Brand: {product.brand}</span>
                      <span>Category: {product.category}</span>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <span className="font-medium text-green-600">
                        {product.currency} {product.price}
                      </span>
                      <span className="flex items-center">
                        <svg className="w-4 h-4 text-yellow-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                        {product.rating} ({product.review_count.toLocaleString()} reviews)
                      </span>
                      <span className={`px-2 py-1 rounded text-xs ${
                        product.availability 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {product.availability ? 'Available' : 'Unavailable'}
                      </span>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => handleSync(product.asin)}
                    disabled={syncing === product.asin}
                    className="ml-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                  >
                    {syncing === product.asin ? 'Syncing...' : 'Sync to DB'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No API Key Warning */}
      {searchResults && searchResults.total_results === 0 && (
        <div className="text-center py-8">
          <div className="mb-4">
            <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 48 48">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 14v20c0 4.418 7.163 8 16 8 1.381 0 2.721-.087 4-.252M8 14c0 4.418 7.163 8 16 8s16-3.582 16-8M8 14c0-4.418 7.163-8 16-8s16 3.582 16 8m0 0v14m0-4c0 4.418-7.163 8-16 8s-16-3.582-16-8" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Amazon API Not Configured</h3>
          <p className="text-gray-600 mb-4">
            To search and sync products from Amazon, please configure your Rainforest API key in the backend environment.
          </p>
          <div className="bg-gray-50 rounded-md p-4 text-left text-sm text-gray-600">
            <p className="font-medium mb-2">Setup Instructions:</p>
            <ol className="list-decimal list-inside space-y-1">
              <li>Get your API key from <a href="https://www.rainforestapi.com/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Rainforest API</a></li>
              <li>Add <code className="bg-gray-200 px-1 rounded">RAINFOREST_API_KEY=your_key_here</code> to your backend .env file</li>
              <li>Restart the backend server</li>
              <li>Try searching again</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  );
}