# GitHub App Setup for Releases

This guide walks through creating a GitHub App to allow semantic-release to bypass branch protection rules securely.

## Why a GitHub App?

semantic-release needs to push version bump commits (CHANGELOG.md, gradle.properties) back to the `main` branch. With branch protection requiring pull requests, a GitHub App provides secure bypass access without compromising security for regular contributors.

## Prerequisites

- Repository with branch protection/repository rules enabled
- Admin access to the organization or personal account
- Access to repository secrets settings

## Step 1: Create the GitHub App

### For Organization Repositories (Recommended)

1. Navigate to your organization settings:
   ```
   https://github.com/organizations/YOUR_ORG_NAME/settings/apps
   ```
   
2. Click **"New GitHub App"**

### For Personal Repositories

1. Navigate to your personal settings:
   ```
   https://github.com/settings/apps/new
   ```

## Step 2: Configure the App

Fill in the following settings:

### Basic Information

**GitHub App name:**
```
kmp-template-release
```
(Or any name under 34 characters)

**Homepage URL:**
```
https://github.com/YOUR_ORG/YOUR_REPO
```

**Description:** (optional)
```
Automated release bot for semantic-release
```

### Identifying and Authorizing Users

- **Uncheck:** "Request user authorization (OAuth) during installation"
- **Uncheck:** "Expire user authorization tokens"
- Leave **Callback URL** empty

### Post Installation

- Leave **Setup URL** empty
- Leave **Redirect on update** unchecked

### Webhook

- **Uncheck:** "Active"
  - We don't need webhooks for this use case

### Permissions

#### Repository Permissions

Set these permissions:

| Permission | Access Level | Purpose |
|------------|-------------|---------|
| **Contents** | Read and write | Push commits, create tags, create releases |
| **Metadata** | Read-only | (Automatically selected, required) |

Leave all other permissions at "No access"

#### Organization Permissions

Leave all at "No access"

#### Account Permissions

Leave all at "No access"

### Subscribe to Events

Leave empty - no event subscriptions needed

### Where can this GitHub App be installed?

**For organization apps:**
- Select: **"Any account"** if you want to reuse across multiple orgs
- OR Select: **"Only on this account"** for tighter security

**For personal apps:**
- Select based on your needs

## Step 3: Create the App

Click **"Create GitHub App"** at the bottom

## Step 4: Generate Private Key

After creation, you'll be on the app's settings page:

1. Scroll down to **"Private keys"** section
2. Click **"Generate a private key"**
3. A `.pem` file will download automatically
4. **Save this file securely** - you'll need it for repository secrets

**Important:** Store the private key securely. If lost, you'll need to generate a new one.

## Step 5: Note the App ID

At the top of the app settings page, you'll see:

```
App ID: 123456
```

Copy this number - you'll need it for repository secrets.

## Step 6: Install the App

1. In the left sidebar, click **"Install App"**
2. Find your organization/account and click **"Install"**
3. Choose installation scope:
   - **"All repositories"** - Recommended if you'll use semantic-release on multiple repos
   - **"Only select repositories"** - More restrictive, select specific repos
4. Click **"Install"**

## Step 7: Get Installation ID

After installation, you'll be redirected to a URL like:

```
https://github.com/settings/installations/12345678
```

The number at the end (`12345678`) is your **Installation ID**. Copy this number.

**Or find it later:**
1. Go to: https://github.com/settings/installations
2. Click **"Configure"** next to your app
3. The Installation ID is in the URL

## Step 8: Add Repository Secrets

Navigate to your repository secrets:

```
https://github.com/YOUR_ORG/YOUR_REPO/settings/secrets/actions
```

Add these **3 secrets**:

### Secret 1: APP_ID

- **Name:** `APP_ID`
- **Value:** Your App ID from Step 5 (e.g., `123456`)

### Secret 2: APP_INSTALLATION_ID

- **Name:** `APP_INSTALLATION_ID`
- **Value:** Your Installation ID from Step 7 (e.g., `12345678`)

### Secret 3: APP_PRIVATE_KEY

- **Name:** `APP_PRIVATE_KEY`
- **Value:** 
  1. Open the `.pem` file from Step 4 in a text editor
  2. Copy the **entire contents** including the header and footer:
     ```
     -----BEGIN RSA PRIVATE KEY-----
     [long string of characters]
     -----END RSA PRIVATE KEY-----
     ```
  3. Paste the entire contents as the secret value

**Security Note:** Never commit the private key to your repository.

## Step 9: Update Release Workflow

Update `.github/workflows/release.yml` to use the GitHub App token:

```yaml
jobs:
  release:
    name: Semantic Release
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    
    steps:
      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}
          
      - name: Checkout code
        uses: actions/checkout@v6
        with:
          fetch-depth: 0
          token: ${{ steps.app-token.outputs.token }}
          
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run semantic-release
        env:
          GITHUB_TOKEN: ${{ steps.app-token.outputs.token }}
        run: npx semantic-release
```

**Key changes:**
- Added `Generate GitHub App token` step at the beginning
- Changed `token` in checkout to use app token
- Changed `GITHUB_TOKEN` env var to use app token

## Step 10: Add App to Branch Protection Bypass List

### For Repository Rules (Recommended)

1. Navigate to repository rules:
   ```
   https://github.com/YOUR_ORG/YOUR_REPO/settings/rules
   ```

2. Find your rule for the `main` branch and click **"Edit"**

3. Scroll to **"Bypass list"** section

4. Click **"Add bypass"** (or the + icon)

5. Look for your app in the dropdown:
   - Should appear as: `kmp-template-release` or `kmp-template-release[bot]`
   - Select it

6. Click **"Save changes"**

### For Traditional Branch Protection

1. Navigate to branch settings:
   ```
   https://github.com/YOUR_ORG/YOUR_REPO/settings/branches
   ```

2. Find your `main` branch rule and click **"Edit"**

3. Scroll to **"Restrict who can push to matching branches"**

4. Add your GitHub App to the exception list

5. Click **"Save changes"**

## Step 11: Test the Setup

1. Merge a PR with a conventional commit message (e.g., `feat: add feature`)
2. The Build & Test workflow should complete
3. The Release workflow should trigger
4. semantic-release should:
   - ✅ Create a new version tag
   - ✅ Update CHANGELOG.md
   - ✅ Update gradle.properties
   - ✅ Push changes to main (using app credentials)
   - ✅ Create GitHub Release

## Troubleshooting

### App doesn't appear in bypass list

**Issue:** Your app isn't showing in the repository rules bypass dropdown.

**Solution:**
- Ensure the app is created under the **organization**, not your personal account
- For org repos, the app must be an organization app
- Refresh the page (Cmd+Shift+R / Ctrl+Shift+R)
- Verify the app is installed on the repository

### "Resource not accessible by integration" error

**Issue:** The app doesn't have sufficient permissions.

**Solution:**
1. Go to app settings
2. Check **Contents** permission is set to "Read and write"
3. If you changed permissions, you may need to re-accept them:
   - Go to https://github.com/settings/installations
   - Click "Configure" next to your app
   - Review and accept new permissions

### "Bad credentials" error

**Issue:** APP_PRIVATE_KEY secret is incorrect.

**Solution:**
1. Verify you copied the **entire** `.pem` file contents including headers
2. Check for extra whitespace or missing characters
3. Regenerate the private key if needed and update the secret

### Release fails with "push declined due to repository rule violations"

**Issue:** The app is not in the bypass list or doesn't have proper permissions.

**Solution:**
1. Verify the app appears in your repository rules bypass list
2. Ensure the app has "Contents: Read and write" permission
3. Check that the workflow is using the app token, not `secrets.GITHUB_TOKEN`

## Security Best Practices

1. **Principle of Least Privilege:**
   - Only grant Contents (read/write) permission
   - Don't grant unnecessary permissions

2. **Private Key Security:**
   - Never commit the `.pem` file to version control
   - Store securely (password manager, secure notes)
   - Rotate keys periodically (annually recommended)

3. **Access Control:**
   - Limit who has admin access to the organization/repo
   - Regularly audit app installations
   - Remove unused apps

4. **Monitoring:**
   - Review workflow runs regularly
   - Check that only semantic-release pushes to main
   - Set up notifications for failed releases

## Rotating the Private Key

If you need to rotate the private key:

1. Go to app settings: https://github.com/organizations/YOUR_ORG/settings/apps/YOUR_APP
2. Scroll to **"Private keys"**
3. Click **"Generate a private key"** (generates new key)
4. Download the new `.pem` file
5. Update `APP_PRIVATE_KEY` secret in repository
6. (Optional) Revoke old keys after verifying new one works

## Additional Resources

- [GitHub Apps Documentation](https://docs.github.com/en/apps)
- [semantic-release with GitHub Actions](https://semantic-release.gitbook.io/semantic-release/recipes/ci-configurations/github-actions)
- [Repository Rules Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
