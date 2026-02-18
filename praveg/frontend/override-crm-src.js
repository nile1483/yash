const fs = require("fs-extra");
const path = require("path");

/**
 * Option A:
 * - Build remains CRM's build (apps/crm)
 * - This script copies ONLY overridden files from crm_customize/src into apps/crm/frontend/src
 * - It also backs up original files (only those touched) into crm_customize/frontend/.backup_src
 *
 * Usage:
 *   yarn apply
 *   yarn status
 */

const crmAppPath = path.resolve(__dirname, "../../crm"); // apps/crm
const crmSrcPath = path.join(crmAppPath, "frontend", "src");

const overrideRoot = path.join(__dirname, "src");
const backupRoot = path.join(__dirname, ".backup_src");

function listFilesRecursive(dir) {
  if (!fs.existsSync(dir)) return [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const out = [];
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...listFilesRecursive(full));
    else out.push(full);
  }
  return out;
}

function relPathFromOverride(file) {
  return path.relative(overrideRoot, file);
}

function status() {
  const files = listFilesRecursive(overrideRoot);
  if (files.length === 0) {
    console.log("No override files found in:", overrideRoot);
    return;
  }

  console.log("Override root:", overrideRoot);
  console.log("CRM src path :", crmSrcPath);
  console.log("Overrides to apply:");
  files.forEach((f) => {
    const rel = relPathFromOverride(f);
    const target = path.join(crmSrcPath, rel);
    const exists = fs.existsSync(target) ? "target exists" : "target missing";
    console.log(" -", rel, `(${exists})`);
  });
}

function apply() {
  if (!fs.existsSync(overrideRoot)) {
    console.log("No overrides folder found:", overrideRoot);
    process.exit(0);
  }
  if (!fs.existsSync(crmSrcPath)) {
    console.error("CRM src folder not found:", crmSrcPath);
    console.error("Is CRM installed at apps/crm ?");
    process.exit(1);
  }

  const files = listFilesRecursive(overrideRoot);
  if (files.length === 0) {
    console.log("No override files to apply.");
    process.exit(0);
  }

  console.log("Applying overrides...");
  files.forEach((srcOverrideFile) => {
    const rel = relPathFromOverride(srcOverrideFile);
    const targetFile = path.join(crmSrcPath, rel);

    // backup original if exists and not already backed up
    if (fs.existsSync(targetFile)) {
      const backupFile = path.join(backupRoot, rel);
      if (!fs.existsSync(backupFile)) {
        fs.ensureDirSync(path.dirname(backupFile));
        fs.copyFileSync(targetFile, backupFile);
      }
    } else {
      // If target doesn't exist, we still allow creating it (new pages/components)
      // No backup possible.
    }

    fs.ensureDirSync(path.dirname(targetFile));
    fs.copyFileSync(srcOverrideFile, targetFile);
    console.log("✅ Overrode:", rel);
  });

  console.log("\nDone.");
  console.log("Next: run from bench root:");
  console.log("  bench build --app crm");
  console.log("  bench --site frappe1.local clear-cache");
}

const args = process.argv.slice(2);
if (args.includes("--status")) status();
else apply();
