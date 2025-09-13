import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&display=optional"
          rel="stylesheet"
        />
        <link rel="icon" href="/favicon.ico" />
        <meta name="description" content="Find Your Perfect Musical Instrument - Expert Reviews, Detailed Comparisons, and Trusted Recommendations" />
        <meta name="keywords" content="musical instruments, guitar, bass, piano, keyboard, compare, reviews, music gear" />
        {/* Site-wide JSON-LD: WebSite with SearchAction */}
        <script
          // eslint-disable-next-line react/no-danger
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebSite',
              name: 'GetYourMusicGear',
              url: 'https://www.getyourmusicgear.com',
              potentialAction: {
                '@type': 'SearchAction',
                target: 'https://www.getyourmusicgear.com/products?search={search_term_string}',
                'query-input': 'required name=search_term_string',
              },
            }),
          }}
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
