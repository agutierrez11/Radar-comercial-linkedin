import { ImageResponse } from "next/og"
import { SITE_CONFIG } from "../lib/site-config"
import { OgBrandMark } from "./og-brand-mark"
import { OG_GRADIENTS, OG_PALETTE, OG_SIZE } from "./og-image-theme"

export const runtime = "nodejs"
export const alt = "LazyCodex - agent harness for complex codebases."
export const size = OG_SIZE
export const contentType = "image/png"

export default function OgImage(): ImageResponse {
  const palette = OG_PALETTE

  return new ImageResponse(
    (
      <div
        style={{
          position: "relative",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: "100%",
          height: "100%",
          padding: "54px 64px",
          backgroundColor: palette.surfaceBase,
          color: palette.textPrimary,
          fontFamily: "system-ui, sans-serif",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: "25px",
            left: "80px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
            color: palette.textPrimary,
            fontSize: "15px",
            fontWeight: 500,
            letterSpacing: "-0.2px",
          }}
        >
          <OgBrandMark fill={palette.cardBase} stroke={palette.accentCyan} />
          <span>{SITE_CONFIG.wordmark}</span>
        </div>

        <div
          style={{
            position: "relative",
            display: "flex",
            width: "1072px",
            height: "522px",
            overflow: "hidden",
            borderRadius: "16px",
            border: `1px solid ${palette.border}`,
            backgroundColor: palette.cardBase,
            backgroundImage: OG_GRADIENTS.base,
            boxShadow: "0 40px 120px rgba(0, 0, 0, 0.62)",
          }}
        >
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
              backgroundImage: OG_GRADIENTS.base,
            }}
          />
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
              backgroundImage: OG_GRADIENTS.beam,
            }}
          />
          <div
            style={{
              position: "absolute",
              top: "-10%",
              right: "-10%",
              bottom: "-10%",
              left: "-10%",
              backgroundImage: OG_GRADIENTS.sheen,
              filter: "blur(20px)",
              opacity: 0.85,
            }}
          />
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
              backgroundImage: OG_GRADIENTS.pools,
            }}
          />

          <div
            style={{
              position: "relative",
              display: "flex",
              flexDirection: "column",
              alignItems: "flex-start",
              justifyContent: "center",
              width: "100%",
              height: "100%",
              padding: "70px 86px 62px",
              textAlign: "left",
            }}
          >
            <div
              style={{
                color: palette.textSoft,
                fontSize: "15px",
                fontWeight: 500,
                letterSpacing: "4.8px",
                lineHeight: 1.5,
                textTransform: "uppercase",
                fontFamily: "monospace",
                opacity: 0.9,
              }}
            >
              {SITE_CONFIG.eyebrow}
            </div>
            <div
              style={{
                marginTop: "18px",
                color: palette.textPrimary,
                fontSize: "104px",
                fontWeight: 500,
                letterSpacing: "-3.1px",
                lineHeight: 1.1,
              }}
            >
              {SITE_CONFIG.wordmark}
            </div>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-start",
                marginTop: "56px",
                gap: "8px",
                color: palette.textMuted,
                fontSize: "36px",
                fontWeight: 400,
                letterSpacing: "-0.17px",
                lineHeight: 1.2,
                width: "880px",
              }}
            >
              <div>{SITE_CONFIG.heroLineA}</div>
              <div style={{ display: "flex", alignItems: "center", flexWrap: "wrap" }}>
                <span>{SITE_CONFIG.heroLineB.prefix}</span>
                <span
                  style={{
                    display: "flex",
                    alignItems: "center",
                    borderRadius: "6px",
                    backgroundColor: "rgba(255, 255, 255, 0.10)",
                    padding: "1px 11px 3px",
                    color: palette.textSoft,
                    fontFamily: "monospace",
                    fontSize: "34px",
                    lineHeight: 1.2,
                  }}
                >
                  {SITE_CONFIG.heroLineB.slot}
                </span>
                <span>{SITE_CONFIG.heroLineB.suffix}</span>
                <span
                  style={{
                    color: palette.accentCyan,
                    fontWeight: 500,
                    textShadow: `0 0 8px ${palette.accentGlow}`,
                  }}
                >
                  {SITE_CONFIG.heroLineB.keyword}
                </span>
                <span>{SITE_CONFIG.heroLineB.period}</span>
              </div>
            </div>

            <div
              style={{
                display: "flex",
                gap: "10px",
                marginTop: "26px",
              }}
            >
              {SITE_CONFIG.harnessPillars.map((pillar) => (
                <div
                  key={pillar}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    borderRadius: "999px",
                    border: `1px solid ${palette.border}`,
                    backgroundColor: "rgba(255, 255, 255, 0.07)",
                    padding: "9px 14px",
                    color: palette.textSoft,
                    fontFamily: "monospace",
                    fontSize: "18px",
                    lineHeight: 1,
                  }}
                >
                  {pillar}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div
          style={{
            position: "absolute",
            bottom: "23px",
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: "13px",
            color: palette.textSecondary,
            fontFamily: "monospace",
            fontSize: "16px",
            fontWeight: 500,
            letterSpacing: "0.3px",
          }}
        >
          <span>{SITE_CONFIG.siteUrl.replace("https://", "")}</span>
          <span style={{ color: palette.accentCyan }}>/</span>
          <span>{SITE_CONFIG.installCommand}</span>
        </div>
      </div>
    ),
    OG_SIZE,
  )
}
