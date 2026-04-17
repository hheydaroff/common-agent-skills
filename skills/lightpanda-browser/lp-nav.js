#!/usr/bin/env node

import { connectAndNavigate } from "./cdp.js";

const url = process.argv[2];
if (!url) {
	console.log("Usage: lp-nav.js <url>");
	console.log("\nNavigates to URL and prints the page title.");
	console.log("\nExample:");
	console.log("  lp-nav.js https://example.com");
	process.exit(1);
}

const { browser, page } = await connectAndNavigate(url);
const title = await page.evaluate(() => document.title).catch(() => "(unknown)");
console.log(`✓ ${title}`);
console.log(`  ${page.url()}`);

await browser.disconnect();
