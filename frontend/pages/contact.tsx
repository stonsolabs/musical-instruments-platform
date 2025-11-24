import Head from 'next/head';

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Contact Us - GetYourMusicGear</title>
        <meta name="description" content="Contact GetYourMusicGear for partnerships, feedback, or support." />
        <link rel="canonical" href="https://www.getyourmusicgear.com/contact" />
        <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
        <meta property="og:url" content="https://www.getyourmusicgear.com/contact" />
      </Head>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Contact Us</h1>
        <p className="text-gray-600 mb-8">We’d love to hear from you. For general inquiries or feedback, reach out via email.</p>
        <a href="mailto:info@getyourmusicgear.com" className="btn-primary inline-flex items-center px-6 py-3">info@getyourmusicgear.com</a>
      </div>
    </div>
  );
}

