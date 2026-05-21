# Extension Management API

```typescript
type ExtensionInstallationInfo = {
  current_branch_name: string;
  current_commit_hash: string;
  is_up_to_date: boolean;
  remote_url: string;
};

function isAdmin(): boolean
function getTavernHelperExtensionId(): string
function getExtensionType(extension_id: string): 'local' | 'global' | 'system' | null
function getExtensionInstallationInfo(extension_id: string): Promise<ExtensionInstallationInfo | null>
function isInstalledExtension(extension_id: string): boolean
function installExtension(url: string, type: 'local' | 'global'): Promise<Response>
function uninstallExtension(extension_id: string): Promise<Response>
function reinstallExtension(extension_id: string): Promise<Response>
function updateExtension(extension_id: string): Promise<Response>
```

- `isAdmin`: Returns whether current user has admin privileges.
- `getTavernHelperExtensionId`: Returns `'JS-Slash-Runner'`.
- `getExtensionType`: Returns the installation type of an extension by ID.
- `getExtensionInstallationInfo`: Fetches git-based info (branch, commit, up-to-date status, remote URL) for an installed extension.
- `isInstalledExtension`: Checks if an extension is installed by ID.
- `installExtension`: Installs an extension from a git URL. Global install requires admin. Returns fetch Response.
- `uninstallExtension`: Uninstalls an extension by ID. Global uninstall requires admin. Returns fetch Response.
- `reinstallExtension`: Reinstalls an extension by uninstalling then installing from its remote URL. Only does something if not up-to-date.
- `updateExtension`: Updates an extension via the ST API. Returns fetch Response.

```typescript
if (await isAdmin()) {
  const result = await installExtension('https://github.com/user/repo', 'local');
  if (result.ok) toastr.success('Extension installed');
}

const info = await getExtensionInstallationInfo('my-extension');
if (info && !info.is_up_to_date) {
  await updateExtension('my-extension');
}
```
