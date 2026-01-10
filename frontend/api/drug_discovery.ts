export default async function handler(req: Request): Promise<Response> {
  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ error: "Method Not Allowed" }),
      { status: 405 }
    );
  }

  try {
    const body = await req.text();

    const backendRes = await fetch(
      "http://4.240.107.18/api/drug_discovery",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body,
      }
    );

    const data = await backendRes.text();

    return new Response(data, {
      status: backendRes.status,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });

  } catch (err: any) {
    return new Response(
      JSON.stringify({
        error: "Proxy failed",
        message: err?.message || "Unknown error",
      }),
      { status: 500 }
    );
  }
}
