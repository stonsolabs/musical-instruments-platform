import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Contact Us - GetYourMusicGear',
  description: 'Get in touch with our team for support, partnerships, or any questions about musical instruments and our comparison platform.',
  keywords: 'contact us, support, musical instruments, customer service, partnership inquiries',
  openGraph: {
    title: 'Contact Us - GetYourMusicGear',
    description: 'Get in touch with our team for support, partnerships, or any questions about musical instruments and our comparison platform.',
    type: 'website',
    url: 'https://getyourmusicgear.com/contact',
  },
  twitter: {
    card: 'summary',
    title: 'Contact Us - GetYourMusicGear',
    description: 'Get in touch with our team for support, partnerships, or any questions about musical instruments and our comparison platform.',
  },
};

export default function ContactPage() {
  const faqs = [
    {
      question: "How do I report an incorrect price or product information?",
      answer: "If you notice any incorrect information on our platform, please contact us with the product details and we'll investigate and correct it promptly."
    },
    {
      question: "Can I suggest a retailer to be added to your platform?",
      answer: "Absolutely! We're always looking to expand our network of trusted retailers. Please send us the retailer's information and we'll evaluate them for partnership."
    },
    {
      question: "How do affiliate links work on your platform?",
      answer: "When you click on a product link and make a purchase, we may earn a small commission at no extra cost to you. This helps us maintain our platform and provide free comparisons."
    },
    {
      question: "Do you ship instruments directly?",
      answer: "No, we don't sell or ship instruments directly. We're a comparison platform that connects you with trusted retailers who handle all sales and shipping."
    },
    {
      question: "How often do you update product information?",
      answer: "We update our product database daily to ensure you have the most current prices and availability information from our partner retailers."
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Contact Us</h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Get in touch with our team for support, partnerships, or any questions about musical instruments
          </p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li className="text-gray-900" aria-current="page">Contact</li>
          </ol>
        </nav>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Contact Form */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Send us a Message</h2>
            <form className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-2">
                    First Name *
                  </label>
                  <input
                    type="text"
                    id="firstName"
                    name="firstName"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Your first name"
                  />
                </div>
                <div>
                  <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-2">
                    Last Name *
                  </label>
                  <input
                    type="text"
                    id="lastName"
                    name="lastName"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Your last name"
                  />
                </div>
              </div>
              
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="your.email@example.com"
                />
              </div>
              
              <div>
                <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">
                  Subject *
                </label>
                <select
                  id="subject"
                  name="subject"
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select a subject</option>
                  <option value="general">General Inquiry</option>
                  <option value="support">Technical Support</option>
                  <option value="partnership">Partnership Opportunity</option>
                  <option value="feedback">Feedback</option>
                  <option value="bug">Report a Bug</option>
                  <option value="other">Other</option>
                </select>
              </div>
              
              <div>
                <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                  Message *
                </label>
                <textarea
                  id="message"
                  name="message"
                  rows={6}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Tell us how we can help you..."
                ></textarea>
              </div>
              
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Send Message
              </button>
            </form>
          </div>

          {/* Contact Information */}
          <div className="space-y-8">
            {/* Company Info */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Get in Touch</h2>
              <div className="space-y-4">
                <div className="flex items-start">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-4 mt-1">
                    <span className="text-blue-600 text-sm">📧</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Email</h3>
                    <p className="text-gray-600">hello@getyourmusicgear.com</p>
                    <p className="text-sm text-gray-500">We typically respond within 24 hours</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-4 mt-1">
                    <span className="text-green-600 text-sm">💬</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Live Chat</h3>
                    <p className="text-gray-600">Available during business hours</p>
                    <p className="text-sm text-gray-500">Monday - Friday, 9 AM - 6 PM CET</p>
                  </div>
                </div>
                
                <div className="flex items-start">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-4 mt-1">
                    <span className="text-purple-600 text-sm">🌍</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Office</h3>
                    <p className="text-gray-600">GetYourMusicGear</p>
                    <p className="text-gray-600">Amsterdam, Netherlands</p>
                    <p className="text-sm text-gray-500">European Headquarters</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Response Time */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-700 rounded-xl p-8 text-white">
              <h3 className="text-xl font-bold mb-4">Response Times</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span>General Inquiries</span>
                  <span className="font-semibold">24 hours</span>
                </div>
                <div className="flex justify-between">
                  <span>Technical Support</span>
                  <span className="font-semibold">4-8 hours</span>
                </div>
                <div className="flex justify-between">
                  <span>Partnership Inquiries</span>
                  <span className="font-semibold">48 hours</span>
                </div>
                <div className="flex justify-between">
                  <span>Bug Reports</span>
                  <span className="font-semibold">2-4 hours</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <section className="mt-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Frequently Asked Questions</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {faqs.map((faq, index) => (
              <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-3">{faq.question}</h3>
                <p className="text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Additional Resources */}
        <section className="mt-16 bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Additional Resources</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Link href="/about" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="w-12 h-12 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-blue-600 text-xl">ℹ️</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">About Us</h3>
              <p className="text-gray-600 text-sm">Learn more about our mission and team</p>
            </Link>
            
            <Link href="/blog" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="w-12 h-12 bg-green-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-green-600 text-xl">📝</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Blog</h3>
              <p className="text-gray-600 text-sm">Read our latest articles and guides</p>
            </Link>
            
            <Link href="/affiliate-disclosure" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="w-12 h-12 bg-purple-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-purple-600 text-xl">🔗</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Affiliate Disclosure</h3>
              <p className="text-gray-600 text-sm">Learn about our affiliate partnerships</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
}
