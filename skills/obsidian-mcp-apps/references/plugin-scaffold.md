# Obsidian MCP Apps plugin scaffold

Use this scaffold when the user wants to move from architecture into implementation.

The goal is not to provide a drop-in finished plugin. The goal is to give a clean first vertical slice that:
- opens a custom view
- connects to one localhost-backed app such as `pi-excalidraw`
- exposes native commands and settings
- leaves room for future MCP Apps and elicitation support

## Suggested file layout

```text
src/
  main.ts
  settings.ts
  settings-tab.ts
  types.ts
  views/
    embedded-app-view.ts
    excalidraw-runtime-view.ts
  services/
    runtime-service.ts
    permission-service.ts
  modals/
    approval-modal.ts
    elicitation-modal.ts
styles.css
manifest.json
package.json
tsconfig.json
```

## `manifest.json` guidance

Use sentence case in visible strings and keep the description natural.

Example:

```json
{
  "id": "mcp-app-host",
  "name": "MCP App Host",
  "version": "0.1.0",
  "minAppVersion": "1.5.0",
  "description": "Hosts embedded MCP Apps and localhost-backed tool UIs inside Obsidian.",
  "author": "Your Name",
  "isDesktopOnly": true
}
```

`isDesktopOnly: true` is a good default for the first version when the app depends on a local runtime or process launching.

## Settings shape

Start small:

```ts
export interface McpAppHostSettings {
  runtimeUrl: string;
  autoOpenOnStartup: boolean;
  autoReconnect: boolean;
  allowDesktopLaunch: boolean;
  trustedExportFolder: string;
}

export const DEFAULT_SETTINGS: McpAppHostSettings = {
  runtimeUrl: "http://127.0.0.1:19274",
  autoOpenOnStartup: false,
  autoReconnect: true,
  allowDesktopLaunch: false,
  trustedExportFolder: "Assets/Diagrams",
};
```

## `main.ts` skeleton

```ts
import { Plugin, WorkspaceLeaf } from "obsidian";
import { McpAppHostSettings, DEFAULT_SETTINGS } from "./settings";
import { McpAppHostSettingTab } from "./settings-tab";
import { ExcalidrawRuntimeView, EXCALIDRAW_RUNTIME_VIEW_TYPE } from "./views/excalidraw-runtime-view";

export default class McpAppHostPlugin extends Plugin {
  settings: McpAppHostSettings;

  async onload(): Promise<void> {
    await this.loadSettings();

    this.registerView(
      EXCALIDRAW_RUNTIME_VIEW_TYPE,
      (leaf) => new ExcalidrawRuntimeView(leaf, this),
    );

    this.addCommand({
      id: "open-embedded-excalidraw-canvas",
      name: "Open embedded Excalidraw canvas",
      callback: async () => {
        await this.activateExcalidrawView();
      },
    });

    this.addCommand({
      id: "reconnect-embedded-excalidraw-canvas",
      name: "Reconnect embedded Excalidraw canvas",
      callback: async () => {
        const leaf = this.getExistingLeaf();
        const view = leaf?.view;
        if (view instanceof ExcalidrawRuntimeView) {
          await view.reloadRuntime();
        } else {
          await this.activateExcalidrawView();
        }
      },
    });

    this.addSettingTab(new McpAppHostSettingTab(this.app, this));
  }

  async onunload(): Promise<void> {
    await this.app.workspace.detachLeavesOfType(EXCALIDRAW_RUNTIME_VIEW_TYPE);
  }

  async loadSettings(): Promise<void> {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings(): Promise<void> {
    await this.saveData(this.settings);
  }

  getExistingLeaf(): WorkspaceLeaf | null {
    const leaves = this.app.workspace.getLeavesOfType(EXCALIDRAW_RUNTIME_VIEW_TYPE);
    return leaves[0] ?? null;
  }

  async activateExcalidrawView(): Promise<void> {
    let leaf = this.getExistingLeaf();
    if (!leaf) {
      leaf = this.app.workspace.getRightLeaf(false);
      await leaf.setViewState({ type: EXCALIDRAW_RUNTIME_VIEW_TYPE, active: true });
    }
    this.app.workspace.revealLeaf(leaf);
  }
}
```

## View skeleton

Use a dedicated view class. Keep view UI concerns in the view and runtime probing in a service.

```ts
import { ItemView, WorkspaceLeaf } from "obsidian";
import type McpAppHostPlugin from "../main";
import { RuntimeService } from "../services/runtime-service";

export const EXCALIDRAW_RUNTIME_VIEW_TYPE = "embedded-excalidraw-runtime";

export class ExcalidrawRuntimeView extends ItemView {
  plugin: McpAppHostPlugin;
  runtimeService: RuntimeService;
  iframeEl: HTMLIFrameElement | null = null;
  statusEl: HTMLDivElement | null = null;

  constructor(leaf: WorkspaceLeaf, plugin: McpAppHostPlugin) {
    super(leaf);
    this.plugin = plugin;
    this.runtimeService = new RuntimeService(plugin.app, plugin);
  }

  getViewType(): string {
    return EXCALIDRAW_RUNTIME_VIEW_TYPE;
  }

  getDisplayText(): string {
    return "Embedded Excalidraw";
  }

  async onOpen(): Promise<void> {
    await this.render();
  }

  async reloadRuntime(): Promise<void> {
    await this.render();
  }

  async render(): Promise<void> {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("mcp-app-host-view");

    const toolbarEl = contentEl.createDiv({ cls: "mcp-app-host-toolbar" });
    this.statusEl = toolbarEl.createDiv({ cls: "mcp-app-host-status", text: "Checking runtime…" });

    const reloadButton = toolbarEl.createEl("button", { text: "Reload" });
    reloadButton.addEventListener("click", () => {
      void this.reloadRuntime();
    });
    this.registerDomEvent(reloadButton, "click", () => {
      void this.reloadRuntime();
    });

    const runtime = await this.runtimeService.getRuntimeState();
    if (!runtime.ok) {
      this.statusEl.setText(runtime.message);
      contentEl.createDiv({
        cls: "mcp-app-host-empty",
        text: "The Excalidraw runtime is unavailable. Update the URL in settings or start the runtime and reload this view.",
      });
      return;
    }

    this.statusEl.setText(`Connected to ${runtime.url}`);
    this.iframeEl = contentEl.createEl("iframe", {
      cls: "mcp-app-host-iframe",
      attr: { src: runtime.url, title: "Embedded Excalidraw runtime" },
    });
  }
}
```

## Runtime service skeleton

Keep probing logic here so it can later support multiple runtimes or MCP Apps.

```ts
import { App, requestUrl } from "obsidian";
import type McpAppHostPlugin from "../main";

export type RuntimeState = {
  ok: boolean;
  url: string;
  message: string;
};

export class RuntimeService {
  constructor(
    private app: App,
    private plugin: McpAppHostPlugin,
  ) {}

  async getRuntimeState(): Promise<RuntimeState> {
    const url = this.plugin.settings.runtimeUrl.replace(/\/$/, "");
    try {
      const response = await requestUrl({ url: `${url}/health`, method: "GET" });
      const data = response.json;
      if (data?.status === "healthy") {
        return { ok: true, url, message: "Runtime is healthy" };
      }
      return { ok: false, url, message: "Runtime responded, but did not report a healthy state." };
    } catch {
      return { ok: false, url, message: "Could not reach the runtime." };
    }
  }
}
```

## Settings tab skeleton

Expose only the settings the user can understand and act on.

```ts
import { App, PluginSettingTab, Setting, normalizePath } from "obsidian";
import type McpAppHostPlugin from "./main";

export class McpAppHostSettingTab extends PluginSettingTab {
  plugin: McpAppHostPlugin;

  constructor(app: App, plugin: McpAppHostPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    new Setting(containerEl)
      .setName("Runtime URL")
      .setDesc("Base URL for the embedded localhost-backed app runtime.")
      .addText((text) =>
        text
          .setPlaceholder("http://127.0.0.1:19274")
          .setValue(this.plugin.settings.runtimeUrl)
          .onChange(async (value) => {
            this.plugin.settings.runtimeUrl = value.trim();
            await this.plugin.saveSettings();
          }),
      );

    new Setting(containerEl)
      .setName("Trusted export folder")
      .setDesc("Vault folder used for safe exports from embedded apps.")
      .addText((text) =>
        text
          .setValue(this.plugin.settings.trustedExportFolder)
          .onChange(async (value) => {
            this.plugin.settings.trustedExportFolder = normalizePath(value.trim());
            await this.plugin.saveSettings();
          }),
      );
  }
}
```

## CSS guidance

Use `styles.css` and Obsidian variables.

```css
.mcp-app-host-view {
  display: flex;
  flex-direction: column;
  gap: var(--size-4-2);
  height: 100%;
}

.mcp-app-host-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--size-4-2);
}

.mcp-app-host-iframe {
  flex: 1 1 auto;
  width: 100%;
  min-height: 320px;
  border: 1px solid var(--background-modifier-border);
  border-radius: var(--radius-m);
  background: var(--background-primary);
}

.mcp-app-host-empty {
  color: var(--text-muted);
}
```

## First extension points to add later

After the first vertical slice works, add:
- form-mode elicitation modal
- URL-mode waiting modal
- export into trusted vault folder
- note-linked scene attachment
- multiple registered app definitions

## Avoid in version 0.1

- full multi-server orchestration
- mobile support promises before testing
- process management unless truly needed
- automatic destructive writes into arbitrary vault locations
