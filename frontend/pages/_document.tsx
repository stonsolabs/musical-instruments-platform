import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  const gtmId = process.env.NEXT_PUBLIC_GTM_ID;

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
        
        {/* Google Tag Manager */}
        {gtmId && (
          <script
            // eslint-disable-next-line react/no-danger
            dangerouslySetInnerHTML={{
              __html: `
                (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
                new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
                j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
                'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
                })(window,document,'script','dataLayer','${gtmId}');
              `,
            }}
          />
        )}
        
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
        {/* Google Tag Manager (noscript) */}
        {gtmId && (
          <noscript
            // eslint-disable-next-line react/no-danger
            dangerouslySetInnerHTML={{
              __html: `<iframe src="https://www.googletagmanager.com/ns.html?id=${gtmId}" height="0" width="0" style="display:none;visibility:hidden"></iframe>`,
            }}
          />
        )}
        
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
