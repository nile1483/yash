const fs = require("fs-extra");
const path = require("path");

/**
 * Restores original CRM files from crm_customize/frontend/.backup_src
 * (only files that were backed up / touched by apply)
 *
 * Usage:
 *   yarn restore
 */

const crmAppPath = path.resolve(__dirname, "../../crm"); // apps/crm
const crmSrcPath = path.join(crmAppPath, "frontend", "src");
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

function restore() {
  if (!fs.existsSync(backupRoot)) {
    console.log("No backup folder found:", backupRoot);
    process.exit(0);
  }
  if (!fs.existsSync(crmSrcPath)) {
    console.error("CRM src folder not found:", crmSrcPath);
    process.exit(1);
  }

  const files = listFilesRecursive(backupRoot);
  if (files.length === 0) {
    console.log("Backup folder exists but has no files:", backupRoot);
    process.exit(0);
  }

  console.log("Restoring CRM src from backup...");
  files.forEach((backupFile) => {
    const rel = path.relative(backupRoot, backupFile);
    const targetFile = path.join(crmSrcPath, rel);

    fs.ensureDirSync(path.dirname(targetFile));
    fs.copyFileSync(backupFile, targetFile);
    console.log("✅ Restored:", rel);
  });

  console.log("\nDone. Next: rebuild CRM assets if you want to revert UI:");
  console.log("  bench build --app crm");
}

restore();
