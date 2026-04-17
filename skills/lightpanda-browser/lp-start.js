#!/usr/bin/env node

import { spawn, execSync } from "node:child_process";
import { writeFileSync } from "node:fs";
import { LP_HOST, LP_PORT, isRunning } from "./cdp.js";

// Check if already running
if (await isRunning()) {
	console.log(`✓ Lightpanda already running on ${LP_HOST}:${LP_PORT}`);
	process.exit(0);
}

// Check lightpanda is installed
try {
	execSync("which lightpanda", { stdio: "pipe" });
} catch {
	console.error("✗ lightpanda not found on PATH");
	console.error("  Install: https://github.com/lightpanda-io/browser");
	process.exit(1);
}

// Start lightpanda serve
const child = spawn(
	"lightpanda",
	["serve", "--host", LP_HOST, "--port", LP_PORT, "--timeout", "600"],
	{ detached: true, stdio: "ignore" },
);
child.unref();

// Write PID for stop script
const pidFile = `${process.env.HOME}/.cache/lightpanda.pid`;
execSync(`mkdir -p "${process.env.HOME}/.cache"`, { stdio: "ignore" });
writeFileSync(pidFile, String(child.pid));

// Wait for it to be ready
let connected = false;
for (let i = 0; i < 20; i++) {
	if (await isRunning()) {
		connected = true;
		break;
	}
	await new Promise((r) => setTimeout(r, 300));
}

if (!connected) {
	console.error("✗ Failed to start Lightpanda");
	try { process.kill(child.pid); } catch {}
	process.exit(1);
}

console.log(`✓ Lightpanda started on ${LP_HOST}:${LP_PORT} (PID: ${child.pid})`);
