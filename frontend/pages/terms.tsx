import Head from 'next/head';

export default function Terms() {
  const updated = '2025-09-06';
  return (
    <>
      <Head>
        <title>Terms of Service | GetYourMusicGear</title>
        <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
        <meta name="description" content="Read the terms that govern use of GetYourMusicGear." />
        <link rel="canonical" href="https://www.getyourmusicgear.com/terms" />
        <meta property="og:url" content="https://www.getyourmusicgear.com/terms" />
      </Head>
      <div className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold mb-3">Terms of Service</h1>
        <p className="text-sm text-gray-500 mb-8">Last updated: {updated}</p>

        <div className="prose prose-gray max-w-none">
          <h2>Acceptance of Terms</h2>
          <p>
            By accessing or using GetYourMusicGear (the “Service”), you agree to these Terms of Service.
            If you do not agree, please do not use the Service.
          </p>

          <h2>Use of the Service</h2>
          <ul>
            <li>Use the Service only for lawful purposes and in accordance with these terms.</li>
            <li>Do not attempt to disrupt, reverse engineer, or misuse the Service.</li>
            <li>We may update or discontinue features at any time.</li>
          </ul>

          <h2>Accounts & Submissions</h2>
          <p>
            If you provide information (e.g., via contact or instrument request forms), you confirm it is
            accurate and that you have the right to share it. We may remove content that violates policies
            or applicable laws.
          </p>

          <h2>Affiliate Disclosure</h2>
          <p>
            We may include affiliate links to third‑party stores. When you click those links, we may earn a
            commission—at no additional cost to you. We do not control or guarantee third‑party products,
            pricing, availability, or policies.
          </p>

          <h2>Content & Accuracy</h2>
          <p>
            Product information and analysis are provided for informational purposes. While we strive for
            accuracy, we do not guarantee completeness or real‑time updates. Always verify details with the
            relevant retailers or manufacturers.
          </p>

          <h2>Prohibited Activities</h2>
          <ul>
            <li>Violating laws or third‑party rights.</li>
            <li>Uploading malicious code or attempting to gain unauthorized access.</li>
            <li>Scraping or heavy automated access beyond fair use.</li>
          </ul>

          <h2>Disclaimers</h2>
          <p>
            THE SERVICE IS PROVIDED “AS IS” AND “AS AVAILABLE,” WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR
            IMPLIED. WE DISCLAIM ALL WARRANTIES INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE,
            AND NON‑INFRINGEMENT.
          </p>

          <h2>Limitation of Liability</h2>
          <p>
            TO THE MAXIMUM EXTENT PERMITTED BY LAW, WE SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL,
            SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR ANY LOSS OF PROFITS OR DATA, ARISING FROM YOUR
            USE OF THE SERVICE.
          </p>

          <h2>Changes to These Terms</h2>
          <p>
            We may update these Terms from time to time. Changes are effective upon posting. Continued use
            of the Service indicates acceptance of the updated Terms.
          </p>

          <h2>Contact</h2>
          <p>
            Questions about these Terms? <a href="/contact">Contact us</a>.
          </p>
        </div>
      </div>
    </>
  );
}
