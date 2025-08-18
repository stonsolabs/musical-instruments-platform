import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Affiliate Disclosure - GetYourMusicGear',
  description: 'Learn about our affiliate partnerships and how we earn commissions when you purchase musical instruments through our platform.',
  keywords: 'affiliate disclosure, affiliate links, commission disclosure, partnership transparency, musical instruments',
  openGraph: {
    title: 'Affiliate Disclosure - GetYourMusicGear',
    description: 'Learn about our affiliate partnerships and how we earn commissions when you purchase musical instruments through our platform.',
    type: 'website',
    url: 'https://getyourmusicgear.com/affiliate-disclosure',
  },
  twitter: {
    card: 'summary',
    title: 'Affiliate Disclosure - GetYourMusicGear',
    description: 'Learn about our affiliate partnerships and how we earn commissions when you purchase musical instruments through our platform.',
  },
};

export default function AffiliateDisclosurePage() {
  const partnerRetailers = [
    {
      name: "Thomann",
      description: "Europe's largest online music store",
      commission: "3-8%",
      features: ["Wide selection", "Fast shipping", "Excellent customer service"]
    },
    {
      name: "Gear4Music",
      description: "UK-based music equipment retailer",
      commission: "4-7%",
      features: ["Competitive prices", "Student discounts", "Trade-in program"]
    },
    {
      name: "Music Store",
      description: "German music instrument specialist",
      commission: "3-6%",
      features: ["Expert advice", "Professional setup", "Warranty support"]
    },
    {
      name: "Andertons",
      description: "UK guitar and bass specialist",
      commission: "4-8%",
      features: ["Premium selection", "Video reviews", "Expert staff"]
    }
  ];

  const faqs = [
    {
      question: "Do affiliate links affect the price I pay?",
      answer: "No, affiliate links do not increase the price you pay. The commission comes from the retailer's marketing budget, not from your purchase price."
    },
    {
      question: "How do you choose which retailers to partner with?",
      answer: "We carefully select retailers based on their reputation, product quality, customer service, shipping policies, and competitive pricing to ensure the best experience for our users."
    },
    {
      question: "Are you biased towards certain retailers?",
      answer: "We strive to provide unbiased comparisons and recommendations. While we earn commissions from affiliate sales, we prioritize helping you find the best products at the best prices."
    },
    {
      question: "Can I still get the same deals without using affiliate links?",
      answer: "Yes, you can visit retailers directly. However, using our affiliate links helps support our platform and allows us to continue providing free comparison services."
    },
    {
      question: "How do you track affiliate sales?",
      answer: "We use tracking cookies and affiliate networks to monitor clicks and purchases. This helps us understand which products and retailers are most popular with our users."
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Affiliate Disclosure</h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Transparency about our affiliate partnerships and commission structure
          </p>
          <p className="text-sm text-blue-200 mt-4">Last updated: January 15, 2025</p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li className="text-gray-900" aria-current="page">Affiliate Disclosure</li>
          </ol>
        </nav>

        <div className="space-y-12">
          {/* Main Disclosure */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <div className="prose prose-lg max-w-none">
              <section className="mb-12">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">What Are Affiliate Links?</h2>
                <p className="text-gray-600 mb-4">
                  GetYourMusicGear participates in various affiliate marketing programs. This means that when you click on certain links on our website and make a purchase, we may earn a commission at no additional cost to you.
                </p>
                <p className="text-gray-600">
                  These affiliate relationships help us maintain and improve our platform, allowing us to provide free comparison services to musicians across Europe.
                </p>
              </section>

              <section className="mb-12">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">How Affiliate Links Work</h2>
                <div className="grid md:grid-cols-3 gap-6 mb-6">
                  <div className="text-center p-6 bg-blue-50 rounded-lg">
                    <div className="w-12 h-12 bg-blue-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                      <span className="text-white text-xl">1</span>
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Click</h3>
                    <p className="text-gray-600 text-sm">You click on a product link on our website</p>
                  </div>
                  <div className="text-center p-6 bg-green-50 rounded-lg">
                    <div className="w-12 h-12 bg-green-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                      <span className="text-white text-xl">2</span>
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Purchase</h3>
                    <p className="text-gray-600 text-sm">You make a purchase on the retailer's website</p>
                  </div>
                  <div className="text-center p-6 bg-purple-50 rounded-lg">
                    <div className="w-12 h-12 bg-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                      <span className="text-white text-xl">3</span>
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2">Commission</h3>
                    <p className="text-gray-600 text-sm">We earn a small commission from the retailer</p>
                  </div>
                </div>
                <p className="text-gray-600">
                  <strong>Important:</strong> The commission comes from the retailer's marketing budget, not from your purchase price. You pay the same price whether you use our affiliate links or visit the retailer directly.
                </p>
              </section>

              <section className="mb-12">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Our Commitment to Transparency</h2>
                <p className="text-gray-600 mb-4">
                  We believe in complete transparency about our affiliate relationships. Here's what you should know:
                </p>
                <ul className="list-disc pl-6 text-gray-600 mb-6">
                  <li>All affiliate links are clearly marked and disclosed</li>
                  <li>We only partner with trusted, reputable retailers</li>
                  <li>Our recommendations are based on product quality and value, not commission rates</li>
                  <li>We maintain editorial independence in our reviews and comparisons</li>
                  <li>You can always visit retailers directly if you prefer</li>
                </ul>
              </section>
            </div>
          </div>

          {/* Partner Retailers */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-8">Our Partner Retailers</h2>
            <div className="grid md:grid-cols-2 gap-6">
              {partnerRetailers.map((retailer, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-900">{retailer.name}</h3>
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                      {retailer.commission} commission
                    </span>
                  </div>
                  <p className="text-gray-600 mb-4">{retailer.description}</p>
                  <div className="space-y-2">
                    {retailer.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-center text-sm text-gray-600">
                        <span className="text-green-500 mr-2">✓</span>
                        {feature}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Commission Structure */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-700 rounded-xl p-8 text-white">
            <h2 className="text-2xl font-bold mb-6">Commission Structure</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold mb-2">3-8%</div>
                <div className="text-blue-100">Average Commission Rate</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold mb-2">25+</div>
                <div className="text-blue-100">Partner Retailers</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold mb-2">0%</div>
                <div className="text-blue-100">Additional Cost to You</div>
              </div>
            </div>
            <p className="text-center text-blue-100 mt-6">
              Commission rates vary by retailer and product category. Higher-value items typically have lower percentage rates but higher absolute commission amounts.
            </p>
          </div>

          {/* FAQ Section */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Frequently Asked Questions</h2>
            <div className="grid md:grid-cols-2 gap-8">
              {faqs.map((faq, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-3">{faq.question}</h3>
                  <p className="text-gray-600">{faq.answer}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Ethical Guidelines */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Our Ethical Guidelines</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">What We Do</h3>
                <ul className="space-y-3 text-gray-600">
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2 mt-1">✓</span>
                    <span>Provide honest, unbiased product comparisons</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2 mt-1">✓</span>
                    <span>Recommend products based on quality and value</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2 mt-1">✓</span>
                    <span>Maintain editorial independence in our content</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2 mt-1">✓</span>
                    <span>Clearly disclose all affiliate relationships</span>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">What We Don't Do</h3>
                <ul className="space-y-3 text-gray-600">
                  <li className="flex items-start">
                    <span className="text-red-500 mr-2 mt-1">✗</span>
                    <span>Let commission rates influence our recommendations</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-red-500 mr-2 mt-1">✗</span>
                    <span>Hide or obscure affiliate links</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-red-500 mr-2 mt-1">✗</span>
                    <span>Partner with unreliable or unethical retailers</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-red-500 mr-2 mt-1">✗</span>
                    <span>Charge users for our comparison services</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Questions About Our Affiliate Program?</h2>
            <p className="text-gray-600 mb-6">
              If you have any questions about our affiliate relationships or how our commission structure works, please don't hesitate to contact us.
            </p>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="font-semibold text-gray-900 mb-2">For General Inquiries</h3>
                <p className="text-gray-600 mb-2">Email: hello@getyourmusicgear.com</p>
                <p className="text-gray-600">We typically respond within 24 hours</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="font-semibold text-gray-900 mb-2">For Partnership Inquiries</h3>
                <p className="text-gray-600 mb-2">Email: partnerships@getyourmusicgear.com</p>
                <p className="text-gray-600">For retailers interested in partnering with us</p>
              </div>
            </div>
          </div>

          {/* Related Links */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">Related Information</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <Link href="/privacy-policy" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
                <div className="w-12 h-12 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-blue-600 text-xl">🔒</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Privacy Policy</h3>
                <p className="text-gray-600 text-sm">Learn about data protection</p>
              </Link>
              
              <Link href="/terms-of-service" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
                <div className="w-12 h-12 bg-green-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-green-600 text-xl">📋</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Terms of Service</h3>
                <p className="text-gray-600 text-sm">Read our terms and conditions</p>
              </Link>
              
              <Link href="/contact" className="text-center p-6 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all">
                <div className="w-12 h-12 bg-purple-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-purple-600 text-xl">📧</span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Contact Us</h3>
                <p className="text-gray-600 text-sm">Get in touch with our team</p>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
