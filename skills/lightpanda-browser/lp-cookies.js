#!/usr/bin/env node

import { connectAndNavigate } from "./cdp.js";

const url = process.argv[2];
if (!url) {
	console.log("Usage: lp-cookies.js <url>");
	console.log("\nNavigates to URL and displays cookies.");
	process.exit(1);
}

const { browser, page } = await connectAndNavigate(url);

const cookies = await page.cookies();

if (cookies.length === 0) {
	console.log("(no cookies)");
} else {
	for (const cookie of cookies) {
		console.log(`${cookie.name}: ${cookie.value}`);
		console.log(`  domain: ${cookie.domain}`);
		console.log(`  path: ${cookie.path}`);
		console.log(`  httpOnly: ${cookie.httpOnly}`);
		console.log(`  secure: ${cookie.secure}`);
		console.log("");
	}
}

await browser.disconnect();
