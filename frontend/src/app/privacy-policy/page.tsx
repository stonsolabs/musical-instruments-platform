import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy - GetYourMusicGear',
  description: 'Learn how we collect, use, and protect your personal information when you use our musical instrument comparison platform.',
  keywords: 'privacy policy, data protection, personal information, cookies, GDPR',
  openGraph: {
    title: 'Privacy Policy - GetYourMusicGear',
    description: 'Learn how we collect, use, and protect your personal information when you use our musical instrument comparison platform.',
    type: 'website',
    url: 'https://getyourmusicgear.com/privacy-policy',
  },
  twitter: {
    card: 'summary',
    title: 'Privacy Policy - GetYourMusicGear',
    description: 'Learn how we collect, use, and protect your personal information when you use our musical instrument comparison platform.',
  },
};

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Privacy Policy</h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            How we collect, use, and protect your personal information
          </p>
          <p className="text-sm text-blue-200 mt-4">Last updated: January 15, 2025</p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li className="text-gray-900" aria-current="page">Privacy Policy</li>
          </ol>
        </nav>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <div className="prose prose-lg max-w-none">
            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">1. Introduction</h2>
              <p className="text-gray-600 mb-4">
                GetYourMusicGear ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website and use our musical instrument comparison platform.
              </p>
              <p className="text-gray-600">
                By using our service, you agree to the collection and use of information in accordance with this policy. If you do not agree with our policies and practices, please do not use our service.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">2. Information We Collect</h2>
              
              <h3 className="text-xl font-semibold text-gray-900 mb-4">2.1 Personal Information</h3>
              <p className="text-gray-600 mb-4">We may collect personal information that you voluntarily provide to us, including:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Name and email address (when you contact us or subscribe to our newsletter)</li>
                <li>Search queries and browsing preferences</li>
                <li>Feedback and communication with our support team</li>
                <li>Information you provide when participating in surveys or promotions</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">2.2 Automatically Collected Information</h3>
              <p className="text-gray-600 mb-4">When you visit our website, we automatically collect certain information, including:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>IP address and device information</li>
                <li>Browser type and version</li>
                <li>Operating system</li>
                <li>Pages visited and time spent on each page</li>
                <li>Referring website</li>
                <li>Click patterns and user interactions</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">2.3 Cookies and Tracking Technologies</h3>
              <p className="text-gray-600 mb-4">We use cookies and similar tracking technologies to:</p>
              <ul className="list-disc pl-6 text-gray-600">
                <li>Remember your preferences and settings</li>
                <li>Analyze website traffic and usage patterns</li>
                <li>Provide personalized content and recommendations</li>
                <li>Improve our website functionality and user experience</li>
                <li>Track affiliate link clicks and conversions</li>
              </ul>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">3. How We Use Your Information</h2>
              <p className="text-gray-600 mb-4">We use the collected information for the following purposes:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Provide and maintain our comparison platform</li>
                <li>Process and respond to your inquiries and support requests</li>
                <li>Send you newsletters and updates (with your consent)</li>
                <li>Analyze usage patterns to improve our service</li>
                <li>Personalize your experience and provide relevant recommendations</li>
                <li>Track affiliate partnerships and commissions</li>
                <li>Comply with legal obligations and protect our rights</li>
              </ul>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">4. Information Sharing and Disclosure</h2>
              <p className="text-gray-600 mb-4">We do not sell, trade, or otherwise transfer your personal information to third parties, except in the following circumstances:</p>
              
              <h3 className="text-xl font-semibold text-gray-900 mb-4">4.1 Service Providers</h3>
              <p className="text-gray-600 mb-4">We may share information with trusted third-party service providers who assist us in:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Website hosting and maintenance</li>
                <li>Analytics and performance monitoring</li>
                <li>Email communication services</li>
                <li>Customer support tools</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">4.2 Legal Requirements</h3>
              <p className="text-gray-600 mb-4">We may disclose your information if required by law or in response to:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Valid legal requests from government authorities</li>
                <li>Court orders or subpoenas</li>
                <li>Protection of our rights, property, or safety</li>
                <li>Prevention of fraud or security threats</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">4.3 Business Transfers</h3>
              <p className="text-gray-600">
                In the event of a merger, acquisition, or sale of assets, your information may be transferred as part of the business transaction, subject to the same privacy protections.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">5. Data Security</h2>
              <p className="text-gray-600 mb-4">We implement appropriate technical and organizational measures to protect your personal information against:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Unauthorized access, alteration, or disclosure</li>
                <li>Data loss or destruction</li>
                <li>Malicious attacks and security breaches</li>
              </ul>
              <p className="text-gray-600">
                However, no method of transmission over the internet or electronic storage is 100% secure. While we strive to protect your information, we cannot guarantee absolute security.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">6. Your Rights and Choices</h2>
              <p className="text-gray-600 mb-4">Depending on your location, you may have the following rights regarding your personal information:</p>
              
              <h3 className="text-xl font-semibold text-gray-900 mb-4">6.1 Access and Portability</h3>
              <p className="text-gray-600 mb-4">You have the right to:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Request access to your personal information</li>
                <li>Receive a copy of your data in a portable format</li>
                <li>Verify the accuracy of your information</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">6.2 Correction and Deletion</h3>
              <p className="text-gray-600 mb-4">You can:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Request correction of inaccurate information</li>
                <li>Request deletion of your personal information</li>
                <li>Withdraw consent for data processing</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">6.3 Cookie Preferences</h3>
              <p className="text-gray-600 mb-4">You can control cookies through your browser settings:</p>
              <ul className="list-disc pl-6 text-gray-600">
                <li>Disable or delete cookies</li>
                <li>Set browser preferences for cookie acceptance</li>
                <li>Use browser extensions to manage tracking</li>
              </ul>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">7. Third-Party Links and Services</h2>
              <p className="text-gray-600 mb-4">
                Our website contains links to third-party websites and services, including affiliate retailers. We are not responsible for the privacy practices of these external sites. We encourage you to review their privacy policies before providing any personal information.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">8. Children's Privacy</h2>
              <p className="text-gray-600">
                Our service is not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13. If you are a parent or guardian and believe your child has provided us with personal information, please contact us immediately.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">9. International Data Transfers</h2>
              <p className="text-gray-600">
                Your information may be transferred to and processed in countries other than your own. We ensure that such transfers comply with applicable data protection laws and implement appropriate safeguards to protect your information.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">10. Changes to This Privacy Policy</h2>
              <p className="text-gray-600 mb-4">
                We may update this Privacy Policy from time to time. We will notify you of any changes by:
              </p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Posting the new Privacy Policy on this page</li>
                <li>Updating the "Last updated" date</li>
                <li>Sending you an email notification for significant changes</li>
              </ul>
              <p className="text-gray-600">
                Your continued use of our service after any changes constitutes acceptance of the updated Privacy Policy.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">11. Contact Us</h2>
              <p className="text-gray-600 mb-4">
                If you have any questions about this Privacy Policy or our data practices, please contact us:
              </p>
              <div className="bg-gray-50 rounded-lg p-6">
                <p className="text-gray-600 mb-2"><strong>Email:</strong> privacy@getyourmusicgear.com</p>
                <p className="text-gray-600 mb-2"><strong>Address:</strong> GetYourMusicGear, Amsterdam, Netherlands</p>
                <p className="text-gray-600">
                  <strong>Data Protection Officer:</strong> For GDPR-related inquiries, please contact our Data Protection Officer at dpo@getyourmusicgear.com
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">12. Legal Basis for Processing (GDPR)</h2>
              <p className="text-gray-600 mb-4">For users in the European Union, we process your personal information based on the following legal grounds:</p>
              <ul className="list-disc pl-6 text-gray-600">
                <li><strong>Consent:</strong> When you explicitly agree to our data processing</li>
                <li><strong>Legitimate Interest:</strong> For website analytics and service improvement</li>
                <li><strong>Contract Performance:</strong> To provide our comparison services</li>
                <li><strong>Legal Obligation:</strong> To comply with applicable laws and regulations</li>
              </ul>
            </section>
          </div>
        </div>

        {/* Related Links */}
        <section className="mt-12 bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Related Information</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Link href="/terms-of-service" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="w-12 h-12 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-blue-600 text-xl">📋</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Terms of Service</h3>
              <p className="text-gray-600 text-sm">Read our terms and conditions</p>
            </Link>
            
            <Link href="/affiliate-disclosure" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="w-12 h-12 bg-green-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-green-600 text-xl">🔗</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Affiliate Disclosure</h3>
              <p className="text-gray-600 text-sm">Learn about our partnerships</p>
            </Link>
            
            <Link href="/contact" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="w-12 h-12 bg-purple-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-purple-600 text-xl">📧</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Contact Us</h3>
              <p className="text-gray-600 text-sm">Get in touch with our team</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
}
