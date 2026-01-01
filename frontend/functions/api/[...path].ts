export async function onRequest(context: any) {
  const { request, params } = context;

  const backendUrl = `http://4.240.107.18/${params.path.join("/")}`;

  return fetch(backendUrl, {
    method: request.method,
    headers: request.headers,
    body: request.method !== "GET" ? await request.text() : undefined,
  });
}
