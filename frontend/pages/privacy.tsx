import Head from 'next/head';

export default function Privacy() {
  const updated = '2025-09-06';
  return (
    <>
      <Head>
        <title>Privacy Policy | GetYourMusicGear</title>
        <meta name="robots" content="noindex" />
        <meta name="description" content="Learn how GetYourMusicGear collects, uses, and protects your data." />
        <link rel="canonical" href="https://www.getyourmusicgear.com/privacy" />
      </Head>
      <div className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold mb-3">Privacy Policy</h1>
        <p className="text-sm text-gray-500 mb-8">Last updated: {updated}</p>

        <div className="prose prose-gray max-w-none">
          <h2>Overview</h2>
          <p>
            This Privacy Policy describes how we collect, use, and safeguard information when you
            use GetYourMusicGear. By using our website, you agree to the practices described here.
          </p>

          <h2>Information We Collect</h2>
          <ul>
            <li>
              <strong>Usage data:</strong> pages visited, clicks, and basic device information to help us improve
              the site. We may use cookies or similar technologies for analytics.
            </li>
            <li>
              <strong>Contact info (optional):</strong> if you submit forms (e.g., instrument requests or contact),
              we receive the details you provide.
            </li>
            <li>
              <strong>Affiliate redirects:</strong> when you click a store link, we may log a non-identifying click
              event to measure performance.
            </li>
          </ul>

          <h2>How We Use Information</h2>
          <ul>
            <li>Operate and improve website features and content.</li>
            <li>Understand aggregate traffic, trends, and performance.</li>
            <li>Support affiliate programs and track outbound clicks.</li>
            <li>Respond to your inquiries and requests.</li>
          </ul>

          <h2>Cookies and Analytics</h2>
          <p>
            We may use cookies and similar technologies (e.g., local storage) to remember preferences
            and analyze usage. You can control cookies through your browser settings.
          </p>

          <h2>Third-Party Links</h2>
          <p>
            Our site contains links to third-party stores and resources. We are not responsible for
            their content or privacy practices. Please review those sites’ policies.
          </p>

          <h2>Data Retention</h2>
          <p>
            We retain usage data only as long as necessary for the purposes outlined above and to comply
            with legal obligations.
          </p>

          <h2>Your Choices</h2>
          <ul>
            <li>Opt out of non-essential cookies via your browser.</li>
            <li>Limit data sharing by avoiding optional forms.</li>
            <li>Contact us to request updates or removal of submitted information.</li>
          </ul>

          <h2>Children’s Privacy</h2>
          <p>
            Our site is not intended for children under 13. We do not knowingly collect personal
            information from children.
          </p>

          <h2>Changes to This Policy</h2>
          <p>
            We may update this Privacy Policy from time to time. Updates are effective when posted
            on this page with the date above.
          </p>

          <h2>Contact</h2>
          <p>
            Have questions? <a href="/contact">Contact us</a> and we’ll be happy to help.
          </p>
        </div>
      </div>
    </>
  );
}
