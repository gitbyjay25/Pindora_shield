export async function onRequest(context: any) {
  const { request } = context;
  const init: RequestInit = {
    method: request.method,
    headers: request.headers,
  };
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = await request.text();
  }
  return fetch("http://4.240.107.18/api/drug_discovery", init);
}
