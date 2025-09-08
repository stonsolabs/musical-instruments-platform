import React, { useState } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';

interface InstrumentRequestFormProps {
  isOpen: boolean;
  onClose: () => void;
}

interface InstrumentRequest {
  brand: string;
  name: string;
  model: string;
  storeLink: string;
  category: string;
  additionalInfo: string;
}

export default function InstrumentRequestForm({ isOpen, onClose }: InstrumentRequestFormProps) {
  const [formData, setFormData] = useState<InstrumentRequest>({
    brand: '',
    name: '',
    model: '',
    storeLink: '',
    category: '',
    additionalInfo: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus('idle');

    try {
      // Use internal proxy to avoid CORS and attach API key server-side
      const response = await fetch(`/api/proxy/v1/instrument-requests`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setSubmitStatus('success');
        setFormData({
          brand: '',
          name: '',
          model: '',
          storeLink: '',
          category: '',
          additionalInfo: ''
        });
        setTimeout(() => {
          onClose();
          setSubmitStatus('idle');
        }, 2000);
      } else {
        throw new Error('Failed to submit request');
      }
    } catch (error) {
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div 
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" 
          onClick={onClose}
        />
        
        {/* Modal panel */}
        <div className="relative inline-block w-full max-w-lg transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left align-bottom shadow-xl transition-all sm:my-8 sm:p-6 sm:align-middle">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-gray-900">
              Request New Instrument
            </h3>
            <button
              type="button"
              className="text-gray-400 hover:text-gray-600 transition-colors"
              onClick={onClose}
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>

          {/* Success Message */}
          {submitStatus === 'success' && (
            <div className="mb-6 rounded-md bg-green-50 p-4">
              <div className="text-sm text-green-800">
                Thank you! Your instrument request has been submitted successfully. We'll review it and add it to our database soon.
              </div>
            </div>
          )}

          {/* Error Message */}
          {submitStatus === 'error' && (
            <div className="mb-6 rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-800">
                Something went wrong. Please try again later.
              </div>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Brand */}
            <div>
              <label htmlFor="brand" className="block text-sm font-medium text-gray-700 mb-2">
                Brand *
              </label>
              <input
                type="text"
                id="brand"
                name="brand"
                required
                value={formData.brand}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-brand-primary focus:border-brand-primary"
                placeholder="e.g., Fender, Gibson, Yamaha"
              />
            </div>

            {/* Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                Instrument Name *
              </label>
              <input
                type="text"
                id="name"
                name="name"
                required
                value={formData.name}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-brand-primary focus:border-brand-primary"
                placeholder="e.g., Stratocaster, Les Paul, P-45"
              />
            </div>

            {/* Model */}
            <div>
              <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-2">
                Model/Variant
              </label>
              <input
                type="text"
                id="model"
                name="model"
                value={formData.model}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-brand-primary focus:border-brand-primary"
                placeholder="e.g., Player Series, Standard, Deluxe"
              />
            </div>

            {/* Category */}
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                Category *
              </label>
              <select
                id="category"
                name="category"
                required
                value={formData.category}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-brand-primary focus:border-brand-primary"
              >
                <option value="">Select a category</option>
                <option value="electric-guitars">Electric Guitars</option>
                <option value="acoustic-guitars">Acoustic Guitars</option>
                <option value="classical-guitars">Classical Guitars</option>
                <option value="electric-basses">Electric Basses</option>
                <option value="acoustic-basses">Acoustic Basses</option>
                <option value="digital-pianos">Digital Pianos</option>
                <option value="acoustic-pianos">Acoustic Pianos</option>
                <option value="synthesizers">Synthesizers</option>
                <option value="studio-monitors">Studio Monitors</option>
                <option value="headphones">Headphones</option>
                <option value="audio-interfaces">Audio Interfaces</option>
                <option value="microphones">Microphones</option>
                <option value="dj-equipment">DJ Equipment</option>
                <option value="drums">Drums</option>
                <option value="orchestral">Orchestral</option>
                <option value="accessories">Accessories</option>
                <option value="other">Other</option>
              </select>
            </div>

            {/* Store Link */}
            <div>
              <label htmlFor="storeLink" className="block text-sm font-medium text-gray-700 mb-2">
                Store Link
              </label>
              <input
                type="url"
                id="storeLink"
                name="storeLink"
                value={formData.storeLink}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-brand-primary focus:border-brand-primary"
                placeholder="https://example.com/product-link"
              />
              <p className="mt-1 text-xs text-gray-500">
                Provide a link from any music store where we can find this instrument
              </p>
            </div>

            {/* Additional Info */}
            <div>
              <label htmlFor="additionalInfo" className="block text-sm font-medium text-gray-700 mb-2">
                Additional Information
              </label>
              <textarea
                id="additionalInfo"
                name="additionalInfo"
                rows={3}
                value={formData.additionalInfo}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-brand-primary focus:border-brand-primary"
                placeholder="Any additional details that would help us add this instrument..."
              />
            </div>

            {/* Buttons */}
            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting || !formData.brand || !formData.name || !formData.category}
                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-brand-primary border border-transparent rounded-md hover:bg-brand-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isSubmitting ? 'Submitting...' : 'Submit Request'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
