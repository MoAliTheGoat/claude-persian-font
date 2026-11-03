export type FontState = { fonts: string[]; current: string; message: string }

declare module 'claude-code' {
  interface PluginState {
    'persian-font': { font: Shaped<FontState>; isOpen: boolean }
  }
}
