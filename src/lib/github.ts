/**
 * GitHub API client for time-vault-secrets repo.
 * Reads are unauthenticated (public repo). Writes use a fine-grained PAT.
 */

const OWNER = "julioflima";
const REPO = "time-vault-secrets";
const API = "https://api.github.com";
const SECRETS_DIR = "secrets";

// Fine-grained PAT with Contents:write scope on time-vault-secrets only.
// This is intentionally public — anyone can append vaults.
// Deletion is prevented via branch protection rules.
const TOKEN = ""; // TODO: set after creating PAT

export type VaultFile = {
    C: string;
    n: number;
    t0: number;
    T: number;
};

export type VaultListItem = {
    V: string;
    name: string;
    downloadUrl: string;
};

function headers(auth = false): HeadersInit {
    const h: Record<string, string> = {
        Accept: "application/vnd.github+json",
    };
    if (auth && TOKEN) {
        h["Authorization"] = `Bearer ${TOKEN}`;
    }
    return h;
}

/** List all vault files in secrets/ directory. No auth needed. */
export async function listVaults(): Promise<VaultListItem[]> {
    const res = await fetch(
        `${API}/repos/${OWNER}/${REPO}/contents/${SECRETS_DIR}`,
        { headers: headers() },
    );

    if (res.status === 404) return []; // empty repo or dir not found
    if (!res.ok) throw new Error(`GitHub API error: ${res.status}`);

    const files: Array<{ name: string; download_url: string }> = await res.json();

    return files
        .filter((f) => f.name.endsWith(".vault.json"))
        .map((f) => ({
            V: f.name.replace(".vault.json", ""),
            name: f.name,
            downloadUrl: f.download_url,
        }));
}

/** Fetch a single vault file by V hex. No auth needed. */
export async function fetchVault(V: string): Promise<VaultFile> {
    const res = await fetch(
        `${API}/repos/${OWNER}/${REPO}/contents/${SECRETS_DIR}/${V}.vault.json`,
        { headers: headers() },
    );

    if (!res.ok) throw new Error(`Vault not found: ${res.status}`);

    const data: { content: string } = await res.json();
    const decoded = atob(data.content.replace(/\n/g, ""));
    return JSON.parse(decoded);
}

/** Publish a vault to the repo. Requires TOKEN. */
export async function publishVault(
    V: string,
    vault: VaultFile,
): Promise<{ ok: boolean; message: string }> {
    if (!TOKEN) {
        return { ok: false, message: "GitHub token not configured" };
    }

    const content = btoa(JSON.stringify(vault, null, 2));
    const path = `${SECRETS_DIR}/${V}.vault.json`;

    const res = await fetch(`${API}/repos/${OWNER}/${REPO}/contents/${path}`, {
        method: "PUT",
        headers: headers(true),
        body: JSON.stringify({
            message: `vault: ${V.slice(0, 8)} | n=${vault.n} | unlock=${vault.T}`,
            content,
        }),
    });

    if (res.status === 409) {
        return { ok: false, message: "A vault with this V already exists" };
    }

    if (res.status === 422) {
        return { ok: false, message: "Vault file already exists" };
    }

    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        return {
            ok: false,
            message: `GitHub API error ${res.status}: ${(body as { message?: string }).message ?? "unknown"}`,
        };
    }

    return { ok: true, message: "Vault published successfully" };
}

/** Check if token is configured. */
export function isTokenConfigured(): boolean {
    return TOKEN.length > 0;
}
