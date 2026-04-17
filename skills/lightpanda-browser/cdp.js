import puppeteer from "puppeteer-core";

const LP_HOST = process.env.LP_HOST || "127.0.0.1";
const LP_PORT = process.env.LP_PORT || "9222";
const LP_URL = `ws://${LP_HOST}:${LP_PORT}/`;

export { LP_HOST, LP_PORT, LP_URL };

/**
 * Connect to Lightpanda CDP server and navigate to a URL.
 * Lightpanda creates a fresh session per WebSocket connection,
 * so we always create a new page and navigate immediately.
 */
export async function connectAndNavigate(url, options = {}) {
	const { timeout = 5000, waitUntil = "domcontentloaded", navTimeout = 15000 } = options;

	const browser = await Promise.race([
		puppeteer.connect({
			browserWSEndpoint: LP_URL,
			defaultViewport: null,
		}),
		new Promise((_, reject) =>
			setTimeout(() => reject(new Error("timeout connecting to Lightpanda")), timeout),
		),
	]).catch((e) => {
		console.error(`✗ Could not connect to Lightpanda at ${LP_URL}: ${e.message}`);
		console.error("  Run: lp-start.js");
		process.exit(1);
	});

	const page = await browser.newPage();

	if (url) {
		await Promise.race([
			page.goto(url, { waitUntil, timeout: navTimeout }),
			new Promise((r) => setTimeout(r, navTimeout)),
		]).catch(() => {});
	}

	return { browser, page };
}

/**
 * Check if Lightpanda CDP server is reachable.
 */
export async function isRunning() {
	try {
		const browser = await Promise.race([
			puppeteer.connect({ browserWSEndpoint: LP_URL, defaultViewport: null }),
			new Promise((_, reject) => setTimeout(() => reject(new Error("timeout")), 2000)),
		]);
		await browser.disconnect();
		return true;
	} catch {
		return false;
	}
}
