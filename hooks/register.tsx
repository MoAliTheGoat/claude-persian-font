import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { FontState } from '../types'

const font = atom({ plugin: 'persian-font', key: 'font' } as const, { fonts: [], current: '', message: '' }, {
  shape: 'font-3',
})
const isOpen = atom({ plugin: 'persian-font', key: 'isOpen' } as const, false)

const RESTART_JOB = 'local.claude-persian-font.restart'
// Single quotes for the shell; a font name comes from a folder name.
const q = (s: string) => `'${s.replace(/'/g, `'\\''`)}'`

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const tool = q(`${$.plugin.root}/scripts/fontswitch.py`)
    const listed = await $.process.run(['/bin/zsh', '-c', `python3 ${tool} list`])
    const cur = await $.process.run(['/bin/zsh', '-c', `python3 ${tool} current`])
    let fonts: string[] = []
    try {
      fonts = JSON.parse(listed.stdout)
    } catch {}
    let current = cur.stdout.trim()
    // First run: start with the bundled Vazirmatn.
    if (current === '' && fonts.includes('Vazirmatn')) {
      const ran = await $.process.run(['/bin/zsh', '-c', `python3 ${tool} use Vazirmatn`])
      if (ran.exitCode === 0) {
        current = 'Vazirmatn'
        $.ui.toast('Persian font installed. Restart Claude once to see it.')
      }
    }
    await update($, font, () => ({ fonts, current, message: '' }))
    await $.command.register({ name: 'persian-font', description: 'Choose the font for Persian text' })
    return next(e)
  })

  on('command.run', { command: 'persian-font' }, async $ => {
    await update($, isOpen, () => true)
    return { text: 'Persian fonts are open above the message box.' }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const { Box, Text, Button } = $.ui.resolve(e)
    const state: FontState = await read($, font)
    if (state.fonts.length === 0) return next(e)

    // Folded: one small dim control; it opens the choices only when pressed.
    if (!(await read($, isOpen))) {
      return (
        <Box justifyContent="flex-end">
          <Button key="open" label={`Aa ${state.current && state.current !== '(off)' ? state.current : 'فونت'}`} plain dimColor onPress={() => void update($, isOpen, () => true)} />
        </Box>
      )
    }

    const choose = async (name: string) => {
      if (name === state.current) return
      await update($, font, s => ({ ...s, message: 'در حال تغییر…' }))
      const tool = q(`${$.plugin.root}/scripts/fontswitch.py`)
      const ran = await $.process.run(['/bin/zsh', '-c', `python3 ${tool} use ${q(name)}`])
      if (ran.exitCode !== 0) {
        await update($, font, s => ({ ...s, message: `نشد: ${ran.stderr.trim() || ran.stdout.trim()}` }))
        return
      }
      await update($, font, s => ({ ...s, current: name, message: 'Claude چند ثانیه بسته و دوباره باز می‌شود…' }))
      // Claude reads fonts only at launch; launchd restarts it so the helper outlives the quit.
      const restart = q(`${$.plugin.root}/scripts/restart.sh`)
      await $.process.run([
        '/bin/zsh',
        '-c',
        `launchctl remove ${RESTART_JOB} 2>/dev/null; launchctl submit -l ${RESTART_JOB} -- /bin/zsh ${restart}`,
      ])
    }

    // Right to left: the first font sits on the right, ✕ on the left.
    return (
      <Box flexDirection="row" gap={1} justifyContent="flex-end">
        {state.message !== '' && <Text dimColor>{state.message}</Text>}
        <Button key="close" label="✕" plain dimColor onPress={() => void update($, isOpen, () => false)} />
        {[...state.fonts].reverse().map(name => (
          <Button
            key={name}
            label={name}
            variant={state.current === name ? 'primary' : undefined}
            dimColor={state.current !== name}
            onPress={() => void choose(name)}
          />
        ))}
      </Box>
    )
  })
}
