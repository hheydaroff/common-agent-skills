#!/usr/bin/env node

import puppeteer from "puppeteer-core";

const b = await Promise.race([
	puppeteer.connect({
		browserURL: "http://localhost:9222",
		defaultViewport: null,
	}),
	new Promise((_, reject) => setTimeout(() => reject(new Error("timeout")), 5000)),
]).catch((e) => {
	console.error("✗ Could not connect to browser:", e.message);
	console.error("  Run: browser-start.js");
	process.exit(1);
});

const p = (await b.pages()).at(-1);

if (!p) {
	console.error("✗ No active tab found");
	process.exit(1);
}

const showValues = process.argv.includes("--show-values");
const cookies = await p.cookies();

for (const cookie of cookies) {
	// Values are session secrets and would land in the agent transcript: redact unless asked.
	console.log(`${cookie.name}: ${showValues ? cookie.value : `<redacted, ${cookie.value.length} chars>`}`);
	console.log(`  domain: ${cookie.domain}`);
	console.log(`  path: ${cookie.path}`);
	console.log(`  httpOnly: ${cookie.httpOnly}`);
	console.log(`  secure: ${cookie.secure}`);
	console.log("");
}

await b.disconnect();
