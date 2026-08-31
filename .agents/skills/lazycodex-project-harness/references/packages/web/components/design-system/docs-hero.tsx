import type { JSX, ReactNode } from "react"

interface DocsHeroProps {
  readonly badge: ReactNode
  readonly children: ReactNode
  readonly title: string
}

export function DocsHero({ badge, children, title }: DocsHeroProps): JSX.Element {
  return (
    <div className="docs-hero">
      <div className="docs-hero-badge">
        <span className="docs-hero-dot" aria-hidden="true" />
        {badge}
      </div>
      <h1 className="docs-hero-title">{title}</h1>
      <p className="docs-hero-tagline">{children}</p>
    </div>
  )
}
