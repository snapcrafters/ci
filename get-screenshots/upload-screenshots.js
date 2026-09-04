const fs = require("node:fs/promises");
const os = require("node:os");
const path = require("node:path");

module.exports = async function uploadScreenshots({ github, core, context, env = process.env }) {
  const [owner, repo, extra] = env.SCREENSHOTS_REPO.split("/");
  if (!owner || !repo || extra) {
    throw new Error("screenshots-repo must use the owner/repository format");
  }

  const runDate = env.RUN_DATE || new Date().toISOString().slice(0, 10).replaceAll("-", "");
  const prefix = `${runDate}-${env.SNAP_NAME}-${env.ISSUE_NUMBER}`;
  const screenshots = [
    { suffix: "screen", source: "screenshot-screen.png" },
    { suffix: "window", source: "screenshot-window.png" },
  ];

  const ref = await github.rest.git.getRef({ owner, repo, ref: "heads/main" });
  const parent = ref.data.object.sha;
  const baseCommit = await github.rest.git.getCommit({ owner, repo, commit_sha: parent });
  const treeEntries = [];

  for (const screenshot of screenshots) {
    const screenshotDir = env.SCREENSHOTS_DIR || path.join(os.homedir(), "ghvmctl-screenshots");
    const content = await fs.readFile(path.join(screenshotDir, screenshot.source), "base64");
    const blob = await github.rest.git.createBlob({ owner, repo, content, encoding: "base64" });
    treeEntries.push({
      path: `${prefix}-${screenshot.suffix}.png`,
      mode: "100644",
      type: "blob",
      sha: blob.data.sha,
    });
  }

  const tree = await github.rest.git.createTree({
    owner,
    repo,
    base_tree: baseCommit.data.tree.sha,
    tree: treeEntries,
  });
  const commit = await github.rest.git.createCommit({
    owner,
    repo,
    message: `data: screenshots for ${context.repo.owner}/${env.SNAP_NAME}#${env.ISSUE_NUMBER}`,
    tree: tree.data.sha,
    parents: [parent],
    author: { name: env.BOT_NAME, email: env.BOT_EMAIL },
    committer: { name: env.BOT_NAME, email: env.BOT_EMAIL },
  });
  await github.rest.git.updateRef({
    owner,
    repo,
    ref: "heads/main",
    sha: commit.data.sha,
    force: false,
  });

  for (const screenshot of screenshots) {
    core.setOutput(
      screenshot.suffix,
      `https://raw.githubusercontent.com/${env.SCREENSHOTS_REPO}/${commit.data.sha}/${prefix}-${screenshot.suffix}.png`,
    );
  }
};
