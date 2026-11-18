#!/usr/bin/env node
// ONE DAY - news-image-20261117 round 2 entry point.
// Runs draw.py and writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
// No network, no timestamps: the same input always yields the same PNG.
const { spawnSync } = require("node:child_process");
const path = require("node:path");

const out = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const r = spawnSync("python3", [path.join(__dirname, "draw.py")], {
  stdio: "inherit",
  env: { ...process.env, MAKEFUN_OUTPUT_DIR: out },
});
process.exit(r.status === null ? 1 : r.status);
