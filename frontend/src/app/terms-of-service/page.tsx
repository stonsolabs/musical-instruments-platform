import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Terms of Service - GetYourMusicGear',
  description: 'Read our terms and conditions for using the GetYourMusicGear musical instrument comparison platform.',
  keywords: 'terms of service, terms and conditions, user agreement, legal terms, platform usage',
  openGraph: {
    title: 'Terms of Service - GetYourMusicGear',
    description: 'Read our terms and conditions for using the GetYourMusicGear musical instrument comparison platform.',
    type: 'website',
    url: 'https://getyourmusicgear.com/terms-of-service',
  },
  twitter: {
    card: 'summary',
    title: 'Terms of Service - GetYourMusicGear',
    description: 'Read our terms and conditions for using the GetYourMusicGear musical instrument comparison platform.',
  },
};

export default function TermsOfServicePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Terms of Service</h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Terms and conditions for using our musical instrument comparison platform
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
            <li className="text-gray-900" aria-current="page">Terms of Service</li>
          </ol>
        </nav>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <div className="prose prose-lg max-w-none">
            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">1. Acceptance of Terms</h2>
              <p className="text-gray-600 mb-4">
                By accessing and using GetYourMusicGear ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
              </p>
              <p className="text-gray-600">
                These Terms of Service ("Terms") govern your use of our website and services. By using our platform, you agree to these terms in full.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">2. Description of Service</h2>
              <p className="text-gray-600 mb-4">
                GetYourMusicGear is a comparison platform that allows users to:
              </p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Compare prices of musical instruments across multiple retailers</li>
                <li>Access detailed product information and specifications</li>
                <li>Read reviews and recommendations</li>
                <li>Access affiliate links to purchase products</li>
                <li>Use comparison tools and features</li>
              </ul>
              <p className="text-gray-600">
                We do not sell products directly but facilitate connections between users and third-party retailers.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">3. User Accounts and Registration</h2>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">3.1 Account Creation</h3>
              <p className="text-gray-600 mb-4">
                While registration is not required to use our basic services, you may choose to create an account to access additional features such as:
              </p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Saved comparisons and favorites</li>
                <li>Personalized recommendations</li>
                <li>Newsletter subscriptions</li>
                <li>Comment and review features</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">3.2 Account Responsibilities</h3>
              <p className="text-gray-600 mb-4">When creating an account, you agree to:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Provide accurate and complete information</li>
                <li>Maintain the security of your account credentials</li>
                <li>Notify us immediately of any unauthorized use</li>
                <li>Accept responsibility for all activities under your account</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">3.3 Account Termination</h3>
              <p className="text-gray-600">
                We reserve the right to terminate or suspend accounts that violate these terms or engage in fraudulent activities.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">4. Acceptable Use Policy</h2>
              <p className="text-gray-600 mb-4">You agree not to use the Service to:</p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Violate any applicable laws or regulations</li>
                <li>Infringe upon intellectual property rights</li>
                <li>Transmit harmful, offensive, or inappropriate content</li>
                <li>Attempt to gain unauthorized access to our systems</li>
                <li>Interfere with the proper functioning of the Service</li>
                <li>Use automated tools to scrape or collect data</li>
                <li>Engage in any form of spam or unsolicited communication</li>
              </ul>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">5. Intellectual Property Rights</h2>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">5.1 Our Content</h3>
              <p className="text-gray-600 mb-4">
                The Service and its original content, features, and functionality are owned by GetYourMusicGear and are protected by international copyright, trademark, patent, trade secret, and other intellectual property laws.
              </p>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">5.2 User Content</h3>
              <p className="text-gray-600 mb-4">
                By submitting content to our platform (reviews, comments, etc.), you grant us a non-exclusive, worldwide, royalty-free license to use, reproduce, and distribute such content.
              </p>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">5.3 Third-Party Content</h3>
              <p className="text-gray-600">
                Product information, images, and descriptions are provided by our retail partners and are subject to their respective intellectual property rights.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">6. Affiliate Relationships and Commissions</h2>
              <p className="text-gray-600 mb-4">
                We maintain affiliate relationships with various retailers. When you click on product links and make purchases, we may earn commissions at no additional cost to you.
              </p>
              <p className="text-gray-600 mb-4">
                These affiliate relationships help us maintain and improve our platform. For more detailed information about our affiliate practices, please see our <Link href="/affiliate-disclosure" className="text-blue-600 hover:text-blue-700">Affiliate Disclosure</Link>.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">7. Disclaimers and Limitations</h2>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">7.1 Service Availability</h3>
              <p className="text-gray-600 mb-4">
                We strive to maintain high availability but do not guarantee uninterrupted access to our Service. We may temporarily suspend or restrict access for maintenance, updates, or other operational reasons.
              </p>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">7.2 Product Information</h3>
              <p className="text-gray-600 mb-4">
                While we work to ensure accuracy, product information, prices, and availability are provided by third-party retailers and may change without notice. We are not responsible for any inaccuracies or changes.
              </p>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">7.3 Third-Party Services</h3>
              <p className="text-gray-600 mb-4">
                Our Service contains links to third-party websites and services. We are not responsible for the content, privacy policies, or practices of these external sites.
              </p>

              <h3 className="text-xl font-semibold text-gray-900 mb-4">7.4 Limitation of Liability</h3>
              <p className="text-gray-600">
                To the maximum extent permitted by law, GetYourMusicGear shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of the Service.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">8. Privacy and Data Protection</h2>
              <p className="text-gray-600 mb-4">
                Your privacy is important to us. Our collection and use of personal information is governed by our <Link href="/privacy-policy" className="text-blue-600 hover:text-blue-700">Privacy Policy</Link>, which is incorporated into these Terms by reference.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">9. Termination</h2>
              <p className="text-gray-600 mb-4">
                We may terminate or suspend your access to the Service immediately, without prior notice, for any reason, including breach of these Terms.
              </p>
              <p className="text-gray-600">
                Upon termination, your right to use the Service will cease immediately, and we may delete your account and associated data.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">10. Governing Law and Jurisdiction</h2>
              <p className="text-gray-600 mb-4">
                These Terms shall be governed by and construed in accordance with the laws of the Netherlands, without regard to its conflict of law provisions.
              </p>
              <p className="text-gray-600">
                Any disputes arising from these Terms or your use of the Service shall be subject to the exclusive jurisdiction of the courts in Amsterdam, Netherlands.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">11. Changes to Terms</h2>
              <p className="text-gray-600 mb-4">
                We reserve the right to modify these Terms at any time. We will notify users of significant changes by:
              </p>
              <ul className="list-disc pl-6 text-gray-600 mb-6">
                <li>Posting the updated Terms on our website</li>
                <li>Updating the "Last updated" date</li>
                <li>Sending email notifications to registered users</li>
              </ul>
              <p className="text-gray-600">
                Your continued use of the Service after changes constitutes acceptance of the updated Terms.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">12. Severability</h2>
              <p className="text-gray-600">
                If any provision of these Terms is found to be unenforceable or invalid, that provision will be limited or eliminated to the minimum extent necessary so that the Terms will otherwise remain in full force and effect.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">13. Entire Agreement</h2>
              <p className="text-gray-600">
                These Terms, together with our Privacy Policy and Affiliate Disclosure, constitute the entire agreement between you and GetYourMusicGear regarding the use of our Service.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">14. Contact Information</h2>
              <p className="text-gray-600 mb-4">
                If you have any questions about these Terms of Service, please contact us:
              </p>
              <div className="bg-gray-50 rounded-lg p-6">
                <p className="text-gray-600 mb-2"><strong>Email:</strong> legal@getyourmusicgear.com</p>
                <p className="text-gray-600 mb-2"><strong>Address:</strong> GetYourMusicGear, Amsterdam, Netherlands</p>
                <p className="text-gray-600">
                  <strong>General Inquiries:</strong> hello@getyourmusicgear.com
                </p>
              </div>
            </section>
          </div>
        </div>

        {/* Related Links */}
        <section className="mt-12 bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Related Information</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Link href="/privacy-policy" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="w-12 h-12 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-blue-600 text-xl">🔒</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Privacy Policy</h3>
              <p className="text-gray-600 text-sm">Learn about data protection</p>
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
