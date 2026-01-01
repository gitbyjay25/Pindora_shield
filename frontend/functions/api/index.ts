export async function onRequest(context: any) {
  const { request } = context;

  const url = new URL(request.url);

  // strip /api prefix
  const backendPath = url.pathname.replace(/^\/api/, "");

  const backendUrl = `http://4.240.107.18${backendPath}${url.search}`;

  return fetch(backendUrl, {
    method: request.method,
    headers: request.headers,
    body: request.method !== "GET" ? await request.text() : undefined,
  });
}
