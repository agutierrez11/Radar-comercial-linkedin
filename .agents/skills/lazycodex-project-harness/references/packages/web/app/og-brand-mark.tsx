import type { JSX } from "react"

interface OgBrandMarkProps {
  readonly fill: string
  readonly stroke: string
}

export function OgBrandMark({ fill, stroke }: OgBrandMarkProps): JSX.Element {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect
        x="3.2"
        y="3.2"
        width="17.6"
        height="17.6"
        rx="4.4"
        fill={fill}
        stroke={stroke}
        strokeWidth="1.3"
      />
      <path
        d="M8 9 V15.2 H14.6"
        fill="none"
        stroke={stroke}
        strokeWidth="1.7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="15.6" cy="9" r="1.6" fill={stroke} />
    </svg>
  )
}
