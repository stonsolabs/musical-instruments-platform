import React from 'react';
import Link from 'next/link';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us - GetYourMusicGear',
  description: 'Learn about GetYourMusicGear, your trusted source for comparing musical instruments across Europe\'s top retailers.',
  keywords: 'about us, musical instruments, comparison platform, music gear, instrument reviews',
  openGraph: {
    title: 'About Us - GetYourMusicGear',
    description: 'Learn about GetYourMusicGear, your trusted source for comparing musical instruments across Europe\'s top retailers.',
    type: 'website',
    url: 'https://getyourmusicgear.com/about',
  },
  twitter: {
    card: 'summary',
    title: 'About Us - GetYourMusicGear',
    description: 'Learn about GetYourMusicGear, your trusted source for comparing musical instruments across Europe\'s top retailers.',
  },
};

export default function AboutPage() {
  const teamMembers = [
    {
      name: "Alex Johnson",
      role: "Founder & CEO",
      bio: "Passionate musician and entrepreneur with over 15 years of experience in the music industry.",
      image: "/images/team-alex.jpg"
    },
    {
      name: "Sarah Chen",
      role: "Head of Product",
      bio: "Former music store manager with deep knowledge of instruments and customer needs.",
      image: "/images/team-sarah.jpg"
    },
    {
      name: "Marcus Rodriguez",
      role: "Lead Developer",
      bio: "Full-stack developer and amateur guitarist who loves building tools for musicians.",
      image: "/images/team-marcus.jpg"
    }
  ];

  const stats = [
    { number: "50,000+", label: "Instruments Compared" },
    { number: "25+", label: "Retail Partners" },
    { number: "100,000+", label: "Happy Customers" },
    { number: "15+", label: "European Countries" }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">About Us</h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Your trusted source for comparing musical instruments across Europe's top retailers
          </p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-gray-600">
            <li><Link href="/" className="hover:text-blue-600">Home</Link></li>
            <li>/</li>
            <li className="text-gray-900" aria-current="page">About</li>
          </ol>
        </nav>

        {/* Mission Section */}
        <section className="mb-16">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                At GetYourMusicGear, we believe that every musician deserves access to the best instruments at the best prices. 
                Our mission is to simplify the process of finding and comparing musical instruments across Europe's top retailers.
              </p>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                Whether you're a beginner looking for your first guitar or a professional musician seeking the perfect addition to your collection, 
                we provide comprehensive comparisons, detailed reviews, and direct links to make your purchase with confidence.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                We partner with trusted retailers across Europe to ensure you have access to authentic instruments with reliable customer service and competitive pricing.
              </p>
            </div>
            <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl p-8 text-white">
              <h3 className="text-2xl font-bold mb-4">Why Choose Us?</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✓</span>
                  <span>Comprehensive price comparisons across 25+ retailers</span>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✓</span>
                  <span>Detailed instrument reviews and specifications</span>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✓</span>
                  <span>Direct affiliate links for seamless purchasing</span>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✓</span>
                  <span>Expert buying guides and recommendations</span>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✓</span>
                  <span>Trusted partnerships with European retailers</span>
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Stats Section - Commented Out */}
        {/* <section className="mb-16">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Our Impact</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-4xl font-bold text-blue-600 mb-2">{stat.number}</div>
                  <div className="text-gray-600">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section> */}

        {/* Story Section - Commented Out */}
        {/* <section className="mb-16">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8">Our Story</h2>
            <div className="prose prose-lg max-w-none text-gray-600">
              <p className="mb-6">
                GetYourMusicGear was founded in 2023 by a group of musicians who were frustrated with the complexity of finding 
                the right instruments at the best prices. We noticed that musicians often had to visit multiple websites, 
                compare prices manually, and struggle to find reliable information about instruments.
              </p>
              <p className="mb-6">
                What started as a simple comparison tool has grown into a comprehensive platform that serves musicians across Europe. 
                We've built partnerships with the most trusted retailers in the industry, ensuring that our users have access to 
                authentic instruments with reliable customer service.
              </p>
              <p className="mb-6">
                Today, we're proud to help thousands of musicians make informed decisions about their instrument purchases. 
                Whether you're a beginner or a professional, our platform provides the tools and information you need to find 
                your perfect instrument.
              </p>
              <p>
                We're committed to continuously improving our platform and expanding our partnerships to serve the European 
                music community better. Our goal is to become the go-to destination for anyone looking to buy musical instruments online.
              </p>
            </div>
          </div>
        </section> */}

        {/* Team Section - Commented Out */}
        {/* <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Meet Our Team</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {teamMembers.map((member, index) => (
              <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
                <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-white text-2xl font-bold">
                    {member.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{member.name}</h3>
                <p className="text-blue-600 font-medium mb-4">{member.role}</p>
                <p className="text-gray-600">{member.bio}</p>
              </div>
            ))}
          </div>
        </section> */}

        {/* Values Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Our Values</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-blue-600 text-2xl">🎯</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Transparency</h3>
              <p className="text-gray-600">
                We believe in complete transparency in our comparisons and recommendations. 
                All affiliate relationships are clearly disclosed.
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-green-600 text-2xl">🤝</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Trust</h3>
              <p className="text-gray-600">
                We only partner with trusted retailers who share our commitment to quality 
                and customer satisfaction.
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-purple-600 text-2xl">🎵</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Passion</h3>
              <p className="text-gray-600">
                We're musicians ourselves, and we're passionate about helping others 
                find the perfect instruments for their musical journey.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-r from-blue-600 to-purple-700 rounded-xl p-8 text-white text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Find Your Perfect Instrument?</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Start comparing thousands of instruments from Europe's top retailers and find the best deals today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/products"
              className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              Browse Instruments
            </Link>
            <Link
              href="/contact"
              className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
            >
              Contact Us
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
}
