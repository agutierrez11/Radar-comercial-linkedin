import type { JSX } from "react"
import { MarketingSection } from "../design-system/layout"
import { COMMANDS } from "../../lib/commands"
import { CommandCard } from "./command-card"

export function CommandCards(): JSX.Element {
  return (
    <MarketingSection className="mt-16 md:mt-24">
      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        {COMMANDS.map((command) => (
          <CommandCard key={command.name} command={command} />
        ))}
      </div>
    </MarketingSection>
  )
}
