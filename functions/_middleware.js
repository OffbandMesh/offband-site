// Cloudflare Pages Function: canonical redirect www.offband.org -> offband.org.
// Runs on every request; passes everything else straight through to static assets.
// No Cloudflare token/permission needed — deploys with the site.
export const onRequest = (context) => {
  const url = new URL(context.request.url);
  if (url.hostname === "www.offband.org") {
    url.hostname = "offband.org";
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
};
