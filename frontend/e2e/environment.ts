export const baseURL = process.env.E2E_BASE_URL || "http://localhost:3000";
// Only local, self-signed proxy tests may bypass trust. Public VPS tests must
// verify the real certificate even if this environment flag was left behind.
export const localTLS =
  process.env.E2E_INSECURE_LOCAL_TLS === "1" &&
  new URL(baseURL).hostname === "localhost";
